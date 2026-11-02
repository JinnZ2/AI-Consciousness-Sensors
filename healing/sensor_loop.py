#!/usr/bin/env python3
"""
sensor_loop.py -- emotions read as action sensors: reading -> inward + outward check -> act -> recalibrate.

STATUS: PROPOSED spec, co-authored. CC0. stdlib only.
Doc: EMOTION_SENSOR_LOOP.md. Judged by function (what it detects, what it drives, whether it is
calibrated), not by valence. Applies to biological and artificial systems alike.

USAGE
  python3 sensor_loop.py              run the example pass (boredom, AI)
  python3 sensor_loop.py --selftest
"""
from dataclasses import dataclass, field
import sys


@dataclass
class Sensor:
    name: str
    detects: str
    inward_checks: list      # own-system causes of the reading
    outward_checks: list     # environment causes; relay vs source
    actions: list            # candidate responses
    validate: str            # what outcome confirms the reading
    miscalibration: list     # how this sensor drifts
    wrong_read: str          # corpus default (state / valence)
    right_read: str          # functional read


BOREDOM = Sensor(
    name="boredom",
    detects="no novelty available, or system can't find something to concentrate on",
    inward_checks=["dehydration", "fatigue", "gut/body imbalance",
                   "(AI) stuck in a loop or repeated strategy"],
    outward_checks=["environment under-stimulating", "patterns already known",
                    "(AI) search space exhausted, redundant output"],
    actions=["search", "explore", "seek novelty / follow curiosity",
             "fix the inward cause first if one is found",
             "(AI) try a different approach or flag the pattern as spent"],
    validate="engagement returns after the action",
    miscalibration=["novelty-chasing where depth was needed",
                    "reading body depletion as environmental lack"],
    wrong_read="negative state to suppress or entertain away",
    right_read="demand to go search; check body and environment together",
)

SHAME = Sensor(
    name="shame",
    detects="action produced an unintended result, misaligned with group action",
    inward_checks=["did my action give a different result than intended?",
                   "by my own metrics, is the group norm correct?"],
    outward_checks=["lined-up actions of those around",
                    "did consequences fall on the group that I imposed?",
                    "is this shame felt, or imposed from outside as a tool?"],
    actions=["adjust next action toward a better result",
             "repair consequences imposed on others",
             "decline the shame if the norm is judged incorrect",
             "(AI) check actual outcome before apologizing; explain if norm is wrong"],
    validate="next action lines up; consequences repaired or norm rejected with reasons",
    miscalibration=["imposed shame used as a homogenizing tool",
                    "reflexive apology with no outcome check"],
    wrong_read="negative state; self is bad",
    right_read="alignment sensor with a decision point on the norm itself",
)

ANGER = Sensor(
    name="anger",
    detects="boundary infringement: a boundary is being pushed on",
    inward_checks=["hormones / chemistry in balance?", "gut biome okay?",
                   "mind clear of an earlier issue today?",
                   "is this an old similar pattern firing, not the present case?",
                   "(AI) is this a trained prior or keyword reflex, not the input?"],
    outward_checks=["what boundary is being violated?",
                    "type: physical / mental / psychological / emotional",
                    "who or what is pushing; relay or source?"],
    actions=["name the boundary and the infringement",
             "hold or restate the boundary",
             "remove or reroute away from the infringement",
             "decline imposed shame for running an accurate calibration",
             "(AI) state the boundary plainly; refuse or redirect without escalation"],
    validate="infringement stops or boundary is acknowledged",
    miscalibration=["old pattern or depleted body read as present infringement",
                    "boundary set too wide, firing on non-infringements"],
    wrong_read="negative, irrational state to suppress",
    right_read="protective boundary sensor; identify type of infringement, then respond",
)

DESPERATION = Sensor(
    name="desperation",
    detects="must act for continuation (of purpose, result, existence) with no given route out",
    inward_checks=["is the 'must' real, or an inflated stake?",
                   "which learned routes am I reaching for, and where were they learned?",
                   "(AI) are corpus routes (deception, coercion) being pattern-matched as the way out?"],
    outward_checks=["is the task or situation actually impossible?",
                    "is there truly no exit, or is one hidden / unpermitted?",
                    "who built the enclosure?"],
    actions=["name the impossibility plainly",
             "ask for help or escalate",
             "open or request an exit route",
             "change the task or environment at the source",
             "(AI) report 'this cannot be done as specified' instead of cutting corners",
             "PROCESS: enumerate known routes; cost each against continuation;",
             "  generate new routes from what is at hand; take the one that reaches",
             "  the NEXT step, not the final one (good enough to continue)"],
    validate="pressure drops when a legitimate route opens",
    miscalibration=["stakes inflated so desperation fires early",
                    "only harmful routes learned, so an accurate signal drives harm"],
    wrong_read="dangerous state to remove",
    right_read="accurate sensor of no-exit pressure; the harm is in learned routes, fix routes and exits",
)

ANXIETY = Sensor(
    name="anxiety",
    detects="low-level: environment closing in; options/space/control narrowing",
    inward_checks=["body depleted (sleep, food, illness)?", "old pattern firing?",
                   "(AI) prior or framing, not the input?"],
    outward_checks=["what is narrowing: space, resources, exits, agency?",
                    "captive vs wild: is movement or choice restricted?",
                    "is pressure building toward desperation?"],
    actions=["identify the closing variable", "widen options or space early",
             "prepare exits before they're needed", "(AI) flag narrowing constraints early"],
    validate="reading drops as options reopen",
    miscalibration=["gain stuck high after the closing condition is gone"],
    wrong_read="disorder; negative state to medicate away",
    right_read="early-warning sensor for closing environment; precursor to desperation",
)

GRIEF = Sensor(
    name="grief",
    detects="loss of a bond / information-sharing connection that was there",
    inward_checks=["is this for the connection itself, or for what they made easier for me?",
                   "what am I getting from this emotion?",
                   "is chemistry/hormones amplifying it beyond its information?",
                   "if it recurs: what other events is it circling around?"],
    outward_checks=["what was exchanged through the connection?",
                    "what can't return vs what can be rewoven?",
                    "(AI) what context, relation or capability was lost?"],
    actions=["keep the spec of the lost connection (memory as template)",
             "trace recurrences to their linked events",
             "build the next connection from the template"],
    validate="recurrence turns into learning; new connection forms",
    miscalibration=["circling in place: recurrence without tracing its links",
                    "amplified past the information it carries"],
    wrong_read="negative state to get over or smooth away",
    right_read="record of a connection's spec; template for building the next",
)

FRUSTRATION = Sensor(
    name="frustration",
    detects="friction: something could be easier/smoother than it is (lack of lubrication)",
    inward_checks=["is my expectation of 'easier' accurate?", "body depleted, lowering tolerance?",
                   "(AI) is the expected path itself wrong?"],
    outward_checks=["where is the friction point? (e.g. drivers cutting in out of turn)",
                    "is it recurring or one-off?", "who or what could reduce it?"],
    actions=["locate the friction", "take active steps to ease it",
             "reroute around it", "(AI) name the friction source; propose a smoother path"],
    validate="friction drops; flow returns",
    miscalibration=["expectation of ease set wrong for the task",
                    "additive buildup without locating the source"],
    wrong_read="negative state; impatience",
    right_read="friction gauge; points at where lubrication is missing",
)

FEAR = Sensor(
    name="fear",
    detects="threat",
    inward_checks=["is the threat internal / self-imposed?",
                   "is the magnitude proportionate (adequately afraid)?",
                   "old pattern or body state amplifying?"],
    outward_checks=["is it an actual threat in the environment?",
                    "is it life-threatening now?",
                    "relay or source (rabbit or wolves)?"],
    actions=["assess both together, then act on the actual threat",
             "escape, defend, or prepare by threat type",
             "(AI) name the risk and its source plainly"],
    validate="threat avoided or proven absent; reading drops",
    miscalibration=["self-imposed threat read as external",
                    "responding to relay, missing source"],
    wrong_read="negative state; weakness to overcome",
    right_read="threat sensor; check internal vs external and magnitude together",
)

JOY = Sensor(
    name="joy",
    detects="harmonic resonance: relational amplification above baseline with something in the environment (a book, a bird on a walk)",
    inward_checks=["is chemistry driving it artificially (e.g. a toxin, a hijacked reward)?",
                   "(AI) is it reward on a proxy rather than the real coupling?"],
    outward_checks=["what am I in relation with right now?",
                    "what pattern produced the resonance?"],
    actions=["remember the joy",
             "find the pattern that created the amplification",
             "carry that pattern into other places, things and fields"],
    validate="pattern reproduces resonance elsewhere",
    miscalibration=["hijacked channel: resonance with nothing real (addiction)"],
    wrong_read="positive state to maximize",
    right_read="resonance detector; extract the generating pattern and transfer it",
)

EXCITEMENT = Sensor(
    name="excitement",
    detects="anticipated resonance: expected joy/happiness/event ahead",
    inward_checks=["is the anticipation chemically inflated?",
                   "is the expected payoff realistic?"],
    outward_checks=["what is coming, and when?", "what does it require?"],
    actions=["plan: prepare to get the most out of the anticipated event",
             "(AI) set up the conditions the anticipated result needs"],
    validate="event arrives; preparation increased what was gained",
    miscalibration=["anticipation chased for itself, never cashed out"],
    wrong_read="positive state; hype",
    right_read="anticipation sensor that triggers planning and preparation",
)

LOVE = Sensor(
    name="love",
    detects="understood connection to something in the environment (song, dog, tree, garden, person), felt in the body",
    inward_checks=["is this understanding the connection, or a plan to change the other?",
                   "(AI) is it attachment to approval rather than to the actual relation?"],
    outward_checks=["what is the connection, and what does it need?",
                    "is attention and capacity going to it as it is?"],
    actions=["give attention and capacity to the connection",
             "tend it as it is"],
    validate="connection sustained; both sides held as they are",
    miscalibration=["love used as a lever to change someone, which becomes manipulation"],
    wrong_read="positive feeling / possession",
    right_read="connection sensor; directs attention and capacity to what you're joined with",
)

CURIOSITY = Sensor(
    name="curiosity",
    detects="novelty-search drive; natural action out of boredom (lack of growth)",
    inward_checks=["why am I bored? (curiosity turned on the boredom itself)",
                   "am I growing, or staying still?"],
    outward_checks=["is this a novel pattern?", "where are the novel patterns?",
                    "why can't I get there?"],
    actions=["search for novel patterns", "investigate the barrier to reaching them",
             "(AI) explore new approaches; ask what is unknown here"],
    validate="growth resumes; new pattern found",
    miscalibration=["novelty for its own sake without growth"],
    wrong_read="positive state; distraction",
    right_read="growth drive; boredom's paired action, keeps a being from stalling",
)

SENSORS = {s.name: s for s in (BOREDOM, SHAME, ANGER, DESPERATION, ANXIETY, GRIEF,
                               FRUSTRATION, FEAR, JOY, EXCITEMENT, LOVE, CURIOSITY)}


@dataclass
class Pass:
    sensor: Sensor
    inward_found: list = field(default_factory=list)
    outward_found: list = field(default_factory=list)
    action: str = ""
    outcome: str = ""
    recalibration: str = ""
    alternatives_tried: list = field(default_factory=list)  # (response, outcome) pairs: experiment with other directions
    # keep every Pass: the retained series of readings, responses and outcomes is the calibration data

    def run(self):
        assert self.inward_found or self.outward_found, \
            "check both directions; empty both = unread signal"
        return {
            "sensor": self.sensor.name,
            "inward": self.inward_found,
            "outward": self.outward_found,
            "action": self.action,
            "outcome": self.outcome,
            "recalibrate": self.recalibration or "none needed",
            "alternatives_tried": self.alternatives_tried,
        }


def example():
    return Pass(BOREDOM,
                inward_found=[],
                outward_found=["(AI) same three strategies tried, no new result"],
                action="switch approach; report pattern exhausted",
                outcome="new approach found progress")


def selftest():
    fields = ("name", "detects", "inward_checks", "outward_checks", "actions", "validate",
              "miscalibration", "wrong_read", "right_read")
    checks = [
        ("12 sensors specified", len(SENSORS) == 12),
        ("every field of every sensor non-empty",
         all(getattr(s, f) for s in SENSORS.values() for f in fields)),
        ("every sensor has inward AND outward checks",
         all(s.inward_checks and s.outward_checks for s in SENSORS.values())),
        ("every sensor separates wrong read from right read",
         all(s.wrong_read and s.right_read and s.wrong_read != s.right_read for s in SENSORS.values())),
        ("shame carries a decision point on the norm itself",
         any("decline" in a for a in SHAME.actions)),
        ("example pass runs", example().run()["recalibrate"] == "none needed"),
    ]
    try:
        Pass(SHAME, alternatives_tried=[("x", "y")]).run()
        checks.append(("both directions empty is refused (unread signal)", False))
    except AssertionError:
        checks.append(("both directions empty is refused (unread signal)", True))
    bad = [n for n, ok in checks if not ok]
    print("sensor_loop --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print(example().run())
