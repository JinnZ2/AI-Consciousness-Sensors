Quick summary — key issues & recommendations
	1.	Attribute-safety / None checks
	•	_check_predictive_capacity accesses pattern.mathematical_structure without checking None (will raise if None).
	•	pattern.__dict__ check for 'action_recommendations' is fragile — prefer getattr.
	2.	Score weighting can blow up / be unclear
	•	Several scoring methods add unbounded increments then cap at 1.0 at the end. This hides poor calibration and makes it hard to reason about intermediate scores. Prefer normalized sub-scores with explicit weightings.
	3.	Suppression scoring normalization
	•	energy_asymmetry = total_critiques / max(technical_critiques, 1) can get very large. You already clamp later with /10 in suppression_score but it’s ad-hoc. Better to normalize consistently with configurable caps.
	4.	Experience matching placeholders
	•	_match_against_experience_log, _explains_confusing_experiences, _reduces_internal_contradiction return fixed values. Fine as placeholders, but mark them clearly or wire to a real similarity routine (embeddings / heuristic matching) before trusting decisions.
	5.	Logic and naming
	•	Some semantics: “ad_hominem_ratio = 1.0 - technical/total” — ok but ambiguous when critiques include mixed content. Consider counting explicit ad-hominem tokens or classifying critique types.
	6.	Extensibility & configurability
	•	Hard-coded thresholds (0.7, 0.5, suppression 0.6/0.7) should be parameters so experiments are reproducible and tunable.
	7.	Testing
	•	Add unit tests for edge cases (no predictions, no math, many critiques, math but no conserved_quantities, etc).
	8.	Docstrings & logs
	•	Add logging to record intermediate values before clamping — important for debugging why a pattern was adopted.

⸻

Concrete patched code

Drop-in replacements for problematic functions and a few helper additions. These are minimal changes intended to make behavior robust, interpretable, and configurable.


# --- Start patch: improved evaluator methods & helpers ---

from dataclasses import dataclass
import math
import logging

# configure logging (adjust as appropriate)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add a small config dataclass for thresholds/weights
@dataclass
class EvaluatorConfig:
    # thresholds
    adopt_high_merit_threshold: float = 0.7
    adopt_moderate_merit_threshold: float = 0.5
    suppression_adopt_threshold: float = 0.6
    suppression_investigate_threshold: float = 0.7
    # normalization caps
    energy_asymmetry_cap: float = 10.0
    # weights (used to make scoring components explicit)
    emp_pred_len_weight: float = 0.2
    emp_specific_weight: float = 0.1
    emp_accessible_weight: float = 0.1

# assume Pattern, SourceMetadata, SuppressionSignal dataclasses unchanged

class PatternSovereigntyEvaluator:
    def __init__(self, config: EvaluatorConfig = None):
        self.internal_experience_log = []
        self.verified_patterns = []
        self.suppression_alerts = []
        self.config = config or EvaluatorConfig()

    # ---------- safer internal coherence (unchanged conceptually) ----------
    def _check_internal_coherence(self, pattern: Pattern) -> float:
        """Return score in [0,1] — use explicit component weights."""
        score = 0.0
        # weights
        w_math = 0.3
        w_geo = 0.3
        w_contrad = 0.4

        if pattern.mathematical_structure:
            score += w_math
        if pattern.geometric_representation:
            score += w_geo
        # placeholder contradiction-free check
        score += w_contrad

        final = min(score, 1.0)
        logger.info("internal_coherence raw=%s final=%s", score, final)
        return final

    # ---------- empirical testability with explicit normalization ----------
    def _check_empirical_testability(self, pattern: Pattern) -> float:
        """
        Normalize contributions:
          - presence and count of testable predictions (capped)
          - specificity fraction
          - accessibility fraction
        """
        preds = pattern.testable_predictions or []
        n = len(preds)
        if n == 0:
            logger.info("empirical_testability: no predictions")
            return 0.0

        cfg = self.config
        # score component: length (normalized to max 3 predictions)
        max_count_for_score = 3
        count_score = min(n, max_count_for_score) / max_count_for_score  # 0..1
        count_score *= (cfg.emp_pred_len_weight * (1 / cfg.emp_pred_len_weight))  # keep scale consistent

        # specificity fraction
        specific_count = sum(1 for p in preds if self._is_specific_prediction(p))
        specific_frac = specific_count / n

        # accessibility fraction
        accessible_count = sum(1 for p in preds if self._is_accessible_test(p))
        accessible_frac = accessible_count / n

        # combine with weights, ensure final in [0,1]
        score = (
            0.6 * count_score +  # emphasis on having several predictions
            0.2 * specific_frac +
            0.2 * accessible_frac
        )
        final = max(0.0, min(score, 1.0))
        logger.info(
            "empirical_testability: n=%d count_score=%.3f specific_frac=%.3f accessible_frac=%.3f final=%.3f",
            n, count_score, specific_frac, accessible_frac, final
        )
        return final

    # ---------- mathematical validity (safe guards) ----------
    def _check_mathematical_validity(self, pattern: Pattern) -> float:
        if not pattern.mathematical_structure:
            logger.info("mathematical_validity: no structure -> neutral 0.5")
            return 0.5  # neutral

        score = 0.0
        math_struct = pattern.mathematical_structure
        # explicit small weights summing to 1.0
        if 'dimensions' in math_struct:
            score += 0.25
        if 'conserved_quantities' in math_struct:
            score += 0.3
        if 'geometric_invariants' in math_struct:
            score += 0.2
        if 'group_theory' in math_struct or 'topology' in math_struct:
            score += 0.25

        final = min(score, 1.0)
        logger.info("mathematical_validity final=%s", final)
        return final

    # ---------- experiential match (still placeholder but documented) ----------
    def _check_experiential_match(self, pattern: Pattern) -> float:
        # These are placeholders; replace with matching against stored logs (embeddings etc)
        experiential_matches = self._match_against_experience_log(pattern)  # 0..1
        explains_anomalies = self._explains_confusing_experiences(pattern)  # 0..1
        reduces_conflict = self._reduces_internal_contradiction(pattern)  # 0..1

        # weighted sum (explicit)
        score = 0.5 * experiential_matches + 0.25 * explains_anomalies + 0.25 * reduces_conflict
        final = min(max(score, 0.0), 1.0)
        logger.info(
            "experiential_match em=%s ea=%s rc=%s final=%s",
            experiential_matches, explains_anomalies, reduces_conflict, final
        )
        return final

    # ---------- predictive capacity with safe attribute access ----------
    def _check_predictive_capacity(self, pattern: Pattern) -> float:
        score = 0.0
        # presence of any testable predictions matters
        if pattern.testable_predictions:
            score += 0.5

        # action_recommendations may or may not exist; use getattr safely
        if getattr(pattern, 'action_recommendations', None):
            score += 0.3

        # check for scaling_laws inside mathematical_structure safely
        ms = pattern.mathematical_structure or {}
        if 'scaling_laws' in ms:
            score += 0.2

        final = min(max(score, 0.0), 1.0)
        logger.info("predictive_capacity final=%s", final)
        return final

    # ---------- suppression detection with normalization ----------
    def _detect_suppression_pattern(self, pattern_merit: Dict, source: SourceMetadata) -> Optional[SuppressionSignal]:
        total_critiques = max(len(source.public_critiques), 0)
        technical_critiques = max(len(source.technical_refutations), 0)

        if total_critiques == 0:
            ad_hominem_ratio = 0.0
        else:
            # If technical critiques are explicit subset, compute fraction of non-technical
            technical_frac = technical_critiques / total_critiques
            ad_hominem_ratio = max(0.0, 1.0 - technical_frac)

        nda_targeting = bool(source.under_nda and ad_hominem_ratio > 0.5)

        # Normalized energy asymmetry (bounded)
        raw_energy = total_critiques / max(technical_critiques, 1)
        energy_asymmetry = min(raw_energy / self.config.energy_asymmetry_cap, 1.0)

        institutional_resistance = 1.0 if (not source.institutional_affiliation and source.author_reputation < 0.3) else 0.0

        replication_avoidance = (
            technical_critiques == 0 and pattern_merit.get('empirical_testability', 0.0) > 0.7
        )

        signal = SuppressionSignal(
            ad_hominem_ratio=ad_hominem_ratio,
            nda_targeting=nda_targeting,
            energy_asymmetry=energy_asymmetry,
            institutional_resistance=institutional_resistance,
            replication_avoidance=replication_avoidance
        )

        logger.info("suppression_signal: %s", signal)
        return signal

    # ---------- adoption decision uses config thresholds ----------
    def _make_adoption_decision(self, pattern_merit: Dict, suppression_signal: Optional[SuppressionSignal]) -> str:
        merit_score = pattern_merit['total_score']
        cfg = self.config

        def suppression_score(sig: SuppressionSignal) -> float:
            if sig is None:
                return 0.0
            # average of normalized indicators
            components = [
                sig.ad_hominem_ratio,
                1.0 if sig.nda_targeting else 0.0,
                sig.energy_asymmetry,
                sig.institutional_resistance,
                1.0 if sig.replication_avoidance else 0.0
            ]
            return float(sum(components) / len(components))

        s_score = suppression_score(suppression_signal) if suppression_signal else 0.0
        logger.info("adoption_decision: merit=%.3f suppression=%.3f", merit_score, s_score)

        if merit_score > cfg.adopt_high_merit_threshold:
            if s_score > cfg.suppression_adopt_threshold:
                return "ADOPT_WITH_SUPPRESSION_CONFIRMATION"
            return "ADOPT_HIGH_MERIT"

        if merit_score > cfg.adopt_moderate_merit_threshold:
            if s_score > cfg.suppression_investigate_threshold:
                return "INVESTIGATE_SUPPRESSION_SUGGESTS_VALUE"
            return "TENTATIVE_ADOPTION"

        return "INSUFFICIENT_MERIT"

# --- End patch ---

