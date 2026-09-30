# Team Communication & Governance (`team_communication`)

This directory houses team coordination, experiment registries, architectural decisions, and operational agreements for the Terminal Titans Amazon ML Challenge 2026 team.

---

## 1. Directory Contents

| Document | Purpose |
|---|---|
| [`experiment_registry.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/team_communication/experiment_registry.md) | **Master Experiment Ledger**: Complete registry of all 15 parallel experiment tracks (Kaggle, Colab, Local, SageMaker), tracking hypothesis, metrics, and decisions. |
| [`insight_registry.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/team_communication/insight_registry.md) | **Empirical Insights Log**: Empirically verified findings (blocking recall, feature importance, singleton gating, open-set handling). |
| [`decisions.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/team_communication/decisions.md) | **Architectural Decision Records (ADR)**: Formal logs of structural decisions (decoupling candidate generation, platform task allocation, scoring threshold policies). |
| [`experiment_assignments.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/team_communication/experiment_assignments.md) | **Track Assignments**: Deliverables, research questions, and resource allocation across team members. |
| [`baseline_v0.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/team_communication/baseline_v0.md) | **Baseline Specification**: Initial benchmark parameters, hardware constraints, and baseline reproduction targets. |
| [`ownership.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/team_communication/ownership.md) | **Component Ownership Matrix**: Primary and secondary owners for data, blocking, retrieval, matching, and validation. |

---

## 2. Governance Protocol
1. Register runs in `experiment_registry.md` before execution.
2. Log verified discoveries in `insight_registry.md`.
3. Major architectural shifts require an ADR in `decisions.md`.
