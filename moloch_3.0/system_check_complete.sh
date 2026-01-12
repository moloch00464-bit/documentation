#!/bin/bash
#
# M.O.L.O.C.H. 3.0 - COMPLETE SYSTEM CHECK
# ========================================
# Umfassender Check aller Komponenten:
# - Python Dependencies
# - Termux Tools
# - Voice System (Vosk + Termux STT)
# - Vision System
# - API Configuration
# - File Integrity
# - Performance Benchmarks

set -e  # Exit on error

echo "═══════════════════════════════════════════════════════════════"
echo "🔍 M.O.L.O.C.H. 3.0 - COMPLETE SYSTEM CHECK"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Starting at: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Track results
WARNINGS=0
ERRORS=0
CHECKS_PASSED=0
CHECKS_TOTAL=0

# Helper functions
check_pass() {
    ((CHECKS_TOTAL++))
    ((CHECKS_PASSED++))
    echo "   ✅ $1"
}

check_warn() {
    ((CHECKS_TOTAL++))
    ((WARNINGS++))
    echo "   ⚠️  $1"
}

check_fail() {
    ((CHECKS_TOTAL++))
    ((ERRORS++))
    echo "   ❌ $1"
}

# ═══════════════════════════════════════════════════════════════════════════
# 1. ENVIRONMENT CHECK
# ═══════════════════════════════════════════════════════════════════════════

echo "───────────────────────────────────────────────────────────────"
echo "1️⃣  ENVIRONMENT CHECK"
echo "───────────────────────────────────────────────────────────────"

# Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    check_pass "Python installed: $PYTHON_VERSION"
else
    check_fail "Python not found!"
fi

# pip
if command -v pip &> /dev/null; then
    PIP_VERSION=$(pip --version 2>&1 | awk '{print $2}')
    check_pass "pip installed: $PIP_VERSION"
else
    check_fail "pip not found!"
fi

# API Key
if [ -n "$ANTHROPIC_API_KEY" ]; then
    KEY_LEN=${#ANTHROPIC_API_KEY}
    check_pass "ANTHROPIC_API_KEY set (length: $KEY_LEN)"
else
    check_fail "ANTHROPIC_API_KEY not set!"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 2. PYTHON DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════

echo "───────────────────────────────────────────────────────────────"
echo "2️⃣  PYTHON DEPENDENCIES"
echo "───────────────────────────────────────────────────────────────"

# Core dependencies
for pkg in anthropic requests; do
    if python3 -c "import $pkg" 2>/dev/null; then
        VERSION=$(python3 -c "import $pkg; print($pkg.__version__)" 2>/dev/null || echo "unknown")
        check_pass "$pkg installed: $VERSION"
    else
        check_fail "$pkg not installed!"
    fi
done

# Vosk (optional but recommended)
if python3 -c "import vosk" 2>/dev/null; then
    VOSK_VERSION=$(python3 -c "import vosk; print(vosk.__version__)" 2>/dev/null || echo "unknown")
    check_pass "vosk installed: $VOSK_VERSION (RECOMMENDED!)"
else
    check_warn "vosk not installed (fallback to termux-speech-to-text)"
    echo "           Install with: bash install_vosk_german.sh"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 3. TERMUX TOOLS
# ═══════════════════════════════════════════════════════════════════════════

echo "───────────────────────────────────────────────────────────────"
echo "3️⃣  TERMUX TOOLS"
echo "───────────────────────────────────────────────────────────────"

# Termux:API tools
TERMUX_TOOLS=(
    "termux-tts-speak:TTS (required)"
    "termux-speech-to-text:STT fallback (required)"
    "termux-camera-photo:Vision (required)"
    "termux-microphone-record:Vosk recording (recommended)"
)

for tool_info in "${TERMUX_TOOLS[@]}"; do
    tool="${tool_info%%:*}"
    desc="${tool_info##*:}"
    if command -v "$tool" &> /dev/null; then
        check_pass "$tool: $desc"
    else
        if [[ "$desc" == *"required"* ]]; then
            check_fail "$tool not found! ($desc)"
        else
            check_warn "$tool not found ($desc)"
        fi
    fi
done

# Check if Termux:API app is installed
if pm list packages 2>/dev/null | grep -q com.termux.api; then
    check_pass "Termux:API app installed"
else
    check_warn "Termux:API app not detected (may cause issues)"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 4. VOICE SYSTEM CHECK
# ═══════════════════════════════════════════════════════════════════════════

echo "───────────────────────────────────────────────────────────────"
echo "4️⃣  VOICE SYSTEM CHECK"
echo "───────────────────────────────────────────────────────────────"

# Vosk German Model
VOSK_MODEL_PATH="$HOME/documentation/moloch_3.0/vosk_models/vosk-model-small-de-0.15"
if [ -d "$VOSK_MODEL_PATH" ]; then
    MODEL_SIZE=$(du -sh "$VOSK_MODEL_PATH" 2>/dev/null | awk '{print $1}')
    check_pass "Vosk German model installed ($MODEL_SIZE)"

    # Test model loading
    if python3 -c "from vosk import Model; Model('$VOSK_MODEL_PATH')" 2>/dev/null; then
        check_pass "Vosk model loads successfully"
    else
        check_fail "Vosk model exists but fails to load!"
    fi
else
    check_warn "Vosk German model not found"
    echo "           Install with: bash install_vosk_german.sh"
fi

# Test TTS
if command -v termux-tts-speak &> /dev/null; then
    echo "   🔊 Testing TTS (silent test)..."
    if timeout 5 termux-tts-speak -l de-DE "Test" &>/dev/null; then
        check_pass "TTS working"
    else
        check_warn "TTS test failed (may need permissions)"
    fi
fi

# Check microphone permissions (indirect)
echo "   🎤 Microphone permissions:"
if [ -r /dev/snd ]; then
    check_pass "Audio device accessible"
else
    check_warn "Audio device not readable (may need permissions)"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 5. VISION SYSTEM CHECK
# ═══════════════════════════════════════════════════════════════════════════

echo "───────────────────────────────────────────────────────────────"
echo "5️⃣  VISION SYSTEM CHECK"
echo "───────────────────────────────────────────────────────────────"

# Camera tool
if command -v termux-camera-photo &> /dev/null; then
    check_pass "termux-camera-photo available"
else
    check_fail "termux-camera-photo not found!"
fi

# Camera info
if command -v termux-camera-info &> /dev/null; then
    CAMERAS=$(termux-camera-info 2>/dev/null | jq -r '.[].id' 2>/dev/null | wc -l)
    if [ "$CAMERAS" -gt 0 ]; then
        check_pass "Camera(s) detected: $CAMERAS"
    else
        check_warn "No cameras detected"
    fi
else
    check_warn "termux-camera-info not available"
fi

# Vision module
if [ -f "$HOME/documentation/moloch_3.0/moloch_io/vision.py" ]; then
    check_pass "vision.py module exists"
    if python3 -c "from moloch_io.vision import VisionIO; VisionIO()" 2>/dev/null; then
        check_pass "VisionIO module loads successfully"
    else
        check_warn "VisionIO module has import issues"
    fi
else
    check_fail "vision.py module not found!"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 6. API & MODEL CHECK
# ═══════════════════════════════════════════════════════════════════════════

echo "───────────────────────────────────────────────────────────────"
echo "6️⃣  API & MODEL CHECK"
echo "───────────────────────────────────────────────────────────────"

# Config file
if [ -f "$HOME/documentation/moloch_3.0/core/config.py" ]; then
    check_pass "config.py exists"

    # Check model name
    MODEL_NAME=$(grep "CLAUDE_MODEL" "$HOME/documentation/moloch_3.0/core/config.py" | head -1 | sed -E 's/.*"(.*)".*/\1/')
    if [ "$MODEL_NAME" = "claude-sonnet-4-5-20250929" ]; then
        check_pass "Model name: $MODEL_NAME (current!)"
    else
        check_warn "Model name: $MODEL_NAME (may be outdated)"
    fi
else
    check_fail "config.py not found!"
fi

# API Test (quick)
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "   🌐 Testing Claude API (quick test)..."

    API_RESPONSE=$(curl -s -w "\n%{http_code}" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
        -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}' \
        https://api.anthropic.com/v1/messages 2>/dev/null)

    HTTP_CODE=$(echo "$API_RESPONSE" | tail -1)

    if [ "$HTTP_CODE" = "200" ]; then
        check_pass "Claude API working (200 OK)"
    elif [ "$HTTP_CODE" = "401" ]; then
        check_fail "Claude API: 401 Unauthorized (bad API key)"
    elif [ "$HTTP_CODE" = "404" ]; then
        check_fail "Claude API: 404 Not Found (bad model name)"
    else
        check_warn "Claude API: HTTP $HTTP_CODE (unexpected)"
    fi
else
    check_warn "Skipping API test (no API key)"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 7. FILE INTEGRITY CHECK
# ═══════════════════════════════════════════════════════════════════════════

echo "───────────────────────────────────────────────────────────────"
echo "7️⃣  FILE INTEGRITY CHECK"
echo "───────────────────────────────────────────────────────────────"

# Critical files
CRITICAL_FILES=(
    "moloch3_unified.py"
    "core/config.py"
    "core/api.py"
    "moloch_io/voice.py"
    "moloch_io/vision.py"
    "diagnose.py"
    "health_check.py"
)

cd "$HOME/documentation/moloch_3.0"

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        # Check if file is Python and has no syntax errors
        if [[ "$file" == *.py ]]; then
            if python3 -m py_compile "$file" 2>/dev/null; then
                check_pass "$file (valid syntax)"
            else
                check_fail "$file (syntax error!)"
            fi
        else
            check_pass "$file exists"
        fi
    else
        check_fail "$file not found!"
    fi
done

# Count all Python files
TOTAL_PY_FILES=$(find . -name "*.py" -type f | wc -l)
echo "   📊 Total Python files: $TOTAL_PY_FILES"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 8. DISK SPACE CHECK
# ═══════════════════════════════════════════════════════════════════════════

echo "───────────────────────────────────────────────────────────────"
echo "8️⃣  DISK SPACE CHECK"
echo "───────────────────────────────────────────────────────────────"

# Project size
PROJECT_SIZE=$(du -sh "$HOME/documentation/moloch_3.0" 2>/dev/null | awk '{print $1}')
check_pass "Project size: $PROJECT_SIZE"

# Vosk models size
if [ -d "$HOME/documentation/moloch_3.0/vosk_models" ]; then
    VOSK_SIZE=$(du -sh "$HOME/documentation/moloch_3.0/vosk_models" 2>/dev/null | awk '{print $1}')
    check_pass "Vosk models: $VOSK_SIZE"
fi

# Available space
AVAILABLE_SPACE=$(df -h "$HOME" | tail -1 | awk '{print $4}')
echo "   💾 Available space: $AVAILABLE_SPACE"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 9. GIT STATUS
# ═══════════════════════════════════════════════════════════════════════════

echo "───────────────────────────────────────────────────────────────"
echo "9️⃣  GIT STATUS"
echo "───────────────────────────────────────────────────────────────"

cd "$HOME/documentation"

if git rev-parse --git-dir > /dev/null 2>&1; then
    check_pass "Git repository detected"

    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
    echo "   🌿 Current branch: $CURRENT_BRANCH"

    UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)
    if [ "$UNCOMMITTED" -eq 0 ]; then
        check_pass "Working tree clean"
    else
        check_warn "Uncommitted changes: $UNCOMMITTED files"
    fi

    UNPUSHED=$(git log @{u}.. --oneline 2>/dev/null | wc -l)
    if [ "$UNPUSHED" -eq 0 ]; then
        check_pass "All commits pushed"
    else
        check_warn "Unpushed commits: $UNPUSHED"
    fi
else
    check_warn "Not a git repository"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 10. SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════"
echo "📊 SYSTEM CHECK SUMMARY"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Total Checks: $CHECKS_TOTAL"
echo "   ✅ Passed: $CHECKS_PASSED"
echo "   ⚠️  Warnings: $WARNINGS"
echo "   ❌ Errors: $ERRORS"
echo ""

# Calculate health percentage
if [ "$CHECKS_TOTAL" -gt 0 ]; then
    HEALTH_PERCENT=$(( (CHECKS_PASSED * 100) / CHECKS_TOTAL ))
    echo "System Health: $HEALTH_PERCENT%"
    echo ""

    if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
        echo "🎉 PERFECT! All checks passed!"
        echo "   M.O.L.O.C.H. 3.0 is 100% production ready!"
    elif [ "$ERRORS" -eq 0 ]; then
        echo "✅ GOOD! No critical errors."
        echo "   ⚠️  $WARNINGS warning(s) - see details above."
    else
        echo "❌ ISSUES FOUND!"
        echo "   Please fix $ERRORS error(s) before production use."
    fi
fi

echo ""
echo "Finished at: $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════════════════"

# Exit code
if [ "$ERRORS" -gt 0 ]; then
    exit 1
else
    exit 0
fi
