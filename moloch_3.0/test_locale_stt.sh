#!/bin/bash
# Test: termux-speech-to-text mit verschiedenen LOCALE Settings

echo "═══════════════════════════════════════════════════════════════"
echo "🔬 TEST: termux-speech-to-text mit LOCALE ENV Variables"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "📊 Aktuelle Environment:"
echo "LANG=$LANG"
echo "LC_ALL=$LC_ALL"
echo "LANGUAGE=$LANGUAGE"
echo ""

echo "─────────────────────────────────────────────────────────────"
echo "TEST 1: Mit LANG=de_DE.UTF-8"
echo "─────────────────────────────────────────────────────────────"
echo "Sprich: 'Das ist ein Test auf Deutsch'"
echo ""

export LANG=de_DE.UTF-8
export LC_ALL=de_DE.UTF-8
export LANGUAGE=de:en

termux-speech-to-text

echo ""
echo "═══════════════════════════════════════════════════════════════"
