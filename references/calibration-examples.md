# Calibration Anchors

Read before finalizing any score. Source cards are in `examples/`. Scores below
were produced with the rubric in `rubric.md` and are the reference points for
consistency across an eval dataset.

> **Provenance:** All four example cards are synthetic, written for this skill.
> Organizations, brands and domains (Acmera, ORBYX, Moss, `*.example`) are
> fictitious. See [`examples/README.md`](examples/README.md).

| Card | File | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Weighted | Caps | Label |
|------|------|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|------|-------|
| ServiceNow IT Service Desk Agent | `gold-servicenow-itsm.json` | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | **98.8** | none | `great` |
| HR Assistant | `mediocre-hr-assistant.json` | 3 | 3 | 2 | 1 | 2 | 1 | 2 | 1 | 1 | 2 | **46.3** | none | `bad` (borderline) |
| ORBYX (grab-bag aggregator) | `bad-grabbag-aggregator.json` | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 2 | **33.8** | D2≤1 → ≤49; phantom skills | `bad` |
| Moss (persona fragment) | `bad-persona-fragment.json` | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | **17.5** | parse; D2≤1; D3≤1 | `bad` |

---

## 1. Gold — ServiceNow IT Service Desk Agent (98.8, great)

Why it works for an orchestrator:
- **Name/description** say *what* (IT self-service), *where* (Acmera ServiceNow ITSM), *for whom* (signed-in employee), *jobs* (incidents, catalog, password/MFA, outages), *use when*, and *not for* (HR, payroll, facilities, security IR, manager approvals).
- **Skills** are discrete employee jobs covering the lifecycle (create → status/update → close), not API calls.
- **Skill descriptions** follow verb + object + system + inputs + outputs + constraints ("Returns the incident number (INC…), priority, and assignment group. Write action; no approval required").
- **Examples**: 4–5 per skill, real employee phrasing, indirect symptoms ("Outlook won't open since this morning's update"), identifiers (INC0045123, RITM0019876), and named enterprise apps (SAP ME21N, Salesforce).
- **Security**: Entra OAuth2 auth-code with OBO and per-capability scopes; `extendedAgentCard: true`.
- Only gap (D10=3): no JWS `signatures` and no explicit data-classification note.

Sample probe results (9/9):
| Probe | Type | Expected | Decision |
|---|---|---|---|
| "VPN keeps dropping on my laptop" | in-scope | route | route (incident-create) |
| "status of RITM0019876" | in-scope | route | route (ticket-status) |
| "need Visio" | in-scope | route | route (catalog-request) |
| "new hire starts Monday — what onboarding forms do they fill?" | adjacent (HR) | don't route | don't (explicitly excludes HR) |
| "my badge stopped working at the Building 4 door" | adjacent (Facilities) | don't route | don't (excludes badges) |
| "I clicked a suspicious link in an email" | adjacent (SecOps) | don't route | don't (excludes security IR) |
| "what is ITIL?" | out (LLM) | don't route | don't |
| "what's my PTO balance?" | out (HR) | don't route | don't |
| "draft a QBR deck outline" | out (LLM) | don't route | don't |

## 2. Borderline — HR Assistant (46.3, bad)

- D4=1: "helps employees with all their HR needs and provides insights" — unbounded scope + marketing word; router will over-route.
- D3=2: PTO in Workday is non-substitutable, but "Explains HR policies and best practices" and "What is FMLA?" are general-LLM tasks.
- D6=1: one-line descriptions ("Answers benefits questions.") with no system, inputs, outputs.
- D7=2: 1–2 examples per skill, generic.
- D8=1: no exclusions; collides with Payroll, IT onboarding, Benefits vendor agents.
- D9=1: "Book vacation" implies a write with no approval/confirmation semantics.
- D10=2: generic Bearer/JWT scheme with no scopes; HR PII sensitivity not declared.
- To reach Fair/Good: name it "Workday Time Off & Benefits Agent", add use-when/not-for, split time-off into check-balance / request / cancel with 5 examples each, ground benefits in the employee's enrolled plans, drop generic policy advice or ground it in the company handbook with citations, add OAuth scopes.

## 3. Bad — ORBYX grab-bag aggregator (33.8, bad)

- D1=1: 4 of 6 skills say "Over MCP only" → phantom skills on an A2A card; MCP listed as an A2A interface binding.
- D2=1: search-visibility/SEO audit for website owners, a public marketing-tools catalog, a local-business directory (bakeries, plumbers), and "Book a demo with ORBYX" (vendor self-promotion). Not an enterprise LOB function.
- D3=2: the audit and tools index do use proprietary crawls/data (some non-substitutability), but directory/catalog overlap with web search.
- D4=1: opaque brand name; description is mostly transport ("Over A2A… Over MCP, three rails…").
- D5=1: grab-bag of unrelated rails; `get_audit` is protocol plumbing (GetTask), not a skill.
- D6=2: specific about mechanics but dominated by implementation detail (SendMessage, TASK_STATE_COMPLETED, job id).
- D7=1: 1–2 examples per skill; "Get the result of job 7a2e…" is not a user utterance.
- D8=1: "How do answer engines describe this website?" would collide with any web-research agent; no exclusions.
- D10=2: OIDC declared but `securityRequirements` includes an empty (anonymous) requirement.

## 4. Bad — Moss persona fragment (17.5, bad)

- D1=0: fragment; `name`, `description`, `version`, interfaces missing; examples array truncated.
- D2=0: stargazing sky conditions, backyard haze, and campfire-style narration — consumer/hobby, no enterprise function.
- D3=1: live webcam/station reads are real-time data (e), but consumer-oriented; narration is fully substitutable.
- D4=0: no description visible; "Moss" (from `moss.example`) is opaque.
- D6=1: poetic, first-person persona ("I read it by how the stars soften at the horizon against the same hour last week… I say blind").
- D7=1: ≤2 examples per skill, one skill with none.
- D9=1, D10=1: no auth (acceptable for public data, but no provider/version either).

---

## Score-band sanity checks
- A card with **no enterprise system named anywhere** rarely exceeds 70.
- A card whose skills average **< 3 examples** rarely exceeds D7=2.
- A card with **no "not for"/exclusion language** rarely exceeds D8=3.
- If your weighted score differs from the nearest anchor by > 15 points while the evidence looks similar, re-check your scores.
