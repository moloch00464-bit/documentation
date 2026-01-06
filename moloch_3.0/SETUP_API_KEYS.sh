#!/bin/bash
###############################################################################
# M.O.L.O.C.H. 3.0 - API KEYS SETUP
# ==================================
# Prüft und konfiguriert API Keys (einmalig!)
###############################################################################

echo "════════════════════════════════════════════════════════════════"
echo "  M.O.L.O.C.H. 3.0 - API KEYS SETUP"
echo "════════════════════════════════════════════════════════════════"
echo ""

BASHRC="$HOME/.bashrc"

###############################################################################
# CHECK IF KEYS ARE ALREADY SET
###############################################################################

echo "🔍 Prüfe ob API Keys bereits konfiguriert sind..."
echo ""

# Load current .bashrc to check
source "$BASHRC" 2>/dev/null || true

ANTHROPIC_SET=false
OPENAI_SET=false

# Check if keys are set
if [ -n "$ANTHROPIC_API_KEY" ] && [ ${#ANTHROPIC_API_KEY} -gt 20 ]; then
    echo "✅ ANTHROPIC_API_KEY gefunden: ${ANTHROPIC_API_KEY:0:10}...${ANTHROPIC_API_KEY: -4}"
    ANTHROPIC_SET=true
else
    echo "⚠️  ANTHROPIC_API_KEY nicht gefunden oder zu kurz"
fi

if [ -n "$OPENAI_API_KEY" ] && [ ${#OPENAI_API_KEY} -gt 20 ]; then
    echo "✅ OPENAI_API_KEY gefunden: ${OPENAI_API_KEY:0:10}...${OPENAI_API_KEY: -4}"
    OPENAI_SET=true
else
    echo "⚠️  OPENAI_API_KEY nicht gefunden oder zu kurz"
fi

echo ""

###############################################################################
# IF BOTH KEYS ARE SET - DONE!
###############################################################################

if [ "$ANTHROPIC_SET" = true ] && [ "$OPENAI_SET" = true ]; then
    echo "════════════════════════════════════════════════════════════════"
    echo "  ✅ API KEYS BEREITS KONFIGURIERT!"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "Beide API Keys sind bereits in ~/.bashrc gesetzt."
    echo "M.O.L.O.C.H. 3.0 kann direkt benutzt werden!"
    echo ""
    echo "Falls du die Keys ändern möchtest:"
    echo "  nano ~/.bashrc"
    echo "  # Suche nach ANTHROPIC_API_KEY und OPENAI_API_KEY"
    echo ""
    exit 0
fi

###############################################################################
# ASK FOR MISSING KEYS
###############################################################################

echo "════════════════════════════════════════════════════════════════"
echo "  📝 API KEYS KONFIGURIEREN"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "M.O.L.O.C.H. 3.0 braucht 2 API Keys:"
echo ""
echo "1. ANTHROPIC_API_KEY (für Claude - Chat & Vision)"
echo "   → Holen auf: https://console.anthropic.com/settings/keys"
echo ""
echo "2. OPENAI_API_KEY (für Whisper - Voice Input)"
echo "   → Holen auf: https://platform.openai.com/api-keys"
echo ""
echo "Die Keys werden EINMALIG in ~/.bashrc gespeichert."
echo "Danach funktioniert M.O.L.O.C.H. automatisch!"
echo ""

# Backup .bashrc
cp "$BASHRC" "$BASHRC.backup_$(date +%Y%m%d_%H%M%S)"
echo "💾 Backup erstellt: $BASHRC.backup_$(date +%Y%m%d_%H%M%S)"
echo ""

###############################################################################
# ASK FOR ANTHROPIC KEY (if not set)
###############################################################################

if [ "$ANTHROPIC_SET" = false ]; then
    echo "────────────────────────────────────────────────────────────────"
    echo "1️⃣  ANTHROPIC API KEY"
    echo "────────────────────────────────────────────────────────────────"
    echo ""
    echo "Dein Anthropic API Key (startet mit sk-ant-):"
    read -r ANTHROPIC_KEY

    # Validate
    if [ -z "$ANTHROPIC_KEY" ] || [ ${#ANTHROPIC_KEY} -lt 20 ]; then
        echo "❌ FEHLER: Ungültiger API Key (zu kurz oder leer)"
        echo "   Bitte Script nochmal ausführen!"
        exit 1
    fi

    # Add to .bashrc
    echo "" >> "$BASHRC"
    echo "# M.O.L.O.C.H. 3.0 - Anthropic API Key (hinzugefügt $(date +%Y-%m-%d))" >> "$BASHRC"
    echo "export ANTHROPIC_API_KEY=\"$ANTHROPIC_KEY\"" >> "$BASHRC"

    echo "✅ ANTHROPIC_API_KEY wurde in ~/.bashrc gespeichert"
    echo ""
fi

###############################################################################
# ASK FOR OPENAI KEY (if not set)
###############################################################################

if [ "$OPENAI_SET" = false ]; then
    echo "────────────────────────────────────────────────────────────────"
    echo "2️⃣  OPENAI API KEY"
    echo "────────────────────────────────────────────────────────────────"
    echo ""
    echo "Dein OpenAI API Key (startet mit sk-):"
    read -r OPENAI_KEY

    # Validate
    if [ -z "$OPENAI_KEY" ] || [ ${#OPENAI_KEY} -lt 20 ]; then
        echo "❌ FEHLER: Ungültiger API Key (zu kurz oder leer)"
        echo "   Bitte Script nochmal ausführen!"
        exit 1
    fi

    # Add to .bashrc
    echo "" >> "$BASHRC"
    echo "# M.O.L.O.C.H. 3.0 - OpenAI API Key (hinzugefügt $(date +%Y-%m-%d))" >> "$BASHRC"
    echo "export OPENAI_API_KEY=\"$OPENAI_KEY\"" >> "$BASHRC"

    echo "✅ OPENAI_API_KEY wurde in ~/.bashrc gespeichert"
    echo ""
fi

###############################################################################
# RELOAD BASHRC
###############################################################################

echo "🔄 Lade ~/.bashrc neu..."
source "$BASHRC"
echo ""

###############################################################################
# VERIFY
###############################################################################

echo "✅ VERIFICATION:"
echo ""

if [ -n "$ANTHROPIC_API_KEY" ] && [ ${#ANTHROPIC_API_KEY} -gt 20 ]; then
    echo "   ✅ ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:0:10}...${ANTHROPIC_API_KEY: -4}"
else
    echo "   ❌ ANTHROPIC_API_KEY nicht geladen!"
fi

if [ -n "$OPENAI_API_KEY" ] && [ ${#OPENAI_API_KEY} -gt 20 ]; then
    echo "   ✅ OPENAI_API_KEY: ${OPENAI_API_KEY:0:10}...${OPENAI_API_KEY: -4}"
else
    echo "   ❌ OPENAI_API_KEY nicht geladen!"
fi

echo ""

###############################################################################
# DONE
###############################################################################

echo "════════════════════════════════════════════════════════════════"
echo "  ✅ API KEYS KONFIGURIERT!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Die API Keys sind jetzt in ~/.bashrc gespeichert."
echo "Bei jedem Termux-Start werden sie automatisch geladen!"
echo ""
echo "🎉 M.O.L.O.C.H. 3.0 ist jetzt einsatzbereit!"
echo ""
echo "NÄCHSTE SCHRITTE:"
echo "  1. bash ~/documentation/moloch_3.0/MIGRATE_FROM_2.0.sh"
echo "  2. bash ~/documentation/moloch_3.0/FIX_WIDGETS.sh"
echo "  3. python3 ~/documentation/moloch_3.0/moloch3_unified.py"
echo ""
