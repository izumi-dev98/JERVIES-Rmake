# MARK LIII final hardening implementation

## Changed areas

- Added a native PyQt `ACTION PERMISSIONS` editor for safe, confirm, and blocked levels.
- Updated plugin reload behavior to avoid reconnecting when no model session is active.
- Added an offscreen GUI smoke test covering setup, permissions, plugins, memory, and confirmation overlays with audio enumeration mocked.
- Added final-hardening spec and plan with tag and rollback guidance.

## Checks and test results

- `python -m unittest discover -s tests -v`: passed, including 11 core tests and 1 GUI smoke test.
- `python -m unittest tests.test_gui_smoke -v`: passed with `QT_QPA_PLATFORM=offscreen`.
- `python -m compileall -q core actions dashboard memory tests ui.py main.py`: passed.
- `git -c core.whitespace=cr-at-eol diff --check`: passed.
- Remote Actions API for `7d6a8e5`: returned zero visible workflow runs; GitHub CLI was unavailable.

## Known limitations

- Active-session plugin reload still reconnects because Gemini Live tool declarations are session-scoped.
- GUI smoke coverage is construction-level, not full click-flow coverage.
- No credential rotation was performed because workspace and history scans found no exposed credential.

## Release and rollback notes

The prior release commits are `e304b42` and `7d6a8e5`. A final tag can be created after this hardening commit with `git tag -a v0.1.0 -m "MARK LIII hardened release" <commit>` and pushed with `git push origin v0.1.0`. Roll back by reverting the hardening commit or returning to the previous known-good commit; preserve local audit and memory data.

## Next handoff

Observe GitHub Actions for the final hardening push. Full interaction tests can expand when a stable desktop test runner is available.