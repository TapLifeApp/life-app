# Life App — Build to Launch

**Product promise:** Start where you are. A little better every day.

Life App is an early-stage personal improvement platform. The long-term vision includes Fitness Builder, Nutrition & Weight, and Money Manager. The first MVP is deliberately narrower: validate and improve the Fitness Builder before expanding.

## Start here

Read `docs/LIFE_APP_MASTER_RECORD.md` for the consolidated product vision, decisions, prior deliverables, open questions, and roadmap. `docs/HISTORY_INDEX.md` is the index to the consolidated history.

## Current status

- **Stage:** Early prototype / pre-MVP
- **Current app:** `app/index.html` (a standalone browser prototype)
- **Data:** Stored locally in the browser; no account, cloud sync, or production backend
- **Verification:** Prototype 1.5 passed JavaScript syntax validation, Python test compilation, unique HTML ID checks, and 57/57 headless Chromium interaction checks using a storage test double. New checks cover a keyboard skip link, visible keyboard focus, reduced-motion preference, accessible progress indicators, selected difficulty state, 1.4-to-1.5 migration, and a simulated local-storage write failure. Native browser storage, physical-device behavior, full accessibility review, qualified safety review, and user validation remain open.
- **Not ready for public launch:** This is not a production-secure application and should not be used to store sensitive personal information.

## Run the prototype

1. Download this repository folder or open `app/index.html` in a modern web browser.
2. For reliable testing, use a computer browser where you can inspect and reset browser data. Some phones may open the file in a preview instead of a full browser.
3. Treat any information entered as test data; browser storage is local to that browser/device.

## Product principles

- Teach the user why a step matters, not just what to do.
- Make progress realistic, understandable, and adaptable.
- Support restarts and recovery without shame or guilt.
- Clearly distinguish evidence-based guidance from estimates and personalized suggestions.
- Avoid unrealistic promises, one-size-fits-all targets, shame, and streak-based pressure.
- Ask: What did I accomplish? What does it mean? What's my next step?

## Immediate development priorities

1. Run manual desktop-browser and physical-phone tests, especially native storage, reset/migration, and timer behavior when backgrounded or locked.
2. Validate the teaching-path hypothesis in 8–12 problem interviews and 5 uncoached prototype sessions.
3. Arrange qualified review of exercise content and safety messaging.
4. Establish a founder-controlled remote code repository and record its URL.
5. Choose production architecture only after the MVP scope and key risks are clearer.

## Repository working rules

- Make small changes that can be tested and reviewed.
- Keep the app runnable after each change.
- Do not claim a feature is finished without a test or other concrete verification.
- Record known issues and test results in `docs/`.
- Never add secrets, passwords, API keys, or real sensitive user data to this repository.

## Folder guide

- `app/` — current prototype app
- `docs/` — product specs, test report, and research templates
- `tests/` — browser interaction smoke test and repeatable checks
- `AGENTS.md` — instructions for coding agents working on this project


## Start here
Read [`START_HERE.md`](START_HERE.md) first for the ordered action plan, the three-part working system, and the current next task.
