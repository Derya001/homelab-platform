# homelab-platform

A self-built platform engineering homelab designed as a working portfolio for DevOps and Platform Engineer roles.

This is not a tutorial follow-along. Every component was designed, troubleshot, and integrated from scratch — including a live IoT-managed smart greenhouse as a real-world managed endpoint.

---

## Stack

| Layer | Technology |
|---|---|
| Virtualization | VirtualBox (AMD Ryzen 5 1600, 16GB RAM) |
| OS | Red Hat Enterprise Linux 9 |
| Kubernetes | K3s (lightweight Kubernetes) |
| Automation Controller | Ansible AWX 2.19.1 (via AWX Operator) |
| Container Platform | Red Hat OpenShift Developer Sandbox (Knative Serverless) |
| Source Control | GitHub (GitOps) |
| Managed Endpoint | Raspberry Pi 4 — Smart Greenhouse (IoT) |

---

## Architecture

```
GitHub (source of truth)
        │
        ▼
   AWX Controller  ──────────────────────────────────────┐
   (K3s / RHEL9)                                         │
        │                                                 │
        ▼                                                 ▼
 Ansible Playbooks                              OpenShift Sandbox
        │                                        └── greenhouse-dashboard
        ▼                                            (Flask, Knative)
 Managed Nodes
        │
        └── Raspberry Pi 4 (Smart Greenhouse)
               ├── BH1750     — light sensor
               ├── SHT31      — temperature + humidity
               ├── ADS1115    — ADC for soil moisture
               ├── Node-RED v4.1.10 (systemd, autostart)
               └── Actuators  — pump + lamp control
```

---

## Repository Structure

```
homelab-platform/
├── ansible/              # Playbooks and roles for managed nodes
├── awx/                  # AWX configuration as code
├── openshift/
│   └── greenhouse-dashboard/   # Flask dashboard (Dockerfile, app.py)
├── greenhouse/
│   ├── flows.json              # Node-RED flow (GitOps managed)
│   ├── playbooks/              # AWX job playbooks
│   └── scripts/                # Python sensor + actuator scripts
└── docs/                 # Setup guides, architecture notes, cheatsheets
```

---

## Project Status

| Component | Status |
|---|---|
| RHEL9 VM (VirtualBox) | ✅ Running |
| K3s cluster | ✅ Running |
| AWX Operator + AWX instance | ✅ Running |
| GitHub → AWX Project sync | ✅ Connected |
| Raspberry Pi as AWX managed node | ✅ Connected (SSH key auth) |
| Smart greenhouse as managed endpoint | ✅ Live |
| OpenShift Developer Sandbox | ✅ Running |
| Greenhouse Dashboard (Flask, OpenShift) | ✅ Deployed |
| GitHub Webhook → AWX auto-trigger | ⏳ Planned |
| Full end-to-end automation demo | ⏳ Planned |

---

## AWX Job Templates

All playbooks are stored in this repo and synced to AWX via the GitOps project connection.

| Job Template | Description |
|---|---|
| `greenhouse-ping` | Connectivity check |
| `greenhouse-restart-nodered` | Restart Node-RED systemd service |
| `greenhouse-backup-flow` | Back up flows.json to GitHub |
| `greenhouse-deploy-flow` | Deploy flows.json from GitHub to Pi |
| `greenhouse-update-pi` | Run apt update + upgrade |
| `greenhouse-check-sensors` | Read live sensor data (10s timeout) |
| `greenhouse-deploy-scripts` | Deploy Python scripts to Pi |

---

## Greenhouse Dashboard

A Flask-based sensor dashboard deployed on OpenShift as a Knative Serverless application.

**Live URL:**  
`https://homelab-platform-derya001-dev.apps.rm1.0a51.p1.openshiftapps.com`

> ⚠️ Knative scale-to-zero is active — first load may take 10–20 seconds to cold-start.

---

## About the Smart Greenhouse

The managed endpoint in this homelab is a real, functioning smart greenhouse — originally built as an MSc thesis project in Mechatronical Engineering.

It integrates:
- Temperature, humidity, soil moisture, and light sensors over I2C
- Actuators for automated pump and lamp control
- A Raspberry Pi 4-based control layer running Node-RED
- Offline-first design: local MQTT broker, systemd-managed services, no cloud dependency

In the context of this homelab, the greenhouse serves as a live, physical managed node — demonstrating end-to-end infrastructure automation on a real-world use case rather than a simulated environment.

---

## Why This Project

This homelab was built to bridge the gap between Linux/Unix system administration and modern platform engineering — covering container orchestration, infrastructure automation, and GitOps workflows in a hands-on, production-like environment.

Target roles: Platform Engineer, DevOps Engineer, Infrastructure Automation Engineer.

---

## Related

- [AWX Operator](https://github.com/ansible/awx-operator)
- [K3s](https://k3s.io)
- [Red Hat OpenShift Developer Sandbox](https://developers.redhat.com/developer-sandbox)
