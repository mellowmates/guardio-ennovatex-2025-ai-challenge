# Samsung EnnovateX 2025 AI Challenge Submission

- **Problem Statement** — On-Device Multi-Agent System for Behavior-Based Anomaly & Fraud Detection: 
Multi-agent system that runs fully on-device, continuously learning and modeling user behaviour patterns to detect anomalies or potential fraud in real-time, without sending sensitive data to external servers. The system can monitor user behaviour patterns (e.g., touch patterns, typing rhythm, app usage, movement) and build local models of “normal” behaviour. It should detect and react to anomalous or suspicious activity (e.g., unauthorized access, bot-like behaviour, spoofing).
- **Team name** — Dev Dream Team
- **Team members (Names)** — Omprakash Panda, Sindhu B L, Vittal G B, Vishwajith Chakravarthy
- **Demo Video Link** — [Youtube](https://youtu.be/kQXd9r5204I) 

---

## Project Artefacts

- **Technical Documentation** — [docs/](./docs)  
  All technical details are written in Markdown inside the docs folder (architecture, agent designs, anomaly logic, setup, troubleshooting).

- **Source Code** — [src/](./src)  
  Fully runnable code with clear entry points (e.g., `src/main.py`), platform notes, and virtual environment setup.

- **Models Used** — N/A  
  Guardio currently uses statistical and behavioral methods (rolling windows, EMA, z-scores) and does not rely on external ML models.

- **Models Published** — N/A

- **Datasets Used** — N/A  
  Guardio learns on-device from live behavioral signals and does not ship datasets.

- **Datasets Published** — N/A

---

## Attribution

This solution is original to Dev Dream Team and built from scratch for Samsung EnnovateX 2025. If any open-source components or prior work are incorporated later, links and contributions will be attributed explicitly here.

---

# Guardio — Adaptive Behavioral Anomaly Detection

<div align="center">

![Guardio Logo](https://img.shields.io/badge/🛡️-Guardio-blue?style=for-the-badge&logoColor=white)

[![Samsung EnnovateX 2025](https://img.shields.io/badge/Samsung-EnnovateX%202025-1F6FEB?style=for-the-badge&logo=samsung&logoColor=white)](https://ennovatex.io)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-FF6B35?style=for-the-badge)](https://customtkinter.tomschimansky.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](./LICENSE)

**An intelligent, privacy‑first anomaly detection system that learns unique behavioral patterns to identify potential security threats in real time.**

[🎬 Demo Video](#demo-video) • [🚀 Quick Start](#quick-start) • [📖 Documentation](#how-it-works) • [🧱 Architecture](#technical-architecture)

</div>

---

## Built for Samsung EnnovateX 2025 AI Challenge

Guardio implements adaptive, on-device behavioral security. It learns normal user activity and flags unusual patterns while preserving privacy through local processing.

### The Problem
- Massive financial loss from evolving threats and unauthorized access
- Static, rule-based systems fail to adapt to changing behaviors
- Privacy concerns with cloud-based behavioral analytics

### Our Solution
- On-device, adaptive anomaly detection that:
  - Learns personal baselines continuously
  - Detects subtle deviations in real time
  - Preserves privacy with local-only processing
  - Adapts thresholds to real-world behavior change

---

## Key Features

### 🧠 Adaptive Intelligence
- Rolling statistics and exponential moving averages
- Multi-agent behavioral analysis (typing, movement, app usage)
- Z-score–based anomaly detection with configurable thresholds

### 🔒 Privacy-First
- 100% on-device processing
- No data transmission
- Works offline; zero cloud dependency

### 🎛️ Professional Controls
- Live sensitivity tuning (1.0σ–6.0σ)
- Alert cooldown management (0–10s)
- One UI–inspired dashboard for clarity

### 📊 Real-Time Monitoring
- Risk score visualization
- Live WPM (typing) analysis and rhythm detection
- Transparent agent status and event log

---

## Demo Video

- ▶️ **YouTube (Unlisted/Public)**: https://www.youtube.com/watch?v=YOUR_VIDEO_ID  
  A short walkthrough showing real-time detection and controls.

---

## Quick Start

### Prerequisites
- Python 3.8+ (Windows/macOS/Linux)
- pip

### Setup

```
git clone https://github.com/mellowmates/guardio-ennovatex-2025-ai-challenge.git
cd ennovatex-2025-ai-challenge-guardio

# Create and activate virtual environment
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python src/main.py
```

### First Launch
1. Click “START MONITORING” to begin learning baselines.  
2. Set detection sensitivity (recommended: 3.0σ).  
3. Configure alert cooldown (recommended: 3 seconds).  
4. Observe live events and anomaly flags in the activity panel.

---

## How It Works

### Behavioral Agents

| Agent | Signals | Detection Method |
|------|---------|------------------|
| MovementAgent | Mouse velocity/acceleration | Deviation from rolling baseline |
| TypingAgent | WPM + inter-key rhythm | Z-score and rhythm anomalies |
| AppUsageAgent | Focus/app switching | Unusual transition patterns |

### Adaptive Learning
1. Baseline learning from recent activity (rolling windows).  
2. EMA adapts to gradual behavior changes.  
3. Latest measurement evaluated via z-score relative to baseline.  
4. Alerts are gated by a cooldown to prevent spam.

---

## Technical Architecture

- **Language**: Python 3.8+  
- **UI**: CustomTkinter (One UI–inspired)  
- **Concurrency**: Multi-threaded agents  
- **Detection**: Rolling mean/std, EMA, z-scores  
- **Privacy**: Local-only processing

### System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| Python | 3.8 | 3.10+ |
| RAM | 2 GB | 4 GB+ |
| Storage | 100 MB | 500 MB |

---

## Configuration

```
# Sensitivity (σ)
VERY_SENSITIVE = 1.0
BALANCED = 3.0   # Recommended
RELAXED = 6.0

# Alert cooldown (seconds)
IMMEDIATE = 0.0
DEFAULT = 3.0
QUIET = 10.0
```

---

## Performance

- High accuracy on significant deviations with tuned thresholds  
- Low CPU and memory footprint (lightweight, thread-based)  
- Sub-100ms detection latency in typical scenarios

---

## Repository Structure

```
.
├─ docs/                                # Technical documentation (Markdown)
│  ├─ images/
│  │  └─ ui-screenshots/
│  │     ├─ UI.png
│  │     └─ working.png
│  ├─ algorithms.md
│  ├─ api-reference.md
│  ├─ architecture.md
│  ├─ changelog.md
│  ├─ contributing.md
│  ├─ index.md
│  ├─ installation.md
│  └─ user-manual.md
├─ src/                                 # Application source code
│  ├─ agents/
│  │  ├─ __init__.py
│  │  ├─ app_usage_agent.py
│  │  ├─ movement_agent.py
│  │  └─ typing_agent.py
│  ├─ __init__.py
│  ├─ dashboard.py
│  └─ main.py
├─ .gitignore
├─ LICENSE
├─ README.md
└─ requirements.txt

```

---

## License

This project is released under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

## Contact

- Team: Dev Dream Team  
- Members: Omprakash Panda, Sindhu B L, Vittal G B, Vishwajith Chakravarthy  
- Email: omprakash11273@gmail.com  
- GitHub: https://github.com/mellowmates/guardio-ennovatex-2025-ai-challenge

---

<div align="center">

Built for Samsung EnnovateX 2025 • Privacy-first adaptive security

</div>
