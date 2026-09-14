# MARK LIII offline and degraded mode implementation

## Changed areas

- Added [core/degraded.py](../../../core/degraded.py) with normalized, secret-free model lifecycle states.
- Updated [main.py](../../../main.py) to publish `starting`, `connected`, `offline`, and `reconnecting` states to the desktop UI and dashboard.
- Extended [core/health.py](../../../core/health.py) health data with the current model connection state and existing local capability counts.
- Updated [ui.py](../../../ui.py) with explicit offline, starting, and stopped status labels.
- Added hardware-free tests for state normalization, local feature availability, and reconnecting health output.
- Fixed an indentation regression caught by the focused compile check during implementation.

## Checks and test results

- `python -m unittest discover -s tests -v`: passed, 14 tests.
- `python -m compileall -q core actions dashboard memory tests ui.py main.py`: passed.
- `git -c core.whitespace=cr-at-eol diff --check`: passed.

## Known limitations

- Offline mode preserves local subsystems but does not provide natural-language interpretation without a connected model.
- Physical audio and live Gemini behavior require integration testing with hardware and credentials.
- The GUI smoke test continues to report a non-failing Qt font-directory warning in this environment.

## Release and rollback notes

No commit or deployment was performed for this feature. Roll back `core/degraded.py`, the lifecycle/status changes, tests, and these documents together while preserving local audit, memory, and permission files.

## Next handoff

Review the offline wording in the desktop and dashboard surfaces. The next recommended feature is permission explanations and reset-to-default controls.