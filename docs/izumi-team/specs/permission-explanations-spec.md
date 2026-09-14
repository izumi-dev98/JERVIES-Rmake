# Permission Explanations and Reset Specification

## Problem

MARK LIII lets users choose `safe`, `confirm`, or `blocked`, but the native editor does not explain the consequences and has no one-click way to restore conservative defaults.

## Target User

A MARK LIII desktop user reviewing or repairing local action safety settings.

## Goal

Make permission choices understandable and reversible without changing the existing enforcement model.

## Scope

- Add stable, display-safe explanations for each permission key.
- Add a reset-to-default operation that removes custom overrides and restores conservative policy defaults.
- Add explanation text and a reset control to the native PyQt permission editor.
- Add hardware-free policy tests.

## Non-goals

- Changing permission defaults.
- Adding new action families.
- Resetting unrelated configuration settings.
- Changing the remote dashboard API in this task.

## Requirements

1. Explanations must not contain secrets, user content, or dynamic command arguments.
2. Reset must affect only permission overrides.
3. Reset defaults must preserve unrelated API, audio, plugin, and identity settings.
4. The native editor must clearly expose the reset action and current consequences.
5. Existing permission enforcement and confirmation behavior must remain unchanged.

## Acceptance Criteria

- Every policy key has a non-empty explanation.
- Reset removes the `permissions` object or leaves it empty while preserving unrelated config keys.
- The editor can display explanations and invoke reset.
- Existing tests and new policy tests pass.

## Assumptions and Risks

- Conservative defaults remain `confirm` for risky action families and `safe` for unlisted actions.
- The native editor is the primary changed UI; dashboard behavior remains compatible.

## Success Measure

Users can understand each permission level and return to safe defaults without manually editing configuration files.
