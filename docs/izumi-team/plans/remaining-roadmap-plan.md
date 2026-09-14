# MARK LIII Remaining Roadmap Plan

| Status | Owner | Task | Dependency | Verification | Handoff |
| --- | --- | --- | --- | --- | --- |
| verified | Project Manager | Define the remaining roadmap and release boundaries | Existing stability work | Spec exists | Security, Backend |
| verified | Security / Backend | Add centralized permission policy and confirmation/audit integration | Existing action and confirm paths | Unit tests; blocked handler test | Frontend, QA |
| verified | Backend | Add plugin counts and safe reload callback | Plugin registry lifecycle | Compile and focused tests | UI, QA |
| verified | Backend | Add degraded-state model/audio/dashboard status contract | Existing health and reconnect loop | State compile and tests | UI, QA |
| verified | Backend | Add filtered and clearable local audit API | Existing audit JSONL | Audit tests; route test | Frontend, Security |
| verified | Backend / Frontend | Add local memory controls | Existing memory manager and overlay | Memory tests; UI compile | QA |
| verified | QA | Add mocked model, dashboard, permissions, plugin, audit, and memory tests | Test seams | Full unittest suite: 11 passed | Review |
| verified | Accessibility / Frontend | Expose permission, audit, plugin, and memory controls accessibly | Existing PyQt/dashboard surfaces | Static review; GUI unavailable | QA |
| verified | Code Review | Review current user changes and new feature diff | Implementation | `git -c core.whitespace=cr-at-eol diff --check` | DevOps |
| verified | DevOps/Git | Run local CI-compatible checks and inspect remote CI readiness | Test suite | Compile, unittest, workflow review | Release |
| verified | Technical Writer / Support | Record usage, risks, rollback, and credential-history guidance | Final behavior | Implementation record | User |
| done | All | Release recommendation and next handoff | Completed checks | Implementation record | User |

## Delivery boundaries

- Implement and verify locally first; do not claim remote CI, commit, merge, deploy, or credential rotation without successful execution.
- Preserve prior stability and guided-setup artifacts.
- Use additive interfaces and keep unknown permissions conservative.
- If a feature requires a GUI display, mark it verified by compile/static review and leave GUI execution as an explicit environment limitation.

## Rollback

Rollback each feature group independently: permission policy, plugin lifecycle, degraded status, audit API, and memory controls. Preserve local audit and memory files unless the user explicitly requests data deletion.
