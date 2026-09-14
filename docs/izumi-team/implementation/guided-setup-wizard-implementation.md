# Guided setup wizard implementation

## Changed areas

- Added [core/setup_wizard.py](../../../core/setup_wizard.py) for display-safe API, model, audio, plugin, and permission readiness states.
- Extended [ui.py](../../../ui.py) so the existing first-run overlay presents a readiness checklist, repair actions, keyboard-focusable controls, and persisted completion markers.
- Preserved unrelated configuration fields when the first-run API key and OS values are saved.
- Added ignored `config/setup_progress.json` persistence containing only known checklist booleans and an update timestamp.
- Added setup-state and persistence tests to [tests/test_stability.py](../../../tests/test_stability.py).

## Checks and test results

- `python -m unittest discover -s tests -v`: passed, 5 tests.
- `python -m py_compile core/setup_wizard.py core/audit.py core/action_loader.py core/confirm.py core/health.py dashboard/server.py ui.py main.py`: passed.
- `git -c core.whitespace=cr-at-eol diff --check`: passed.
- Existing CI workflow already discovers `tests/`, so the new tests are included in push and pull-request checks.

## Known limitations

- The initial wizard performs local audio enumeration and may show `manual review` for permissions because operating-system permission APIs are platform-specific.
- Plugin status is shown as pending until normal application initialization performs plugin discovery; the existing plugin manager remains the detailed repair surface.
- Model readiness means API-key configuration, not a live Gemini request.
- PyQt visual interaction was not automated in the headless environment; UI correctness was checked by compilation and targeted code review.

## Release or rollback notes

No commit, merge, deployment, or external service call was performed. Roll back the helper, `ui.py` changes, tests, ignore entry, and feature documents together if the wizard is not desired.

## Next handoff

User review of the first-run checklist wording and repair flow. The next recommended feature is action permissions with `safe`, `confirm`, and `blocked` levels, built on the existing confirmation gate and audit events.