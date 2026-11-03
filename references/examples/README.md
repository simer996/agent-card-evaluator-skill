# Example agent cards

Calibration inputs for the agent-card-quality-eval skill. Scores and rationale are in
[`../calibration-examples.md`](../calibration-examples.md).

All cards are **synthetic**, written for this skill. Organizations, brands and
domains (Acmera, ORBYX, Moss, `*.example`) are fictitious, and any resemblance
to real agents is coincidental.

| File | Expected label | What it illustrates |
|---|---|---|
| `gold-servicenow-itsm.json` | `great` | Enterprise IT service desk card: named system, discrete lifecycle skills, rich examples, explicit exclusions, scoped OAuth. |
| `mediocre-hr-assistant.json` | `bad` (borderline) | Real enterprise domain undermined by a vague description, one-line skills, thin examples and no boundaries. |
| `bad-grabbag-aggregator.json` | `bad` | Opaque brand, transport leakage, "MCP only" phantom skills, protocol plumbing as a skill, vendor self-promotion, unrelated skill grab-bag, anonymous access. |
| `bad-persona-fragment.json` | `bad` | Truncated/unparseable fragment with a poetic first-person persona and hobby/consumer skills. |
