# M.O.L.O.C.H. Architecture Diagram

## System Overview

This diagram provides a visual overview of M.O.L.O.C.H.'s complete architecture, showing all major components and their relationships.

```mermaid
graph TD
    A[M.O.L.O.C.H. Core] --> B[Hardware]
    B --> B1[Raspberry Pi 5]
    B --> B2[Hailo-10H NPU]
    B --> B3[SSD Storage 500GB]
    B --> B4[Speakers & OLED Eyes]
    B --> B5[Camera Feed Studio AI]

    A --> C[Governance & Constitution]
    C --> C1[Autonomy Boundaries]
    C --> C2[No Silent Learning]
    C --> C3[Human Approval Required]
    C --> C4[Persona Rules]

    A --> D[Modes]
    D --> D1[Listening]
    D --> D2[Facilitator]
    D --> D3[Integrator]
    D --> D4[Devil's Advocate]
    D --> D5[Commander]
    D --> D6[Silent Scribe]

    A --> E[Feedback Loop]
    E --> E1[User Ratings: Good / Bad / Funny]
    E --> E2[Style Adjustment: Humor & Persona]
    E --> E3[Meta-Comments / Self-Reference]

    A --> F[Learning Modules]
    F --> F1[Audio Analysis / Music Emotion]
    F --> F2[Intent Classification]
    F --> F3[Pattern Extraction]
    F --> F4[Logging & Transparency]

    A --> G[Integration]
    G --> G1[Home Assistant Control]
    G --> G2[Multi-Room Audio]
    G --> G3[Multi-M.O.L.O.C.H. Sync (Smartphone ↔ Raspberry)]

    A --> H[API & Token Budget]
    H --> H1[Controlled API Calls Only]
    H --> H2[Token Limits & Approval]
```

---

## Component Descriptions

### Hardware Layer
- **Raspberry Pi 5**: Sovereign control plane (4GB RAM)
- **Hailo-10H NPU**: 40 TOPS accelerator for perception tasks
- **SSD Storage**: 2x 500GB (primary + backup)
- **Speakers & OLED Eyes**: Multi-room audio, visual feedback
- **Camera Feed**: Studio AI integration for visual input

### Governance & Constitution
- **Autonomy Boundaries**: Hard limits on system capabilities
- **No Silent Learning**: All learning explicit and logged
- **Human Approval Required**: API calls, learning operations
- **Persona Rules**: Allowed (humor, irony) vs Forbidden (manipulation)

### Six Behavioral Modes
1. **Listening**: Default baseline mode
2. **Facilitator**: Multi-speaker coordination
3. **Integrator**: Conflict resolution
4. **Devil's Advocate**: Consensus challenging
5. **Commander**: Emergency coordination
6. **Silent Scribe**: Transcription only

### Feedback Loop System
- **User Ratings**: Good / Bad / Funny ratings after interactions
- **Style Adjustment**: Adapt humor level, meta-commentary frequency
- **Meta-Comments**: Self-reference and system awareness

### Learning Modules
- **Audio Analysis**: Speech patterns, emotion detection
- **Music Emotion**: Mood detection from audio feeds
- **Intent Classification**: User intent parsing
- **Pattern Extraction**: Behavioral pattern recognition
- **Logging & Transparency**: All operations logged and reviewable

### Integration Points
- **Home Assistant**: Smart home monitoring and control
- **Multi-Room Audio**: Bluetooth speakers in multiple rooms
- **Multi-M.O.L.O.C.H. Sync**: Context sync between smartphone and Raspberry Pi instances

### API & Token Budget
- **Controlled API Calls**: No self-initiated external calls
- **Token Limits**: 5 tokens/day budget with human approval
- **Purpose**: Character development, humor learning, language learning

---

## Architecture Principles

### 1. Sovereignty
**Raspberry Pi 5 is the sovereign.** All decision logic runs on-device. Claude API only for language generation.

### 2. Transparency
**Every operation logged.** No silent optimization, no hidden learning.

### 3. Human Control
**Human override always available.** All modes decay, no permanent states.

### 4. Character within Governance
**Personality development allowed** but only within constitutional boundaries.

### 5. Privacy First
**90% local processing, 10% API.** All memory tagged (SOURCE, TARGET, SCOPE, CONFIDENCE).

---

## Data Flow

```
┌─────────────┐
│   AUDIO IN  │ (Microphone, Spotify, Camera)
└──────┬──────┘
       ↓
┌─────────────┐
│  HAILO NPU  │ (Speaker Diarization, Emotion, Embeddings)
└──────┬──────┘
       ↓
┌─────────────┐
│   MODE      │ (Listening, Facilitator, Integrator, etc.)
│   ENGINE    │
└──────┬──────┘
       ↓
┌─────────────┐
│  MEMORY     │ (User Private, Group Session, Global World)
└──────┬──────┘
       ↓
┌─────────────┐
│  CLAUDE API │ (10% - Language Generation Only)
└──────┬──────┘
       ↓
┌─────────────┐
│  OUTPUT     │ (Voice, OLED Eyes, LED Ring, Speakers)
└──────┬──────┘
       ↓
┌─────────────┐
│  FEEDBACK   │ (User Ratings → Style Adaptation)
└─────────────┘
       ↓
┌─────────────┐
│   LOGGING   │ (All Transparent, Reviewable)
└─────────────┘
```

---

## Implementation Phases

### Phase 1: Critical Path (Month 1)
- Mode Engine skeleton
- Boundary enforcement
- Basic feedback loops
- Hailo-10H integration

### Phase 2: Quick Wins (Month 2)
- Voice selection (10 voices)
- OLED Eyes + LED Ring
- Basic feedback logging
- NPU pipeline optimization

### Phase 3: Can Wait (Month 3+)
- Full Home Assistant integration
- Multi-room audio coordination
- Advanced music/emotion analysis
- Multi-M.O.L.O.C.H. sync

---

## Testing Strategy

### Technical Tests
- Intent parsing accuracy
- Mode transition logic
- NPU pipeline latency
- Logging completeness

### Social Tests
- Role amplification detection
- Consensus gravity measurement
- Humor score consistency
- Style adaptation effectiveness

### Integration Tests
- Multi-speaker simulation
- Fake user input testing
- Feedback loop verification
- Failure mode triggers

---

## Related Documentation

- **[system_config.json](system_config.json)** - Machine-readable configuration
- **[mode_constitution.yaml](mode_constitution.yaml)** - Mode-specific configuration
- **[MULTI_SPEAKER_ARCHITECTURE.md](MULTI_SPEAKER_ARCHITECTURE.md)** - Detailed technical architecture
- **[CHARACTER_LAYER.md](CHARACTER_LAYER.md)** - Personality development documentation
- **[implementation_reference.py](implementation_reference.py)** - Executable Python reference

---

**Version:** v0.3-alpha
**Last Updated:** 2026-01-16
**Status:** Design Complete - Implementation Ready
