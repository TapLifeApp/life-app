# Life App Fitness Builder — Competitor Audit 0.1

**Research date:** 2026-10-16 (official product/help pages rechecked during Prototype 1.3 work)  
**Purpose:** inform MVP differentiation and testable product hypotheses. This is a desk review of official product/help pages and store descriptions, not hands-on testing, a verified pricing survey, or evidence of user demand. Competitor feature descriptions are vendor claims.

## Summary
Established products already do workout generation, video/trainer-led instruction, detailed exercise logging, progress charts, routines, and personalization. Life App should not try to win by having the largest exercise library or the most sophisticated training algorithm in its first release. Its initial hypothesis should be a **beginner-friendly teaching path** that consistently explains: current stage, one next action, why that action fits, how to adjust it, and what the app knows versus estimates.

## Comparison

| Product | Publicly described strengths | Implication for Life App | Potential gap to test (not assumed fact) |
|---|---|---|---|
| **Fitbod** | Personalizes exercise selection and sets/reps/weights around experience, goals, equipment and workout history; supports substitutions and exercise demonstrations. Its current help page says workout selection responds to goal, experience, equipment, workout length, logged performance, user feedback and muscle recovery; the same page describes adapting resistance over time. [How Fitbod Creates Your Workout](https://help.fitbod.me/hc/en-us/articles/360004429814-How-Fitbod-Creates-Your-Workout) · [How Fitbod Adapts](https://help.fitbod.me/hc/en-us/articles/43492523917207-How-does-Fitbod-adapt-as-I-get-stronger) | Users may expect workouts to adapt to their equipment, experience and feedback. Start with transparent, conservative rules rather than claiming algorithmic intelligence. | Test whether beginners understand *why* a recommendation changed and whether they prefer a simple, explainable path. |
| **Hevy** | Workout/routine logging, rest timers, RPE, exercise history, charts, personal records, custom exercises and social features; some advanced features and Hevy Trainer are paid-tier features according to its help page. [Feature guide](https://help.hevyapp.com/hc/en-us/articles/33106320824727-Everything-You-Need-to-Know-About-the-Hevy-App-2026-Features-Guide) · [Features](https://www.hevyapp.com/features/) | Strong tracking is table stakes for strength users. Keep core logging fast and avoid competing on social features in the MVP. | Test whether a new user can understand progress from Life App's plain-language explanations without needing advanced charts. |
| **Nike Training Club** | Offers trainer-led videos, progress tracking and multi-week training programmes; its Canadian page describes flexible at-home and gym options. [Nike Training Club Canada](https://www.nike.com/ca/ntc-app) | High-quality instruction and curated programs are credible user expectations. Life App can begin with a smaller, more focused catalogue. | Test whether a small adaptive plan feels more actionable than a broad content library to the target audience. |
| **Strong** | Workout/routine logging, exercise instructions and animated videos, rest timers, records, charts and cloud sync described in its store listing. [Google Play listing](https://play.google.com/store/apps/details?hl=en-US&id=io.strongapp.strong) | Logging, timers, exercise guidance and visible trends are established category features. Reliability and data clarity matter. | Test whether the missing piece for Life App's target users is not more tracking, but knowing what to do next and why. |

## Prototype 1.1 recheck (2026-10-16)

- Fitbod's current official help pages describe recommendations that use preferences, logged performance, equipment, exercise feedback and estimated muscle recovery. Fitbod also says it eases recommendations after breaks. This reinforces that Life App should not claim personalization as a unique feature; its testable angle remains the plain-language explanation and beginner-controlled next step. [Workout generation](https://help.fitbod.me/hc/en-us/articles/360004429814-How-Fitbod-Creates-Your-Workout) · [Adaptation](https://help.fitbod.me/hc/en-us/articles/43492523917207-How-does-Fitbod-adapt-as-I-get-stronger)
- Hevy's official feature list continues to emphasize workout logging, progress tracking and social features, reinforcing that reliable tracking is an established category expectation. [Features](https://www.hevyapp.com/features/)
- Nike Training Club Canada's official page currently describes 200+ free workouts, trainer-led instruction and multi-week programs. That is a broad content-library alternative; Life App's early test should measure whether users understand and trust a smaller teaching path, not claim the app has more content. [Nike Training Club Canada](https://www.nike.com/ca/ntc-app)

These are official-source desk checks, not hands-on competitor use or user validation. Product pages and features can change.

## Prototype 1.2 design decision: progress without streak pressure

- Strava’s official help page describes a weekly Streaks feature, qualifying uploads, and what happens when a week is missed. This is a documented competitor engagement mechanic, not evidence that all users like or benefit from it. https://support.strava.com/en-us/articles/15401580-streaks-on-strava
- Apple’s Canadian Fitness App Store description says users can customize activity rings by day of week or pause them for rest days. This shows at least one mainstream fitness ecosystem supports flexibility around rest. https://apps.apple.com/ca/app/apple-fitness/id1208224953
- Prototype 1.2 removes the “Day streak” dashboard counter and shows “Active days this week” instead. The intent is to show activity without framing missed days as a broken streak. This is a values-led design choice and still needs usability testing; it is not a validated competitive advantage.

## Feature-level takeaways

- **Personalization:** Fitbod already describes experience/equipment/history-driven adaptation. Life App's differentiator cannot simply be “personalized workouts.”
- **Tracking:** Hevy and Strong provide extensive logging and progress features. Life App should track the minimum useful facts for its teaching loop: session, completed movements, duration, self-reported difficulty, safety stop and next recommendation.
- **Instruction:** Nike Training Club and Fitbod emphasize trainer-led/video or exercise demonstrations. The current prototype has text cues and emoji, not professionally reviewed demonstration media. This is a known limitation for later MVP content work.
- **Teaching:** The opportunity to test is whether explicit stage + next action + rationale + confidence label + easy alternative improves comprehension and return use. The audit does not prove this is a market gap.
- **Safety and trust:** Do not imitate engagement mechanics that reward activity regardless of recovery. Safety reports must take precedence over progression; population guidelines must not be shown as a mandatory first-week quota.
- **Commercial boundary:** Hevy's public guide describes free/pro limits. Pricing and feature boundaries change frequently; this audit does not recommend a Life App price.

## Prototype 1.3 competitor recheck (2026-10-16)

- Fitbod's current official help pages describe personalized exercise selection based on goal, experience, available equipment, workout length, logged performance, exercise feedback, and muscle recovery. Fitbod also offers exercise demonstrations and progressive recommendations. This sets a high bar for personalization; Life App should not claim superior workout intelligence from a small rule-based prototype.
- Hevy's 2026 official feature guide describes set/rep/weight logging, routines, rest timers, RPE, workout history/charts, body measurements, exercise demonstrations, and paid trainer/progression features. This establishes detailed tracking as a mature competitor strength.
- Product implication: the most defensible early Life App test is not a larger library or more metrics. Test whether beginners can explain their current stage, next manageable action, why it fits, and how to scale back safely. User interviews and observed usability sessions are still required before calling this a differentiator.

## Life App positioning hypothesis

> **Life App is the fitness guide for people who want to start or restart, understand why their next step makes sense, and build a routine without guilt.**

This is a product hypothesis, not validated positioning. It should be tested in 8–12 problem interviews and five uncoached prototype sessions before substantial production investment.

## Recommended experiments

1. Ask interviewees to describe their last attempt to start/restart fitness before showing the prototype.
2. Give a tester the prototype and ask them to say where they are on the path, what to do next and why.
3. Compare comprehension of the path card against a workout-only screen; do not infer success from compliments alone.
4. Observe whether a tester can find the safety-stop and data-clear controls without coaching.
5. Track completion without help, explanation recall, perceived control/trust and voluntary return within seven days.

## Research sources

- Fitbod, *Getting Started with Fitbod: A New User's Guide* (updated 2026): https://help.fitbod.me/hc/en-us/articles/30721771750039-Getting-Started-with-Fitbod-A-New-User-s-Guide
- Fitbod Help Center, *How Fitbod Creates Your Workout* (updated September 14, 2026; rechecked for Prototype 1.3): https://help.fitbod.me/hc/en-us/articles/360004429814-How-Fitbod-Creates-Your-Workout
- Fitbod Help Center, *How does Fitbod choose which exercises to give me?* (updated September 2026; rechecked for Prototype 1.3): https://help.fitbod.me/hc/en-us/articles/43489509474455-How-does-Fitbod-choose-which-exercises-to-give-me
- Hevy Help Centre, *Everything You Need to Know About the Hevy App (2026 Features Guide; rechecked for Prototype 1.3): https://help.hevyapp.com/hc/en-us/articles/33106320824727-Everything-You-Need-to-Know-About-the-Hevy-App-2026-Features-Guide
- Hevy Help Centre, *RPE vs RIR: What They Mean and How to Use Them in Hevy* (checked 2026-10-16): https://help.hevyapp.com/hc/en-us/articles/34490600233111-RPE-vs-RIR-What-They-Mean-and-How-to-Use-Them-in-Hevy
- Nike Training Club Canada, *NTC App* (rechecked for Prototype 1.3): https://www.nike.com/ca/ntc-app
- Fitbod, *How Fitbod Generates Your Personalized Workouts* (June 9, 2026): https://fitbod.me/blog/fitbod-algorithm/
- Hevy, *Features*: https://www.hevyapp.com/features/
- Nike Training Club, Google Play listing: https://play.google.com/store/apps/details?id=com.nike.ntc
- Strong, Google Play listing: https://play.google.com/store/apps/details?hl=en-US&id=io.strongapp.strong

- Strava Help Center, *Streaks on Strava* (checked 2026-10-16): https://support.strava.com/en-us/articles/15401580-streaks-on-strava
- Apple Fitness, Canadian App Store listing (checked 2026-10-16): https://apps.apple.com/ca/app/apple-fitness/id1208224953
