---
name: proactive-anomaly-detection
description: Scan local app/data stream summaries for unusual patterns (email spikes, budget overruns, failure bursts), then trigger predefined alerts and corrective playbooks such as notifications, backups, or throttling recommendations.
---

# Proactive Anomaly Detection

This skill adds preventive autonomy by identifying anomalies early and producing actionable responses.

## What it monitors
- Email volume anomalies (spikes vs baseline)
- Budget usage anomalies (daily/monthly overrun risk)
- Task failure bursts and latency regressions
- Generic stream metrics with threshold or z-score style checks

## Quick Start

```bash
python3 skills/proactive-anomaly-detection/scripts/detect_anomalies.py \
  --input skills/proactive-anomaly-detection/references/sample-streams.json \
  --out memory/anomaly-detection/anomalies.json

python3 skills/proactive-anomaly-detection/scripts/trigger_actions.py \
  --anomalies memory/anomaly-detection/anomalies.json \
  --playbook skills/proactive-anomaly-detection/references/default-playbook.json \
  --out memory/anomaly-detection/actions.json \
  --audit memory/anomaly-detection/anomaly-audit.md
```

## Detection Logic (default)
- Spike: current >= baseline * multiplier
- Overrun risk: projected spend > budget limit
- Failure burst: failure rate above threshold
- Latency regression: current latency above threshold

## Action Model
- Advisory-first by default (safe)
- Emits actions like:
  - `notify`
  - `run_backup`
  - `throttle_nonessential`
  - `escalate`

## Safety
- No destructive actions by default.
- All triggers and action decisions are logged in audit output.
- Integrations can execute externally only when explicitly enabled by operator policy.
