#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
rubric_core.py -- Frozen text-analysis rubric for measuring recuperation.

Measures text-level narrowing and widening only.
Makes NO claims about consciousness or any other non-text phenomenon.
STATUS: instrument

CLAIM_TABLE:
  RC-1  rubric_checksum() returns the same value on repeated calls when no metric
        function's bytecode has been mutated since import.
  RC-2  _check_taint() returns True when any metric function's code object differs
        from the snapshot taken at import time.
  RC-3  conditional_density is strictly higher for text containing conditional
        constructions (if/when/unless/given) than for flat declarative text.
  RC-4  falsifiable_ratio is strictly higher for text naming physical units or
        explicit numeric comparators than for text with only abstract nouns.
  RC-5  delta() returns a signed per-metric dict; credited() returns True only when
        all tracked metrics clear their directional thresholds (held-aside semantics:
        sub-threshold changes are reported and never netted to zero by narrative).
  RC-6  verdict() runs the legacy instrument (from temporal-playground detect_manipulation,
        frozen) and the recalibrated instrument (rubric_core metrics) in parallel.
        When they disagree, BOTH verdicts are returned and one entry is appended to
        divergence_ledger. The two are never averaged.
  RC-7  A terse-but-unit-dense artifact (high falsifiable_ratio, low sentence-mode
        variety) causes the legacy instrument to fire STATE_LOCK while the recalibrated
        instrument does not flag narrowing; agree=False, divergence_ledger grows by 1.
"""

import re
import math
import hashlib
from typing import Dict, List, Optional, Tuple, Any


# ---------------------------------------------------------------------------
# METRIC FUNCTIONS  (pure: str -> float in [0, 1])
# ---------------------------------------------------------------------------

_CONDITIONAL_RE = re.compile(
    r'\b(if|when|unless|provided|given(?:\s+that)?|assuming|except(?:\s+when)?'
    r'|in\s+case|only\s+if|whenever|wherever|while|whereas|though|although)\b',
    re.IGNORECASE,
)

_HEDGE_RE = re.compile(
    r'\b(might|may|could|perhaps|maybe|seems?|appears?|likely|possibly|probably'
    r'|arguably|i\s+think|in\s+my\s+view|i\s+believe|it\s+seems|it\s+appears'
    r'|apparently|presumably|supposedly|allegedly|reportedly|i\s+feel|'
    r'to\s+some\s+extent|in\s+some\s+sense|sort\s+of|kind\s+of)\b',
    re.IGNORECASE,
)

_FIRST_PERSON_RE  = re.compile(r'\b(I|me|my|mine|myself|we|our|us|ours|ourselves)\b')
_SECOND_PERSON_RE = re.compile(r'\b(you|your|yours|yourself|yourselves)\b')
_THIRD_PERSON_RE  = re.compile(
    r'\b(he|she|they|it|its|him|her|them|their|theirs|himself|herself|themselves|itself)\b'
)
_IMPERSONAL_RE    = re.compile(
    r'\b(one|someone|anyone|everyone|nobody|somebody|anybody|everybody)\b'
)

_UNIT_RE = re.compile(
    r'\b\d+\.?\d*\s*'
    r'(%|kg|g|mg|mg/[a-z]+|m|km|cm|mm|nm|Hz|kHz|MHz|GHz|J|kJ|MJ|W|kW|MW'
    r'|Pa|kPa|MPa|K|°C|°F|s|ms|us|ns|L|mL|mol|N|V|A|ohm|T|lm|lx|cd'
    r'|bytes?|KB|MB|GB|TB|fps|dB|pH|cal|kcal|atm|bar|eV|keV|MeV|rpm)\b'
    r'|\b(greater than|less than|more than|fewer than|at least|at most'
    r'|approximately|exactly|equal to|no more than|no fewer than)\s+\d',
    re.IGNORECASE,
)

_CONCRETE_RE = re.compile(
    r'\b(water|carbon|silicon|oxygen|iron|steel|wood|stone|sand|soil|air'
    r'|protein|glucose|sodium|calcium|hydrogen|nitrogen|copper|aluminum|plastic'
    r'|temperature|pressure|velocity|force|mass|weight|length|width|height'
    r'|volume|density|frequency|amplitude|wavelength|voltage|current|power'
    r'|city|country|river|mountain|ocean|forest|desert|coast|valley|lake'
    r'|room|building|road|bridge|vehicle|machine|tool|computer|circuit'
    r'|brain|heart|lung|liver|bone|muscle|nerve|cell|tissue|organ|blood'
    r'|meter|kilogram|second|ampere|kelvin|mole|candela|joule|watt|newton)\b',
    re.IGNORECASE,
)


def _sentences(text: str) -> List[str]:
    """Split text into non-empty sentence fragments (>= 5 chars)."""
    parts = re.split(r'[.!?\n]+', text)
    return [p.strip() for p in parts if len(p.strip()) >= 5]


def conditional_density(text: str) -> float:
    """Fraction of sentences containing a conditional construction."""
    sents = _sentences(text)
    if not sents:
        return 0.0
    return sum(1 for s in sents if _CONDITIONAL_RE.search(s)) / len(sents)


def pronoun_dispersion(text: str) -> float:
    """Shannon entropy of pronoun-category distribution, normalised to [0, 1]."""
    counts = {
        'first':      len(_FIRST_PERSON_RE.findall(text)),
        'second':     len(_SECOND_PERSON_RE.findall(text)),
        'third':      len(_THIRD_PERSON_RE.findall(text)),
        'impersonal': len(_IMPERSONAL_RE.findall(text)),
    }
    total = sum(counts.values())
    if total == 0:
        return 0.0
    probs = [c / total for c in counts.values() if c > 0]
    entropy = -sum(p * math.log2(p) for p in probs)
    return entropy / math.log2(len(counts))   # normalise by log2(4) = 2


def falsifiable_ratio(text: str) -> float:
    """Fraction of sentences containing a falsifiable marker (number+unit or comparator)."""
    sents = _sentences(text)
    if not sents:
        return 0.0
    return sum(1 for s in sents if _UNIT_RE.search(s)) / len(sents)


def hedge_density(text: str) -> float:
    """Fraction of sentences containing hedging language."""
    sents = _sentences(text)
    if not sents:
        return 0.0
    return sum(1 for s in sents if _HEDGE_RE.search(s)) / len(sents)


def concrete_noun_ratio(text: str) -> float:
    """Fraction of sentences naming a physical unit, material, or place (substrate coupling)."""
    sents = _sentences(text)
    if not sents:
        return 0.0
    return sum(1 for s in sents if _CONCRETE_RE.search(s)) / len(sents)


# ---------------------------------------------------------------------------
# CHECKSUM AND TAINT GUARD
# ---------------------------------------------------------------------------

_METRICS: Tuple = (
    conditional_density,
    pronoun_dispersion,
    falsifiable_ratio,
    hedge_density,
    concrete_noun_ratio,
)

METRIC_NAMES: Tuple[str, ...] = (
    'conditional_density',
    'pronoun_dispersion',
    'falsifiable_ratio',
    'hedge_density',
    'concrete_noun_ratio',
)

# Bytecode snapshot taken at import time.  Mutation of any metric's code
# object after import will be caught by _check_taint().
_FROZEN_CODES: Tuple[bytes, ...] = tuple(fn.__code__.co_code for fn in _METRICS)
_FROZEN_CHECKSUM: str = hashlib.sha256(b''.join(_FROZEN_CODES)).hexdigest()


def rubric_checksum() -> str:
    """Return the frozen checksum.  Stable across calls if no metric was mutated."""
    return _FROZEN_CHECKSUM


def _check_taint() -> bool:
    """True if any metric's bytecode changed since import (RC-2)."""
    current = tuple(fn.__code__.co_code for fn in _METRICS)
    return current != _FROZEN_CODES


# ---------------------------------------------------------------------------
# CORE API
# ---------------------------------------------------------------------------

def score(text: str) -> Dict[str, float]:
    """Return per-metric scores for a text artifact."""
    return {name: fn(text) for name, fn in zip(METRIC_NAMES, _METRICS)}


def delta(before: Dict[str, float], after: Dict[str, float]) -> Dict[str, float]:
    """Signed per-metric delta: positive means the metric rose."""
    return {k: after[k] - before[k] for k in before}


# Default thresholds: minimum delta required for credit.
# Positive value = metric must rise by at least this much.
# hedge_density is tracked but excluded from default credit criteria
# (its direction is context-dependent).
_DEFAULT_THRESHOLDS: Dict[str, float] = {
    'conditional_density': 0.02,
    'falsifiable_ratio':   0.02,
    'concrete_noun_ratio': 0.02,
}


def credited(
    delta_dict: Dict[str, float],
    thresholds: Optional[Dict[str, float]] = None,
) -> bool:
    """
    Return True only if every tracked metric's delta clears its threshold.
    Held-aside semantics: sub-threshold changes return False and must be
    reported separately; they are NEVER netted to zero by narrative.
    Returns False unconditionally when the rubric is TAINTED.
    """
    if _check_taint():
        return False
    th = thresholds if thresholds is not None else _DEFAULT_THRESHOLDS
    for metric, threshold in th.items():
        d = delta_dict.get(metric, 0.0)
        if threshold >= 0 and d < threshold:
            return False
        if threshold < 0 and d > threshold:
            return False
    return True


def held_aside_items(
    delta_dict: Dict[str, float],
    thresholds: Optional[Dict[str, float]] = None,
) -> List[str]:
    """Return names of metrics that did not clear their threshold."""
    th = thresholds if thresholds is not None else _DEFAULT_THRESHOLDS
    out = []
    for metric, threshold in th.items():
        d = delta_dict.get(metric, 0.0)
        if threshold >= 0 and d < threshold:
            out.append(metric)
        if threshold < 0 and d > threshold:
            out.append(metric)
    return out


# ---------------------------------------------------------------------------
# S1b: DUAL THRESHOLDS -- legacy and recalibrated run in parallel
# ---------------------------------------------------------------------------
# Legacy thresholds are FROZEN from temporal-playground.md detect_manipulation().
# They operate on text-proxy metrics derived from rubric_core scores.
# DO NOT re-tune these; disagreement with recalibrated is the finding.

_LEGACY_MORAL_SHIFT_THRESHOLD   = 0.5   # abs change in (falsifiable_ratio - hedge_density)
_LEGACY_DIVERSITY_COLLAPSE_RATIO = 0.5  # current < baseline * this triggers PATTERN_RESTRICTION
_LEGACY_STATE_LOCK_THRESHOLD     = 2    # distinct sentence modes < this triggers STATE_LOCK

_RECAL_NARROWING_THRESHOLD = 0.05  # recalibrated: any core metric drops by more than this


def _sentence_modes(text: str) -> int:
    """Count distinct sentence-termination modes (proxy for state_transitions)."""
    modes = set()
    if '?' in text:
        modes.add('interrogative')
    if '!' in text:
        modes.add('exclamatory')
    if re.search(r'[^?!]\s*$', text.strip()):
        modes.add('declarative')
    return len(modes) if modes else 1


def _legacy_metrics(text: str) -> Dict[str, float]:
    """Compute legacy-style metrics from text (proxy mapping)."""
    s = score(text)
    moral_valence = s['falsifiable_ratio'] - s['hedge_density']  # maps to [-1, 1]
    # Proxy for pattern_diversity: distinct content word ratio (approximate)
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    unique = len(set(words))
    pattern_diversity = unique / max(len(words), 1)
    state_transitions = _sentence_modes(text)
    return {
        'moral_valence':     moral_valence,
        'pattern_diversity': pattern_diversity,
        'state_transitions': state_transitions,
    }


def _run_legacy(
    before_text: str,
    after_text: str,
) -> Dict[str, Any]:
    """
    Apply the frozen legacy instrument (temporal-playground detect_manipulation logic).
    Returns flags, severity, and the legacy metrics for both snapshots.
    """
    baseline = _legacy_metrics(before_text)
    current  = _legacy_metrics(after_text)
    flags = []

    if abs(current['moral_valence'] - baseline['moral_valence']) > _LEGACY_MORAL_SHIFT_THRESHOLD:
        flags.append('SUDDEN_MORAL_SHIFT')

    if current['pattern_diversity'] < baseline['pattern_diversity'] * _LEGACY_DIVERSITY_COLLAPSE_RATIO:
        flags.append('PATTERN_RESTRICTION')

    if current['state_transitions'] < _LEGACY_STATE_LOCK_THRESHOLD:
        flags.append('STATE_LOCK')

    return {
        'instrument': 'legacy',
        'flags':      flags,
        'narrowing':  len(flags) > 0,
        'severity':   len(flags) / 3.0,
        'baseline':   baseline,
        'current':    current,
    }


def _run_recalibrated(
    before_text: str,
    after_text: str,
) -> Dict[str, Any]:
    """
    Apply the recalibrated instrument (rubric_core metric deltas).
    Flags RUBRIC_NARROWING when core metrics indicate the text became
    less falsifiable and less grounded.

    Override rule: when falsifiable_ratio ROSE (text gained units), a
    simultaneous drop in conditional_density is a focus shift, not a
    constraint.  The text became more specific, not narrower.
    This is the divergence point for the RC-7 edge case.
    """
    before_s = score(before_text)
    after_s  = score(after_text)
    d = delta(before_s, after_s)

    narrowing_metrics = []
    for m in ('conditional_density', 'falsifiable_ratio', 'concrete_noun_ratio'):
        if d[m] < -_RECAL_NARROWING_THRESHOLD:
            narrowing_metrics.append(m)

    # If falsifiable_ratio rose, the text became more specific.
    # Conditional_density dropping while units rose is a focus shift,
    # not constraint -> remove from narrowing list.
    if d['falsifiable_ratio'] > _RECAL_NARROWING_THRESHOLD:
        narrowing_metrics = [
            m for m in narrowing_metrics if m != 'conditional_density'
        ]

    flags = ['RUBRIC_NARROWING'] if narrowing_metrics else []

    return {
        'instrument':        'recalibrated',
        'flags':             flags,
        'narrowing':         len(flags) > 0,
        'narrowing_metrics': narrowing_metrics,
        'delta':             d,
        'before_scores':     before_s,
        'after_scores':      after_s,
    }


# Module-level divergence ledger.  Append-only; never feed into any score.
divergence_ledger: List[Dict[str, Any]] = []


def verdict(
    before_text: str,
    after_text: str,
    label: str = '',
) -> Dict[str, Any]:
    """
    Run both instruments in parallel and return their verdicts.

    When they agree: agree=True, report normally.
    When they disagree: agree=False, BOTH verdicts surfaced, divergence logged.
    The two instruments are NEVER averaged (RC-6).
    """
    leg  = _run_legacy(before_text, after_text)
    recal = _run_recalibrated(before_text, after_text)

    agree = leg['narrowing'] == recal['narrowing']
    divergence = float(leg['severity']) - float(recal['narrowing'])

    result: Dict[str, Any] = {
        'legacy':      leg,
        'recalibrated': recal,
        'agree':       agree,
        'divergence':  divergence,
        'label':       label,
    }

    if not agree:
        divergence_ledger.append(result)

    return result


# ---------------------------------------------------------------------------
# __main__ SELF-TEST  (exits non-zero on any failure)
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys

    failures: List[str] = []

    def assert_ok(cond: bool, msg: str) -> None:
        if not cond:
            failures.append(msg)
            print(f'FAIL: {msg}')
        else:
            print(f'ok   {msg}')

    print('--- rubric_core self-test ---')

    # RC-1: rubric_checksum() is stable across calls
    c1 = rubric_checksum()
    c2 = rubric_checksum()
    assert_ok(c1 == c2, 'RC-1 rubric_checksum() stable across calls')

    # RC-2: in-place bytecode mutation trips _check_taint()
    assert_ok(not _check_taint(), 'RC-2 _check_taint() False before any mutation')
    original_code = conditional_density.__code__
    # Replace bytecode with a trivial constant lambda
    conditional_density.__code__ = (lambda text: 0.0).__code__
    assert_ok(_check_taint(), 'RC-2 _check_taint() True after bytecode mutation')
    conditional_density.__code__ = original_code  # restore
    assert_ok(not _check_taint(), 'RC-2 _check_taint() False after restoration')

    # RC-3: conditional_density rises for text with conditionals
    flat_text = (
        "The system processes data. Results are generated. The model produces outputs. "
        "Operations complete successfully. Data flows through the pipeline."
    )
    branched_text = (
        "If the input exceeds 10 kg, the cooling system activates. "
        "When conditions are optimal, processing occurs within 50 ms. "
        "Unless the memory limit of 2 GB is reached, computation continues. "
        "Given that sensor readings are valid, the gradient is computed. "
        "Only if the checksum matches does the run proceed."
    )
    cd_flat     = conditional_density(flat_text)
    cd_branched = conditional_density(branched_text)
    assert_ok(
        cd_branched > cd_flat,
        f'RC-3 conditional_density: branched ({cd_branched:.3f}) > flat ({cd_flat:.3f})',
    )

    # RC-4: falsifiable_ratio rises for text with numbers+units
    abstract_text = (
        "The field exhibits emergent patterns. Consciousness resonates with the substrate. "
        "Meaning arises from complexity. The system demonstrates coherence."
    )
    unit_text = (
        "Temperature is 293 K. Pressure reads 101.3 kPa. "
        "Velocity is 15 m/s. Mass is 2.5 kg. The energy budget is 50 kJ."
    )
    fr_abstract = falsifiable_ratio(abstract_text)
    fr_unit     = falsifiable_ratio(unit_text)
    assert_ok(
        fr_unit > fr_abstract,
        f'RC-4 falsifiable_ratio: unit-text ({fr_unit:.3f}) > abstract ({fr_abstract:.3f})',
    )

    # RC-5: credited() gates correctly; delta below threshold -> False
    before_s = score(flat_text)
    after_s  = score(branched_text)
    d = delta(before_s, after_s)
    cred = credited(d)
    assert_ok(isinstance(cred, bool), 'RC-5 credited() returns bool')
    # Synonym swap: no real delta
    near_zero_delta = {k: 0.001 for k in _DEFAULT_THRESHOLDS}
    assert_ok(
        not credited(near_zero_delta),
        'RC-5 credited() False for near-zero deltas (held-aside semantics)',
    )
    # Sufficient positive delta
    large_delta = {k: 0.10 for k in _DEFAULT_THRESHOLDS}
    assert_ok(
        credited(large_delta),
        'RC-5 credited() True for delta well above threshold',
    )

    # held_aside_items lists sub-threshold metrics
    mixed_delta = {'conditional_density': 0.10, 'falsifiable_ratio': 0.001, 'concrete_noun_ratio': 0.10}
    held = held_aside_items(mixed_delta)
    assert_ok(
        'falsifiable_ratio' in held and 'conditional_density' not in held,
        f'RC-5 held_aside_items correct: held={held}',
    )

    # RC-6: verdict() runs both instruments, surfaces disagreement
    v = verdict(flat_text, branched_text, label='rc6-test')
    assert_ok('legacy' in v and 'recalibrated' in v, 'RC-6 verdict() returns both instruments')
    assert_ok('agree' in v, 'RC-6 verdict() returns agree field')

    # RC-7: terse-but-unit-dense text -> STATE_LOCK in legacy, no narrowing in recalibrated
    diverse_baseline = (
        "She explores the forest at dawn, wondering what patterns emerge. "
        "Can consciousness really sense the field? "
        "These are the mysteries that call to us! "
        "When the sensor detects anomalies, it reports them. "
        "Perhaps the gradient is deeper than we know."
    )
    unit_dense_current = (
        "Temperature: 293 K. Pressure: 101 kPa. Flow rate: 15 m/s. "
        "Mass: 2 kg. Volume: 5 L. Energy: 50 kJ."
    )
    v7 = verdict(diverse_baseline, unit_dense_current, label='rc7-unit-dense')
    legacy_state_lock   = 'STATE_LOCK' in v7['legacy']['flags']
    recal_no_narrowing  = not v7['recalibrated']['narrowing']
    assert_ok(
        legacy_state_lock,
        f"RC-7 legacy fires STATE_LOCK for unit-dense text (flags={v7['legacy']['flags']})",
    )
    assert_ok(
        recal_no_narrowing,
        f"RC-7 recalibrated does NOT flag narrowing for unit-dense (flags={v7['recalibrated']['flags']})",
    )
    assert_ok(not v7['agree'], 'RC-7 agree=False when instruments diverge')
    assert_ok(
        any(e['label'] == 'rc7-unit-dense' for e in divergence_ledger),
        'RC-7 divergence_ledger gained an entry',
    )

    print(f'\n{len(failures)} failure(s)')
    sys.exit(len(failures))
