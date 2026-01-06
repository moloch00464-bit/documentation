#!/data/data/com.termux/files/usr/bin/bash
#
# M.O.L.O.C.H. 3.0 - Voice Diagnose
# ==================================
# Findet raus, warum termux-speech-to-text nicht funktioniert
#

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🔍 M.O.L.O.C.H. 3.0 - VOICE DIAGNOSE"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# 1. Check if termux-api package is installed
echo "📦 1. Checking termux-api package..."
if pkg list-installed | grep -q termux-api; then
    echo "   ✅ termux-api package IS installed"
    pkg list-installed | grep termux-api
else
    echo "   ❌ termux-api package NOT installed"
    echo "   → Run: pkg install termux-api"
    exit 1
fi
echo ""

# 2. Check which termux commands are available
echo "🔧 2. Available termux-* commands:"
ls $PREFIX/bin/termux-* 2>/dev/null | while read cmd; do
    basename "$cmd"
done
echo ""

# 3. Check if termux-speech-to-text exists
echo "🎤 3. Checking termux-speech-to-text..."
if command -v termux-speech-to-text &>/dev/null; then
    echo "   ✅ termux-speech-to-text EXISTS"
    echo "   Path: $(which termux-speech-to-text)"
else
    echo "   ❌ termux-speech-to-text NOT FOUND"
    echo "   → This is the problem!"
    exit 1
fi
echo ""

# 4. Check if termux-camera-photo exists (for comparison)
echo "📸 4. Checking termux-camera-photo (Vision)..."
if command -v termux-camera-photo &>/dev/null; then
    echo "   ✅ termux-camera-photo EXISTS"
else
    echo "   ❌ termux-camera-photo NOT FOUND"
fi
echo ""

# 5. Test termux-speech-to-text (quick test)
echo "🧪 5. Testing termux-speech-to-text..."
echo "   Running: termux-speech-to-text --help"
termux-speech-to-text --help 2>&1 | head -5
echo ""

# 6. Check Termux:API app
echo "📱 6. Checking Termux:API app..."
if pm list packages | grep -q com.termux.api; then
    echo "   ✅ Termux:API app IS installed"
else
    echo "   ❌ Termux:API app NOT installed"
    echo "   → Install from F-Droid or Play Store"
fi
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "✅ DIAGNOSE COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
