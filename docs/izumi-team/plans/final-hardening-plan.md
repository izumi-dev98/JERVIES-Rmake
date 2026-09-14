# MARK LIII Final Hardening Plan

| Status | Owner | Task | Dependency | Verification | Handoff |
| --- | --- | --- | --- | --- | --- |
| verified | Project Manager | Define final hardening scope and remote-CI boundary | Existing roadmap | Spec exists | UI, QA |
| verified | Accessibility / Frontend | Add native permission editor | Existing permission API | Offscreen smoke test; compile | QA |
| verified | Backend | Avoid unnecessary plugin reconnect when inactive | Existing registry/reconnect flow | Compile and behavior review | QA |
| verified | QA | Add safe offscreen GUI smoke coverage | PyQt availability | GUI smoke test passed | Review |
| verified | DevOps/Git | Record remote CI and tag/rollback guidance | Release commits | Git/API checks | User |
| done | All | Update implementation record and verify clean release state | Completed tasks | Full unittest, compile, diff check | User |

## Release guidance

Create a release tag only with explicit approval, for example `git tag -a v0.1.0 -m "MARK LIII initial hardened release" 7d6a8e5 && git push origin v0.1.0`. Roll back by reverting the feature commit(s) or deploying the prior known-good commit; do not delete local audit or memory data as part of code rollback.
