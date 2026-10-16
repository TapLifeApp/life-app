# Life App Roadmap — Working Copy

Use `../START_HERE.md` for the step-by-step execution plan. This roadmap is the shorter milestone checklist. Work in order and do not mark work complete without evidence.

## Milestone 1 — Project and repository setup
- [ ] Keep the ZIP backup and attach the package to the ChatGPT Project if supported.
- [ ] Move relevant prior Life App conversations into the ChatGPT Project where possible.
- [ ] Create a founder-controlled remote code repository and import the package contents.
- [ ] Record the repository URL in the master record and development log.

## Milestone 2 — Real prototype testing
- [x] Run headless Chromium interaction checks at mobile and desktop viewports (57/57 pass in Prototype 1.5; test harness uses a storage test double because normal navigation is blocked in this execution environment).
- [x] Run JavaScript syntax validation.
- [ ] Test all navigation and main user flows in a normal browser on desktop and phone.
- [ ] Verify native local data persists after reload/browser restart and reset behaves predictably.
- [x] Correct timer logic to use elapsed wall-clock time and add a visibility-change refresh; physical phone lock/background testing remains open.
- [ ] Record actual browser/device versions and any defects from manual tests.

## Milestone 3 — Fix critical fitness behavior
- [x] Tie feedback/check-ins to the exact saved workout/session.
- [x] Add a safety-stop flow that logs pain/unsafe reports without counting them as completed workouts or allowing progression.
- [x] Require a difficulty check-in before saving a completed session.
- [x] Add repeatable browser interaction checks for check-in, progression, safety, timer and reset behavior.
- [ ] Arrange qualified review of exercise guidance before public release.

## Milestone 4 — Validate the problem and MVP
- [x] Produce a desk-research competitor audit with official sources in `docs/COMPETITOR_AUDIT_0_1.md` (not a substitute for user validation).
- [ ] Conduct 8–12 user interviews.
- [ ] Observe 5 people using the prototype without coaching them through it.
- [ ] Record usability problems, confusion, and what users actually value.
- [ ] Revise and approve MVP scope based on evidence; do not claim validation before these activities occur.

## Milestone 5 — Production architecture
- [ ] Compare responsive web/PWA and cross-platform mobile approaches.
- [ ] Choose and document the first production platform and architecture.
- [ ] Design authentication, secure backend storage, sync, export, deletion, backups, and privacy controls.
- [ ] Add automated checks and a documented release process.

## Milestone 6 — Build and prepare the first release
- [ ] Implement the approved Fitness Builder MVP in the selected production stack.
- [ ] Test security, accessibility, performance, and supported devices.
- [ ] Prepare support, privacy disclosures, terms, consent-aware analytics, and release materials.
- [ ] Pilot with a small group, address issues, then decide on wider release.

## Previous build checkpoint — Prototype 1.2 (2026-10-16)
- [x] Harden JSON restore by rejecting duplicate workout/session IDs and bounding imported session/feedback counts; added regression checks that invalid imports do not mutate current data.
- [x] Prototype 1.1 previously introduced the `lifeAppPrototype11` storage key and migration from Prototype 1.0; Prototype 1.2 now migrates from 1.1 and preserves supported older keys.
- [x] Fixed storage-version mismatch: Prototype 1.2 uses `lifeAppPrototype12` and migrates from `lifeAppPrototype11` plus supported legacy `lifeAppPrototype09`, `lifeAppPrototype08`, `lifeAppPrototype07`, and `lifeAppPrototype06` keys as well as supported older keys.
- [x] Extended automated tests to verify previous-version migration preserves saved preferences and session history.
- [x] Added initial accessibility semantics: active navigation announces `aria-current="page"`, pause/resume exposes `aria-pressed`, and session state changes are announced politely without announcing every timer tick.
- [x] Preserved original session check-ins when users submit a separate Path review; the latest review can influence the next-step recommendation without rewriting the workout record.
- [x] Added user-triggered JSON export and validated restore for preferences, workout history, and Path feedback; restore confirms before replacing data and rejects invalid files. Automated tests verify export content, invalid-file safety, and preservation of safety-stop records.
- [x] Fixed restore ordering: imported workout sessions are sorted newest-first by parsed session date, so the most recent session—not arbitrary backup array order—drives the Path recommendation and safety-stop precedence. Added regression tests for out-of-order backup data and the newest imported safety stop.
- [x] Ran JavaScript syntax validation, HTML ID uniqueness check, and headless Chromium interaction suite: 45/45 pass, including mobile (390 × 844) and desktop (1440 × 900) layout/overflow checks, duplicate-ID rejection, and import limits. The Prototype 1.2 package was rechecked in the previous build pass.
- [x] Replaced the dashboard’s “Day streak” metric with “Active days this week” to align with the no-streak-pressure product principle.
- [x] Fixed weekly dashboard aggregation to count distinct active days and exclude future-dated sessions; added regression checks for both behaviors.
- [x] Rechecked competitor positioning: Strava explicitly offers weekly streaks, while Apple Fitness supports customizable goals and pausing rings for rest days; recorded the comparison as a design choice, not proof of user preference.
- [x] Ran the expanded interaction suite: 45/45 pass in the Prototype 1.2 pass. Test harness uses injected HTML and a storage double; mobile tap overlap was carried forward as a usability defect to fix in Prototype 1.3.
- [x] Rechecked official Fitbod, Hevy and Nike Training Club product/help pages and updated the competitor audit with dated source notes.
- [ ] Confirm native browser storage and timer behavior on physical devices.
- [ ] Complete manual keyboard/screen-reader review and full accessibility audit.

The test harness injects the HTML and uses a storage test double because normal file/localhost navigation is blocked in this environment. Passing tests do not prove native storage durability or physical-device behavior. See `docs/PROTOTYPE_TEST_REPORT.md`.

- [ ] Validate native browser storage, export/restore and timer behavior on actual desktop and phone devices; automated injected-HTML tests are not a substitute.


## Previous build checkpoint — Prototype 1.3 (2026-10-16)
- [x] Fixed mobile interaction overlap: workout controls receive scroll margin and extra bottom breathing room above fixed navigation.
- [x] Made toast notifications non-interactive so they cannot intercept taps on workout or navigation controls; positioned mobile toasts above the fixed navigation.
- [x] Changed navigation scroll behavior from smooth to immediate to avoid motion and automation flakiness during screen changes.
- [x] Ensured all-time totals and the teaching path ignore future-dated sessions, including future-dated safety-stop records; added regression tests.
- [x] Bumped visible app/export version and storage key to 1.3 / `lifeAppPrototype13`; migrate from `lifeAppPrototype12` and supported earlier keys without deleting the source data.
- [x] Added regression coverage for 1.2-to-1.3 migration and kept all earlier migration, export/restore, safety and progression checks.
- [x] Fixed future-dated imported records so they do not inflate all-time metrics or override the current teaching path; added regression coverage for both.
- [x] Verified 48/48 headless Chromium checks pass, JavaScript syntax passes, Python test harness compiles, and all HTML IDs are unique. Current source and final package are re-verified in this session.
- [x] Rechecked official Fitbod and Hevy help pages for competitor positioning. The audit remains desk research, not user validation or independent hands-on testing.
- [ ] Test the app in a normal desktop browser and on a physical phone, especially native storage, timer backgrounding/lock, keyboard/screen-reader use, and JSON file handling.
- [ ] Complete qualified review of exercise guidance before public release.

The headless harness injects the HTML and uses a storage test double because normal file/localhost navigation is blocked in this environment. It verifies app logic and interactions, but does not prove native storage durability or physical-device behavior.

## Previous build checkpoint — Prototype 1.4 (2026-10-16)
- [x] Added a keyboard skip link to main content and a clear focus-visible outline for keyboard navigation.
- [x] Respect `prefers-reduced-motion` by minimizing transitions and disabling animated scrolling for users who request reduced motion.
- [x] Added accessible progressbar labels and values for workout exercise progress and the optional weekly target.
- [x] Grouped session difficulty choices under an accessible label and expose the selected response with `aria-pressed`; reset now clears the selected state for the next session.
- [x] Bumped visible app/export version and storage key to 1.4 / `lifeAppPrototype14`; migrate from 1.3 and supported earlier keys without deleting source data.
- [x] Added regression checks for skip-link focus visibility, reduced-motion settings, progress semantics, difficulty-state semantics/reset, and 1.3-to-1.4 migration.
- [x] Verified 56/56 headless Chromium checks pass at mobile (390 × 844) and desktop (1440 × 900) configurations; JavaScript syntax passes, Python test compilation passes, and HTML has 74 unique IDs.
- [ ] Conduct full keyboard-only, screen-reader, contrast and accessibility review on supported browsers/devices; these targeted smoke checks are not a full accessibility audit.
- [ ] Test native storage, JSON file handling, timer backgrounding/lock and touch controls on a physical phone and normal desktop browser.
- [ ] Conduct 8–12 interviews, five uncoached usability sessions, and qualified exercise/safety review before production release.

The automated suite injects HTML into Chromium and uses a storage test double. It verifies app logic and targeted accessibility semantics but does not prove native storage durability, physical-device behavior, or full WCAG conformance.

## Later expansion
Fitness Builder is the first MVP. Nutrition & Weight and Money Manager remain part of the long-term connected-platform vision, but should not be built out until the first module has been validated and the platform foundations are sound.


## Current build checkpoint — Prototype 1.5 (2026-10-16)
- [x] Catch local-storage write failures and show a clear warning rather than a misleading success confirmation for preferences, session saves, path feedback and backup restore. Failed session saves remain in the current page memory so the user can attempt an export, but they are not guaranteed to survive reload.
- [x] Make legacy migration more resilient: keep successfully parsed old data in memory if writing the new key fails, and skip an unreadable legacy key while checking later supported keys.
- [x] Bump visible app/export version and storage key to 1.5 / `lifeAppPrototype15`; migrate from Prototype 1.4 and supported earlier keys without deleting the source data.
- [x] Add regression coverage for 1.4-to-1.5 migration and simulated storage-write failure.
- [x] Verify **57/57** headless Chromium checks pass, JavaScript syntax and Python test compilation pass, and HTML IDs remain unique.
- [ ] Test real browser storage persistence and failure behavior on supported desktop and phone devices; injected storage tests are not a substitute.
- [ ] Complete full accessibility review, user interviews/usability sessions, and qualified exercise-content review.

This is a resilience improvement, not a guarantee that browser storage cannot fail or that unsaved data will survive closing the page. The app still has no production backend or cloud backup.
