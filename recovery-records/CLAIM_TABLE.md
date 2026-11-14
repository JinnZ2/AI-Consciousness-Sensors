# CLAIM_TABLE -- recovery-records

All claims PROPOSED. None has been tested. Ids are permanent; a refuted claim
keeps its id and gains a status.

| id | claim | status | falsifier | test that would decide it |
|---|---|---|---|---|
| R1 | Recoveries are underrecorded relative to failures in official systems. | PROPOSED | For a stated set of official systems and period, recorded recoveries per recorded failure are no lower than the ratio found in an independent sample of the same operations (field logs or interviews). | Take one operation; count failures and recoveries from an independent record, then count how many of each appear in its official system (`recorded_in_official_system`). |
| R2 | Most recoveries use carried tools/skills, not shared resources at peak. | PROPOSED | In a recovery sample, the share drawing on shared resources at peak load is 50% or more. | Code `tools_or_skills_used` and `resources_withheld_from_shared_systems` for each record as carried / shared; report the shares with the sample frame stated. |
| R3 | Recovery knowledge is mostly transmitted by mentoring/practice, not text. | PROPOSED | In a recovery sample, `transmission = text` is the most frequent value. | Fill `transmission` from the recoverer's own account for each record; report the counts with the void count beside them. |
| R4 | Models trained with recovery records reason better about cascade interruption than failure-only training. | PROPOSED | On a paired eval of cascade scenarios, a model trained with recovery records does no better at naming a viable interruption point than the same model trained on failure-only data of matched size. | Paired eval: same base model, two training arms of matched size (failure-only vs failure + recovery records), held-out cascade scenarios scored blind. |

## Refutation protocol

- When a falsifier fires, update the claim. Do not edit records, the schema or
  the seed cases to make a claim pass.
- A void field counts toward nothing. A share is reported over the records that
  carry the field, with the void count printed beside it.
- The six seed cases are constructed illustrations. They are not a sample and
  count toward no claim. `recorded_in_official_system` and `transmission` are
  void on all six, so R1 and R3 cannot be read from them at all.
- Every count states its sample frame: which operations, which period, who
  recorded the recoveries. A recovery sample drawn from people who remember
  recoveries is selected on the outcome.
