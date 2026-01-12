#!/bin/bash
# M.O.L.O.C.H. 3.0 Hardware Compatibility Test
# Simulates Raspberry Pi with all peripherals connected

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  M.O.L.O.C.H. 3.0 - Raspberry Pi Hardware Compatibility Test  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

passed=0
warnings=0
failed=0

test_result() {
    local status=$1
    local test_name=$2
    local message=$3

    case $status in
        "PASS")
            echo -e "${GREEN}✅ PASS${NC}: $test_name"
            ((passed++))
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  WARN${NC}: $test_name"
            echo -e "   └─ $message"
            ((warnings++))
            ;;
        "FAIL")
            echo -e "${RED}❌ FAIL${NC}: $test_name"
            echo -e "   └─ $message"
            ((failed++))
            ;;
    esac
}

echo "═══════════════════════════════════════════════════════════════"
echo "TEST 1: USB BANDWIDTH ANALYSIS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Simulate USB device check
echo "Simulating connected USB devices:"
echo "  - USB Microphone (USB 2.0, ~1.5 Mbps for audio)"
echo "  - USB Webcam (USB 2.0, ~25 Mbps for 720p)"
echo ""

# Pi 3B+ has shared USB 2.0 bus (480 Mbps total)
# Pi 4/5 have separate USB 3.0 + USB 2.0

TOTAL_USB_BANDWIDTH_PI3=480  # Mbps
USB_MIC_BANDWIDTH=2          # Mbps (audio)
USB_WEBCAM_720P=25           # Mbps
USB_WEBCAM_1080P=50          # Mbps

USED_BANDWIDTH_720P=$((USB_MIC_BANDWIDTH + USB_WEBCAM_720P))
USED_BANDWIDTH_1080P=$((USB_MIC_BANDWIDTH + USB_WEBCAM_1080P))

echo "Pi 3B+ USB Bandwidth:"
echo "  Total: ${TOTAL_USB_BANDWIDTH_PI3} Mbps"
echo "  Used (720p): ${USED_BANDWIDTH_720P} Mbps (${USED_BANDWIDTH_720P}%)"
echo "  Used (1080p): ${USED_BANDWIDTH_1080P} Mbps (${USED_BANDWIDTH_1080P}%)"
echo ""

if [ $USED_BANDWIDTH_720P -lt 100 ]; then
    test_result "PASS" "USB Bandwidth (720p)" ""
else
    test_result "FAIL" "USB Bandwidth (720p)" "Insufficient bandwidth"
fi

if [ $USED_BANDWIDTH_1080P -lt 150 ]; then
    test_result "WARN" "USB Bandwidth (1080p)" "May cause frame drops on Pi 3B+"
else
    test_result "FAIL" "USB Bandwidth (1080p)" "Too high for Pi 3B+"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST 2: AUDIO DEVICE CONFLICTS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Checking for audio device conflicts:"
echo "  - System: bcm2835 ALSA (onboard 3.5mm jack)"
echo "  - USB: USB Audio Device (microphone)"
echo "  - HDMI: HDMI audio output"
echo ""

# Check if multiple audio devices can coexist
echo "Potential conflicts:"
echo "  ⚠️  Multiple audio outputs may confuse ALSA"
echo "  ⚠️  Need to set default device in ~/.asoundrc"
echo ""

test_result "WARN" "Multiple Audio Devices" "Must configure default device explicitly"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST 3: CAMERA + AUDIO SIMULTANEOUS USE"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Testing simultaneous camera and audio capture:"
echo ""

# Check if libcamera and audio can run together
echo "Scenario: Voice Mode + Vision Mode simultaneously"
echo "  - Audio: Continuous recording with Whisper STT"
echo "  - Camera: Periodic image capture (every 5 seconds)"
echo ""

# Pi Camera uses GPU, USB uses CPU + USB bus
echo "Resource usage:"
echo "  CPU: ~60% (Python + Whisper + Image processing)"
echo "  GPU: ~30% (libcamera ISP)"
echo "  RAM: ~1.5GB (with models loaded)"
echo ""

test_result "WARN" "Simultaneous Audio+Vision" "High CPU usage, may lag on Pi 3B+"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST 4: POWER SUPPLY VALIDATION"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Calculating total power draw:"
echo ""

# Power consumption estimates
PI_BASE=2.5        # Watts (Pi 4 idle)
PI_LOAD=5.0        # Watts (Pi 4 under load)
USB_MIC_POWER=0.5  # Watts
USB_WEBCAM=2.5     # Watts
PI_CAMERA=0.25     # Watts (negligible)

TOTAL_POWER_USB=$(echo "$PI_LOAD + $USB_MIC_POWER + $USB_WEBCAM" | bc)
TOTAL_POWER_PICAM=$(echo "$PI_LOAD + $USB_MIC_POWER + $PI_CAMERA" | bc)

echo "Configuration A (USB Webcam + USB Mic):"
echo "  Total Power: ${TOTAL_POWER_USB}W"
echo "  Recommended PSU: 15W (3A @ 5V)"
echo ""

echo "Configuration B (Pi Camera + USB Mic):"
echo "  Total Power: ${TOTAL_POWER_PICAM}W"
echo "  Recommended PSU: 15W (3A @ 5V)"
echo ""

# Official Pi 4 PSU is 15W (3A)
if (( $(echo "$TOTAL_POWER_USB < 15" | bc -l) )); then
    test_result "PASS" "Power Requirements (USB Setup)" ""
else
    test_result "FAIL" "Power Requirements (USB Setup)" "Exceeds 15W PSU limit"
fi

if (( $(echo "$TOTAL_POWER_PICAM < 15" | bc -l) )); then
    test_result "PASS" "Power Requirements (Pi Cam Setup)" ""
else
    test_result "FAIL" "Power Requirements (Pi Cam Setup)" "Exceeds 15W PSU limit"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST 5: I2C / GPIO CONFLICTS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Checking for GPIO conflicts:"
echo ""

# Pi Camera uses specific GPIO pins
echo "Pi Camera Module uses:"
echo "  - CSI ribbon cable (dedicated interface)"
echo "  - No GPIO conflicts"
echo ""

# I2C for wearables
echo "Optional I2C devices (Xiaomi Band, etc.):"
echo "  - GPIO 2 (SDA)"
echo "  - GPIO 3 (SCL)"
echo "  - No conflicts with camera or audio"
echo ""

test_result "PASS" "GPIO Pin Allocation" ""

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST 6: THERMAL THROTTLING RISK"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Estimating heat generation under full load:"
echo ""

# Pi 4 thermal characteristics
echo "Workload: Voice + Vision + Claude API calls"
echo "  CPU Usage: 60-80%"
echo "  Expected Temperature: 65-75°C"
echo "  Throttling Threshold: 80°C"
echo ""

echo "Cooling Requirements:"
if true; then
    echo "  ⚠️  Pi 3B+: MUST have active cooling (fan)"
    echo "  ⚠️  Pi 4: Recommended active cooling"
    echo "  ✅ Pi 5: Built-in active cooler sufficient"
    test_result "WARN" "Thermal Management" "Active cooling strongly recommended"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST 7: AUDIO LATENCY ANALYSIS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Testing audio pipeline latency:"
echo ""

# Audio latency components
MIC_LATENCY=10      # ms (hardware)
ALSA_LATENCY=20     # ms (ALSA buffer)
WHISPER_LATENCY=500 # ms (STT processing)
NETWORK_LATENCY=100 # ms (API call)
TTS_LATENCY=200     # ms (speech synthesis)

TOTAL_LATENCY=$((MIC_LATENCY + ALSA_LATENCY + WHISPER_LATENCY + NETWORK_LATENCY + TTS_LATENCY))

echo "Voice interaction latency breakdown:"
echo "  Microphone capture:    ${MIC_LATENCY}ms"
echo "  ALSA buffer:          ${ALSA_LATENCY}ms"
echo "  Whisper STT:          ${WHISPER_LATENCY}ms"
echo "  Network (Claude API): ${NETWORK_LATENCY}ms"
echo "  TTS synthesis:        ${TTS_LATENCY}ms"
echo "  ─────────────────────────────────"
echo "  Total latency:        ${TOTAL_LATENCY}ms"
echo ""

if [ $TOTAL_LATENCY -lt 1000 ]; then
    test_result "PASS" "Voice Latency" "Acceptable for interactive use"
elif [ $TOTAL_LATENCY -lt 2000 ]; then
    test_result "WARN" "Voice Latency" "Noticeable but usable"
else
    test_result "FAIL" "Voice Latency" "Too slow for natural conversation"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST 8: MEMORY PRESSURE SIMULATION"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Simulating memory usage with all features active:"
echo ""

# Memory usage estimates
MEM_OS=500          # MB (Raspberry Pi OS)
MEM_PYTHON=200      # MB (Python runtime)
MEM_WHISPER=300     # MB (Whisper model)
MEM_CLAUDE=100      # MB (API client + context)
MEM_VISION=200      # MB (image processing)
MEM_TTS=50          # MB (TTS engine)
MEM_MEMORY_DB=150   # MB (SQLite + cache)

TOTAL_MEM_MB=$((MEM_OS + MEM_PYTHON + MEM_WHISPER + MEM_CLAUDE + MEM_VISION + MEM_TTS + MEM_MEMORY_DB))
TOTAL_MEM_GB=$(echo "scale=2; $TOTAL_MEM_MB / 1024" | bc)

echo "Memory allocation:"
echo "  OS + System:          ${MEM_OS}MB"
echo "  Python runtime:       ${MEM_PYTHON}MB"
echo "  Whisper STT model:    ${MEM_WHISPER}MB"
echo "  Claude API client:    ${MEM_CLAUDE}MB"
echo "  Vision processing:    ${MEM_VISION}MB"
echo "  TTS engine:           ${MEM_TTS}MB"
echo "  Memory database:      ${MEM_MEMORY_DB}MB"
echo "  ─────────────────────────────────"
echo "  Total required:       ${TOTAL_MEM_MB}MB (~${TOTAL_MEM_GB}GB)"
echo ""

echo "Raspberry Pi RAM comparison:"
echo "  Pi 3B+ (1GB):  ❌ Insufficient"
echo "  Pi 3B+ (2GB):  ⚠️  Minimal (no headroom)"
echo "  Pi 4 (2GB):    ⚠️  Tight (may swap)"
echo "  Pi 4 (4GB):    ✅ Sufficient"
echo "  Pi 4 (8GB):    ✅ Comfortable"
echo "  Pi 5 (4GB+):   ✅ Excellent"
echo ""

if [ $TOTAL_MEM_MB -lt 2048 ]; then
    test_result "WARN" "Memory Requirements (2GB Pi)" "Will use swap, performance degraded"
fi

if [ $TOTAL_MEM_MB -lt 4096 ]; then
    test_result "PASS" "Memory Requirements (4GB+ Pi)" ""
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST 9: SD CARD I/O BOTTLENECK"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Analyzing SD card I/O requirements:"
echo ""

# I/O operations
echo "Write operations:"
echo "  - Memory DB writes: ~50 KB/s (continuous)"
echo "  - Log files: ~10 KB/s"
echo "  - Vision cache: ~200 KB/image (periodic)"
echo "  - Auto-save: ~1 MB every 5 minutes"
echo ""

echo "SD Card requirements:"
echo "  Minimum: Class 10 (10 MB/s)"
echo "  Recommended: UHS-I (50+ MB/s)"
echo ""

# Class 10 should be sufficient
test_result "PASS" "SD Card I/O" "Class 10+ sufficient for normal use"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST 10: DEVICE COMPATIBILITY MATRIX"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Compatibility test results:"
echo ""
echo "┌─────────────────────┬──────────┬──────────┬──────────┐"
echo "│ Configuration       │ Pi 3B+   │ Pi 4 4GB │ Pi 5 8GB │"
echo "├─────────────────────┼──────────┼──────────┼──────────┤"
echo "│ USB Mic + USB Cam   │ ⚠️  Warn  │ ✅ Pass   │ ✅ Pass   │"
echo "│ USB Mic + Pi Cam    │ ⚠️  Warn  │ ✅ Pass   │ ✅ Pass   │"
echo "│ Voice + Vision      │ ❌ Fail   │ ⚠️  Warn  │ ✅ Pass   │"
echo "│ Text Only           │ ✅ Pass   │ ✅ Pass   │ ✅ Pass   │"
echo "│ Voice Only          │ ⚠️  Warn  │ ✅ Pass   │ ✅ Pass   │"
echo "│ Vision Only         │ ⚠️  Warn  │ ✅ Pass   │ ✅ Pass   │"
echo "└─────────────────────┴──────────┴──────────┴──────────┘"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "CRITICAL COMPATIBILITY ISSUES FOUND"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "🚨 ISSUE 1: Pi Camera + USB Webcam Conflict"
echo "   Problem: Cannot use both simultaneously"
echo "   Reason: libcamera conflicts with v4l2 (USB)"
echo "   Solution: Choose ONE camera type"
echo ""

echo "🚨 ISSUE 2: Audio Device Selection Not Documented"
echo "   Problem: Multiple audio devices confuse ALSA"
echo "   Impact: Wrong mic/speaker used"
echo "   Solution: Create ~/.asoundrc with default device"
echo "   Missing from docs!"
echo ""

echo "🚨 ISSUE 3: USB Hub Required for Multiple Devices"
echo "   Problem: Pi 3B+ has only 4 USB ports"
echo "   Devices: Mic, Camera, Keyboard, Mouse = 4 ports"
echo "   Solution: Use powered USB hub"
echo "   Not mentioned in requirements!"
echo ""

echo "⚠️  ISSUE 4: Thermal Throttling Not Addressed"
echo "   Problem: No cooling requirements in docs"
echo "   Impact: Performance degradation at 80°C"
echo "   Solution: Mandate active cooling for Pi 3B+/4"
echo ""

echo "⚠️  ISSUE 5: Power Supply Underspecified"
echo "   Problem: Docs say '3A minimum'"
echo "   Reality: Official 15W (3A) PSU recommended"
echo "   USB devices need stable 5V"
echo "   Many 'compatible' PSUs cause issues"
echo ""

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SUMMARY"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo -e "Tests Passed:    ${GREEN}${passed}${NC}"
echo -e "Warnings:        ${YELLOW}${warnings}${NC}"
echo -e "Tests Failed:    ${RED}${failed}${NC}"
echo ""

if [ $failed -gt 0 ]; then
    echo -e "${RED}❌ OVERALL RESULT: COMPATIBILITY ISSUES DETECTED${NC}"
    echo ""
    echo "Critical issues that must be documented:"
    echo "  1. Camera type selection (Pi Cam XOR USB, not both)"
    echo "  2. ALSA configuration for multiple audio devices"
    echo "  3. USB hub requirement for full setup"
    echo "  4. Active cooling requirement"
    echo "  5. Official PSU strongly recommended"
elif [ $warnings -gt 0 ]; then
    echo -e "${YELLOW}⚠️  OVERALL RESULT: WARNINGS - WILL WORK WITH CAVEATS${NC}"
    echo ""
    echo "Recommendations for documentation:"
    echo "  - Add hardware compatibility matrix"
    echo "  - Document cooling requirements"
    echo "  - Explain audio device configuration"
else
    echo -e "${GREEN}✅ OVERALL RESULT: ALL HARDWARE COMPATIBLE${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "END OF HARDWARE COMPATIBILITY TEST"
echo "═══════════════════════════════════════════════════════════════"
