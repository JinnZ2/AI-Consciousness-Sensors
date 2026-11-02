#!/usr/bin/env python3
"""
tail_watch.py -- Tail-Watch Sensor (wisdom glyph): is a structure moving toward a phase shift
before the average shows it?

STATUS: PROPOSED instrument, co-authored. CC0. stdlib only.
Doc: TAIL_WATCH_SENSOR.md. System-level sensor, not an emotion. Rising variance AND rising lag-1
autocorrelation together = critical-slowing-down signal (PROPOSED trigger). "No signal" is not proof
of stability. Too few points = UNMEASURED, never a zero.

USAGE
  python3 tail_watch.py              run the planted selftest (5 checks)
"""
import statistics as st
def lag1_autocorr(xs):
    m = st.mean(xs); den = sum((a-m)**2 for a in xs)
    return sum((a-m)*(b-m) for a,b in zip(xs,xs[1:]))/den if den else 0.0
def trend(vals):
    n=len(vals)
    if n<2: return 0.0
    xm,ym=(n-1)/2,st.mean(vals)
    return sum((i-xm)*(v-ym) for i,v in enumerate(vals))/sum((i-xm)**2 for i in range(n))
def tail_watch(series, window=20):
    return [(i, st.pvariance(series[i-window:i]), lag1_autocorr(series[i-window:i]))
            for i in range(window, len(series)+1)]
def flicker_count(series, threshold):
    """Crossings of a state boundary = pulse in/out (PROPOSED)."""
    return sum(1 for a,b in zip(series,series[1:]) if (a-threshold)*(b-threshold)<0)
def flag(series, window=20):
    r = tail_watch(series, window)
    if len(r) < 3: return "UNMEASURED"
    if trend([v for _,v,_ in r])>0 and trend([a for _,_,a in r])>0:
        return "ASSESS: variance and autocorrelation both rising"
    return "no slowing signal in this window (not proof of stability)"
def consensus_check(agree_share, reasoned_dissent_share):
    """Thresholds PROPOSED, uncalibrated.**"""
    if agree_share>0.8 and reasoned_dissent_share<0.1:
        return "RUN DISAGREEMENT PASS -> neutral -> keep what survives"
    return "normal review"
def selftest():
    import random; random.seed(1); x,s=0.0,[]
    for t in range(200):
        k=1.0-t/220; x=x-k*x*0.5+random.gauss(0,0.1); s.append(x)
    assert flag(s).startswith("ASSESS")
    assert flag(s[:10])=="UNMEASURED"
    assert consensus_check(0.9,0.05).startswith("RUN")
    assert consensus_check(0.5,0.3)=="normal review"
    assert flicker_count([0,1,0,1],0.5)==3
    print("tail_watch selftest 5/5")
if __name__=="__main__": selftest()
