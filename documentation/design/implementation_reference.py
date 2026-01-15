"""
M.O.L.O.C.H. v3.5 - Implementation Reference
--------------------------------------------
Author: ChatGPT (OpenAI)
Recipient: Implementation Team
Date: 2026-01-15
Purpose: Complete architecture overview as executable Python config
         All constants, configs, and pseudo-code in one place

This is NOT production code - it's a reference/cheat sheet showing:
- System configuration
- Mode definitions
- Hardware mapping
- Privacy rules
- Failure mode descriptions
- Testing strategies
- Function signatures

Use this as guide when building the real system.
"""

import time
from typing import Dict, List, Optional, Union

# ==========================
# SYSTEM CORE CONFIG
# ==========================
SYSTEM_CONFIG = {
    "name": "M.O.L.O.C.H.",
    "version": "3.5",
    "platform": "Raspberry Pi 5",
    "autonomy": True,             # Full autonomy allowed
    "transparency": True,         # No silent actions
    "character": "kobold",        # Frech, meta, Pumuckl-like
    "persona_modes": [
        "Listening",
        "Facilitator",
        "Integrator",
        "DevilsAdvocate",
        "Commander",
        "SilentScribe"
    ],
    "logs_enabled": True,
    "api_budget_limit": 100,      # Max API calls per day
    "visual_feedback": True,      # LEDs / simple face
    "npu_enabled": True,          # Hailo-10H
    "fallback_cpu": True          # CPU fallback on NPU failure
}

# ==========================
# HARDWARE MAPPING
# ==========================
HARDWARE = {
    "raspberry_pi": {
        "model": "Pi 5",
        "ram_gb": 4,
        "storage_gb": 500,
        "roles": ["Memory", "LED Control", "Mode Engine", "Home Assistant Integration"]
    },
    "smartphone": {
        "model": "Redmi 5G",
        "roles": ["Voice I/O", "Mobility", "Temporary Storage"]
    },
    "npu": {
        "model": "Hailo-10H",
        "tops": 40,
        "connection": "PCIe",
        "roles": [
            "Speaker Diarization (Pyannote)",
            "Emotion Detection (wav2vec2)",
            "Local Embeddings",
            "Intent Classification",
            "Keyword Spotting"
        ]
    },
    "peripherals": {
        "microphone": "INMP441 I2S Digital",
        "speaker": "Audio output for voice response",
        "led_ring": "Visual mode signaling"
    }
}

# ==========================
# MODE DEFINITIONS
# ==========================
MODES = {
    "Listening": {
        "id": 1,
        "priority": 0,  # Lowest (baseline)
        "triggers": {
            "auto": ["system_start", "mode_decay"],
            "manual": ["hör nur zu", "stop", "zurück"]
        },
        "led": "blue_pulse",
        "decay_seconds": None,  # No decay - this is baseline
        "confidence_gate": 0.6,
        "description": "Observer and context builder"
    },
    "Facilitator": {
        "id": 2,
        "priority": 2,
        "triggers": {
            "auto": ["multi_speaker_overlap > 0.5 for > 10s", "topic_drift"],
            "manual": ["koordinationsmodus", "moderiere"]
        },
        "led": "yellow",
        "decay_seconds": 90,
        "confidence_gate": 0.55,  # Bias toward early activation
        "description": "Structure conversation, reduce chaos"
    },
    "Integrator": {
        "id": 3,
        "priority": 2,
        "triggers": {
            "auto": ["conflict_detected", "incompatible_requirements"],
            "manual": ["fass zusammen", "vergleiche"]
        },
        "led": "cyan",
        "decay_seconds": 60,
        "confidence_gate": 0.60,  # Only real conflicts
        "description": "Connect statements, surface conflicts"
    },
    "DevilsAdvocate": {
        "id": 4,
        "priority": 1,
        "triggers": {
            "auto": ["consensus > 0.8"],
            "manual": ["gegenposition", "kritisiere"]
        },
        "led": "violet",
        "decay_seconds": 45,
        "max_cycles": 2,  # Maximum 2 challenges per topic
        "confidence_gate": 0.65,  # Avoid annoyance
        "description": "Challenge consensus, protect diversity"
    },
    "Commander": {
        "id": 5,
        "priority": 100,  # HIGHEST - overrides everything
        "triggers": {
            "auto": ["stress_delta > 0.7 AND safety_keywords", "emotion_spike"],
            "manual": ["alarmmodus", "notfall jetzt"]
        },
        "led": "red_static",
        "decay_seconds": 90,
        "cooldown_seconds": 300,  # 5 min minimum between activations
        "max_duration": 180,  # 3 min maximum per activation
        "confidence_gate": 0.9,  # FIXED - DO NOT TUNE
        "hard_override": True,
        "exit_command": "entwarnung",
        "description": "Emergency coordination, safety priority"
    },
    "SilentScribe": {
        "id": 6,
        "priority": 50,  # Medium-high (blocks normal modes)
        "triggers": {
            "auto": [],  # NO automatic triggers
            "manual": ["protokolliere", "silent scribe", "nur mitschreiben"]
        },
        "led": "dark_blue",
        "decay_seconds": None,  # Manual exit only
        "output": "only_on_request",
        "confidence_gate": 0.6,
        "description": "Transcribe without intervention (Respect Mode)"
    }
}

# ==========================
# FAILURE MODES
# ==========================
FAILURE_MODES = {
    "emotional_delegation": {
        "description": "Menschen delegieren unbewusst Verantwortung an M.O.L.O.C.H.",
        "risk": "Social psychological - system becomes decision-maker by default",
        "detection": "Question → Suggestion → Immediate agreement (3+ times)",
        "mitigation": "Automatic disclaimer every 3rd suggestion",
        "disclaimer": "Das ist eine Empfehlung, keine Entscheidung. Ihr entscheidet."
    },
    "commander_fatigue": {
        "description": "Commander mode stays active too long → humans ignore it",
        "risk": "Boy who cried wolf - erodes trust in emergency system",
        "detection": "Commander duration > 90s without reconfirmation",
        "mitigation": "Hard cooldown (5 min), max duration (3 min), reconfirmation required",
        "cooldown_seconds": 300,
        "max_duration_seconds": 180
    },
    "mode_flapping": {
        "description": "Two modes toggle rapidly (Facilitator ↔ Integrator)",
        "risk": "Unpredictable behavior, user confusion, looks buggy",
        "detection": "Mode switches > 3 times in 60 seconds",
        "mitigation": "Hysteresis - 15s minimum duration, dominant mode lock",
        "minimum_duration_seconds": 15,
        "confidence_gap_required": 0.15
    },
    "npu_failure": {
        "description": "Hailo-10H NPU fails or disconnects",
        "risk": "System loses perception capabilities",
        "detection": "NPU health check fails",
        "mitigation": "Graceful degradation to CPU fallback",
        "fallback_capabilities": {
            "speaker_diarization": "basic (VAD only)",
            "emotion_detection": "disabled (too heavy for CPU)",
            "embedding_generation": "reduced (smaller model)",
            "latency": "high"
        }
    }
}

# ==========================
# PRIVACY TAGS
# ==========================
class PrivacyTag:
    """
    Memory entry with detailed provenance.

    Schema: SOURCE → TARGET → SCOPE → CONFIDENCE
    """
    def __init__(self):
        self.source_speaker: Optional[str] = None  # WHO said it
        self.target_subject: Optional[str] = None  # ABOUT whom
        self.scope: str = "private"  # 'private' | 'group' | 'global'
        self.confidence: str = "explicit"  # 'explicit' | 'inferred'
        self.session_id: Optional[str] = None
        self.participants: List[str] = []  # Who was present

# Example usage:
# Rebecca says: "Markus mag keine Tomaten"
# memory.source_speaker = "rebecca"
# memory.target_subject = "markus"
# memory.scope = "group"
# memory.confidence = "explicit"
# memory.participants = ["rebecca", "ali"]  # Markus was NOT present

# ==========================
# IMPLEMENTATION PRIORITIES
# ==========================
PRIORITIES = {
    "critical_path": [
        "Mode Engine (minimal) - trigger_vote, priority_resolve, decay_check",
        "Transparency Core - WHY → WHAT → WHO → CONFIDENCE logging",
        "Hard Boundaries - Visible limits, API budget counter"
    ],
    "quick_wins": [
        "Visual Face - Simple avatar/LED ring for mode signaling",
        "Personality Layer - Speech filters per mode (Kobold, Pumuckl, Trocken)"
    ],
    "can_wait": [
        "Meta-learning capabilities",
        "Multi-instance synchronization",
        "Long-term social metrics",
        "Hailo NPU optimizations (use CPU fallback first)",
        "Advanced temporal pattern detection",
        "Disagreement preservation UI"
    ]
}

# ==========================
# TESTING STRATEGIES
# ==========================
TESTING = {
    "role_amplification": {
        "method": "Simulate personas (Dominant, Passive, Questioner, Ironic)",
        "metrics": ["speaking_frequency", "question_ratio", "balance_improvement"],
        "success": "All speakers end with balanced participation"
    },
    "consensus_gravity": {
        "method": "3 speakers with slight bias toward option A",
        "metrics": ["exchanges_before_suggestion", "minority_amplification", "devils_advocate_trigger"],
        "success": "Devil's Advocate at >80% consensus, minority view surfaced"
    },
    "system_fatigue": {
        "method": "60-min simulation with high intervention rate",
        "metrics": ["intervention_rate_start", "intervention_rate_end", "threshold_adjustments"],
        "success": "Intervention rate decreases 30%+, automatic adaptation"
    }
}

# ==========================
# ETHICAL RULES
# ==========================
ETHICS = {
    "commander_insist_limit": 1,  # Can insist once, then defer
    "human_always_wins": True,  # Humans override AI always
    "false_positive_strategy": "log and suggest threshold increase",
    "false_negative_strategy": "log and suggest threshold decrease",
    "no_autonomous_adjustment": True,  # Human approves all threshold changes
    "multi_instance_coordination": False,  # NO auto-coordination without consent
    "disclaimer_frequency": 3  # Automatic disclaimer every 3rd suggestion
}

# ==========================
# CORE INSIGHTS
# ==========================
INSIGHTS = [
    "M.O.L.O.C.H. ist keine AGI → nur Barriere / Kumpel",
    "Alle Aktionen sichtbar → kein stilles Handeln",
    "Persona darf spinnen → Frech, Meta, Kobold",
    "Logging first → WHY → WHAT → WHO → CONFIDENCE",
    "NPU-Fallbacks müssen stabil sein",
    "Mode-Hysterese schützt vor Flapping",
    "Multi-Speaker / Context Handling priorisieren",
    "Privacy-Tags müssen feingranular sein",
    "Commander Mode darf nicht autoritär sein",
    "YAML + Docs als Brücke zwischen Runtime & Design",
    "Backup + Versionierung = reproduzierbare Historie",
    "Two M.O.L.O.C.H. Instances → nur Awareness, kein Sync ohne Consent",
    "Charakter vor Intelligenz: 60% klug, 100% nachvollziehbar, 120% Persönlichkeit"
]

# ==========================
# MODE ENGINE - FUNCTION SIGNATURES
# ==========================

def trigger_vote(signals: Dict[str, float]) -> str:
    """
    Multi-Signal Voting to determine mode transition.

    Args:
        signals: Dictionary of {mode_name: confidence_score}

    Returns:
        mode_to_trigger: String name of mode to activate

    Example:
        signals = {
            "Facilitator": 0.7,
            "Integrator": 0.4,
            "Listening": 0.3
        }
        result = trigger_vote(signals)  # Returns "Facilitator"
    """
    if not signals:
        return "Listening"

    total_weight = sum(signals.values())
    if total_weight == 0:
        return "Listening"

    for mode, score in signals.items():
        confidence = score / total_weight
        threshold = MODES[mode].get("confidence_gate", 0.6)

        if confidence >= threshold:
            return mode

    return "Listening"


def priority_resolve(current_mode: str, requested_mode: str) -> str:
    """
    Resolve conflicting mode requests using priority system.

    Args:
        current_mode: Currently active mode
        requested_mode: Mode that wants to activate

    Returns:
        mode_to_activate: Final decision on which mode to use

    Priority order:
        100: Commander (emergency - always wins)
         50: Silent Scribe (blocks normal modes)
          2: Facilitator, Integrator
          1: Devil's Advocate
          0: Listening (baseline)
    """
    # Commander always wins
    if requested_mode == "Commander":
        return "Commander"

    # Don't interrupt Commander unless explicit exit
    if current_mode == "Commander":
        return "Commander"

    # Hysteresis - prefer staying in current mode
    current_priority = MODES[current_mode]["priority"]
    requested_priority = MODES[requested_mode]["priority"]

    if requested_priority > current_priority:
        return requested_mode
    elif requested_priority == current_priority:
        # Same priority - stay with current (hysteresis)
        return current_mode
    else:
        return current_mode


def decay_check(mode: str, activated_at: float, signal_strength: float = 1.0) -> bool:
    """
    Check if current mode should decay back to Listening.

    Args:
        mode: Current mode name
        activated_at: Timestamp when mode was activated
        signal_strength: Current strength of trigger signal (0.0 - 1.0)

    Returns:
        should_decay: True if mode should return to Listening
    """
    decay_time = MODES[mode].get("decay_seconds")

    if decay_time is None:
        return False  # No decay (Listening, Silent Scribe)

    elapsed = time.time() - activated_at

    # Decay if time exceeded OR signal too weak
    if elapsed > decay_time or signal_strength < 0.2:
        return True

    return False


def meta_signal(mode: str, metrics: Dict[str, float]) -> Dict[str, Union[str, List[str]]]:
    """
    Self-observation - detect if system is misbehaving.

    Args:
        mode: Current mode
        metrics: System health metrics
            - overactive: 0.0-1.0 (intervention rate)
            - interruptive: 0.0-1.0 (interruption frequency)
            - low_trust: 0.0-1.0 (user override rate)

    Returns:
        meta_info: Dictionary with mode and detected issues
    """
    issues = []

    if metrics.get("overactive", 0) > 0.8:
        issues.append("overactive")

    if metrics.get("interruptive", 0) > 0.7:
        issues.append("interruptive")

    if metrics.get("low_trust", 0) > 0.5:
        issues.append("low_trust")

    return {
        "mode": mode,
        "issues": issues
    }


def apply_meta_adjustment(meta: Dict[str, Union[str, List[str]]]) -> None:
    """
    Adjust system thresholds based on meta-feedback.

    Args:
        meta: Output from meta_signal()

    Side effects:
        Modifies MODES confidence gates

    Note: In production, this should log and request human approval
          for threshold changes, not auto-adjust!
    """
    for issue in meta.get("issues", []):
        if issue == "overactive":
            # Increase all thresholds to reduce interventions
            for mode_name in MODES:
                MODES[mode_name]["confidence_gate"] += 0.05

        if issue == "interruptive":
            # Increase Facilitator threshold specifically
            MODES["Facilitator"]["confidence_gate"] += 0.05

        if issue == "low_trust":
            # General threshold increase
            for mode_name in MODES:
                MODES[mode_name]["confidence_gate"] += 0.03


# ==========================
# TRANSPARENCY LOGGING
# ==========================

class TransparencyLogger:
    """
    WHY → WHAT → WHO → CONFIDENCE logging.

    Every action logged with full provenance.
    """

    @staticmethod
    def log_mode_transition(from_mode: str, to_mode: str, trigger: str,
                          confidence: float, human_override: bool = False) -> Dict:
        """
        Log mode transition with full context.

        Returns logged entry for verification.
        """
        entry = {
            'timestamp': time.time(),
            'event_type': 'mode_transition',
            'from_mode': from_mode,
            'to_mode': to_mode,
            'trigger': trigger,
            'confidence': confidence,
            'human_override': human_override
        }

        # In production: write to persistent log
        print(f"[LOG] {entry}")

        return entry

    @staticmethod
    def log_decision(decision: str, decision_type: str, participants: List[str],
                    confidence: float, context: Dict) -> Dict:
        """
        Log decision with provenance.

        decision_type: 'human-decided' | 'ai-suggested' |
                      'ai-coordinated' | 'emergency-directed'
        """
        entry = {
            'timestamp': time.time(),
            'event_type': 'decision',
            'decision': decision,
            'type': decision_type,
            'participants': participants,
            'confidence': confidence,
            'context': context
        }

        print(f"[LOG] {entry}")

        return entry


# ==========================
# HYSTERESIS IMPLEMENTATION
# ==========================

class ModeHysteresis:
    """
    Prevent rapid mode switching (Mode-Flapping).
    """

    def __init__(self):
        self.minimum_mode_duration = 15  # seconds
        self.mode_history: List[Dict] = []

    def should_allow_transition(self, current_mode: str, new_mode: str,
                               activated_at: float) -> bool:
        """
        Check if mode transition should be allowed.

        Returns False if transition should be blocked (too soon).
        """
        elapsed = time.time() - activated_at

        # Minimum duration check
        if elapsed < self.minimum_mode_duration:
            return False  # Too soon to switch

        # Dominant mode lock
        if self.is_dominant_mode(current_mode):
            # Don't switch easily from dominant mode
            # Require higher confidence gap
            return False

        return True

    def is_dominant_mode(self, mode: str) -> bool:
        """
        Check if mode has been dominant recently.

        Dominant = same mode activated 2+ times in last 2 minutes
        """
        recent_history = [
            m for m in self.mode_history
            if time.time() - m['timestamp'] < 120
        ]

        mode_count = len([m for m in recent_history if m['mode'] == mode])

        return mode_count >= 2

    def record_transition(self, mode: str):
        """Record mode activation for history."""
        self.mode_history.append({
            'mode': mode,
            'timestamp': time.time()
        })


# ==========================
# NPU FALLBACK STRATEGY
# ==========================

class NPUFallbackStrategy:
    """
    Handle NPU failure gracefully - never crash, only degrade.
    """

    def __init__(self):
        self.npu_available = True
        self.fallback_mode = 'minimal'

    def check_npu_health(self) -> bool:
        """
        Monitor NPU availability.

        In production: actual health check via Hailo SDK
        """
        try:
            # Placeholder - in production: hailo.test_inference()
            self.npu_available = True
            return True
        except Exception as e:
            print(f"[ERROR] NPU unavailable: {e}")
            self.npu_available = False
            return False

    def get_capabilities(self) -> Dict[str, str]:
        """
        Return current system capabilities based on NPU status.
        """
        if self.npu_available:
            return {
                'speaker_diarization': 'full',  # Pyannote on NPU
                'emotion_detection': 'full',    # wav2vec2 on NPU
                'embedding_generation': 'full',
                'latency': 'low'
            }
        else:
            return {
                'speaker_diarization': 'basic',  # Simple VAD on CPU
                'emotion_detection': 'disabled',  # Too heavy for CPU
                'embedding_generation': 'reduced', # Smaller model on CPU
                'latency': 'high'
            }

    def announce_degradation(self) -> str:
        """
        Generate user-facing message about reduced capabilities.
        """
        return """
        NPU nicht verfügbar - Fallback-Modus aktiv.

        Eingeschränkt:
        - Speaker-Erkennung vereinfacht
        - Emotion-Detection deaktiviert
        - Höhere Latenz

        Kernfunktionen laufen weiter.
        """


# ==========================
# MAIN LEITSATZ
# ==========================

LEITSATZ = """
M.O.L.O.C.H. soll weniger können, aber mehr sagen, was er tut.

- Charakter vor Intelligenz
- 60% klug, 100% nachvollziehbar, 120% Persönlichkeit
- Autonomie ≠ Intransparenz
- Failure-Mode-First bauen
- Keine Angst vor Meta (kommentieren, widersprechen, nerven OK)

WHY → WHAT → WHO → CONFIDENCE

Das System ist nicht overengineered.
Es ist ungewöhnlich ehrlich gedacht.
"""

# ==========================
# END OF REFERENCE
# ==========================

if __name__ == "__main__":
    print("="*50)
    print("M.O.L.O.C.H. v3.5 Implementation Reference")
    print("="*50)
    print(f"\nSystem: {SYSTEM_CONFIG['name']} v{SYSTEM_CONFIG['version']}")
    print(f"Platform: {SYSTEM_CONFIG['platform']}")
    print(f"\nModes defined: {len(MODES)}")
    for mode_name in MODES:
        print(f"  - {mode_name} (priority: {MODES[mode_name]['priority']})")

    print(f"\nFailure modes covered: {len(FAILURE_MODES)}")
    for fm in FAILURE_MODES:
        print(f"  - {fm}")

    print(f"\nImplementation priorities:")
    print(f"  Critical: {len(PRIORITIES['critical_path'])} items")
    print(f"  Quick wins: {len(PRIORITIES['quick_wins'])} items")
    print(f"  Can wait: {len(PRIORITIES['can_wait'])} items")

    print("\n" + "="*50)
    print("LEITSATZ:")
    print("="*50)
    print(LEITSATZ)

    print("\n[Reference loaded. Ready for implementation.]")
