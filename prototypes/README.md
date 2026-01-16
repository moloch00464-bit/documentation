# M.O.L.O.C.H. Prototypes

This directory contains early-stage prototypes and proof-of-concept implementations for M.O.L.O.C.H. components.

---

## Dashboard Prototype

**File:** `dashboard_prototype.py`

### Description

A visual transparency interface demonstrating M.O.L.O.C.H.'s core principle: **all operations are visible and auditable**.

### Features

**Left Panel:**
- **Active Mode**: Shows current behavioral mode (Listening, Facilitator, Devil's Advocate, etc.)
- **User Feedback**: Displays last user rating (👍 Witzig, 👌 Gut, 😐 Meh)
- **Learning Events**: Transparent log of all learning operations
  - Audio emotion pattern updates
  - User feedback integration
  - Persona tone adjustments
  - Intent classifier refinements
  - Context memory extensions

**Right Panel:**
- **Persona**: Current voice selection and humor level
- **Hardware Status**: SSD usage, speaker status, camera status

### Running the Prototype

```bash
python prototypes/dashboard_prototype.py
```

**Requirements:**
- Python 3.7+
- tkinter (usually included with Python)

### Screenshot

```
┌─────────────────────────────────────────────────────────┐
│   M.O.L.O.C.H. v0.1 — Transparent Autonomy Active      │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────┐              │
│ │ Active Mode     │  │ Persona         │              │
│ │  Listening      │  │  Voice: #3      │              │
│ └─────────────────┘  │  Humor: Medium  │              │
│ ┌─────────────────┐  └─────────────────┘              │
│ │ User Feedback   │  ┌─────────────────┐              │
│ │  Last: 👍 Witzig│  │ Hardware Status │              │
│ └─────────────────┘  │  SSD: 320/500GB │              │
│ ┌─────────────────┐  │  Speakers: On   │              │
│ │ Learning Events │  │  Camera: Idle   │              │
│ │ (Transparent)   │  └─────────────────┘              │
│ │ • Audio emotion │                                    │
│ │   pattern update│                                    │
│ │ • User feedback │                                    │
│ │   integrated    │                                    │
│ │ • Persona tone  │                                    │
│ │   adjusted      │                                    │
│ └─────────────────┘                                    │
└─────────────────────────────────────────────────────────┘
```

### Purpose

This prototype demonstrates:

1. **Transparency**: All learning events visible in real-time
2. **User Control**: Feedback mechanism front and center
3. **System State**: Current mode, persona, hardware status always visible
4. **Constitutional Compliance**: No hidden operations

### Design Principles

- **Dark Theme**: Reduces eye strain for long monitoring sessions
- **Left-to-Right Flow**: User sees mode → feedback → learning events
- **Real-time Updates**: 3-second refresh cycle (configurable)
- **Minimal Clutter**: Only essential information displayed

### Next Steps

**Planned Enhancements:**
- [ ] Connect to actual Mode Engine (replace mock data)
- [ ] Add mode transition history graph
- [ ] Implement user feedback input buttons
- [ ] Add API budget meter (5 tokens/day)
- [ ] Show confidence scores for mode transitions
- [ ] Add "Export Logs" button
- [ ] Integrate with Hailo NPU metrics (if available)

### Constitutional Alignment

This dashboard embodies M.O.L.O.C.H.'s core principle:

> "I may learn, but not secretly. I may search, but I may not decide alone what is important."

**Every learning operation is logged and visible.**

---

## Future Prototypes

- **Mode Transition Visualizer**: Real-time graph of mode changes
- **Feedback Annotation Tool**: UI for giving detailed feedback
- **NPU Metrics Dashboard**: Hailo-10H performance monitoring
- **Multi-M.O.L.O.C.H. Sync Demo**: Smartphone ↔ Raspberry Pi sync visualization

---

**Version:** v0.1-prototype
**Last Updated:** 2026-01-16
**Status:** Mock/Simulation (not connected to real system)
