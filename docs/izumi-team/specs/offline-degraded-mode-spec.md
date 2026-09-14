# MARK LIII Offline and Degraded Mode Specification

## Problem

Local memory, permissions, audit logs, and settings can operate without Gemini, but the application does not expose a stable offline/degraded state when the Live model connection fails. Users see reconnecting behavior without a clear distinction between model offline and the rest of the assistant remaining available.

## Target User

A MARK LIII desktop user working through a temporary network, API, or model outage.

## Goal

Make offline capability explicit while preserving local features and making model, audio, and dashboard status readable in the desktop and remote interfaces.

## Scope

- Add a small normalized model connection state: `starting`, `connected`, `offline`, `reconnecting`, and `stopped`.
- Publish state changes to the desktop UI, dashboard status broadcast, and health endpoint.
- Keep local memory, permissions, audit, settings, and safe local actions available regardless of model state.
- Add hardware-free tests for state normalization and health output.

## Non-goals

- Replacing Gemini Live with a full offline conversational model.
- Automatically executing natural-language commands without a model.
- Changing audio device behavior or claiming physical audio readiness.
- Sending local data to a network service while offline.

## Requirements

1. Model state must never expose API keys or exception payloads containing secrets.
2. Connection failure must publish `offline` before backoff/retry begins.
3. A retry attempt must publish `reconnecting`, and a successful session must publish `connected`.
4. Dashboard health must include the current model connection state.
5. Desktop status must distinguish offline/reconnecting from connected.
6. Local memory, permission, audit, and settings operations must not require an active model session.
7. Tests must run without network, hardware, GUI, or Gemini credentials.

## Acceptance Criteria

- A failed model connection transitions health to `offline` and publishes an offline status.
- Retry transitions health to `reconnecting`; successful connection transitions to `connected`.
- Existing local test suite remains green.
- No secret or raw exception text is placed in dashboard health/status payloads.

## Assumptions and Risks

- The existing reconnect loop remains the single owner of model lifecycle state.
- Dashboard clients may reconnect and fetch health after missing a broadcast.
- Offline local operations are those already implemented outside `_execute_tool` model dispatch; natural-language command interpretation remains unavailable.

## Success Measure

Users can tell whether MARK LIII is offline, reconnecting, or connected, while local safety and memory controls remain usable during a model outage.
