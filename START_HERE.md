# Life App — Start Here

This file is the practical instruction sheet for moving Life App forward. Follow the numbered steps in order. Do not skip ahead to production features before testing the current prototype and confirming the MVP.

## The three-part working system

1. **ChatGPT Project — “Life App — Build to Launch”**: home for conversations, decisions, specifications, and deliverables. Move relevant earlier Life App conversations into this Project using each conversation's menu when available. The assistant cannot automatically move every old conversation.
2. **Development sessions**: each session should have one concrete objective, produce or verify a deliverable, update the development log, and end with the next action. Do not claim background work continues after a session.
3. **Code repository and coding workflow**: the permanent home for source code and its history. The ZIP is a starter package, not yet a remote Git repository. The founder must create/control the remote repository and keep access.

## Ordered action plan

### Step 1 — Establish the working home
- [ ] Keep this ZIP saved as a backup.
- [ ] Attach/upload the ZIP and key reference documents to the ChatGPT Project if the interface permits.
- [ ] Move relevant earlier Life App conversations into the Project where possible.
- [ ] Use `docs/LIFE_APP_MASTER_RECORD.md` as the central decision record.
- **Done when:** the Project contains the package and the key prior conversations have been moved or are listed as not yet moved.

### Step 2 — Set up the permanent code repository
- [ ] Create a repository under a founder-controlled account (GitHub is a practical default).
- [ ] Upload/import the contents of this ZIP; do not upload the ZIP as the only repository file.
- [ ] Confirm `README.md`, `AGENTS.md`, `START_HERE.md`, `app/index.html`, and `docs/` are visible in the repository.
- [ ] Keep the repository private while the app is early-stage and contains no approved public release.
- [ ] Record the repository URL in `docs/DEVELOPMENT_LOG.md` and the master record.
- **Done when:** the source files are browsable online and there is a known way to make and review changes.

### Step 3 — Run the first real tests
- [ ] Open `app/index.html` in a desktop browser and on a phone.
- [ ] Check every screen and navigation control.
- [ ] Complete a workout, reload the app, and confirm what data persists.
- [ ] Test short/long session settings and each equipment option.
- [ ] Test timer behavior while changing tabs, locking the phone, and returning.
- [ ] Record each issue with steps to reproduce, expected behavior, actual behavior, and severity.
- **Done when:** there is a written test record based on actual browser/device testing. Syntax checks alone do not count.

### Step 4 — Fix the two highest-priority fitness logic gaps
- [ ] Link each effort/recovery check-in to the exact completed workout.
- [ ] Add a clear stop/modify response when a user reports pain or an unsafe movement.
- [ ] Ensure progression recommendations explain why they were made and never encourage pushing through pain.
- [ ] Add repeatable tests for these behaviors.
- **Done when:** test cases pass for ordinary feedback, missed sessions, and pain/unsafe reports. Qualified exercise review is still required before public launch.

### Step 5 — Validate the need and narrow the MVP
- [ ] Conduct 8–12 interviews with likely users.
- [ ] Observe 5 people trying the prototype without coaching them.
- [ ] Capture confusion, unmet needs, and the actions users actually take.
- [ ] Revise and approve the MVP requirements based on findings.
- **Done when:** findings and resulting decisions are documented; do not claim validation before research occurs.

### Step 6 — Select the production approach
- [ ] Compare a responsive web app/PWA with cross-platform mobile options against cost, learning curve, offline behavior, privacy, and future growth.
- [ ] Choose the initial platform and document why.
- [ ] Design account/authentication, secure storage, sync, backup, export/delete, privacy, and testing approach.
- [ ] Decide what user data is truly necessary to collect.
- **Done when:** the production architecture and MVP scope are approved before a large rewrite begins.

### Step 7 — Build the production MVP
- [ ] Implement only the approved Fitness Builder MVP.
- [ ] Keep Nutrition & Weight and Money Manager in the long-term vision, not the first release scope.
- [ ] Add automated tests, accessibility checks, privacy/security review, and a documented release process.
- [ ] Get qualified review of exercise guidance.
- **Done when:** the release candidate passes its agreed test checklist and has support/privacy/terms materials.

### Step 8 — Release, learn, and expand carefully
- [ ] Release to a small test group first.
- [ ] Collect consent-aware feedback and fix serious issues.
- [ ] Decide whether the Fitness Builder is ready for wider release based on evidence.
- [ ] Only then plan the next module and test pricing/business model assumptions.

## Work-session rule

At the start of each session, read this file, `docs/LIFE_APP_MASTER_RECORD.md`, and `docs/DEVELOPMENT_LOG.md`. Work on the earliest unchecked task that can be completed with available access. At the end, record: what changed, files changed, tests actually run, known limitations, and the single next task. Never label an item complete without evidence.

## Current next task

**Run the manual desktop-browser and physical-phone test pass for Prototype 1.5.** Focus on native storage across reload/restart, JSON export and file handling, clear/reset and migration from 1.4, the timer while backgrounded/locked, keyboard/screen-reader navigation, reduced-motion behavior, and the pain/safety-stop flow. The automated headless Chromium checks passed 57/57, but the execution environment required injected HTML and a storage test double, so they do not replace this manual test. Then create a founder-controlled remote repository and record its URL. Use `docs/COMPETITOR_AUDIT_0_1.md` to inform 8–12 problem interviews; do not treat desk research as user validation.
