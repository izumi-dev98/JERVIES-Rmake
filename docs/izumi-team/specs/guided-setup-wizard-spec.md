# Guided Setup Wizard Specification

## Problem

MARK LIII's first-run overlay collects only the Gemini API key and operating system. Users cannot see whether audio, model, plugins, or local permissions are ready, and setup progress is not retained when a check fails or the app closes.

## Target User

A new MARK LIII user completing first-run setup on a desktop computer without needing to understand the project's internal settings panels.

## Goal

Turn the existing initialization overlay into a guided, resumable readiness checklist that identifies blockers and routes users to the correct repair action without exposing secrets or requiring a live model connection during the check.

## Scope

- Add a testable setup-state helper that checks API key, model configuration, microphone, speaker, plugins, and permissions.
- Persist only checklist completion and selected repair metadata under an ignored local config file.
- Extend the existing PyQt setup overlay with checklist rows, status updates, and repair actions.
- Preserve the existing API-key and OS setup behavior.
- Reuse existing audio device and plugin discovery APIs.

## Non-goals

- Performing a paid Gemini request during setup.
- Automatically changing operating-system permissions or firewall settings.
- Replacing the existing audio-device picker, plugin manager, or settings drawer.
- Storing API keys, device data beyond existing settings, or permission tokens in setup progress.
- Implementing action permission levels or the audit dashboard in this task.

## Requirements

1. The wizard must report safe readiness states for API key, model, microphone, speaker, plugins, and permissions.
2. Health checks must not include the API key value or user command content.
3. API key and OS setup must remain available from the first-run flow.
4. Audio checks must distinguish system default from a selected device and flag a selected device that is no longer enumerated.
5. Plugin readiness must show active and rejected counts without importing secrets into the wizard state.
6. Permission readiness must be explicit and may be `manual review` when the platform cannot be checked safely.
7. Progress must survive restart in a local ignored JSON file.
8. Each failed or incomplete row must expose a repair action or a clear manual instruction.
9. The wizard must be usable with keyboard focus and visible status text.
10. Existing tests must remain hardware-free; hardware checks must be injectable or safely mocked.

## Acceptance Criteria

- A missing API key produces a `blocked` API and model state without exposing a value.
- A configured API key produces a `ready` API state and a `ready` model-configuration state.
- A saved audio device missing from the enumerated list produces a repairable `attention` state.
- Plugin and permission states are represented even when no plugins are installed or permissions cannot be inspected.
- Closing and reopening the wizard restores persisted checklist progress without persisting secrets.
- The overlay provides keyboard-focusable repair and continue controls.
- Existing baseline tests and new setup-state tests pass without microphone, speaker, GUI, network, or Gemini credentials.

## Assumptions and Risks

- The existing configuration file remains the source of truth for API key, OS, and audio settings.
- Audio enumeration can be slow or unavailable, so the wizard must accept an injected checker and display an unavailable state rather than blocking startup indefinitely.
- Plugin discovery has already occurred by the time the normal `JarvisUI` is wired by `main.py`; the first-run overlay may initially show plugin status as pending.
- Platform permission APIs differ; manual review is safer than claiming access.

## Success Measure

A new user can identify the next setup action from one screen, resume after restarting MARK LIII, and reach a clear ready or manual-review state without entering the main conversation loop blindly.
