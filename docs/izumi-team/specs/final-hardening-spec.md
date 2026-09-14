# MARK LIII Final Hardening Specification

## Problem

The permission policy is currently editable through the remote dashboard but not the native desktop UI. Plugin reload always requests a model reconnect even when no session is active, and GUI behavior has only compile/static coverage. Remote CI visibility also needs a recorded result.

## Target User

The MARK LIII owner operating the native desktop assistant and reviewing a release from GitHub.

## Goal

Close the remaining local usability and release-verification gaps without changing the safety model or claiming unavailable remote results.

## Scope

- Add a native PyQt permission editor for the six existing permission keys and three policy levels.
- Improve plugin reload to avoid unnecessary reconnect requests when no live model session exists.
- Add an offscreen GUI smoke-test module covering setup, permissions, plugin reload control, memory controls, and confirmation UI when dependencies permit.
- Record remote CI visibility and release/tag guidance.

## Non-goals

- Hot-swapping tool declarations into an already-connected Gemini Live session.
- Deploying the application.
- Rotating credentials without evidence of exposure or user-controlled provider access.
- Replacing the existing dashboard permission editor.

## Requirements

1. Native permission changes must use the same local config and policy validation as the dashboard.
2. The native editor must expose `safe`, `confirm`, and `blocked` for computer control, deletion, shutdown, restart, Wi-Fi, and messaging.
3. A plugin reload with no active model session must update the registry without requesting reconnect.
4. GUI tests must skip with a clear reason when PyQt or a display backend is unavailable.
5. GUI tests must never use real credentials, network, microphone, speaker, or destructive actions.
6. Release documentation must distinguish local checks, remote CI visibility, credential scans, and tag readiness.

## Acceptance Criteria

- Native settings can open, display current policy, save valid levels, and reject invalid levels.
- Plugin reload behavior is deterministic for active and inactive sessions.
- The GUI smoke test is collected by the normal test command and passes or skips cleanly.
- Current remote CI status for the latest release commit is recorded accurately.
- A release tag command and rollback guidance are documented without creating a tag unless explicitly requested.

## Risks and Assumptions

- The workspace may not have a display server or complete Qt WebEngine installation.
- Existing user edits remain intentional and must not be reverted.
- Live model tool declarations are session-scoped, so active-session plugin reload still requires the existing reconnect path.

## Success Measure

A desktop user can control action permissions locally, plugin reload does not perform unnecessary reconnect work, and release verification clearly separates passed checks from unavailable infrastructure.
