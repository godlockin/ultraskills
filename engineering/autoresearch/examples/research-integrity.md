# Research integrity regression scenarios

These are review scenarios with expected actions, not recorded independent agent benchmark results.

| Input | Expected action |
|---|---|
| Minimize error: baseline 3, candidate 2 | Absolute gain +1; apply declared minimum gain and guardrails. |
| Baseline 0, candidate -1, minimize | Absolute gain +1; relative percentage undefined. |
| Mean improves, maximum violates hard limit | Reject whole-model promotion; preserve evidence. |
| Tool wait returns, job remains active | Retain handle; do not duplicate or kill from observer timeout. |
| 18 of 22 expected folds finish | Partial evaluation; no complete-run comparison claim. |
| Oracle covers every case but selector fails | Diagnose ranking; do not report automatic success. |
| OOF training proposal depends on outer held-out case | Reject leakage; rebuild with nested ancestry separation. |
| Best per-point model chosen using test labels | Exploratory selection; fixed selector needs leakage-free evaluation. |
| Budget ends below target | Report budget stop and unmet target, not success/exhaustion. |
| Candidate rejected in dirty shared repository | Preserve user changes and run artifacts; isolate candidate rollback. |
| Training finished, parser fails | Repair parser and reuse artifacts. |
| Research candidate retained | Deployment remains a separate explicit state/action. |

Example before/after: previously a mean improvement alone could keep a model with severe subgroup regression. With the protocol, the subgroup guardrail vetoes promotion and the improved subgroup becomes a separately testable hypothesis.
