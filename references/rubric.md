# Agent Card Quality Rubric (enterprise orchestration)

Each dimension is scored **0–4**. Use the anchor that best matches; when torn
between two, choose the lower one unless the checklist is ≥80% satisfied.
Checklists are evidence aids, not additive points.

Anchor meaning across all dimensions:
- **4 Exemplary** — an orchestrator would route correctly with high confidence; nothing material to fix.
- **3 Solid** — minor gaps; routing mostly correct.
- **2 Partial** — usable but ambiguity or missing info would cause misroutes.
- **1 Weak** — present but largely unhelpful or misleading.
- **0 Absent / harmful** — missing, invalid, or actively misleading.

---

## D1 — Spec Conformance & Structural Integrity (weight 5)

Checklist (A2A v1.0; accept 0.3 equivalents):
- [ ] Parses as JSON; is a complete object (not a fragment).
- [ ] Required top-level: `name`, `description`, `supportedInterfaces` (each with `url`, `protocolBinding` ∈ {JSONRPC, GRPC, HTTP+JSON or declared custom}, `protocolVersion`), `version`, `capabilities`, `defaultInputModes`, `defaultOutputModes`, `skills` (non-empty).
  - 0.3 equivalents: `url` + `preferredTransport` + `protocolVersion` (+ `additionalInterfaces`).
- [ ] Every skill has `id` (unique), `name`, `description`, `tags` (non-empty).
- [ ] Interface URLs are absolute HTTPS (no localhost/http in a production card).
- [ ] Input/output modes are valid media types (`text/plain`, `application/json`, `application/pdf`, …), not free words like "text".
- [ ] `version` is meaningful (semver preferred).
- [ ] Every advertised skill is actually invocable over the declared A2A interface(s). Skills that say "MCP only", "via REST API", "coming soon" are **phantom skills**.
- [ ] No unknown/misspelled fields that suggest a hand-rolled schema (e.g. `capabilites`, `skill`).

| Score | Anchor |
|---|---|
| 4 | All required fields valid; HTTPS; valid MIME types; unique skill ids; no phantom skills. |
| 3 | One minor issue (missing optional `provider`, non-semver version, a loose MIME type). |
| 2 | Several minor issues, or one phantom skill, or legacy-format inconsistencies. |
| 1 | Missing a required skill field across skills, multiple phantom skills, or http/localhost URL. |
| 0 | Not parseable, fragment, or missing required top-level fields. |

---

## D2 — Enterprise Relevance & Business Value (weight 15)

Does the agent serve an identifiable enterprise function (see
`enterprise-domains.md`) for employees, partners, or customers of an
enterprise, against enterprise systems or governed data?

Checklist:
- [ ] Maps clearly to a business function (ITSM, HR, Sales, Service, Procurement, Finance, Supply Chain, Legal, GRC, Security, Knowledge, industry-specific like Pharma/Healthcare/FSI).
- [ ] Names or clearly implies a system of record / LOB app (ServiceNow, Workday, SAP, Dynamics 365, Salesforce, Coupa, Veeva, Epic, internal ERP…).
- [ ] Target persona is an enterprise role (employee, agent, buyer, AP clerk, field rep, clinician, CRA, recruiter…).
- [ ] Value is measurable (deflects tickets, shortens cycle time, enforces policy, reduces manual entry).
- [ ] Not consumer/hobby (weather at a lake, recipes, personal narration), not vendor self-promotion (book a call with us, buy our service), not SEO/marketing-tool-for-SMBs unless clearly positioned for an enterprise marketing function.

| Score | Anchor |
|---|---|
| 4 | Explicit enterprise function + named system(s) + persona + clear business outcome. |
| 3 | Clear function and persona; system implied rather than named. |
| 2 | Plausibly useful to some enterprise teams but generic or prosumer-oriented; mixed with non-enterprise skills. |
| 1 | Primarily consumer, hobbyist, or vendor-marketing; enterprise use is incidental. |
| 0 | No enterprise relevance or a novelty/persona agent. |

---

## D3 — Delegation Necessity / Non-Substitutability (weight 15)

Would a capable general LLM (with web search) be unable to fulfil the request
without this agent? Agents earn delegation by having at least one of:
**(a)** access to a system of record / proprietary or tenant data,
**(b)** ability to take governed actions (create, update, approve, submit),
**(c)** enforcement of enterprise policy/entitlements,
**(d)** specialized validated computation or certified content (e.g. regulatory labeling, safety databases),
**(e)** real-time operational data unavailable to the LLM.

Checklist:
- [ ] Each skill states which of (a)–(e) it relies on, or it is obvious from the text.
- [ ] Examples could not be answered by the LLM alone (e.g. "what's the status of INC0045123" vs "what is ITIL").
- [ ] No skills that are pure text generation (summarize, write a poem, narrate, explain a concept, translate) unless tied to governed data.

| Score | Anchor |
|---|---|
| 4 | Every skill depends on enterprise data/actions; probe test shows the LLM alone fails on in-scope queries. |
| 3 | Most skills non-substitutable; one skill is generic. |
| 2 | About half the skills are generic LLM capabilities or public-web lookups. |
| 1 | Mostly things the LLM can already do (general Q&A, writing, public info). |
| 0 | Entirely substitutable (echo, chit-chat, narration, generic advice). |

---

## D4 — Agent Description Clarity & Scope (weight 10)

The top-level `description` is the orchestrator's first filter. Ideal shape
(2–4 sentences, ~40–120 words):
**"<Role/what> for <persona> in <system/domain>. It can <3–5 core jobs>. Use it
when <trigger conditions>. It does not <key exclusions>."**

Checklist:
- [ ] States the business purpose in the first sentence.
- [ ] Names the domain/system and target users.
- [ ] Summarizes the main jobs consistent with the skills list.
- [ ] Gives a "use when" and ideally a "not for" clause.
- [ ] Plain business language; no marketing superlatives, poetry, first-person persona voice, or protocol/transport details.
- [ ] `name` is descriptive (e.g. "ServiceNow IT Service Desk Agent"), not a bare brand/acronym ("ORBYX", "Moss").

| Score | Anchor |
|---|---|
| 4 | Meets all checklist items; a router could decide on most queries from the description alone. |
| 3 | Clear purpose and domain; missing "use when"/"not for" or slightly long. |
| 2 | Purpose discernible but buried in jargon, transport detail, or lists of unrelated features. |
| 1 | Vague, marketing, or poetic; name is an opaque brand. |
| 0 | Missing, placeholder ("An agent"), or misleading. |

---

## D5 — Skill Decomposition & Cohesion (weight 10)

Checklist:
- [ ] Each skill = one user-recognizable job ("Create a purchase requisition"), not a whole product area ("Procurement") nor a low-level API call ("get_record_by_sys_id").
- [ ] Skills do not overlap; an utterance maps to one skill.
- [ ] All skills serve the agent's stated purpose (cohesion). Unrelated grab-bag skills (audit + directory + booking + catalog) indicate an aggregator, not an agent.
- [ ] Count is reasonable (typically 2–12). One skill is fine if the agent is truly single-purpose.
- [ ] Lifecycle coverage where relevant (create → check status → update → cancel/escalate).
- [ ] Polling/plumbing is not modelled as a skill (e.g. "get result of run id" is protocol `GetTask`, not a user skill).

| Score | Anchor |
|---|---|
| 4 | Discrete, non-overlapping, cohesive, right-sized; covers the lifecycle users need. |
| 3 | Minor overlap or one skill at the wrong granularity. |
| 2 | Several skills mis-sized, overlapping, or one/two off-purpose skills. |
| 1 | Grab-bag of unrelated capabilities, or one mega-skill covering everything. |
| 0 | No meaningful skills. |

---

## D6 — Skill Description Precision (weight 10)

Ideal skill description template:
**"<Verb> <business object> in <system> [for <persona/scope>]. Requires <key inputs>. Returns <output>. <Constraints: approvals, limits, regions, read-only>."**

Checklist (evaluate per skill, then average):
- [ ] Action verb + concrete business object.
- [ ] System/data source named.
- [ ] Required inputs listed (IDs, dates, cost center, employee id…).
- [ ] Output described (record number, status, PDF, table).
- [ ] Constraints/limits stated (approval thresholds, only own records, region, latency).
- [ ] Plain, literal language — no metaphor, persona voice ("I read it by how the stars soften…"), or marketing.
- [ ] No transport/implementation noise ("over MCP", "SendMessage returns a task…").
- [ ] `tags` are domain-meaningful (`itsm`, `incident`, `servicenow`) not generic (`ai`, `tool`, `helper`).

| Score | Anchor |
|---|---|
| 4 | ≥5 checklist items on nearly every skill; literal and specific. |
| 3 | Most skills have verb+object+system+output; inputs/constraints sometimes missing. |
| 2 | Descriptions are short or generic ("Handles HR questions"); outputs unclear. |
| 1 | Poetic, marketing, implementation-centric, or one-liners repeating the name. |
| 0 | Missing or copy of skill name. |

---

## D7 — Example Utterance Quality & Coverage (weight 15)

`examples` are the strongest semantic routing signal. They should look like
what a real employee types into a corporate chat.

Checklist:
- [ ] ≥3 examples per skill (≥5 is exemplary); none missing.
- [ ] Realistic enterprise phrasing in user voice, with concrete entities (ticket/PO/case numbers, cost centers, product names, dates, employee roles).
- [ ] Diversity: varied verbs, lengths, formality, and intents within the skill (create vs check vs update), including at least one indirect phrasing ("my laptop won't connect to VPN" vs "create an incident").
- [ ] Examples are unambiguously in-scope for *this* skill, not interchangeable across skills.
- [ ] No examples answerable by a general LLM ("What is SEO?").
- [ ] Multilingual examples only if the agent claims multilingual support.
- [ ] No real PII or secrets in examples.

| Score | Anchor |
|---|---|
| 4 | Every skill ≥3 (most ≥5) realistic, diverse, entity-bearing examples. |
| 3 | Every skill has ≥2–3 good examples; limited diversity. |
| 2 | Some skills have 0–1 examples, or examples are generic/templated. |
| 1 | Few examples overall, mostly generic, consumer, or answerable by an LLM. |
| 0 | No examples anywhere. |

---

## D8 — Routing Discriminability & Boundaries (weight 10)

In an enterprise, the orchestrator sees *dozens* of agents (IT, HR, Facilities,
Finance, Procurement…). The card must make the right agent win and the wrong
agent lose.

Checklist:
- [ ] Explicit negative scope ("Does not handle payroll disputes — use HR Payroll agent", "Read-only; cannot approve").
- [ ] Domain-unique vocabulary (system names, object types, IDs) that separates it from adjacent agents.
- [ ] Coverage boundaries: which regions, business units, systems, record types.
- [ ] Tags distinctive and consistent with description/skills.
- [ ] Probe test: ≥7/9 probes decided correctly and confidently from the card alone.

| Score | Anchor |
|---|---|
| 4 | Explicit exclusions + unique vocabulary; probe ≥8/9. |
| 3 | Unique vocabulary, no explicit exclusions; probe 7/9. |
| 2 | Overlaps with obvious neighbours; probe 5–6/9. |
| 1 | Generic language would attract many unrelated queries; probe 3–4/9. |
| 0 | Router cannot tell when to use it; probe ≤2/9. |

---

## D9 — Action Semantics & Interaction Contract (weight 5)

Checklist:
- [ ] Each skill clear on read-only vs write/transactional side effects.
- [ ] Approval / human-in-the-loop / confirmation behaviour stated for writes (e.g. "drafts the PO and returns it for user confirmation before submit").
- [ ] Long-running / async behaviour consistent with `capabilities.streaming` / `pushNotifications`.
- [ ] Input needs stated (what the agent will ask for, `input-required` states).
- [ ] Skill-level `inputModes`/`outputModes` set where they differ (e.g. accepts `application/pdf` invoices, returns `application/json`).
- [ ] Output artifact type described.

| Score | Anchor |
|---|---|
| 4 | Side effects, approvals, async behaviour, and I/O are explicit and consistent. |
| 3 | Mostly clear; one aspect missing. |
| 2 | Read/write ambiguous for some skills; I/O defaults only. |
| 1 | Contradictions (claims async with no push/stream) or no indication of side effects for write skills. |
| 0 | Nothing about how interaction works. |

---

## D10 — Trust, Security & Governance Signals (weight 5)

Checklist:
- [ ] `securitySchemes` + `securityRequirements` present and suitable: OAuth2 / OIDC / mTLS for enterprise (API key acceptable for internal read-only; anonymous only for public content).
- [ ] Per-skill `securityRequirements` / scopes for sensitive or write skills (least privilege).
- [ ] Indicates user-delegated vs app identity where relevant (acts "on behalf of the signed-in user").
- [ ] `provider.organization` + `provider.url`, `documentationUrl`, semantic `version`.
- [ ] Data sensitivity declared where relevant (PII, PHI/HIPAA, GxP, SOX, GDPR, export controlled).
- [ ] `extendedAgentCard` used if sensitive skills are hidden from anonymous discovery.
- [ ] `signatures` (JWS) present — bonus, not required.
- [ ] No embedded secrets, tokens, internal hostnames in prose, or personal data.

| Score | Anchor |
|---|---|
| 4 | Enterprise-grade auth with scoped access, provider/docs/version, sensitivity declared. |
| 3 | Appropriate auth + provider/docs; no per-skill scoping or sensitivity notes. |
| 2 | Auth present but weak/mismatched (anonymous allowed for write skills, API key for PHI). |
| 1 | No auth on an agent touching enterprise data, or missing provider/version. |
| 0 | Secrets/PII in card, or write agent fully unauthenticated. |

---

## Common anti-patterns (quick reference)

| Anti-pattern | Example | Dimensions hit |
|---|---|---|
| Opaque brand name | `"name": "Moss"` | D4, D8 |
| Poetic / persona voice | "A slow read, in my own voice" | D4, D6, D3 |
| Marketing copy | "Revolutionary AI that transforms your workflow" | D4, D6 |
| Transport leakage | "Over A2A: send the hostname to SendMessage…" | D4, D6 |
| Phantom skills | "Over MCP only (tools/call crawl_check)" | D1, D5 |
| Grab-bag agent | SEO audit + AI tool catalog + local business directory + book a call | D5, D8, D2 |
| Plumbing as skill | "Read a finished audit" = GetTask | D5 |
| Thin examples | 1 example per skill | D7 |
| LLM-substitutable | "Summarize text", "Explain a concept" | D3 |
| Vendor self-service | "Book a demo with ORBYX" | D2 |
| No boundaries | "Helps with anything HR related" | D8 |
| Hidden side effects | "Manages purchase orders" (creates? approves?) | D9 |
| Anonymous writes | `securityRequirements: [{}]` on a write skill | D10 |
