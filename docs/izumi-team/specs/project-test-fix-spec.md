# MARK LIII Project Test and Fix Specification

## Problem

The project needs a current verification pass after the release and CI changes, with any reproducible local errors fixed without disturbing the clean release baseline.

## Target User

The MARK LIII maintainer preparing or validating the released desktop assistant.

## Goal

Run the complete local test, compile, and entrypoint smoke checks, repair verified failures if any exist, and record the exact outcome.

## Scope

- Run `python -m unittest discover -s tests -v`.
- Compile all Python source and test modules.
- Parse the main application entry modules.
- Review warnings and distinguish them from failures.
- Fix only reproducible project errors.

## Non-goals

- Changing behavior when all checks pass.
- Running destructive desktop actions, real model calls, or credential-dependent integrations.
- Claiming remote CI success from local results.

## Acceptance Criteria

- The full unittest suite passes.
- All targeted Python modules compile.
- `main.py` and `ui.py` parse successfully.
- Any failure is either fixed and reverified or documented as blocked with its smallest unblocker.
- Non-failing environment warnings are documented separately from errors.

## Assumptions and Risks

- GUI checks may use Qt offscreen mode and may emit environment-specific font warnings.
- Local checks do not prove remote GitHub Actions success or live Gemini/audio hardware behavior.
- The worktree is clean at the start of verification.

## Success Measure

The maintainer has a reproducible local verification result and a concise record of any remaining environmental limitations.
