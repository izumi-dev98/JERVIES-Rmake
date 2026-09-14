# MARK LIII Remaining Roadmap Specification

## Problem

MARK LIII has a first-run wizard, confirmation gate, audit records, plugin discovery, local memory, and a remote dashboard, but these capabilities are not yet connected into a single permissioned and diagnosable operating model. Several workflows remain difficult to test without hardware or external services.

## Target User

The MARK LIII owner who needs to run a personal desktop assistant safely, understand degraded states, control stored memory, and recover from plugin or model failures.

## Goal

Complete the highest-value stability and control features while preserving local-first behavior, existing user changes, and explicit human confirmation for irreversible actions.

## Scope

1. Add centralized action permissions with `safe`, `confirm`, and `blocked` levels for computer control, deletion, shutdown, messaging, and related action families.
2. Connect permission decisions to the existing confirmation gate and audit log without logging arguments or secrets.
3. Replace setup wizard plugin `pending` status with discovered active/rejected counts and provide a reload path.
4. Surface offline/degraded model, audio, and dashboard states while leaving local memory and actions available.
5. Add audit filtering by date, action, event, and status plus an authenticated local clear-log action.
6. Add memory view, edit, delete, export, and forget operations through existing memory APIs/UI.
7. Add mocked model, dashboard API, permission, plugin, audit, and memory tests. Add GUI tests only when a desktop-capable runner is available.
8. Review the worktree, run local checks and CI-compatible checks, and prepare a release/rollback recommendation.

## Non-goals

- Deploying or merging changes automatically.
- Rotating credentials without user-controlled access to the credential provider.
- Replacing Gemini, PyQt, FastAPI, plugin, or memory architectures.
- Building a remote multi-user authorization service.
- Treating a local configuration check as proof of a live model or hardware connection.

## Requirements

- Deny blocked actions before side effects.
- Require the existing human confirmation UI for confirm-level actions.
- Allow safe actions without a confirmation round trip.
- Store permission policy locally without secrets and default unknown actions to confirm or blocked according to their risk.
- Keep audit records metadata-only and make clear-log authenticated and local.
- Reload plugins without duplicating modules or losing the current registry on a failed reload.
- Report model, audio, and dashboard status distinctly when the model is offline.
- Keep memory operations local, explicit, reversible where possible, and free of credential logging.
- All new checks must run without hardware, network, GUI, or API credentials unless explicitly marked integration-only.
- Do not report remote CI or credential rotation as complete unless actually performed.

## Acceptance Criteria

- Representative safe, confirm, and blocked actions have deterministic tests.
- A blocked action does not call its handler; a confirm action enters the existing gate; a safe action executes once and is audited.
- The setup wizard shows actual plugin active/rejected counts after discovery and can request a reload.
- Degraded state preserves local memory/action operations and is visible in health/status output.
- Audit API supports bounded filters and clear-log with authentication; no record contains arguments or secrets.
- Memory controls can list, update, delete, export, and forget a selected memory entry.
- Mocked model and dashboard API tests pass in the local test suite.
- CI-compatible compile and test commands pass.
- Release notes identify uncommitted work, unrun remote CI, credential-history limitations, and rollback steps.

## Assumptions and Risks

- Existing user modifications in `main.py` and other files are intentional and must be preserved.
- The current confirmation gate is the authority for human approval.
- Plugin reload may require rebuilding tool declarations and reconnecting the model session; a failed reload must keep the prior registry.
- GUI tests may be blocked by the current environment's lack of a display server.
- Git remote access and credential rotation cannot be assumed from the local workspace.

## Success Measure

A user can see why an action is allowed or blocked, recover from a plugin/model problem without losing local capabilities, manage audit and memory data locally, and run the verification suite without hardware or secrets.
