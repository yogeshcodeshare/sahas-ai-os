"""Regenerate the endpoint catalog in references/ghl-api.md from GHL's official OpenAPI specs.

Usage:
    git clone --depth 1 https://github.com/GoHighLevel/highlevel-api-docs <dir>
    python -I scripts/build-ghl-api-catalog.py <dir>

Only the text between the CATALOG markers in references/ghl-api.md is replaced; the hand-written
quick start and recipes above it are kept.
"""
import glob
import json
import os
import subprocess
import sys

START = "<!-- CATALOG:START -->"
END = "<!-- CATALOG:END -->"
METHODS = ("get", "post", "put", "patch", "delete")


def param_list(op):
    out = []
    for p in op.get("parameters", []):
        if p.get("in") in ("path", "query") and p.get("name"):
            out.append(p["name"] + ("*" if p.get("required") else ""))
    return ", ".join(out)


def body_fields(spec, op):
    schema = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
    ref = schema.get("$ref")
    if not ref:
        return ""
    s = spec.get("components", {}).get("schemas", {}).get(ref.split("/")[-1], {})
    req = set(s.get("required") or [])
    props = list(s.get("properties", {}))
    return ", ".join(p + ("*" if p in req else "") for p in props[:14]) + (" …" if len(props) > 14 else "")


def version_of(op):
    for p in op.get("parameters", []):
        if p.get("name") == "Version":
            enum = p.get("schema", {}).get("enum")
            if enum:
                return enum[0]
    return "—"


def scope_of(op):
    sec = op.get("security") or [{}]
    for entry in sec:
        for _, scopes in entry.items():
            if scopes:
                return ", ".join(scopes)
    return "—"


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def build(docs_dir):
    lines = []
    commit = subprocess.run(["git", "-C", docs_dir, "log", "-1", "--format=%h %cs"],
                            capture_output=True, text=True).stdout.strip()
    files = sorted(glob.glob(os.path.join(docs_dir, "apps", "*.json")))
    total = 0
    sections = []
    for f in files:
        spec = json.load(open(f, encoding="utf8"))
        name = os.path.splitext(os.path.basename(f))[0]
        rows = []
        for path, item in spec.get("paths", {}).items():
            for m, op in item.items():
                if m not in METHODS:
                    continue
                rows.append((m.upper(), path, op.get("summary", ""), scope_of(op), version_of(op),
                             param_list(op), body_fields(spec, op)))
        if not rows:
            continue
        total += len(rows)
        sec = [f"### {spec.get('info', {}).get('title', name)} (`apps/{name}.json`, {len(rows)} endpoints)", "",
               "| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |",
               "|---|---|---|---|---|---|---|"]
        for r in rows:
            sec.append("| " + " | ".join(cell(x) if i != 1 else f"`{x}`" for i, x in enumerate(r)) + " |")
        sections.append("\n".join(sec))
    lines.append(f"Generated from GoHighLevel/highlevel-api-docs @ {commit}: {total} endpoints in "
                 f"{len(sections)} APIs. Regenerate with `scripts/build-ghl-api-catalog.py`.")
    lines.append("")
    lines.append("**Index:** " + " · ".join(
        s.splitlines()[0].replace("### ", "").split(" (")[0] for s in sections))
    lines.append("")
    lines.extend(s + "\n" for s in sections)

    events = sorted(os.path.splitext(os.path.basename(p))[0]
                    for p in glob.glob(os.path.join(docs_dir, "docs", "webhook events", "*.md")))
    lines.append("### Webhook events (`docs/webhook events/`)")
    lines.append("")
    lines.append(", ".join(f"`{e}`" for e in events))
    lines.append("")
    return "\n".join(lines)


def main():
    docs_dir = sys.argv[1]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target = os.path.join(root, "references", "ghl-api.md")
    text = open(target, encoding="utf8").read()
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    new = head + START + "\n" + build(docs_dir) + "\n" + END + tail
    open(target, "w", encoding="utf8", newline="\n").write(new)
    print("updated", target)


if __name__ == "__main__":
    main()
