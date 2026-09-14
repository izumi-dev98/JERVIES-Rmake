# Guided Setup Wizard Plan

| Status | Owner | Task | Dependency | Verification | Handoff |
| --- | --- | --- | --- | --- | --- |
| verified | Project Manager | Define the resumable checklist MVP and acceptance criteria | Existing first-run overlay | Spec exists | UI/UX, Backend |
| verified | Backend Developer | Add pure setup-state checks and ignored progress persistence | Existing config and audio/plugin APIs | Unit tests | Frontend, QA |
| verified | UI/UX and Accessibility | Extend the setup overlay with statuses, repair actions, and keyboard flow | Setup-state helper | Static review and focused UI inspection | QA |
| verified | Frontend Developer | Wire repair actions to existing API, audio, plugin, and settings surfaces | UI design | PyQt compile/import check | QA |
| verified | QA Engineer | Add hardware-free tests for all states and persistence | Testable helper | `python -m unittest discover -s tests -v` | Code Review |
| verified | Security | Review persisted progress and status output for secret leakage | Implementation | Secret-scan assertions | Code Review |
| verified | Code Review | Review current diff and line endings | All edits | `git -c core.whitespace=cr-at-eol diff --check` | Release |
| verified | Technical Writer | Update setup guidance if the user-facing flow changes | Final UI | Spec and implementation record | User |
| verified | DevOps/Git | Confirm CI runs the new tests | Tests | Existing CI workflow includes test discovery | Release |
| done | All | Record implementation results and next handoff | Completed checks | Implementation record | User |

## Decisions

- Extend the existing `SetupOverlay` instead of creating a second window.
- Keep setup state in a local ignored JSON file containing only booleans, statuses, and timestamps.
- Treat model readiness as configuration readiness; a live Gemini request remains outside first-run checks.
- Use injectable callbacks for audio/plugin/permission checks so tests never need hardware or network access.

## Rollback

Revert the wizard helper, overlay additions, tests, and documentation together. Existing API-key setup and settings panels remain the fallback path.
