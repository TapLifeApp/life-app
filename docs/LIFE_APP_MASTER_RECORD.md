# Life App — Master Record

**Last consolidated:** 2026-10-16
**Current prototype:** 1.5 — local-save failure handling; 57/57 automated smoke checks pass, with real browser/device validation still open.  
**Status:** Early prototype / pre-MVP; not ready for public release.  
**Brand promise:** “Start where you are. A little better every day.”  
**Alternate closing line:** “Build the discipline. Become who you can be.”

## 1. Purpose and product philosophy
Life App is intended to help people who feel stuck, overwhelmed, lost, or who have repeatedly tried and failed to make progress. It should make improvement feel possible and practical, without making users feel inadequate.

The product cycle is: **Choose → Do → Track → Learn → Improve → Repeat.**

The experience should consistently answer:
- What did I accomplish?
- What does it mean?
- What is my next step?

### Non-negotiable principles
- Teach users at every level: what to do, why it matters, what realistic progress can look like, and what to do next.
- Break goals into manageable steps and adapt the next step to the user's context and results.
- Clearly distinguish evidence-based guidance from estimates and personalized suggestions.
- Avoid one-size-fits-all targets, unrealistic promises, shame, guilt, and addictive streak/points mechanics.
- Support rest, recovery, setbacks, and restarting without blame.
- Keep recommendations conservative, understandable, and explainable.

## 2. Product scope and modules
### Long-term connected platform
1. **Fitness Builder** — guided workouts, exercise demonstrations, timers, session logging, progression, recovery-aware coaching, and progress learning.
2. **Nutrition & Weight** — food diary, calories/protein, meal tracking, weight trends, meal planning, and grocery planning.
3. **Money Manager** — income/expenses, bills, debt, budgets, savings, forecasts, and later Canadian financial-institution connections through a vetted provider. Never collect or store bank passwords directly.

Future areas may include habits/productivity, home/life administration, well-being, learning, relationships, career, purpose, and enjoyment. These are future possibilities, not committed MVP scope.

### MVP direction
Start with **Fitness Builder**. Keep the architecture and product vision compatible with a connected platform, but do not build every module at once. Validate the first module before expanding into nutrition and money management.

## 3. Audience and user experience
- Help users start from their actual current level rather than an assumed ideal.
- Make the next action obvious and achievable.
- Show progress in context, including effort and consistency, without turning missed days into failure.
- Use plain language; the founder is learning software development and prefers clear explanations of technical concepts.
- Keep guidance transparent about uncertainty and limitations.

## 4. Fitness Builder requirements and safety
- Workouts should be guided, trackable, and adaptable to equipment and available time.
- Exercise progression must be conservative and explainable, not driven by arbitrary streaks.
- Check-in feedback must be linked to the exact workout/session it describes.
- If a user reports pain or that an exercise feels unsafe, advise stopping that movement and provide a safer modification or appropriate professional guidance when warranted; never encourage pushing through pain.
- Exercise recommendations require qualified review before public launch.
- Existing fitness progression rules document is a draft, not professionally approved medical or exercise advice.

## 5. Current prototype
**Latest:** Prototype 1.5, `app/index.html` (all Prototype 1.4 features plus resilient local-save failure handling and 1.4-to-1.5 migration; 57/57 automated interaction checks pass, but real-device testing remains open).

Current screens/features include:
- Today dashboard
- Workout session
- Progress history
- “Your Path” learning screen
- Settings
- Workout selection that responds to equipment choice (dumbbells, bodyweight, bands, gym)
- Session duration influences the number of exercise cards
- Beginner selection limits the initial plan to four movements
- Weekly dashboard counts completed sessions since Monday, distinct active days and moving minutes; future-dated records are excluded; progress history shows all-time records
- Manual JSON export/restore of preferences, sessions and Path feedback, with schema checks, field normalization and confirmation before replacement.
- Migration from supported earlier prototype storage keys when available
- Learning screen explains early rule-based recommendations and references WHO public-health guidance

### Known technical limits
- Browser local storage only; no account, secure backend, cloud sync, or cross-device backup. Manual JSON export/restore is available, but it is not a secure or automatic backup system.
- Not production-secure; do not use it to store sensitive personal information.
- Path reviews now append separate feedback records linked to the session and do not rewrite the original workout check-in. A safety-stop flow is implemented, but its content and progression rules still need qualified review. The 1.4 storage key migrates from 1.3 and older supported keys. Future-dated imported records are retained in history but do not affect current/all-time progress or the teaching-path recommendation until their date is reached. Restored workout history is normalized newest-first by timestamp, preventing an out-of-order backup from making an older workout or safety stop appear to be the latest session. Restore also rejects duplicate session IDs and caps imported session/feedback counts so feedback cannot ambiguously link to duplicate workouts or overwhelm the interface. Automated checks are not substitutes for browser/device testing.
- Full interactive browser testing, phone testing, accessibility checks, timer edge cases (including backgrounding/locking the phone), usability testing, and qualified exercise review remain outstanding.

## 6. Development approach agreed with the founder
Use all three as the primary workflow:
1. **ChatGPT Project** as the home for the roadmap, decisions, specs, and files.
2. **Substantial development sessions** for research, design, implementation, and review.
3. **A permanent code repository and coding workflow** for source code, version history, automated checks, and eventual release.

The founder wants the actual app built, not endless planning or throwaway mockups. The assistant should lead the next practical step, explain simply, provide concrete deliverables, and report next steps after each response. Do not claim background work after a response or claim completion without a real deliverable and honest verification.

## 7. Roadmap
### Stage 1 — Stabilize and test prototype
- [x] Add session-specific feedback/check-ins and safety-stop handling.
- [x] Add repeatable headless Chromium interaction tests; 57/57 passed with a test storage double (latest Prototype 1.5).
- [x] Add teaching-path next-action and rationale cards.
- [x] Improve timer elapsed-time handling and clear-data migration behavior.
- [ ] Test all navigation and primary user flows in a normal browser.
- [ ] Verify native persistence after reload/browser restart and reset behavior.
- [ ] Test timers while switching tabs or locking a physical phone.
- [ ] Check phone and desktop layout/usability and accessibility.

### Stage 2 — Validate the problem and MVP
- [ ] Conduct 8–12 user interviews.
- [ ] Observe 5 people using the prototype without coaching them through it.
- [ ] Record usability issues, confusion, and what users actually value.
- [ ] Revise and approve MVP scope based on evidence; do not claim validation before these activities occur.

### Stage 3 — Production foundations
- [ ] Compare practical web/mobile technology options.
- [ ] Choose and document architecture.
- [ ] Establish a founder-controlled code repository and version history.
- [ ] Add automated checks and a release process.
- [ ] Design authentication, secure backend storage, sync, export/delete controls, backups, and privacy protections.

### Stage 4 — Build and prepare a release
- [ ] Implement approved MVP in selected production stack.
- [ ] Test security, accessibility, performance, and supported devices.
- [ ] Obtain qualified review of fitness guidance.
- [ ] Prepare support, privacy disclosures, terms, consent-aware analytics, and web/app-store release materials.

## 8. Business model — exploratory only
Options discussed: useful free core, subscriptions to individual modules, bundles, or a full-platform subscription. No final pricing or monetization decision has been made.

## 9. Existing project deliverables
- `app/index.html` — Prototype 1.5
- `archive/prototype_versions/` — Prototypes 0.1, 0.2, and 0.3
- `docs/Life_App_MVP_Blueprint_Draft_0_1.docx` — draft MVP blueprint
- `docs/Life_App_Teaching_and_Progress_System_Spec_0_1.docx` — teaching/progress system specification
- `docs/Life_App_Fitness_Progression_Rules_0_1.docx` — draft progression rules
- `docs/Life_App_Fitness_Competitor_Scorecard_Template.xlsx` — competitor research template
- `docs/Life_App_User_Validation_Guide_0_1.docx` — interview/usability guide
- `docs/PROTOTYPE_README.md` and `docs/PROTOTYPE_TEST_REPORT.md` — prototype handoff and test notes
- `media/` — existing Life App preview/promotional videos available at consolidation time
- `AGENTS.md` — instructions for coding agents
- `docs/ROADMAP.md` — working roadmap
- `docs/COMPETITOR_AUDIT_0_1.md` — official-source desk research and product hypotheses
- `tests/browser-smoke.py` — repeatable headless Chromium interaction checks
- `docs/DEVELOPMENT_LOG.md` — development history

## 10. Decisions not yet made
- Production technology stack and deployment platform
- Account/authentication and backend architecture
- Whether to launch as web app, mobile app, or both first
- Monetization/pricing
- Final MVP feature boundary after user validation
- Final exercise content and expert review process

## 11. Immediate next actions
Follow the ordered checklist in `START_HERE.md`. The current next actions are:
1. Test Prototype 1.5 in a normal browser and on a physical phone, especially native storage, JSON export/restore and file handling, reset/migration, timer backgrounding, keyboard/screen-reader navigation and the safety-stop flow.
2. Create a founder-controlled remote code repository and import the package contents; the ZIP is a backup, not a remote repository.
3. Conduct 8–12 problem interviews and five uncoached usability sessions; validate whether users can explain their stage, next action and rationale.
4. Arrange qualified review of exercise content and safety messaging before public release.
The latest headless Chromium interaction checks and limits are recorded in `docs/PROTOTYPE_TEST_REPORT.md` (Prototype 1.5: 57/57 checks passed; native storage/device testing remains open).

## 12. Project-folder consolidation note
This master record consolidates the Life App decisions and deliverables available in the working context as of the date above. It does **not** mean every historical ChatGPT conversation has been moved into the ChatGPT Project. Moving prior conversations into a Project must be done through ChatGPT's conversation menu if that option is available. The ZIP package is designed to be attached to the Project as a single consolidated source bundle.
