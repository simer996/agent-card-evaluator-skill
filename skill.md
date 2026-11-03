---
name: agent-card-quality-eval
description: Evaluate the quality of an A2A (Agent2Agent, Linux Foundation) agent card for enterprise orchestration — decides whether a card is great, acceptable, or bad at telling an orchestrator LLM when to delegate a user query to the agent. Scores 10 weighted dimensions (spec conformance, enterprise relevance, delegation necessity, description clarity, skill granularity, skill precision, examples, routing discriminability, action semantics, security/governance) and emits a table plus a JSON label record for building eval datasets. Triggers - "evaluate this agent card", "grade agent card", "is this a good agent card", "score A2A card", "agent card quality", "label agent cards for eval dataset", "review agent-card.json".
metadata:
  author: simer996
  version: "1.0"
  a2a_spec_version: "1.0.0 (backward compatible with 0.2.x / 0.3.x cards)"
compatibility: Requires Python 3.9+ for the optional structural linter (stdlib only).
---

# agent-card-quality-eval

Judge whether an **A2A agent card** gives an enterprise orchestrator (e.g. an
M365 Copilot / Copilot Studio / Claude / Agentforce / Gemini Enterprise style router)
enough precise, trustworthy signal to decide **"delegate this user query to
this agent — or not."** Output is a scored table plus a machine-readable label
so results can be accumulated into an eval dataset.

## Background you must apply (A2A spec v1.0)

- The agent card is the agent's self-describing manifest, served at
  `/.well-known/agent-card.json` or via a registry. Clients use it "to determine
  an agent's suitability, structure requests, and ensure secure communication."
- Required `AgentCard` fields: `name`, `description`, `supportedInterfaces[]`
  (`url`, `protocolBinding`, `protocolVersion`), `version`, `capabilities`,
  `defaultInputModes`, `defaultOutputModes`, `skills[]`.
  Optional: `provider{organization,url}`, `documentationUrl`, `iconUrl`,
  `securitySchemes`, `securityRequirements`, `signatures`.
- Required `AgentSkill` fields: `id`, `name`, `description`, `tags[]`.
  Optional: `examples[]`, `inputModes`, `outputModes`, `securityRequirements`.
- Agents are **opaque** — the orchestrator sees *only* the card, not the
  agent's tools or prompts. Anything not in the card does not exist for routing.
- Legacy 0.2/0.3 cards use top-level `url`, `preferredTransport`,
  `protocolVersion`, `security`, `supportsAuthenticatedExtendedCard`. Accept
  them; note the version, do not double-penalize.

The orchestrator's routing decision is driven mostly by `description`, skill
`name`/`description`, `examples`, and `tags`. So
the **semantic dimensions carry ~85% of the weight**; spec plumbing is a gate,
not the goal.

## Workflow

1. **Ingest.** Accept JSON (file path, pasted text, or URL to
   `agent-card.json`). If it is a fragment or malformed, still evaluate the
   semantic content you can see and record `parse_status: "fragment"` — a
   fragment always fails D1.
2. **Run the structural linter** (deterministic evidence for D1, D5, D7, D10):
   ```
   python "<skill_dir>/scripts/lint_agent_card.py" <card.json | ->
   ```
   Use `-` to read from stdin. It prints JSON with errors, warnings, and stats
   (skill count, examples per skill, off-A2A skills, vague words, etc.).
   If Python is unavailable, perform the same checks manually from
   `references/rubric.md` §D1.
3. **Classify the agent.** Using `references/enterprise-domains.md`, identify:
   business function, likely system(s) of record, target persona, and whether
   it reads, writes, or orchestrates. If it maps to no enterprise function,
   say so — it caps D2.
4. **Simulate the orchestrator (probe test).** Write 9 probe queries a real
   enterprise employee might type into a company chat assistant:
   - 3 **in-scope** queries (should route here),
   - 3 **adjacent** queries (plausibly confusable with a neighbouring agent,
     e.g. "new hire needs a laptop" — HR onboarding vs IT asset request),
   - 3 **out-of-scope** queries (general LLM knowledge or other domains).
   For each, decide from the card alone: route / don't route / ambiguous.
   Count how many the card lets you decide correctly and confidently. This is
   primary evidence for D3 and D8.
5. **Score each dimension 0–4** using the anchors in `references/rubric.md`.
   Cite concrete evidence (quote the field) for every score. Never score from
   vibes.
6. **Apply gates & caps** (below), compute the weighted score, assign a grade
   and a dataset label.
7. **Calibrate.** Before finalizing, compare against the anchors in
   `references/calibration-examples.md`. A card should not outscore the gold
   example unless it is genuinely better on the same evidence.
8. **Emit output** in the exact format below.

## Dimensions and weights

| ID | Dimension | Weight | Core question |
|----|-----------|-------:|---------------|
| D1 | Spec Conformance & Structural Integrity | 5 | Is it a valid, complete A2A card the client can actually use? |
| D2 | Enterprise Relevance & Business Value | 15 | Does it serve a real enterprise business function / LOB system for employees? |
| D3 | Delegation Necessity (Non-Substitutability) | 15 | Would the orchestrator LLM *need* this agent, or could it answer alone? |
| D4 | Agent Description Clarity & Scope | 10 | Can a router grasp who/what/which system/for whom in one read? |
| D5 | Skill Decomposition & Cohesion | 10 | Are skills discrete, task-level, non-overlapping, and coherent with one agent purpose? |
| D6 | Skill Description Precision | 10 | Does each skill state action + business object + system + inputs + outputs + limits, in plain business language? |
| D7 | Example Utterance Quality & Coverage | 15 | Are there enough realistic, diverse, entity-bearing user requests per skill? |
| D8 | Routing Discriminability & Boundaries | 10 | Does the card say what it does NOT do and separate itself from adjacent agents? |
| D9 | Action Semantics & Interaction Contract | 5 | Are read vs write, approvals/HITL, async behaviour, I/O modes, and outputs clear? |
| D10 | Trust, Security & Governance Signals | 5 | Are auth, scopes, provider, versioning, docs, data sensitivity declared appropriately? |

Weighted score (0–100) = Σ(score_i / 4 × weight_i).

## Gates and caps (apply after scoring)

| Condition | Effect |
|-----------|--------|
| D3 ≤ 1 (LLM could do it unaided) | Overall capped at 49 → max grade **Poor** |
| D2 ≤ 1 (consumer/hobby/self-promotional, no enterprise function) | Overall capped at 49 |
| D7 = 0 (no examples anywhere) | Overall capped at 59 |
| Any skill advertised that is **not reachable over A2A** (e.g. "MCP only") | D1 and D5 each ≤ 2; list as critical issue |
| Card cannot be parsed / required top-level fields missing | D1 = 0; overall capped at 69 |
| Write/transactional agent with **no** security scheme | D10 = 0; flag as critical |
| Card contains secrets, internal hostnames in prose, or PII | D10 = 0; flag as critical |

## Grades and dataset labels

| Weighted score | Grade | `label` |
|---:|---|---|
| 85–100 | Excellent | `great` |
| 70–84 | Good | `good` |
| 50–69 | Fair | `needs_work` |
| 0–49 | Poor | `bad` |

## Output format (always use exactly this)

````
## Agent Card Quality Evaluation — <agent name> (v<version>)

**Verdict:** <Grade> — <score>/100 · label: `<label>`
**Classified as:** <function> · <system(s) of record> · <persona> · <read|write|mixed>
**One-line rationale:** <why an orchestrator would / would not route well with this card>

| # | Dimension | Weight | Score (0-4) | Weighted | Key evidence (quoted) | Top fix |
|---|-----------|-------:|:-----------:|---------:|-----------------------|---------|
| D1 | Spec Conformance & Structural Integrity | 5 | x | y.y | ... | ... |
| ... all 10 rows ... |
| | **Total** | **100** | | **NN.N** | | |

**Gates/caps applied:** <none | list>

### Orchestrator probe results
| Probe | Type | Expected | Card-only decision | Correct? |
|-------|------|----------|--------------------|----------|
(9 rows)
Routing confidence: n/9 correct & confident.

### Per-skill breakdown
| Skill id | Discrete task? | Precision (0-4) | # examples | Example quality (0-4) | Issue |
|----------|---------------|:---------------:|-----------:|:---------------------:|-------|

### Critical issues
- ...

### Top 3 rewrites (highest impact first)
1. <field> → <concrete rewritten text>

### Dataset record
```json
{ "agent_name": "...", "card_version": "...", "a2a_protocol_version": "...",
  "parse_status": "ok|fragment|invalid", "domain": "...", "systems": ["..."],
  "scores": {"D1":0,"D2":0,"D3":0,"D4":0,"D5":0,"D6":0,"D7":0,"D8":0,"D9":0,"D10":0},
  "weighted_score": 0.0, "caps_applied": ["..."], "grade": "...", "label": "...",
  "probe_accuracy": "n/9", "critical_issues": ["..."], "rationale": "..." }
```
````

## Batch mode (building the eval dataset)

When given multiple cards (folder, JSONL, or list):
1. Evaluate each independently with the full workflow — do not let one card's
   score anchor another's.
2. Append each dataset record as one line to `agent_card_evals.jsonl` in the
   user's chosen output folder (ask once if not given).
3. Finish with a summary table: `agent | domain | score | label | top issue`,
   plus label distribution. Warn if the set is heavily skewed (e.g. >70% one
   label) since that weakens the eval dataset.

## Evaluator rules

- Judge **only what the card says**. Do not give credit for capabilities you
  guess the vendor has; the orchestrator cannot guess either.
- Quote evidence. Every score needs a field quote or an explicit "absent".
- Penalize marketing, poetic, first-person-persona, or vague language
  ("insights", "magic", "a slow read in my own voice") — it does not help
  routing.
- Penalize transport/implementation chatter in descriptions (JSON-RPC method
  names, "over MCP", run ids) — that belongs in interfaces/docs, not routing
  text — unless it clarifies a real constraint.
- Do not penalize a narrow agent for being narrow; penalize it for being
  **vague** or **incoherent**. One sharp skill beats seven fuzzy ones.
- Reward explicit enterprise grounding: named systems of record (ServiceNow,
  Workday, SAP S/4HANA, Ariba, Dynamics 365, Salesforce, Veeva, Epic...),
  business objects (incident, PO, requisition, opportunity, case, contract,
  shift, deviation), identifiers (INC0012345, PO 4500012345), and policies.
- Be consistent: re-read the rubric anchors for any score you are unsure of.

## Reference files

- `references/rubric.md` — full 0–4 anchors and checklists per dimension.
- `references/enterprise-domains.md` — enterprise functions, top SaaS/LOB
  systems, canonical agent skills, business objects, and sensitivity per
  domain; use for D2/D3/D6/D7 grounding.
- `references/calibration-examples.md` — scored anchors: two bad cards
  (ORBYX grab-bag aggregator, Moss persona fragment), a mediocre card, and a gold card.
  All are synthetic.
- `references/examples/README.md` — what each synthetic example card illustrates.
- `scripts/lint_agent_card.py` — deterministic structural linter.
