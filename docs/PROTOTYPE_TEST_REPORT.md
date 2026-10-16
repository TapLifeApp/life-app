# Prototype test report — Prototype 1.5

**Date:** 2026-10-16  
**Tested artifact:** `app/index.html` — Prototype 1.5  
**Status:** Targeted automated checks pass; native browser/device, full accessibility and production checks remain open.

## Changes covered
- Teaching path with a next action and plain-language rationale; feedback adapts recommendations conservatively.
- Timer computes remaining time from a deadline and catches up after visibility changes.
- Completed sessions require a difficulty check-in linked to the saved session. Pain/unsafe reports stop exercise actions and create a distinct safety-stop record that is not counted as a completed workout or used to advance the path.
- Path review feedback is stored separately from the original session check-in. Future-dated sessions do not inflate current progress or override the current teaching path.
- JSON backup restore checks file size, JSON/schema shape and record fields; confirms before replacing local data; normalizes imported values; preserves safety-stop status when pain is reported; rejects duplicate session IDs; caps imported sessions and feedback; and sorts history newest-first. This is prototype-level validation, not a security review.
- Storage key/export metadata is aligned to version 1.5 (`lifeAppPrototype15`); migration from 1.4 and supported earlier keys preserves source keys. Storage write failures are caught and reported instead of falsely confirming that preferences, feedback, sessions or restores were saved. Legacy migration attempts retain imported data in memory if writing the new key fails.
- Mobile bottom spacing and non-interactive toast behavior reduce overlap risk.
- Accessibility improvements: keyboard skip link, visible focus styling, `prefers-reduced-motion` support, labelled progress indicators, grouped/labelled difficulty controls with `aria-pressed`, and reset of selection state.

## Automated checks run
- Inline JavaScript syntax validation with `node --check`: **PASS**.
- Python test harness compilation with `python -m py_compile tests/browser-smoke.py`: **PASS**.
- HTML ID audit: **74 IDs, 74 unique; no duplicate IDs**.
- Headless Chromium interaction smoke test: **57/57 PASS**, with mobile (390 × 844) and desktop (1440 × 900) viewport configurations.
  - Dashboard rendering, weekly distinct active days, all-time progress and future-date exclusion.
  - Mobile/desktop layout without horizontal overflow; active navigation semantics.
  - Teaching path action/rationale, equipment preferences and workout setup.
  - Timer start, pause/resume state, wall-clock catch-up and session check-in.
  - Safety-stop behavior, exclusion from completed totals, non-overwritable safety feedback and progression blocking.
  - History persistence in a fresh page context; clear-data behavior across current and supported migration keys.
  - Separate path feedback, progression gate and newest-safety-stop precedence.
  - Migration from Prototype 0.5, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3 and 1.4 storage keys.
  - Simulated browser storage write failure shows a warning rather than a false save confirmation.
  - Skip-link target and focus visibility; reduced-motion preference; progressbar semantics; difficulty selection state; basic accessible-name checks for buttons/form controls and a single page H1.
  - JSON export contents and non-mutation; restore validation for valid/invalid files, unknown fields, safety preservation, newest-first ordering, duplicate IDs, excessive histories and cancelled confirmation.
  - No browser JavaScript page errors during the run.

## Test-environment limitation
Normal navigation to `file://` and `localhost` is blocked in this execution environment. The harness injects the HTML into Chromium and uses a small `localStorage` test double. This verifies application logic and targeted interactions, but does **not** prove native browser storage durability, physical-device layout, or real timer behavior while a phone is locked/backgrounded. Targeted accessibility smoke tests are not a full WCAG or screen-reader audit.

## Still not verified
- Native localStorage persistence across reloads and browser restarts on supported browsers.
- Timer behavior on a physical iPhone/Android device while backgrounded or locked.
- Full keyboard-only, screen-reader, contrast and accessibility audit.
- Desktop and physical-phone usability, including observed beginner users.
- Security/privacy review, user interviews and usability sessions.
- Qualified exercise professional review of exercise content, progression rules and safety messaging.
- Production accounts, backend, sync, automated backups, guaranteed deletion, privacy disclosures and release process. Local JSON export/restore is manual and is not a production backup system.

## Next manual test pass
1. Open `app/index.html` in a normal desktop browser and on a phone; record browser and device versions.
2. Test settings, navigation, workout completion, feedback, history and safety-stop flows with test data, especially bottom controls and toast messages on mobile.
3. Reload/restart the browser to confirm native storage; test clear/reset and migration from Prototype 1.4.
4. Background the tab and lock/unlock the phone while the timer is active.
5. Verify JSON export and restore; check duplicate IDs, oversized history, invalid files and cancelled confirmations do not replace existing data.
6. Use keyboard-only navigation and a screen reader to check skip link, active navigation, pause/resume, session status, progress indicators and safety messages.
7. Check reduced-motion behavior, contrast and text zoom. Record reproducible issues before recruiting 8–12 interviewees and five uncoached prototype testers.
