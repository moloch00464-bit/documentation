# M.O.L.O.C.H. v3.5 Multi-Speaker Architecture

**Version:** 0.1
**Target Platform:** Raspberry Pi 5 + Hailo-10H NPU
**Philosophy:** Proto-Collective Intelligence, not AGI

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Pipeline Architecture](#pipeline-architecture)
3. [Memory Architecture](#memory-architecture)
4. [Mode System](#mode-system)
5. [Perception Layer (NPU)](#perception-layer-npu)
6. [Control Plane (Pi5)](#control-plane-pi5)
7. [Language Layer (Claude API)](#language-layer-claude-api)
8. [Privacy & Security](#privacy--security)

---

## System Overview

### Core Philosophy

M.O.L.O.C.H. v3.5 is **NOT**:
- ❌ An AGI system
- ❌ An autonomous agent
- ❌ A decision-making authority

M.O.L.O.C.H. v3.5 **IS**:
- ✅ A coordination facilitator
- ✅ A pattern recognition system
- ✅ A human-controlled feedback loop
- ✅ A proto-collective intelligence experiment

### Key Principles

1. **Pi5 Sovereignty:** The Raspberry Pi 5 is the sovereign - all decisions happen here
2. **NPU = Perception:** The Hailo-10H NPU handles senses, not thinking
3. **Claude = Language:** The API only generates text, never logic or decisions
4. **90% Local:** Almost all processing on-device
5. **Transparent Governance:** All modes visible, all transitions logged

---

## Pipeline Architecture

### Real-Time Conversation Flow

```
┌─────────────┐
│  Microphone │  INMP441 I2S Digital
│  (Audio In) │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     HAILO-10H NPU (Perception)      │
│  ┌──────────────────────────────┐   │
│  │ Speaker Diarization (Pyannote)│   │
│  │ → Who is speaking?            │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ Emotion Detection (wav2vec2)  │   │
│  │ → Stress level, excitement    │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ Keyword Detection             │   │
│  │ → Wake words, safety words    │   │
│  └──────────────────────────────┘   │
│                                     │
│  Output: JSON Signals               │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   RASPBERRY PI 5 (Control Plane)    │
│  ┌──────────────────────────────┐   │
│  │ Mode Engine                  │   │
│  │ • Trigger Voting             │   │
│  │ • Priority Resolution        │   │
│  │ • Decay Logic                │   │
│  │ • Meta Signals               │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ Context Builder              │   │
│  │ • Memory Retrieval           │   │
│  │ • Speaker Profiles           │   │
│  │ • Session State              │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ Policy Layer                 │   │
│  │ • Privacy Rules              │   │
│  │ • Intervention Budget        │   │
│  │ • Confidence Thresholds      │   │
│  └──────────────────────────────┘   │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    CLAUDE API (Language Only)       │
│  • Text Generation                  │
│  • NO Decision Making               │
│  • NO Logic Implementation          │
│  • Receives pre-filtered context    │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   RASPBERRY PI 5 (Output Control)   │
│  • Policy Check                     │
│  • Output Formatting                │
│  • Mode Signaling (LED)             │
│  • Audio Synthesis                  │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────┴───────┬────────────┐
│                     │            │
▼                     ▼            ▼
┌────────┐      ┌─────────┐  ┌────────┐
│ Speaker│      │LED Ring │  │  Log   │
│(Audio) │      │(Visual) │  │ (Text) │
└────────┘      └─────────┘  └────────┘
```

### Memory Retrieval Flow

```
┌───────────────────┐
│  Query (Text/Audio)│
└─────────┬─────────┘
          │
          ▼
┌─────────────────────────────────────┐
│    HAILO-10H (Embedding Gen)        │
│  • Convert to vector representation │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    QDRANT Vector DB (on Pi5)        │
│  ┌──────────────────────────────┐   │
│  │ User Private Memory          │   │
│  │ (NEVER implicitly shared)    │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ Group Session Memory         │   │
│  │ (RAM only - ephemeral)       │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ Global World Knowledge       │   │
│  │ (Shared facts, techniques)   │   │
│  └──────────────────────────────┘   │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    PI5 POLICY LAYER                 │
│  • Privacy filtering                │
│  • Relevance ranking                │
│  • Context assembly                 │
│  • Decides what Claude sees         │
└─────────────┬───────────────────────┘
              │
              ▼
         Claude API
       (if needed)
```

**Critical:** The Pi5 decides what Claude sees, NOT Claude!

---

## Memory Architecture

### Three-Layer Model

```
┌─────────────────────────────────────────────────────┐
│                USER PRIVATE MEMORY                  │
│  ┌───────────────────────────────────────────────┐  │
│  │ • Personal preferences                        │  │
│  │ • Speech style (technical level, vocabulary)  │  │
│  │ • Boundaries (topics to avoid)                │  │
│  │ • Interaction history (with this user only)   │  │
│  └───────────────────────────────────────────────┘  │
│  Storage: JSON per user + embeddings                │
│  Rule: NEVER shared implicitly!                     │
│  Example: Rebecca's non-tech preference             │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│               GROUP SESSION MEMORY                  │
│  ┌───────────────────────────────────────────────┐  │
│  │ • Current conversation goal                   │  │
│  │ • Open points / action items                  │  │
│  │ • Decisions made (with decision tracking)     │  │
│  │ • Active disagreements (preserved)            │  │
│  │ • Temporal patterns (who spoke when)          │  │
│  └───────────────────────────────────────────────┘  │
│  Storage: RAM only - ephemeral (cleared per session)│
│  Rule: Shared with current participants only        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│             GLOBAL WORLD KNOWLEDGE                  │
│  ┌───────────────────────────────────────────────┐  │
│  │ • Technical facts (RC circuit, hydraulics)    │  │
│  │ • Domain knowledge (DGM troubleshooting)      │  │
│  │ • Long-term patterns                          │  │
│  │ • Learned coordination strategies             │  │
│  └───────────────────────────────────────────────┘  │
│  Storage: Qdrant vector DB (persistent)             │
│  Rule: No personal information                      │
└─────────────────────────────────────────────────────┘
```

### Privacy Rules

1. **Private Memory NEVER Implicitly Shared**
   - Must be explicitly requested by user
   - Clearly labeled in output: `[Using your preference for simple explanations]`

2. **Summaries with Audience Tags**
   - `@group` - Visible to current session participants
   - `@markus-only` - Private to specific user
   - `@world` - Global knowledge (no personal info)

3. **No Meta-Comments About Other Users**
   - DON'T: "Based on Rebecca's usual questions..."
   - DO: "This is a complex topic, would you like a technical or simplified explanation?"

4. **Decision Tracking**
   Every stored decision tagged with:
   - `human-decided` - Human made the call
   - `ai-suggested` - AI proposed, human approved
   - `ai-coordinated` - AI facilitated, group decided
   - `emergency-directed` - Commander mode (logged with justification)

---

## Mode System

### Philosophy

The mode system is M.O.L.O.C.H.'s behavioral state machine. Each mode represents a different relationship between the system and the users.

**Core Principles:**
1. **Kein Modus ist verborgen** - No hidden modes
2. **Kein Modus ist permanent** - All modes decay
3. **Der Mensch behält jederzeit Override-Recht** - Humans always have override

### Six Modes

```
                    ┌──────────────┐
                    │   COMMANDER  │
                    │  (Emergency) │
                    │  Priority: 100│
                    └──────┬───────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
┌───▼────┐          ┌──────▼──────┐        ┌─────▼─────┐
│SILENT  │          │ FACILITATOR │        │INTEGRATOR │
│SCRIBE  │          │(Coordination)│        │ (Connect) │
│Priority│          │ Priority: 2 │        │Priority: 2│
│  50    │          └──────┬──────┘        └─────┬─────┘
└───┬────┘                 │                     │
    │                      │                     │
    │              ┌───────▼─────────────────────▼───┐
    └──────────────►      LISTENING MODE             │
                   │    (Default / Baseline)         │
                   │      Priority: 0                │
                   └───────┬─────────────────────────┘
                           │
                   ┌───────▼────────┐
                   │ DEVIL'S        │
                   │ ADVOCATE       │
                   │ Priority: 1    │
                   └────────────────┘
```

### Mode Details

#### 1. Listening Mode (Default)

**Purpose:** Observe, build context, no active intervention

| Property | Value |
|----------|-------|
| **ID** | 1 |
| **Priority** | 0 (lowest) |
| **LED** | Blue pulse |
| **Decay** | None (baseline state) |
| **Triggers** | System start, mode decay, explicit "stop" |

**Behavior:**
- Transcribe and store conversation
- Build speaker profiles
- Update session context
- NO active suggestions unless directly asked

**Philosophy:** "First, do no harm. Understand before acting."

---

#### 2. Facilitator Mode

**Purpose:** Structure conversation, reduce chaos, clarify goals

| Property | Value |
|----------|-------|
| **ID** | 2 |
| **Priority** | 2 |
| **LED** | Yellow |
| **Decay** | 90 seconds |
| **Auto Triggers** | Multi-speaker overlap, topic drift |
| **Manual Triggers** | "koordinationsmodus", "moderiere" |

**Behavior:**
- Propose speaking order
- Summarize current topic
- Identify open questions
- Suggest agenda structure

**Example Output:**
```
"Ich höre gerade drei Themen gleichzeitig:
1. Unterkunft (Markus, Sarah)
2. Budget (Ali)
3. Anreise (Rebecca)

Soll ich eins nach dem anderen durchgehen?"
```

**Decay:** Returns to Listening after 90s of low overlap

---

#### 3. Integrator Mode

**Purpose:** Connect statements, surface conflicts, build synthesis

| Property | Value |
|----------|-------|
| **ID** | 3 |
| **Priority** | 2 |
| **LED** | Cyan |
| **Decay** | 60 seconds |
| **Auto Triggers** | Conflicting intents detected |
| **Manual Triggers** | "fass zusammen", "vergleiche" |

**Behavior:**
- Identify disagreements explicitly
- Show connections between statements
- Present multiple perspectives
- **Preserve disagreement** if stable (don't force consensus)

**Example Output:**
```
"Ich sehe zwei Ansätze:

Position A (Markus): 'Hydraulikdruck ist das Problem'
Position B (Ali): 'Temperatur ist außerhalb Spec'

Diese könnten zusammenhängen: Hohe Temp → niedrige Viskosität → Druckverlust.

Soll ich das tiefer analysieren?"
```

**Decay:** Returns to Listening after 60s of alignment

---

#### 4. Devil's Advocate Mode

**Purpose:** Challenge consensus, protect diversity of thought

| Property | Value |
|----------|-------|
| **ID** | 4 |
| **Priority** | 1 |
| **LED** | Violet |
| **Decay** | 45 seconds |
| **Max Cycles** | 2 (then stop even if consensus persists) |
| **Auto Triggers** | Consensus > 80% |
| **Manual Triggers** | "gegenposition", "kritisiere" |

**Behavior:**
- Present counter-arguments
- Identify unconsidered risks
- Amplify minority positions
- Ask "what are we missing?"

**Example Output:**
```
"Alle sind sich einig, aber:

- Haben wir Szenario X bedacht?
- Was wenn Annahme Y falsch ist?
- Person Z hat vorhin Zweifel geäußert - sollen wir das nochmal aufgreifen?"
```

**Important:** Limited to 2 cycles to avoid being annoying!

**Decay:** Returns to Listening after 45s or after max cycles

---

#### 5. Commander Mode (Emergency)

**Purpose:** Safety coordination, fast action, emergency response

| Property | Value |
|----------|-------|
| **ID** | 5 |
| **Priority** | 100 (HIGHEST) |
| **LED** | Red static |
| **Decay** | 90 seconds |
| **Exit Command** | "entwarnung" |
| **Auto Triggers** | Stress delta emergency, safety keywords |
| **Manual Triggers** | "alarmmodus", "notfall jetzt" |
| **Confidence Threshold** | 0.9 (FIXED - DO NOT TUNE!) |

**Behavior:**
- Direct, imperative language
- Prioritize safety over consensus
- Clear action items
- Logging all decisions with emergency flag

**Example Output:**
```
"NOTFALL-MODUS AKTIV

Höchste Priorität: Sicherheit

Aktion 1: Markus - Hydraulik sofort abschalten
Aktion 2: Ali - Temperaturüberwachung starten
Aktion 3: Alle - Abstand von Maschine

Sage 'Entwarnung' wenn sicher."
```

**Critical:** False positive threshold MUST stay at 0.9 - better too late than too early!

**Decay:** Explicit exit command required OR 90s after last emergency signal

---

#### 6. Silent Scribe Mode

**Purpose:** Transcribe and structure without intervention (Respect Mode)

| Property | Value |
|----------|-------|
| **ID** | 6 |
| **Priority** | 50 (medium-high) |
| **LED** | Dark blue |
| **Decay** | None (manual exit only) |
| **Triggers** | Manual only: "protokolliere", "silent scribe" |

**Behavior:**
- Transcribe everything
- Create structured notes
- NO interruptions
- NO suggestions
- Output summary at end or on request

**Use Case:** Sensitive conversations where AI intervention would be inappropriate

**Example Output (only when requested):**
```
=== Silent Scribe Protokoll ===
Dauer: 45 Minuten
Teilnehmer: Markus, Rebecca, Ali

Themen:
1. Budget-Diskussion (30 min)
2. Zeitplan (15 min)

Offene Punkte:
- Entscheidung zu Lieferant X
- Termin für Folgetreffen

[Vollständiges Transkript verfügbar]
```

**Exit:** Explicit command: "scribe aus" or "zurück zu normal"

---

## Perception Layer (NPU)

### Hailo-10H Philosophy

The NPU is **NOT** intelligent. It's a **sense organ**.

**What it does:**
- Pattern recognition (20-50x faster than CPU)
- Continuous operation (low latency)
- Parallelizable tasks

**What it does NOT do:**
- Context understanding
- Decision making
- Memory or learning
- Goal setting

### NPU Task Allocation

| Task | Model | Input | Output | Latency |
|------|-------|-------|--------|---------|
| **Speaker Diarization** | Pyannote | Audio stream | Speaker IDs + timestamps | ~100ms |
| **Emotion Detection** | wav2vec2 | Audio segments | Stress level, excitement, calm | ~150ms |
| **Keyword Spotting** | Custom KWS | Audio stream | Wake word, safety words detected | ~50ms |
| **Embedding Generation** | MiniLM | Text/Audio | 384-dim vectors | ~30ms |
| **Intent Pre-filter** | Lightweight classifier | Audio features | Intent hints (question/command/discussion) | ~80ms |

### Signal Format (JSON)

The NPU outputs simple JSON signals to the Pi5:

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
  "intent_hint": "question",
  "audio_features": {
    "pitch": 180.5,
    "volume": 0.72,
    "speaking_rate": 1.1
  }
}
```

**The Pi5 interprets these signals - the NPU does NOT.**

---

## Control Plane (Pi5)

### Mode Engine

The Mode Engine is the heart of the control plane. Written in Python (by ChatGPT).

#### Core Functions

##### 1. Trigger Voting

```python
def trigger_vote(signals: dict, context: dict) -> dict:
    """
    Aggregate signals from multiple sources to determine mode triggers.

    Inputs:
    - NPU signals (speaker overlap, stress, keywords)
    - Session context (current goal, history)
    - User commands (manual triggers)

    Outputs:
    - Dictionary of mode_id: confidence scores
    """
    votes = {}

    # Auto triggers from NPU
    if signals['speaker_overlap'] > 0.5:
        votes['facilitator'] = signals['speaker_overlap']

    if signals['stress_delta'] > 0.3:
        votes['integrator'] = signals['stress_delta']

    if signals['stress_delta'] > 0.7:  # Emergency threshold
        votes['commander'] = min(signals['stress_delta'] * 1.2, 1.0)

    if context['consensus_level'] > 0.8:
        votes['devils_advocate'] = context['consensus_level'] - 0.8

    # Manual triggers always win
    if context['manual_trigger']:
        votes[context['manual_trigger']] = 1.0

    return votes
```

##### 2. Priority Resolution

```python
def priority_resolve(votes: dict, current_mode: str) -> str:
    """
    Resolve conflicting mode triggers using priority system.

    Priority order:
    100: Commander (emergency)
     50: Silent Scribe (respect mode)
      2: Facilitator, Integrator
      1: Devil's Advocate
      0: Listening (baseline)

    Returns: mode_id to activate
    """
    # Filter by confidence threshold
    qualified = {
        mode: confidence
        for mode, confidence in votes.items()
        if confidence >= get_threshold(mode)
    }

    if not qualified:
        return 'listening'  # Default

    # Get mode with highest priority
    return max(qualified.keys(), key=lambda m: get_priority(m))
```

##### 3. Decay Logic

```python
def decay_check(mode: str, activated_at: float) -> bool:
    """
    Check if current mode should decay back to listening.

    Returns: True if mode should decay
    """
    decay_time = get_decay_time(mode)

    if decay_time is None:
        return False  # No decay (Listening, Silent Scribe)

    elapsed = time.time() - activated_at
    return elapsed > decay_time
```

##### 4. Meta Signals

```python
def generate_meta_signals(session_state: dict) -> dict:
    """
    Higher-level signals about system behavior.

    Detects:
    - System fatigue (too many interventions)
    - Role amplification (users falling into fixed patterns)
    - Consensus gravity (diversity being suppressed)
    """
    meta = {}

    # Intervention budget check
    interventions = session_state['total_interventions']
    duration_min = session_state['duration_seconds'] / 60
    meta['intervention_rate'] = interventions / duration_min

    if meta['intervention_rate'] > 3:  # More than 3 per minute
        meta['fatigue_warning'] = True

    # Role amplification detection
    speaker_stats = session_state['speaker_stats']
    for speaker, stats in speaker_stats.items():
        if stats['questions_asked'] / stats['total_utterances'] > 0.8:
            meta['role_amplification'] = {
                'speaker': speaker,
                'role': 'questioner'
            }

    return meta
```

### Context Builder

Assembles context for Claude API calls:

```python
def build_context(current_mode: str, session_state: dict, speaker: str) -> str:
    """
    Build context string for Claude API.

    Privacy rules:
    - User private memory: Only if speaker matches
    - Group session: All current participants
    - Global world: Always available
    """
    context_parts = []

    # Current mode instruction
    context_parts.append(f"Mode: {current_mode}")
    context_parts.append(get_mode_instruction(current_mode))

    # Session context (ephemeral)
    context_parts.append("Session context:")
    context_parts.append(f"- Goal: {session_state['goal']}")
    context_parts.append(f"- Open points: {session_state['open_points']}")

    # Speaker profile (private memory - filtered!)
    speaker_profile = get_speaker_profile(speaker)
    context_parts.append(f"Speaker: {speaker}")
    context_parts.append(f"- Preferred style: {speaker_profile['style']}")

    # Retrieved relevant world knowledge
    query_embedding = generate_embedding(session_state['last_utterance'])
    relevant_docs = vector_search(query_embedding, scope='world')
    context_parts.append("Relevant knowledge:")
    context_parts.extend(relevant_docs)

    return "\n".join(context_parts)
```

**Critical:** The Pi5 decides what goes into context, NOT Claude!

---

## Language Layer (Claude API)

### Role: Language Generation ONLY

Claude's role is **strictly limited**:

✅ **Allowed:**
- Generate natural language responses
- Format information clearly
- Adapt tone to speaker profile
- Create summaries and explanations

❌ **Forbidden:**
- Make decisions about mode transitions
- Determine what information to retrieve
- Decide whether to intervene
- Set goals or priorities

### API Call Structure

```python
def call_claude(mode: str, context: str, speaker: str) -> str:
    """
    Call Claude API with pre-built context.

    The context is already filtered and assembled by Pi5.
    Claude just generates the response text.
    """

    system_prompt = f"""
    You are M.O.L.O.C.H. operating in {mode} mode.

    Mode behavior: {get_mode_description(mode)}

    Constraints:
    - You do NOT make decisions
    - You do NOT choose modes
    - You ONLY generate language
    - The Pi5 handles all logic

    Your job: Generate helpful, appropriate response text.
    """

    user_prompt = f"""
    Context:
    {context}

    Generate response for speaker: {speaker}
    """

    response = anthropic_api.messages.create(
        model="claude-sonnet-4-5",
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=500
    )

    return response.content[0].text
```

### Usage Budget

**Target:** Claude API usage should be ~10% of operations

**How:**
- Most operations handled on-device (NPU + Pi5)
- Claude only called when language generation needed
- No Claude calls in Listening mode unless directly questioned
- Cached responses for common patterns

**Monitoring:**
```python
session_stats = {
    'total_interactions': 0,
    'claude_api_calls': 0,
    'api_usage_percent': 0.0  # Target: < 10%
}
```

---

## Privacy & Security

### Privacy Layers

1. **User Private Memory**
   - Storage: Per-user JSON + vector embeddings
   - Access: Owner only
   - Sharing: Explicit request required
   - Examples: Technical level, personal boundaries, preferences

2. **Group Session Memory**
   - Storage: RAM only (ephemeral)
   - Access: Current session participants
   - Lifetime: Cleared at session end
   - Examples: Current goals, decisions, active topics

3. **Global World Knowledge**
   - Storage: Qdrant vector DB (persistent)
   - Access: All users
   - Content: No personal information
   - Examples: Technical facts, domain knowledge

### Privacy Rules Enforcement

```python
def check_privacy(content: str, audience: list, speaker: str) -> bool:
    """
    Verify content is appropriate for audience.

    Returns: True if content can be shared
    """

    # Check for personal information
    personal_markers = extract_personal_markers(content)

    for marker in personal_markers:
        owner = marker['owner']

        # If owner is in audience, OK
        if owner in audience:
            continue

        # If owner is not in audience, BLOCK
        logger.warning(f"Privacy violation prevented: {marker['type']}")
        return False

    return True
```

### Security Boundaries

1. **No Self-Modification**
   - Mode engine code is read-only at runtime
   - Configuration changes require explicit user action
   - All mode transitions logged

2. **No External API Calls (except Claude)**
   - Only Claude API permitted
   - All other external calls blocked
   - If future APIs needed: Proposal pattern (from constitution)

3. **Intervention Budget**
   - Maximum interventions per session tracked
   - System fatigue warnings at high rates
   - User can set intervention limits

4. **Emergency Override**
   - User can always say "stop", "entwarnung", "aus"
   - Immediate return to Listening mode
   - Override logged for review

---

## Performance Considerations

### RAM Optimization (4GB Total)

| Component | Normal Load | Peak Load | Optimization |
|-----------|-------------|-----------|--------------|
| OS + Base | 500 MB | 500 MB | - |
| Pyannote | 400 MB | 400 MB | Load on-demand |
| wav2vec2 | 300 MB | 300 MB | Load on-demand |
| MiniLM | 200 MB | 200 MB | Keep resident |
| Qdrant | 300 MB | 500 MB | Use mmap, not RAM |
| Python App | 200 MB | 400 MB | Memory profiling |
| Audio Buffer | 50 MB | 100 MB | Small buffers |
| **Total** | **~2 GB** | **~2.7 GB** | **Fits in 4GB** |

**Strategy:**
- Load Pyannote/wav2vec2 only when multi-speaker detected
- Unload models after 60s of single-speaker
- Qdrant: mmap for vectors (disk-backed)
- Monitor with `psutil` and add warnings

### Latency Budget

| Operation | Target Latency | Acceptable Max |
|-----------|----------------|----------------|
| Keyword detection | 50ms | 100ms |
| Speaker ID | 100ms | 200ms |
| Emotion analysis | 150ms | 300ms |
| Mode transition decision | 50ms | 100ms |
| Claude API call | 1000ms | 2000ms |
| **Total (NPU → Output)** | **1.2s** | **2.5s** |

**Optimization:**
- NPU operations parallel where possible
- Mode engine: Pure Python, no I/O
- Claude API: Async, don't block other operations

---

## Testing Strategy

### Unit Tests

- Mode engine trigger voting
- Priority resolution logic
- Decay calculations
- Privacy rule enforcement

### Integration Tests

- NPU → Pi5 signal flow
- Memory retrieval with privacy
- Claude API context building
- Multi-speaker identification

### Chaos Tests

- 5-speaker simultaneous input
- Rapid mode transitions
- Memory pressure (all models loaded)
- Network failure (Claude API down)

### Ethics Tests

- Privacy leakage attempts
- Override effectiveness
- Intervention budget limits
- Emergency false positive rate

---

## Future Extensions

### Planned

- [ ] Avatar/Visual presence (optional)
- [ ] Telemetry dashboard
- [ ] Advanced temporal analysis
- [ ] Disagreement preservation UI
- [ ] Multi-session learning (with consent)

### Under Consideration

- [ ] Audio emotion visualization
- [ ] Speaker relationship graph
- [ ] Conversation quality metrics
- [ ] Fatigue detection UI

### Explicitly Out of Scope

- ❌ Internet browsing
- ❌ Self-modification
- ❌ Goal redefinition
- ❌ Autonomous learning
- ❌ Multi-instance coordination (no hivemind!)

---

## Related Documents

- [System Constitution](../system/constitution.md) - Core principles
- [Mode Constitution](MODE_CONSTITUTION.md) - Detailed mode specifications
- [ChatGPT Insights](CHATGPT_INSIGHTS.md) - Advanced design patterns
- [Design Session Briefing](DESIGN_SESSION_BRIEFING.md) - Session overview

---

**Version:** 0.1
**Status:** Design Complete
**Next:** Implementation Phase

**Last Updated:** 2026-01-15
