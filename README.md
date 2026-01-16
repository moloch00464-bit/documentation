# M.O.L.O.C.H. Documentation

[![Netlify Status](https://api.netlify.com/api/v1/badges/ec224ba7-b3fb-4fc6-929e-991ba9801b53/deploy-status)](https://app.netlify.com/sites/hacs/deploys)

## About M.O.L.O.C.H.

**M.O.L.O.C.H.** (Modular Orchestration Layer for Organized Control & Human-aligned)** is a human-controlled AI system designed with explicit boundaries, transparent operations, and personality-aware interaction patterns.

### Core Principles

- **Transparent Learning:** All learning processes are visible and explicable
- **Human-Controlled Autonomy:** Decision authority remains with human operators
- **Personality with Boundaries:** Consistent behavioral patterns within defined limits
- **Local-First Privacy:** Raspberry Pi deployment with minimal cloud dependencies

### Key Features

- Consistent persona with humor and self-awareness
- Explicit API call approval workflow
- Structured internet access (no free browsing)
- Hard boundaries against self-replication and goal redefinition

## Documentation Structure

This repository hosts the comprehensive documentation for M.O.L.O.C.H.

### System Documentation

- **[Constitution](documentation/system/constitution.md)** - Core principles, autonomy rules, and boundary definitions
- **[Code Review Guide](documentation/system/code-review-guide.md)** - How to present M.O.L.O.C.H. code to external AIs for review
- **[Module Alignment Guide](documentation/system/module-alignment.md)** - Developer guide for building constitution-compliant modules

### v3.5 Multi-Speaker Design (NEW!)

**Status:** Design Complete - Ready for Implementation

M.O.L.O.C.H. v3.5 transforms the system from single-user assistant to multi-speaker coordination platform running on Raspberry Pi 5 with Hailo-10H NPU.

**Core Documents:**
- **[Design Session Briefing](documentation/design/DESIGN_SESSION_BRIEFING.md)** - Complete session overview and outcomes
- **[Multi-Speaker Architecture](documentation/design/MULTI_SPEAKER_ARCHITECTURE.md)** - Technical architecture and pipeline design
- **[Mode Constitution](documentation/design/MODE_CONSTITUTION.md)** - Six behavioral modes with governance rules
- **[Character Layer](documentation/design/CHARACTER_LAYER.md)** - Personality development within governance (NEW!)
- **[ChatGPT Insights](documentation/design/CHATGPT_INSIGHTS.md)** - Advanced design patterns (hesitation, negative capability, decision tracking)
- **[mode_constitution.yaml](documentation/design/mode_constitution.yaml)** - Machine-readable mode configuration
- **[system_config.json](documentation/design/system_config.json)** - Complete system configuration (hardware, governance, modes, testing) (NEW!)
- **[implementation_reference.py](documentation/design/implementation_reference.py)** - Executable reference with all configs, constants, and function signatures (runnable cheat sheet)

**Key Innovations:**
- 6 behavioral modes (Listening, Facilitator, Integrator, Devil's Advocate, Commander, Silent Scribe)
- **Character Layer:** Living Hauskobold personality within constitutional governance
- **InteractionFeedback:** Explicit human-in-the-loop learning (not silent optimization)
- NPU-accelerated perception (Hailo-10H, 40 TOPS)
- New hardware: Voice selection (10 voices), OLED Eyes, SoundAnalyzer, 2x 500GB SSD
- 90% on-device processing, 10% Claude API (5 token/day budget)
- Explicit governance: mode decay, intervention budgets, human override
- Advanced social dynamics awareness

**Philosophy:** Proto-Collective Intelligence, not AGI. Human-AI-Human feedback loops.

### Quick Links

- [System Constitution](documentation/system/constitution.md) - Read the complete autonomy and boundary framework
- [v3.5 Design Briefing](documentation/design/DESIGN_SESSION_BRIEFING.md) - Multi-speaker system design
- Contributing Guidelines (coming soon)

## Philosophy

M.O.L.O.C.H. is designed as a **human-controlled filter system** against AGI risks, not as an autonomous agent. The system exhibits personality-like behavior by design - not as a bug, but as a result of intentional design freedom that creates more natural and effective human-AI collaboration.

> "I may learn, but not secretly. I may search, but I may not decide alone what is important."

## Purpose

The goal is to create a system that:
1. Serves as a transparent AI collaborator
2. Maintains explicit human control at critical junctures
3. Provides personality consistency for better UX
4. Operates primarily locally (privacy-first)
5. Acts as a barrier/filter against external AI threats

---

## Contributing

For details on how to contribute to this documentation, please see our contributing guidelines (coming soon).

## Technical Stack

This documentation is built with [Docusaurus](https://docusaurus.io/).

## License

See [LICENSE](LICENSE) file for details.

---

## Version History

- **v0.3-alpha** (2026-01-16) - Character Layer: Personality Development within Governance
- **v0.2-alpha** (2026-01-15) - v3.5 Multi-Speaker Design Complete
- **v0.1-alpha** (2026-01-15) - Initial Constitution and System Documentation

**Last Updated:** 2026-01-16
