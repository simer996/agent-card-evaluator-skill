#!/usr/bin/env python3
"""Deterministic structural linter for A2A agent cards (spec v1.0, tolerant of 0.2/0.3).

Usage:
    python lint_agent_card.py card.json
    type card.json | python lint_agent_card.py -

Prints a JSON report: parse_status, detected_spec, errors, warnings, stats, per_skill.
The report is evidence for the LLM evaluator; it does not produce the final grade.
"""
import json
import re
import sys

VALID_BINDINGS = {"JSONRPC", "GRPC", "HTTP+JSON"}
MIME_RE = re.compile(r"^[a-zA-Z0-9][\w.+-]*/[\w.+*-]+(;.*)?$")
SEMVER_RE = re.compile(r"^\d+\.\d+(\.\d+)?([-+].*)?$")
OFF_A2A_RE = re.compile(
    r"\b(mcp only|over mcp only|only (over|via) mcp|via rest api only|not available over a2a|coming soon|tools/call)\b",
    re.I,
)
TRANSPORT_NOISE_RE = re.compile(
    r"\b(sendmessage|gettask|listtasks|subscribetotask|json-?rpc|tools/call|run id|task_state_\w+|over a2a|over mcp)\b",
    re.I,
)
VAGUE_RE = re.compile(
    r"\b(magic|seamless(ly)?|revolutionary|cutting[- ]edge|insights?|anything|everything|whisper|my own voice|"
    r"powerful|next[- ]gen|world[- ]class|effortless(ly)?|delight)\b",
    re.I,
)
FIRST_PERSON_RE = re.compile(r"(^|[\s\"'])(I|I'm|I'll|me|my)\b")
GENERIC_TAGS = {"ai", "agent", "tool", "tools", "helper", "assistant", "llm", "a2a", "misc", "general", "chat"}
SECRET_RE = re.compile(r"(api[_-]?key\s*[:=]|bearer\s+[a-z0-9._-]{20,}|sk-[a-z0-9]{20,}|password\s*[:=])", re.I)
ENTITY_RE = re.compile(r"(\b[A-Z]{2,6}[-_]?\d{3,}\b|\b\d{5,}\b|\$\s?\d|\bQ[1-4]\b|\b20\d\d\b)")


def load(arg):
    raw = sys.stdin.read() if arg == "-" else open(arg, encoding="utf-8-sig").read()
    try:
        return json.loads(raw), "ok", raw
    except json.JSONDecodeError as e:
        # Try wrapping a fragment (e.g. starts with ',' or a bare key list)
        frag = raw.strip().lstrip(",").strip()
        if not frag.startswith("{"):
            frag = "{" + frag
        for suffix in ("", "}", "]}", "]}]}", "\"]}]}"):
            try:
                return json.loads(frag + suffix), "fragment", raw
            except json.JSONDecodeError:
                continue
        return None, f"invalid: {e}", raw


def text_flags(text):
    flags = []
    if not text:
        return flags
    if TRANSPORT_NOISE_RE.search(text):
        flags.append("transport_noise")
    if VAGUE_RE.search(text):
        flags.append("vague_or_marketing:" + ",".join(sorted({m.group(0).lower() for m in VAGUE_RE.finditer(text)})))
    if FIRST_PERSON_RE.search(text):
        flags.append("first_person_voice")
    if OFF_A2A_RE.search(text):
        flags.append("not_reachable_over_a2a")
    return flags


def lint(card, parse_status):
    errors, warnings = [], []
    if card is None:
        return {"parse_status": parse_status, "errors": ["card could not be parsed"], "warnings": [], "stats": {}, "per_skill": []}
    if parse_status == "fragment":
        errors.append("card is a fragment (not a complete JSON object)")

    is_v1 = "supportedInterfaces" in card
    is_legacy = "url" in card or "preferredTransport" in card
    detected = "1.0" if is_v1 else ("0.2/0.3" if is_legacy else "unknown")

    required = ["name", "description", "version", "capabilities", "defaultInputModes", "defaultOutputModes", "skills"]
    required += ["supportedInterfaces"] if is_v1 or not is_legacy else ["url"]
    for f in required:
        if f not in card or card[f] in (None, "", []):
            errors.append(f"missing required field: {f}")

    # Interfaces
    urls = []
    if is_v1:
        for i, itf in enumerate(card.get("supportedInterfaces") or []):
            for f in ("url", "protocolBinding", "protocolVersion"):
                if not itf.get(f):
                    errors.append(f"supportedInterfaces[{i}] missing {f}")
            b = itf.get("protocolBinding")
            if b and b not in VALID_BINDINGS:
                warnings.append(f"supportedInterfaces[{i}] non-core protocolBinding '{b}' (custom or non-A2A, e.g. MCP)")
            urls.append(itf.get("url", ""))
    else:
        urls.append(card.get("url", ""))
        for itf in card.get("additionalInterfaces") or []:
            urls.append(itf.get("url", ""))
    for u in urls:
        if u and (u.startswith("http://") or "localhost" in u or "127.0.0.1" in u):
            errors.append(f"non-production interface URL: {u}")

    # Modes
    for f in ("defaultInputModes", "defaultOutputModes"):
        for m in card.get(f) or []:
            if not MIME_RE.match(str(m)):
                warnings.append(f"{f} value '{m}' is not a media type")

    ver = str(card.get("version", ""))
    if ver and not SEMVER_RE.match(ver):
        warnings.append(f"version '{ver}' is not semver-like")

    prov = card.get("provider") or {}
    if not prov.get("organization") or not prov.get("url"):
        warnings.append("provider.organization/url missing")
    if not card.get("documentationUrl"):
        warnings.append("documentationUrl missing")

    sec_schemes = card.get("securitySchemes") or {}
    sec_reqs = card.get("securityRequirements", card.get("security")) or []
    anonymous_allowed = any(
        (isinstance(r, dict) and (r == {} or r.get("schemes") == {})) for r in sec_reqs
    )
    if not sec_schemes:
        warnings.append("no securitySchemes declared")
    if anonymous_allowed:
        warnings.append("securityRequirements allows anonymous access (empty requirement)")

    desc = card.get("description") or ""
    agent_flags = text_flags(desc)
    for fl in agent_flags:
        warnings.append(f"agent description: {fl}")
    if SECRET_RE.search(json.dumps(card)):
        errors.append("possible secret/credential embedded in card")
    name = card.get("name") or ""
    if name and len(name.split()) == 1 and (name.isupper() or len(name) <= 6):
        warnings.append(f"agent name '{name}' is an opaque brand/acronym, not descriptive")

    # Skills
    per_skill, ids = [], set()
    total_examples = 0
    skills = card.get("skills") or []
    for i, s in enumerate(skills):
        sid = s.get("id") or f"<skill[{i}]>"
        miss = [f for f in ("id", "name", "description", "tags") if not s.get(f)]
        if miss:
            errors.append(f"skill {sid} missing required: {', '.join(miss)}")
        if s.get("id") in ids:
            errors.append(f"duplicate skill id: {sid}")
        ids.add(s.get("id"))
        ex = [e for e in (s.get("examples") or []) if isinstance(e, str) and e.strip()]
        total_examples += len(ex)
        sdesc = s.get("description") or ""
        flags = text_flags(sdesc)
        tags = [str(t).lower() for t in (s.get("tags") or [])]
        if tags and all(t in GENERIC_TAGS for t in tags):
            flags.append("generic_tags_only")
        if len(ex) < 3:
            flags.append(f"few_examples({len(ex)})")
        if len(set(e.lower() for e in ex)) < len(ex):
            flags.append("duplicate_examples")
        if sdesc and len(sdesc.split()) < 8:
            flags.append("very_short_description")
        if sdesc.strip().lower() == str(s.get("name", "")).strip().lower():
            flags.append("description_equals_name")
        if s.get("securityRequirements"):
            flags.append("has_skill_level_security")
        per_skill.append({
            "id": sid,
            "description_words": len(sdesc.split()),
            "examples": len(ex),
            # Heuristic only (IDs, amounts, years); named systems like "SAP" are not counted.
            "examples_with_identifiers": sum(1 for e in ex if ENTITY_RE.search(e)),
            "tags": tags,
            "flags": flags,
        })

    off_a2a = [p["id"] for p in per_skill if "not_reachable_over_a2a" in p["flags"]]
    if off_a2a:
        errors.append(f"skills not reachable over A2A (phantom skills): {off_a2a}")

    stats = {
        "detected_spec": detected,
        "skill_count": len(skills),
        "total_examples": total_examples,
        "skills_with_lt3_examples": sum(1 for p in per_skill if p["examples"] < 3),
        "skills_with_0_examples": sum(1 for p in per_skill if p["examples"] == 0),
        "agent_description_words": len(desc.split()),
        "streaming": (card.get("capabilities") or {}).get("streaming"),
        "pushNotifications": (card.get("capabilities") or {}).get("pushNotifications"),
        "security_schemes": list(sec_schemes.keys()),
        "anonymous_allowed": anonymous_allowed,
        "signed": bool(card.get("signatures")),
    }
    return {"parse_status": parse_status, "errors": errors, "warnings": warnings, "stats": stats, "per_skill": per_skill}


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    card, status, _ = load(sys.argv[1])
    print(json.dumps(lint(card, status), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
