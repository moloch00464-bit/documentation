#!/usr/bin/env python3
"""
Quick API Model Test
Tests if the Claude model name works
"""

import os
import sys
import requests

# Add moloch_3.0 to path
sys.path.insert(0, '/home/user/documentation/moloch_3.0')

from core.config import CLAUDE_MODEL, ANTHROPIC_API_KEY

print("═" * 60)
print("M.O.L.O.C.H. 3.0 - API Model Test")
print("═" * 60)
print()

# Check API key
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set!")
    print("   Run: export ANTHROPIC_API_KEY='your-key'")
    sys.exit(1)

print(f"✅ API Key found: {ANTHROPIC_API_KEY[:20]}...")
print(f"📡 Testing model: {CLAUDE_MODEL}")
print()

# Test API
try:
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers={
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        },
        json={
            'model': CLAUDE_MODEL,
            'max_tokens': 50,
            'messages': [{'role': 'user', 'content': 'Sag nur "MOLOCH LEBT!" auf Deutsch.'}]
        }
    )

    print(f"Status: {response.status_code}")
    print()

    if response.status_code == 200:
        print("✅ API & MODEL FUNKTIONIEREN!")
        print()
        data = response.json()
        if 'content' in data and len(data['content']) > 0:
            text = data['content'][0].get('text', '')
            print(f"🤖 Claude antwortet: {text}")
    elif response.status_code == 401:
        print("❌ 401 Unauthorized - API Key falsch!")
    elif response.status_code == 404:
        print(f"❌ 404 Not Found - Model '{CLAUDE_MODEL}' existiert nicht!")
        print()
        print("Verfügbare Modelle sollten sein:")
        print("  - claude-sonnet-4-5-20250929 (Sonnet 4.5)")
        print("  - claude-opus-4-5-20251101 (Opus 4.5)")
    else:
        print(f"❌ Fehler {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

print()
print("═" * 60)
