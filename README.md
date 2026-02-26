# Proactive Anomaly Detection (OpenClaw Skill)

A preventive autonomy skill for OpenClaw that scans integrated app/data stream summaries for unusual patterns (email spikes, budget overrun risk, failure bursts, latency regressions) and generates predefined alert/corrective playbook actions.

## What it does

- Detects anomalies in operational streams
- Classifies severity (`medium`, `high`)
- Maps anomalies to predefined response actions
- Produces machine-readable action output + human audit log

## Included files

- `SKILL.md` — skill behavior and operating guidance
- `scripts/detect_anomalies.py` — anomaly scanner
- `scripts/trigger_actions.py` — response/playbook engine
- `references/sample-streams.json` — sample stream input
- `references/default-playbook.json` — default action rules
- `_meta.json` — metadata

## Quick Start

```bash
python3 scripts/detect_anomalies.py \
  --input references/sample-streams.json \
  --out ./out/anomalies.json

python3 scripts/trigger_actions.py \
  --anomalies ./out/anomalies.json \
  --playbook references/default-playbook.json \
  --out ./out/actions.json \
  --audit ./out/anomaly-audit.md
```

## Detection model (default)

- Spike: `current >= baseline * multiplier`
- Budget overrun risk: `projected > budget limit`
- Failure burst: `failure_rate > threshold`
- Latency regression: `p95 latency > threshold`

## Action model

Default action types:
- `notify`
- `run_backup`
- `throttle_nonessential`
- `offload_candidate`
- `escalate`

All actions are advisory by default and intended to be executed via approved operator workflows.

## Safety

- No destructive actions by default
- Full decision/audit output for traceability
- Integrations can be enabled explicitly per environment

## Commercial Support & Custom Builds

Want this adapted to your workflow or stack?

- Custom implementation
- Integration with your existing OpenClaw setup
- Security hardening + approval-gated actions
- Ongoing optimization and support

Contact: **DirtyLeopard.com**

## Service Packages

| Package | Price | Includes |
|---|---:|---|
| Starter Skill | $399 | 1 custom skill, setup docs, 1 revision |
| Growth Bundle | $1,200 | 3 custom skills, workflow integration, 14-day support |
| Operator Suite | $3,000+ | 5–8 skills, orchestration, security/reliability tuning |

For commercial licensing or retainers, open an issue in this repo or contact via DirtyLeopard.com.

## License

MIT
