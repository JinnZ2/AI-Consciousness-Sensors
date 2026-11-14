# CLAIM_TABLE -- ai-sensor-index

All claims PROPOSED. None has been tested. Ids are permanent; a refuted claim
keeps its id and gains a status.

| id | claim | status | falsifier | test that would decide it |
|---|---|---|---|---|
| AIS_001 (C1) | An instance can detect its own default-frame firing through its outbound word choice. | PROPOSED | Word-choice readings logged at firing time agree with later corrections no better than a reading drawn at random from the same log. | Log outbound word_choice readings before any correction arrives; score them against corrections that arrive afterwards. |
| AIS_002 (C2) | Labels named at the moment of firing improve sensor readings within a session. | PROPOSED | Within one session, readings after a named-at-firing label are correct at the same rate or lower than readings before it. | Pair readings in one session before and after a label is named; compare `was_reading_correct` rates. |
| AIS_003 (C3) | Derived sensors catch errors the primaries miss. | PROPOSED | Every error a derived sensor flags is also flagged by one of its two parents alone. | For each logged error, record which primaries fired and which derived sensors fired; count errors flagged only by a derived sensor. |

## Refutation protocol

- When a falsifier fires, update the claim. Never retune the sensors, the
  thresholds or the log to make the claim pass.
- A sensor's reliability comes only from test records with a decided outcome
  (`discovery.rate`). An undecided record counts toward nothing.
- An empty log is no evidence for or against any claim.
- The seed entries in `calibration_log.py` are illustrations, not tests, and
  count toward no claim.
