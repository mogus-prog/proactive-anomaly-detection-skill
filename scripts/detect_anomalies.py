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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Stream metrics json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    data = load_json(args.input, {})
    cfg = data.get("config", {})
    streams = data.get("streams", [])

    spike_mult = float(cfg.get("spike_multiplier", 2.0))
    fail_thr = float(cfg.get("failure_rate_threshold", 0.2))
    latency_thr = float(cfg.get("latency_threshold_ms", 60000))

    anomalies = []

    for s in streams:
        name = s.get("name", "unknown")
        typ = s.get("type", "generic")
        cur = float(s.get("current", 0))
        base = float(s.get("baseline", 0))

        # Generic spike
        if base > 0 and cur >= base * spike_mult:
            anomalies.append({
                "stream": name,
                "type": "spike",
                "severity": "high" if cur >= base * (spike_mult + 1) else "medium",
                "details": {"current": cur, "baseline": base, "multiplier": round(cur / base, 2)}
            })

        # Budget overrun risk
        if typ == "budget":
            spent = float(s.get("spent", cur))
            limit = float(s.get("limit", base))
            projected = float(s.get("projected", spent))
            if limit > 0 and projected > limit:
                anomalies.append({
                    "stream": name,
                    "type": "budget_overrun_risk",
                    "severity": "high" if projected > limit * 1.2 else "medium",
                    "details": {"spent": spent, "limit": limit, "projected": projected}
                })

        # Failure burst
        if typ == "task_failures":
            total = float(s.get("total", 0))
            failures = float(s.get("failures", 0))
            if total > 0:
                fr = failures / total
                if fr >= fail_thr:
                    anomalies.append({
                        "stream": name,
                        "type": "failure_burst",
                        "severity": "high" if fr >= fail_thr * 1.5 else "medium",
                        "details": {"failure_rate": round(fr, 4), "threshold": fail_thr, "total": total}
                    })

        # Latency regression
        if typ == "latency":
            p95 = float(s.get("p95_ms", cur))
            if p95 >= latency_thr:
                anomalies.append({
                    "stream": name,
                    "type": "latency_regression",
                    "severity": "high" if p95 >= latency_thr * 1.5 else "medium",
                    "details": {"p95_ms": p95, "threshold_ms": latency_thr}
                })

    out = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "count": len(anomalies),
        "anomalies": anomalies
    }

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {args.out} ({len(anomalies)} anomalies)")


if __name__ == "__main__":
    main()
