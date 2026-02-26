#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, timezone


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def select_actions(anomaly, rules):
    atype = anomaly.get("type")
    sev = anomaly.get("severity", "medium")
    candidates = rules.get(atype, rules.get("default", []))
    actions = []
    for a in candidates:
        act = dict(a)
        if sev == "high" and act.get("escalate_on_high", False):
            act["priority"] = "urgent"
        else:
            act.setdefault("priority", "normal")
        actions.append(act)
    return actions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anomalies", required=True)
    ap.add_argument("--playbook", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--audit", required=True)
    args = ap.parse_args()

    an = load_json(args.anomalies, {"anomalies": []})
    pb = load_json(args.playbook, {"rules": {"default": []}})

    rules = pb.get("rules", {})
    items = []

    for anomaly in an.get("anomalies", []):
        acts = select_actions(anomaly, rules)
        items.append({
            "anomaly": anomaly,
            "actions": acts
        })

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "count": len(items),
        "items": items
    }

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    os.makedirs(os.path.dirname(args.audit) or ".", exist_ok=True)
    with open(args.audit, "w", encoding="utf-8") as f:
        f.write(f"# Proactive Anomaly Detection Audit ({result['timestamp']})\n\n")
        f.write(f"- Total anomalies: {len(items)}\n\n")
        for i, it in enumerate(items, start=1):
            a = it["anomaly"]
            f.write(f"## {i}. {a.get('type')} [{a.get('severity')}] on `{a.get('stream')}`\n")
            f.write(f"Details: `{a.get('details')}`\n\n")
            f.write("Actions:\n")
            for act in it["actions"]:
                f.write(f"- {act.get('action')} (priority: {act.get('priority')})\n")
            f.write("\n")

    print(f"Wrote {args.out}")
    print(f"Wrote {args.audit}")


if __name__ == "__main__":
    main()
