# MARK LIII stability specification

## Problem and user goal

MARK LIII needs a safer, repeatable release baseline while adding clearer startup readiness feedback, auditable computer actions, and a more accessible dashboard setup experience.

## Scope

- Ensure secret configuration is ignored by Git.
- Remove trailing whitespace in the current changed files without changing behavior.
- Add a baseline automated test suite and CI checks.
- Add startup health information for API key, audio devices, model configuration, and discovered actions/plugins.
- Add a local audit log for computer-control actions and confirmations.
- Improve dashboard accessibility and provide a guided first-run setup path.

## Non-goals

- Changing live production infrastructure or publishing a release.
- Replacing the existing UI or authentication model.
- Storing secret values in logs, tests, documentation, or audit records.

## Requirements

1. `config/api_keys.json` and other secret paths must be ignored by Git.
2. Automated checks must run syntax compilation and the baseline tests in CI.
3. Health output must report readiness without exposing secrets.
4. Audit records must avoid secrets and retain action/result/time information locally.
5. Dashboard controls must have accessible labels and a clear setup entry point.

## Acceptance criteria

- `git check-ignore config/api_keys.json` succeeds.
- Python source compiles and baseline tests pass locally.
- CI workflow runs the same compile and test checks on push and pull request.
- Startup health report includes key, audio, model, actions, and plugins status without secret values.
- A computer-control action can write a local audit record with action and result.
- Dashboard login and application pages include an accessible first-run/setup path and labeled controls.

## Assumptions and risks

- The dashboard remains local/LAN scoped and users retain responsibility for their local credentials.
- Existing modified files contain user work and must not be overwritten beyond requested whitespace cleanup or additive changes.
- Audio readiness can be reported from saved configuration and device discovery; it cannot guarantee physical hardware works until used.

## Roles and handoffs

Project Manager owns scope and plan. Security owns secret-ignore and audit privacy. QA owns baseline tests. Code Review owns whitespace and verification. DevOps owns CI. Accessibility owns dashboard labels and setup path.
