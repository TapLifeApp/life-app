# Instructions for coding agents

## Mission
Build Life App into a useful, safe, understandable personal-improvement product. The brand promise is: “Start where you are. A little better every day.”

## How to work
- Inspect the existing code before changing it.
- Make the smallest useful change for the current task; avoid rewriting the app without a clear reason.
- Preserve the current standalone prototype's ability to run in a browser unless the task explicitly changes the architecture.
- Explain changes in plain language for a beginner founder.
- After every change, run the available checks and report exactly what passed, failed, or was not tested.
- Do not claim browser/device testing unless it actually happened.
- Keep README and test notes current when behavior or known limitations change.

## Product requirements
- Teach at every level: explain what to do, why it matters, what progress can realistically look like, and what to do next.
- Separate evidence-based guidance from estimates and personalized suggestions.
- Keep recommendations adaptable and conservative; don't present general health guidance as diagnosis or medical advice.
- If a user reports pain or that an exercise feels unsafe, don't encourage pushing through. Stop/modify the movement and offer a safer next step.
- Avoid shame, guilt, unrealistic promises, and streak-based pressure.
- Keep the product centered on: “What did I accomplish? What does it mean? What's my next step?”

## Privacy and security
- The current prototype uses local browser storage and has no production backend or authentication.
- Never store credentials, API keys, or real sensitive user information in code or test fixtures.
- Do not describe local storage as secure cloud storage or imply data sync exists.
- Before launch, design authentication, secure storage, export/delete controls, backups, and privacy disclosures.

## Definition of done
A task is done only when:
1. The requested code or documentation change exists.
2. Relevant checks have been run and results are reported honestly.
3. Known limitations and any manual testing still needed are stated.
