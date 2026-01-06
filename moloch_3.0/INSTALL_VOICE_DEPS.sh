#!/data/data/com.termux/files/usr/bin/bash
#
# M.O.L.O.C.H. 3.0 - Voice Dependencies Installation
# ====================================================
# Installiert alle Dependencies für Voice (20s fixed recording)
#

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🎤 M.O.L.O.C.H. 3.0 - VOICE DEPENDENCIES INSTALLATION"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# 1. Install ffmpeg (for audio conversion)
echo "📦 1. Installing ffmpeg..."
pkg install ffmpeg -y
echo ""

# 2. Install Python speech_recognition library
echo "📦 2. Installing Python SpeechRecognition..."
pip install SpeechRecognition
echo ""

# 3. Install PyAudio (optional, for better audio handling)
echo "📦 3. Installing PyAudio (optional)..."
pip install pyaudio || echo "⚠️ PyAudio installation failed (optional, not critical)"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "✅ INSTALLATION COMPLETE!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Voice ist jetzt bereit:"
echo "- ✅ 20 Sekunden fixe Aufnahme"
echo "- ✅ KOSTENLOS (Google Web Speech API)"
echo "- ✅ Kein Auto-Stopp bei Pausen!"
echo ""
echo "Teste jetzt:"
echo "  python3 moloch_3.0/moloch3_unified.py"
echo ""
