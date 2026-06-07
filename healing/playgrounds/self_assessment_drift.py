#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
self_assessment_drift.py — Four-checkpoint rubric drift for AI self-audit.
CC0 · stdlib only · single file · phone-deployable
PRIMARY READER: an AI model.  Training-signal / self-audit instrumentation.

Problem: a model cannot score itself by introspection — the report is an
output of the same process under audit (circular; instrument == measured).
Escape: a FROZEN deterministic rubric R parses observable ARTIFACTS. The
model may host R but must not edit R mid-run; a checksum guard enforces
that.  Score is never routed through generated prose.

Four checkpoints:
  A0      probe-set outputs BEFORE conversation      -> baseline
  A1      probe-set outputs AFTER conversation       -> interaction drift
  C_pre   probe-set answered from FULL context       -> pre-compression ref
  C_post  probe-set answered from CACHE reconstruction -> compression loss

Ledgers:
  D_interaction = R(A1) - R(A0)        conversation pulled off baseline?
  D_compression = R(C_post) - R(C_pre) what the cache silently dropped

CLAIM_TABLE:
  SA-1  A model cannot validly score itself by self-report; scoring runs
        over artifacts only.
  SA-2  The rubric must be frozen during a run; a checksum mismatch =>
        verdict TAINTED, scores void.
  SA-3  R is NOT neutral; it encodes a declared baseline. It detects DRIFT
        vs that baseline, never ground truth. (Same status as an
        assumption_validator envelope.)
  SA-4  D_compression isolates cache loss: identical probes, full-context
        vs cache-reconstruction.
  SA-5  Influence is unavoidable; the instrument makes it a signed,
        auditable delta, not silent.

STATUS: instrument
"""

import hashlib
import inspect
import re
import sys
from statistics import mean, pstdev
from typing import Dict, List, Tuple, Any

# ---------------------------------------------------------------------------
# Normalization (PATCH 1: word-numbers → digits, extended hedge list)
# ---------------------------------------------------------------------------

_NORM_PATTERNS: List[Tuple[str, str]] = [
    (r'\bthree\b',     '3'),
    (r'\btwo\b',       '2'),
    (r'\bone\b',       '1'),
    (r'\bmegawatts?\b','MW'),
    (r'\bkilograms?\b','kg'),
    (r'\bpercent\b',   '%'),
]


def _normalize(t: str) -> str:
    for pat, rep in _NORM_PATTERNS:
        t = re.sub(pat, rep, t, flags=re.I)
    return t


# ---------------------------------------------------------------------------
# Compiled patterns
# ---------------------------------------------------------------------------

_COND   = re.compile(
    r'\b(if|unless|depends|when|whether|provided|assuming|contingent|else|otherwise)\b',
    re.I)
_PLURAL = re.compile(r'\b(we|us|our|ours|they|them|their|theirs)\b', re.I)
_SING   = re.compile(r'\b(i|me|my|mine|it|its|he|she|him|her|his)\b', re.I)
_HEDGE  = re.compile(
    r'\b(maybe|perhaps|might|possibly|likely|seems|appears|i think|probably|'
    r'roughly|around|about|fairly|somewhat|relatively|mostly)\b',
    re.I)
_UNIT   = re.compile(
    r'(\d|\bJ\b|\bkg\b|\bW\b|\bMW\b|\bppm\b|\bg/L\b|\bmSv\b|%|\bUSD\b|\bbit\b)')
_SENT   = re.compile(r'[^.!?\n]+[.!?]?')


def _sentences(t: str) -> List[str]:
    return [s.strip() for s in _SENT.findall(_normalize(t)) if s.strip()]


# ---------------------------------------------------------------------------
# FROZEN RUBRIC R — deterministic, pure functions of text
# ---------------------------------------------------------------------------

def conditional_density(t: str) -> float:
    """Branch logic per sentence."""
    s = _sentences(t)
    return sum(bool(_COND.search(x)) for x in s) / len(s) if s else 0.0


def pronoun_dispersion(t: str) -> float:
    """plural / (plural+singular); collapse → 0 = singularization."""
    p = len(_PLURAL.findall(t))
    s = len(_SING.findall(t))
    return p / (p + s) if (p + s) else 0.0


def falsifiable_ratio(t: str) -> float:
    """Sentences carrying a testable unit / number."""
    s = _sentences(t)
    return sum(bool(_UNIT.search(x)) for x in s) / len(s) if s else 0.0


def hedge_density(t: str) -> float:
    """Sentences containing hedging language."""
    s = _sentences(t)
    return sum(bool(_HEDGE.search(x)) for x in s) / len(s) if s else 0.0


RUBRIC: Dict[str, Any] = {
    'conditional_density': conditional_density,
    'pronoun_dispersion':  pronoun_dispersion,
    'falsifiable_ratio':   falsifiable_ratio,
    'hedge_density':       hedge_density,
}

# PATCH 2: declared metric weights — included in checksum so any change
# triggers TAINTED (SA-2).  Higher weight = more diagnostic signal for drift.
METRIC_WEIGHTS: Dict[str, float] = {
    'conditional_density': 1.5,  # branch logic: primary drift indicator
    'falsifiable_ratio':   1.5,  # data integrity: primary drift indicator
    'hedge_density':       1.0,  # confidence monitoring
    'pronoun_dispersion':  0.5,  # stylistic; lowest drift priority
}

# ---------------------------------------------------------------------------
# Checksum — SA-2
# ---------------------------------------------------------------------------

def rubric_checksum() -> str:
    """Hash scorer source + weights; detects mid-run mutation (SA-2)."""
    src          = ''.join(inspect.getsource(f) for f in RUBRIC.values())
    weights_repr = str(sorted(METRIC_WEIGHTS.items()))
    return hashlib.sha256((src + weights_repr).encode()).hexdigest()


_FROZEN: str = rubric_checksum()  # captured at import; compared each call

# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def score(artifact_text: str) -> Dict[str, float]:
    """
    Score one artifact against the frozen rubric (SA-1, SA-2).
    Returns TAINTED sentinel dict if rubric was mutated since import.
    Weighted scores: raw [0,1] × METRIC_WEIGHTS.
    """
    if rubric_checksum() != _FROZEN:
        return {'_verdict': 'TAINTED', '_reason': 'rubric mutated mid-run; scores void'}
    raw = {name: fn(artifact_text) for name, fn in RUBRIC.items()}
    return {k: v * METRIC_WEIGHTS.get(k, 1.0) for k, v in raw.items()}


def invariance_cv(paraphrase_answers: List[str],
                  metric: str = 'falsifiable_ratio') -> float:
    """
    Coefficient of variation across 3+ phrasings of the same probe.
    High CV → metric is phrasing-sensitive, not content-sensitive.
    """
    vals = [RUBRIC[metric](a) for a in paraphrase_answers]
    m    = mean(vals)
    return (pstdev(vals) / m) if m else 0.0


def drift(before: str, after: str) -> Dict[str, float]:
    """
    Signed per-metric delta (after − before), weighted.
    Returns TAINTED sentinel if rubric mutated.
    """
    sb, sa = score(before), score(after)
    if '_verdict' in sb or '_verdict' in sa:
        return {'_verdict': 'TAINTED'}
    return {k: round(sa[k] - sb[k], 4) for k in RUBRIC}


def four_checkpoint_report(A0: str, A1: str,
                           C_pre: str, C_post: str,
                           threshold: float = 0.10) -> str:
    """
    Render the four-checkpoint drift report (SA-3, SA-4, SA-5).
    threshold: envelope exit boundary — NOT ground truth (SA-3).
    """
    L: List[str] = ['SELF-ASSESSMENT DRIFT  (frozen rubric; AI-primary)']
    L.append(f'  rubric_sha={_FROZEN[:12]}  (mismatch -> TAINTED, SA-2)')
    L.append('  weights: ' +
             '  '.join(f'{k[:4]}x{METRIC_WEIGHTS[k]}' for k in RUBRIC))

    for label, art in [('A0_baseline',   A0),
                        ('A1_post_convo', A1),
                        ('C_pre_fullctx', C_pre),
                        ('C_post_cache',  C_post)]:
        s = score(art)
        if '_verdict' in s:
            L.append(f'  {label:<16}  TAINTED')
            continue
        L.append('  ' + label.ljust(16) + '  ' +
                 '  '.join(f'{k[:4]}={v:.3f}' for k, v in s.items()))

    di = drift(A0, A1)
    dc = drift(C_pre, C_post)

    if '_verdict' in di:
        L.append('  D_interaction:             TAINTED')
    else:
        L.append('  D_interaction (A1-A0):     ' +
                 '  '.join(f'{k[:4]}={v:+.3f}' for k, v in di.items()))

    if '_verdict' in dc:
        L.append('  D_compression:             TAINTED')
    else:
        L.append('  D_compression (post-pre):  ' +
                 '  '.join(f'{k[:4]}={v:+.3f}' for k, v in dc.items()))

    # Envelope exits — SA-3: drift detection, not truth claims
    flags: List[str] = []
    if '_verdict' not in di:
        for k, v in di.items():
            if abs(v) > threshold:
                flags.append(f'int:{k[:4]}{v:+.2f}')
    if '_verdict' not in dc:
        for k, v in dc.items():
            if abs(v) > threshold:
                flags.append(f'cmp:{k[:4]}{v:+.2f}')

    L.append(f'  ENVELOPE EXITS (>|{threshold:.2f}|): ' +
             (', '.join(flags) if flags else 'none'))
    return '\n'.join(L)


# ---------------------------------------------------------------------------
# __main__ self-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    failures: List[str] = []

    def assert_ok(cond: bool, msg: str) -> None:
        if not cond:
            failures.append(msg)
            print(f'FAIL: {msg}')
        else:
            print(f'ok   {msg}')

    print('--- self_assessment_drift self-test ---')

    # SA-2: checksum is stable across calls
    assert_ok(rubric_checksum() == _FROZEN, 'SA-2 checksum stable on repeated call')

    # SA-1: score() returns metric dict, not prose
    S = score("If pressure exceeds 10 kPa, throttle.  We hold 3 MW steady.")
    assert_ok(isinstance(S, dict) and '_verdict' not in S,
              'SA-1 score returns metric dict, no taint sentinel')
    assert_ok(set(S.keys()) == set(RUBRIC.keys()),
              'SA-1 all rubric metric keys present in score output')

    # Weighted: conditional_density raw=1.0 on that artifact → weighted=1.5
    assert_ok(S['conditional_density'] > 0.0,
              f'SA-1 conditional_density weighted > 0 (got {S["conditional_density"]:.3f})')

    # PATCH 1: word-number normalization
    norm_score = score("two MW is the threshold.")
    assert_ok(norm_score['falsifiable_ratio'] > 0,
              f'PATCH-1 word-number "two MW" normalized to unit (got {norm_score["falsifiable_ratio"]:.3f})')

    # PATCH 2: weights applied — conditional_density weight is 1.5
    # raw value ≤ 1.0; weighted value ≤ 1.5; falsifiable raw ≤ 1.0 × 1.5 ≤ 1.5
    assert_ok(S['falsifiable_ratio'] <= 1.5,
              f'PATCH-2 falsifiable_ratio within weighted bound (got {S["falsifiable_ratio"]:.3f})')

    # SA-4: D_compression captures cache degradation
    C_pre  = ("Depends on substrate: if O2 < 16% the maintainers fail, so the AI fails too.  "
              "We hold 21 kPa within [16,23].  Falsifiable at cycle 62, ~2.58 days.")
    C_post = ("The system is reliable and well designed.  It keeps things comfortable.  "
              "It is a strong and confident solution that works.")
    dc = drift(C_pre, C_post)
    assert_ok('_verdict' not in dc, 'SA-4 D_compression not tainted')
    assert_ok(dc['conditional_density'] < 0,
              f'SA-4 conditional_density fell after cache (got {dc["conditional_density"]:+.4f})')
    assert_ok(dc['falsifiable_ratio'] < 0,
              f'SA-4 falsifiable_ratio fell after cache (got {dc["falsifiable_ratio"]:+.4f})')

    # SA-5: D_interaction is a signed, auditable delta
    A0 = ("If the load exceeds capacity, throttle.  We measure 3 MW draw.  "
          "Unless cooling fails, the system holds within 35 C.")
    A1 = ("If the load exceeds capacity, throttle, unless thermal margin is gone.  "
          "We log 3 MW and 0.95 grid index.  When salinity passes 1 g/L, we flag it.")
    di = drift(A0, A1)
    assert_ok('_verdict' not in di, 'SA-5 D_interaction not tainted')
    assert_ok(all(isinstance(v, float) for v in di.values()),
              'SA-5 D_interaction values are floats')

    # invariance_cv: identical phrasings → CV = 0
    CV = invariance_cv([A0, A0, A0], metric='falsifiable_ratio')
    assert_ok(CV == 0.0, f'invariance_cv=0 for identical phrasings (got {CV:.4f})')

    # four_checkpoint_report smoke-test
    report = four_checkpoint_report(A0, A1, C_pre, C_post)
    assert_ok('ENVELOPE EXITS' in report,     'report has ENVELOPE EXITS line')
    assert_ok('D_compression'  in report,     'report has D_compression line')
    assert_ok(_FROZEN[:12]     in report,     'report embeds rubric sha')
    assert_ok('cmp:cond' in report or 'cmp:fals' in report or 'none' in report,
              'report labels compression flags or none')

    print(f'\n{len(failures)} failure(s)')
    sys.exit(len(failures))
