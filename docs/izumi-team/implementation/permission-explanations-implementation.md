# Permission explanations and reset implementation

## Changed areas

- Added stable explanations for every permission policy key.
- Added `reset_policy()` which removes only permission overrides and preserves API, audio, identity, and plugin settings.
- Updated the native permission editor to display consequences and provide `RESET DEFAULTS`.
- Added policy tests for explanation coverage and configuration preservation.

## Checks and test results

- `python -m unittest tests.test_stability tests.test_gui_smoke -v`: passed, 15 tests.
- `python -m py_compile core/permissions.py ui.py`: passed.
- GUI smoke test passed in offscreen mode; Qt emitted only the known font-directory warning.

## Known limitations

- The remote dashboard permission editor does not yet display the same explanation text or reset button.
- Reset is intentionally immediate and affects only permission overrides.

## Release and rollback notes

No commit or deployment was performed for this feature. Roll back the policy/UI/test/document changes together; configuration data outside `permissions` remains untouched.

## Next handoff

Run the full suite and decide whether to mirror explanations/reset into the remote dashboard.