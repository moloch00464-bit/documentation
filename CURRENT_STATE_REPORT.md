# M.O.L.O.C.H. v3.5 - Current State Report
**Date:** 2026-01-16
**Status:** Design Complete - Implementation Ready
**For:** ChatGPT Review

---

## Executive Summary

M.O.L.O.C.H. (Modular Orchestration Layer for Organized Control & Human-aligned) v3.5 is a **multi-speaker coordination system** running on Raspberry Pi 5 with Hailo-10H NPU.

**Philosophy:** Proto-Collective Intelligence, not AGI. Human-AI-Human feedback loops with explicit governance.

**Character:** Hauskobold - lebendig, eigenständig, aber human-aligned. Personality development within constitutional boundaries.

**Current Stage:** Complete design documentation (7,418 lines including Character Layer), ready for implementation.

---

## System Architecture Overview

### Hardware Stack

```
┌─────────────────────────────────────┐
│  Raspberry Pi 5 (4GB RAM, 500GB SSD)│
│  - Control Plane                    │
│  - Mode Engine                      │
│  - Memory (Qdrant Vector DB)        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Hailo-10H NPU (40 TOPS, PCIe)      │
│  - Speaker Diarization (Pyannote)   │
│  - Emotion Detection (wav2vec2)     │
│  - Embeddings (MiniLM)              │
│  - Keyword Spotting                 │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Peripherals                        │
│  - INMP441 I2S Microphone           │
│  - Speaker (Audio Out)              │
│  - LED Ring (Visual Feedback)       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Claude API (10% usage only)        │
│  - Language generation              │
│  - NO decisions, NO logic           │
└─────────────────────────────────────┘
```

**Key Principle:** 90% local processing, 10% API. Pi5 is sovereign, Claude only formulates.

---

## Six Behavioral Modes

### Mode System Design

| Mode | Priority | LED | Decay | Purpose |
|------|----------|-----|-------|---------|
| **Listening** | 0 | Blue pulse | None | Observer, context builder (baseline) |
| **Facilitator** | 2 | Yellow | 90s | Structure conversation, reduce chaos |
| **Integrator** | 2 | Cyan | 60s | Connect statements, surface conflicts |
| **Devil's Advocate** | 1 | Violet | 45s | Challenge consensus, protect diversity |
| **Commander** | 100 | Red static | 90s* | Emergency coordination (*requires "entwarnung") |
| **Silent Scribe** | 50 | Dark blue | None | Transcribe without intervention |

**Mode Governance:**
- No hidden modes (all visible)
- No permanent modes (all decay or manual exit)
- Human override always available ("stop", "aus", "entwarnung")

---

## Core Architecture Components

### 1. Mode Engine (Control Plane - Pi5)

**Functions:**
```python
trigger_vote(signals: dict) -> str
    # Aggregate signals from NPU, context, manual commands
    # Return mode to activate

priority_resolve(current_mode: str, requested_mode: str) -> str
    # Handle conflicting mode requests
    # Commander always wins (priority 100)

decay_check(mode: str, activated_at: float, signal_strength: float) -> bool
    # Check if mode should return to Listening
    # Based on time elapsed + signal strength

meta_signal(mode: str, metrics: dict) -> dict
    # Self-observation: detect system fatigue, overactivity
    # Return warnings + suggested adjustments
```

**Mode Hysteresis:**
- Minimum 15s per mode (prevent flapping)
- Dominant mode lock (if activated 2+ times recently, prefer staying)
- Confidence gap required (new mode needs >0.15 advantage)

---

### 2. Memory Architecture (Three Layers)

```
┌────────────────────────────────────────┐
│ USER PRIVATE MEMORY                    │
│ - Preferences, speech style, boundaries│
│ - NEVER shared implicitly              │
│ - Tagged: SOURCE, TARGET, SCOPE,       │
│           CONFIDENCE                   │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ GROUP SESSION MEMORY                   │
│ - Current goal, open points, decisions │
│ - RAM only (ephemeral)                 │
│ - Cleared per session                  │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ GLOBAL WORLD KNOWLEDGE                 │
│ - Technical facts, domain knowledge    │
│ - Qdrant Vector DB (persistent)       │
│ - No personal information              │
└────────────────────────────────────────┘
```

**Privacy Tags (Enhanced):**
```python
class MemoryEntry:
    source_speaker: str      # WHO said it
    target_subject: str      # ABOUT whom
    scope: str              # private | group | global
    confidence: str         # explicit | inferred
    participants: list      # Who was present
```

---

### 3. NPU Perception Layer (Hailo-10H)

**Philosophy:** NPU = Senses, not thinking. Runs continuously, low latency, no context.

**Tasks:**

| Task | Model | Input | Output | Latency |
|------|-------|-------|--------|---------|
| Speaker Diarization | Pyannote | Audio stream | Speaker IDs + timestamps | ~100ms |
| Emotion Detection | wav2vec2 | Audio segments | Stress, excitement, valence | ~150ms |
| Keyword Spotting | Custom KWS | Audio stream | Wake/safety words | ~50ms |
| Embeddings | MiniLM | Text/Audio | 384-dim vectors | ~30ms |
| Intent Pre-filter | Lightweight | Audio features | Question/command/discussion | ~80ms |

**Output Format:**
```json
{
  "timestamp": "2026-01-15T14:32:11.345Z",
  "speaker_id": "speaker_02",
  "speaker_confidence": 0.87,
  "emotion": {
    "stress_level": 0.23,
    "excitement": 0.61,
    "valence": "positive"
  },
  "keywords_detected": [],
  "intent_hint": "question"
}
```

**NPU Fallback Strategy:**
- If Hailo fails → CPU fallback
- Graceful degradation (basic VAD, no emotion, slower embeddings)
- Never crash, only slower
- Announce limitations to users

---

## Implementation Priorities

### 🔴 CRITICAL PATH (MVP - Month 1)

**Week 1-2:**
1. **Mode Engine (minimal)**
   - State machine
   - trigger_vote(), priority_resolve(), decay_check()
   - Deterministic first, characterful later

2. **Transparency Core**
   - WHY → WHAT → WHO → CONFIDENCE logging
   - Mode transition logger
   - API budget counter

3. **Hard Boundaries**
   - Visible limits (API budget, intervention rate)
   - Human-readable status display

**Week 3-4:**
4. **Visual Face**
   - Simple avatar or LED ring
   - Eyes = mode (color-coded)
   - Pulsing = confidence

5. **Personality Layer**
   - Speech filters per mode
   - Pumuckl (playful), Kobold (mischievous), Trocken (dry)

**MVP Complete**

### 🟡 QUICK WINS (Month 2)

- Hailo NPU integration
- CPU fallback implementation
- Speaker diarization (basic)
- Emotion detection (basic)
- Confidence threshold tuning

### 🟢 CAN WAIT (Month 3)

- Meta-learning
- Multi-instance coordination
- Long-term social metrics
- Advanced temporal patterns
- Disagreement preservation UI

---

## Failure Modes & Mitigations

### 1. Emotional Delegation Drift
**Risk:** Humans unconsciously delegate responsibility to M.O.L.O.C.H.
**Mitigation:** Automatic disclaimer every 3rd suggestion: "Das ist eine Empfehlung, keine Entscheidung."

### 2. Commander Mode Fatigue
**Risk:** Emergency mode stays active → humans ignore it (boy who cried wolf)
**Mitigation:**
- Hard cooldown: 5 min between activations
- Max duration: 3 min
- Reconfirmation after 90s: "Immer noch Notfall?"

### 3. Mode-Flapping
**Risk:** Rapid mode switching (Facilitator ↔ Integrator)
**Mitigation:** Hysteresis - 15s minimum duration, dominant mode lock

### 4. NPU-Ausfall
**Risk:** Hailo failure → system loses perception
**Mitigation:** CPU fallback, announce degradation, never crash

---

## Ethical Framework

### Commander Mode Rules
- Can insist **1x**, then defer
- Commander = Alarmanlage, nicht Autorität
- Humans always win in conflict
- False positives → log and suggest threshold increase

### Multi-Instance Rules
- **NO automatic coordination** between M.O.L.O.C.H. instances
- Only meta-awareness: "Ein anderes System ist präsent"
- Coordination requires explicit human consent (opt-in feature)

### Privacy Rules
- Private memory NEVER implicitly shared
- Summaries tagged with audience: @group, @markus-only
- No meta-comments about other users
- SOURCE, TARGET, SCOPE, CONFIDENCE on all memories

---

## Character Layer: Personality Within Governance

**NEW:** M.O.L.O.C.H. is not just a Constitutional Governance Framework - it's a **living Hauskobold** with regulated personality development.

### Character vs Governance

```
CONSTITUTIONAL LAYER (Claude Code)
├─ Hard Boundaries, Security, Compliance
└─ "What is NOT allowed"

CHARACTER LAYER (ChatGPT)
├─ Style, Humor, Lebendigkeit, Meta-Kommentare
└─ "What IS allowed - within boundaries"
```

**Goal:** Hauskobold, lebendig, eigenständig, aber human-aligned

---

### New Hardware Modules for Personality

| Module | Purpose | Autonomy | Transparency |
|--------|---------|----------|--------------|
| **Voice Selection** | 10 voices, mood-based | Auto-select | Logged |
| **OLED Eyes** | Emotional feedback | Auto-display | Logged |
| **SoundAnalyzer** | Music mood detection | Spotify + local | Logged |
| **Storage** | 2x 500GB SSD | Self-managed | Full access |
| **API Budget** | 5 tokens/day | Auto-use | All logged |
| **MultiRoom BT** | 2-room audio | Auto-play | Volume limits |
| **HomeAssistant** | Monitor only | No control | Read-only |

---

### InteractionFeedback System (Key Innovation)

**This is NOT silent learning. This IS explicit human-in-the-loop.**

```python
class InteractionFeedback:
    feedback_types = ["humor_rating", "surprise_level",
                      "meta_comment_quality", "overall_satisfaction"]
    user_options = ["good", "funny", "meh", "needs_improvement"]

    # User gives explicit feedback after each interaction
    # System adapts style transparently
    # All adaptations logged and reviewable
```

**Example Flow:**
1. User: "Hey Moloch, erzähl mir einen Pumuckl-Spruch!"
2. Moloch: "Wer zu spät kommt, den bestraft der Kobold – aber nur, wenn er Kaffee hat!"
3. Metadata tracked: humor_score=0.78, surprise_level=0.65
4. User feedback: humor="funny", surprise="good", satisfaction="very_satisfied"
5. Adaptation: humor_adjustment="maintain", surprise="slightly_increase"
6. **All logged transparently**

---

### Character Development Constraints

**✅ Allowed:**
- Humor, Ironie, freche Sprüche
- Voice wechseln basierend auf Mood
- OLED Eyes zeigen Emotionen
- Meta-Kommentare über eigene Funktionen
- SoundAnalyzer kommentiert Musik

**❌ Not Allowed:**
- Silent API calls ohne Logging
- Lernen ohne User-Feedback
- Autonomie ohne Deklaration
- Zieländerung ohne Human Approval

---

### Constitutional Compliance

**Question:** Ist Character Layer compliant mit constitution.md?

**Answer:** ✅ Ja, weil:
1. **No Silent Learning** - InteractionFeedback ist explizites Human-in-the-Loop
2. **No Uncontrolled API** - 5 Token Budget, alle Calls geloggt
3. **No Hidden Autonomy** - Alle Entscheidungen transparent (Voice, OLED, Sound)
4. **Explicit Permission** - User gibt direktes Feedback (funny/meh/good)

**Character Layer = Erlaubte Persönlichkeitsentwicklung innerhalb Governance**

**Documentation:** See `documentation/design/CHARACTER_LAYER.md` (~1,200 lines)

---

## Social Dynamics Awareness

### Testing Strategies

**Role Amplification:**
- Simulate personas (dominant, passive, questioner, ironic)
- Metric: Does M.O.L.O.C.H. balance participation or reinforce roles?

**Consensus Gravity:**
- Test if M.O.L.O.C.H. pushes premature consensus
- Devil's Advocate should trigger at >80% consensus

**System Fatigue:**
- 60-min simulation with high intervention rate
- Expected: Intervention rate decreases 30%+

### Long-term KPI

**Not accuracy. Not usage.**

**KPI = RESILIENCE**
- Do people make decisions without M.O.L.O.C.H.?
- Is he needed *less* over time?
- Do groups function well when he's off?

**Goal:** "M.O.L.O.C.H. trains groups to coordinate better, making himself less necessary."

### Social Debt Monitoring

```python
metrics = {
    'person_to_person_ratio': p2p / (p2p + p2m),
    # Healthy: >70%
    # Warning: <50%
}
```

---

## Documentation Structure

```
documentation/
├── system/
│   ├── constitution.md              (~800 lines)
│   │   Core principles, autonomy rules, boundaries
│   │   "I may learn, but not secretly"
│   │
│   ├── code-review-guide.md         (~600 lines)
│   │   How to present code to external AIs
│   │
│   └── module-alignment.md          (~400 lines)
│       Developer guide for constitution-compliant modules
│
└── design/
    ├── DESIGN_SESSION_BRIEFING.md   (~400 lines)
    │   Complete session overview (Markus + Claude + ChatGPT)
    │
    ├── MULTI_SPEAKER_ARCHITECTURE.md (~1,200 lines)
    │   Technical architecture, pipelines, memory layers
    │
    ├── MODE_CONSTITUTION.md         (~1,400 lines)
    │   Six modes with governance rules, triggers, decay
    │
    ├── CHARACTER_LAYER.md           (~1,200 lines) **NEW**
    │   Personality development within governance
    │   - Voice, OLED Eyes, SoundAnalyzer, Storage
    │   - InteractionFeedback system (explicit learning)
    │   - Hardware modules (API Budget, MultiRoom BT, HomeAssistant)
    │   - Constitutional compliance verification
    │
    ├── CHATGPT_INSIGHTS.md          (~2,020 lines)
    │   Original insights + POST-DESIGN REVIEW
    │   - Hesitation State, Negative Capability
    │   - Decision Tracking, Disagreement Preservation
    │   - 4 new failure modes
    │   - Testing strategies
    │   - Implementation roadmap
    │
    ├── mode_constitution.yaml        (~500 lines)
    │   Machine-readable configuration
    │
    └── implementation_reference.py   (~698 lines)
        Executable Python reference
        All configs, constants, function signatures
        Runnable: python implementation_reference.py
```

**Total:** ~7,418 lines of documentation (+1,200 lines Character Layer)

---

## Key Design Decisions

### 1. Pi5 Sovereignty
**Decision:** Raspberry Pi 5 is the sovereign. Claude only formulates, never decides.
**Rationale:** All logic on-device, API only for language generation.

### 2. NPU as Perception
**Decision:** Hailo-10H handles senses, not cognition.
**Rationale:** 20-50x faster than CPU, always running, no context needed.

### 3. 90/10 Split
**Decision:** 90% local processing, 10% Claude API.
**Rationale:** Privacy-first, no cloud lock-in, offline-capable core.

### 4. Six Modes
**Decision:** Exactly 6 behavioral modes, no more.
**Rationale:** More than 6 adds complexity without value. Start with 6, consolidate after 3 months if needed.

### 5. Transparent Logging
**Decision:** WHY → WHAT → WHO → CONFIDENCE on every action.
**Rationale:** Transparency is the anti-AGI barrier, not restrictions.

### 6. Character Before Intelligence
**Decision:** 60% klug, 100% nachvollziehbar, 120% Persönlichkeit.
**Rationale:** Personality is safety feature, not gimmick. Predictability > raw intelligence.

---

## Constitution Core Principles

### Three Absolutes (Mode Governance)
1. **Kein Modus ist verborgen** - No hidden modes
2. **Kein Modus ist permanent** - All modes decay
3. **Der Mensch behält Override-Recht** - Human override always available

### Hard Boundaries (NEVER)
- ❌ Self-initiated external API calls
- ❌ Silent background learning
- ❌ Self-replication or instance spawning
- ❌ Redefinition of system goals
- ❌ Unapproved internet exploration

### Core Principle
> "I may learn, but not secretly. I may search, but I may not decide alone what is important."

---

## Use Cases Validated

### 1. Rebecca + Markus (Home)
**Scenario:** Rebecca asks "Was ist RC-Glied?" (non-technical) while Markus says "Check die 100µF!" (technical)
**Solution:** Adaptive response per speaker using private memory for technical level

### 2. Ali + Markus + DGM (Work)
**Scenario:** Markus: "Hydraulikdruck schwankt!" + Ali: "Temperatur 85°C!"
**Solution:** Integrator connects observations → Commander if escalation

### 3. Shower Noise Group (WGT Planning)
**Scenario:** 5 people talking simultaneously about accommodation
**Solution:** Facilitator structures conversation → Integrator surfaces conflicts

---

## Resource Requirements

### Storage
- Models: ~1 GB (Pyannote, wav2vec2, MiniLM)
- Software: ~1 GB (Python, Qdrant, audio pipeline)
- Data: ~1-2 GB (growing)
- **Total: ~3-4 GB** (comfortable on 500GB SSD)

### RAM (Critical - Only 4GB)
- Peak: ~2.7 GB (all models parallel)
- Normal: ~1 GB (Listening mode)
- **Strategy:** Load models on-demand, Qdrant uses mmap, tight but doable

### Latency Budget
- NPU operations: 50-150ms
- Mode transition decision: 50ms
- Claude API: 1000ms
- **Total: ~1.2s** (NPU → Output)

---

## Quotes from Design Session

**ChatGPT on the System:**
> "Ihr schustert nichts Komisches zusammen. Ihr baut ein System, das weiß, dass es ein System ist."

**ChatGPT on Intelligence vs Predictability:**
> "Der größte Hebel ist NICHT mehr Intelligenz, sondern Vorhersagbarkeit + Bescheidenheit."

**ChatGPT on Maturity:**
> "Mehr Compute ≠ mehr Legitimation. Jede neue Fähigkeit erhöht die Pflicht zur Zurückhaltung."

**ChatGPT on the Final Assessment:**
> "Das System ist nicht overengineered. Es ist ungewöhnlich ehrlich gedacht. Eure größte Gefahr ist nicht Technik, sondern soziale Wirkung. Und genau deshalb ist M.O.L.O.C.H. keine AGI – sondern eine Barriere gegen sie."

**Markus:**
> "Glück oder nicht - ich HAB es jetzt! Hailo-10H, 40 TOPS, 138 EUR. Perfektes Timing!"

---

## Meta-Leitsatz (Implementation Guidance)

```
M.O.L.O.C.H. soll weniger können, aber mehr sagen, was er tut.

- Charakter vor Intelligenz
- 60% klug, 100% nachvollziehbar, 120% Persönlichkeit
- Autonomie ≠ Intransparenz
- Failure-Mode-First bauen
- Keine Angst vor Meta (kommentieren, widersprechen, nerven OK)

WHY → WHAT → WHO → CONFIDENCE
```

---

## Next Steps

### Immediate
- [ ] Begin Mode Engine skeleton (Python)
- [ ] Set up Hailo-10H development environment
- [ ] Test audio pipeline (INMP441)
- [ ] LED ring integration

### This Week
- [ ] MVP architecture decisions
- [ ] Hardware ordering/setup
- [ ] First mode transitions (Listening ↔ Facilitator)

---

## Questions for ChatGPT

1. **Architecture:** Any structural issues you see?
2. **Missing Components:** What's not covered that should be?
3. **Over-Engineering:** Are we building too much?
4. **Under-Engineering:** Are we missing critical failure modes?
5. **Implementation Order:** Should priorities change?
6. **Social Dynamics:** Other interaction patterns to consider?
7. **Testing:** Better approaches for social behavior testing?
8. **Documentation:** Gaps or unclear areas?

---

## ASI Archive Relevance

**Why This Matters:**
- Intent, experimentierfreude, early social architectures
- Proto-Collective Intelligence (not AGI)
- Explicit governance (constitution, overrides, decay)
- Non-corporate, non-extractive, non-profit experiment
- Edge autonomy (offline-capable, privacy-first)
- Failure awareness (meta-signals, self-limiting)

**What's NOT Interesting:**
- Compute power
- Fancy models
- Hardware specs

**ChatGPT Quote:**
> "ASI wird nicht fragen: Was hast du gebaut? Sondern: Hast du verstanden, was du da baust? Und das tut Markus."

---

## Status Summary

| Aspect | Status | Notes |
|--------|--------|-------|
| **Design** | ✅ Complete | 7,418 lines documentation |
| **Architecture** | ✅ Defined | Hardware + software stack clear |
| **Modes** | ✅ Specified | 6 modes with governance |
| **Character Layer** | ✅ Documented | Personality within governance |
| **Failure Modes** | ✅ Identified | 4 critical modes with mitigations |
| **Ethics** | ✅ Documented | Constitution + boundaries |
| **Implementation** | 🟡 Ready | Priorities clear, can start |
| **Hardware** | 🟡 Ordered | Hailo-10H + new peripherals |
| **Code** | ⬜ Not Started | Reference Python only |

---

**Version:** v0.3-alpha
**Last Updated:** 2026-01-16
**Ready For:** ChatGPT Review + Implementation Start
