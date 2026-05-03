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
| Automation Controller | Ansible AWX (via AWX Operator) |
| Container Platform | Red Hat OpenShift Developer Sandbox |
| Source Control | GitHub (GitOps) |
| Managed Endpoint | Raspberry Pi — Smart Greenhouse (IoT) |

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
        │                                        (container workloads)
        ▼
 Managed Nodes
        │
        └── Raspberry Pi (Smart Greenhouse)
               ├── Temperature sensor
               ├── Humidity sensor
               ├── Soil moisture sensor
               └── Actuators (automated environmental control)
```

---

## Repository Structure

```
homelab-platform/
├── ansible/        # Playbooks and roles for managed nodes
├── awx/            # AWX configuration as code
├── openshift/      # OpenShift manifests and deployments
├── greenhouse/     # Smart greenhouse integration and playbooks
└── docs/           # Setup guides, architecture notes, cheatsheets
```

---

## Project Status

| Component | Status |
|---|---|
| RHEL9 VM (VirtualBox) | ✅ Running |
| K3s cluster | ✅ Running |
| AWX Operator + AWX instance | ✅ Running |
| GitHub → AWX Project sync | ✅ Connected |
| OpenShift Developer Sandbox | 🔄 In progress |
| Raspberry Pi network integration | 🔄 In progress |
| Smart greenhouse as managed endpoint | 🔄 In progress |
| Full end-to-end automation demo | ⏳ Planned |

---

## About the Smart Greenhouse

The managed endpoint in this homelab is a real, functioning smart greenhouse — built as an MSc thesis project in Mechatronical Engineering.

It integrates:
- Temperature, humidity, and soil moisture sensors
- Actuators for automated environmental control
- A Raspberry Pi-based control layer
- Offline-first design for resilience without cloud dependency

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
