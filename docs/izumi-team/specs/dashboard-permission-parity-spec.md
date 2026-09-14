# Dashboard Permission Parity Specification

## Problem

The native permission editor explains action consequences and can reset local overrides, but the authenticated remote dashboard only exposes level selectors.

## Target User

A MARK LIII user managing permissions from a phone or browser through the remote dashboard.

## Goal

Make remote permission management consistent with the native editor while preserving authentication and local configuration safety.

## Scope

- Return permission explanations from the authenticated permissions API.
- Add an authenticated reset endpoint that preserves unrelated configuration.
- Display explanations and a reset control in the dashboard.
- Add route and policy tests.

## Non-goals

- Changing permission defaults or enforcement.
- Adding new action families.
- Exposing API keys, command arguments, or raw configuration.

## Requirements

1. Permission explanations must be static and secret-free.
2. Reset must use the existing policy reset function and preserve unrelated settings.
3. Reset must require an authenticated dashboard session and explicit browser confirmation.
4. Invalid permission levels remain rejected.
5. Existing dashboard health, audit, and command flows remain unchanged.

## Acceptance Criteria

- Authenticated `/api/permissions` returns levels and explanations.
- Authenticated `/api/permissions/reset` resets only permission overrides.
- Unauthenticated permission and reset requests are rejected.
- Dashboard renders explanations and a reset button.
- Full local tests and compilation pass.

## Assumptions and Risks

- The dashboard already uses bearer-token authentication.
- Browser confirmation is sufficient for resetting local policy because reset is reversible through the editor.

## Success Measure

Native and remote users see the same permission consequences and can restore defaults safely.
