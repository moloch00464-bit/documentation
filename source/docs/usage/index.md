---
title: Usage Guide
description: "How to use M.O.L.O.C.H. 3.0 on Raspberry Pi"
---

# Using M.O.L.O.C.H. 3.0

Welcome to the M.O.L.O.C.H. 3.0 usage guide! This section covers how to interact with and use all features of your autonomous AI system.

## Quick Start

After installation, M.O.L.O.C.H. 3.0 can be run in different modes depending on your needs.

### Running M.O.L.O.C.H.

Navigate to your installation directory and activate the virtual environment:

```bash
cd ~/moloch_3.0
source venv/bin/activate
```

Then choose your preferred mode:

#### Text Mode (Default)

Basic text-based interaction:

```bash
python3 moloch3.py
```

**Best for:**
- Testing and debugging
- Low-resource situations
- SSH/headless operation
- Basic AI interaction

---

#### Voice Mode

Full voice interaction with speech recognition and synthesis:

```bash
python3 moloch3_voice.py
```

**Features:**
- Speech-to-Text (Whisper)
- Text-to-Speech (multiple engines)
- Automatic silence detection
- Natural conversation flow

**Requirements:**
- USB microphone or audio HAT
- Speakers or headphones
- Audio configured and tested

---

#### Vision Mode

Add camera capabilities to your interactions:

```bash
python3 moloch3_vision.py
```

**Features:**
- Camera capture and analysis
- Claude Vision API integration
- Image description and OCR
- Visual memory storage

**Requirements:**
- Raspberry Pi Camera Module or USB webcam
- Camera enabled in raspi-config
- Sufficient lighting

---

#### Unified Mode (Recommended)

All features enabled - voice, vision, and full autonomy:

```bash
python3 moloch3_unified.py
```

**Features:**
- Complete autonomous operation
- Voice + Vision + Memory
- All tools and integrations
- Maximum capabilities

**Requirements:**
- All hardware configured
- Minimum 4GB RAM recommended
- Sufficient API credits

---

## Basic Interaction

### Starting a Conversation

**Text Mode:**
Simply type your message and press Enter.

**Voice Mode:**
1. Start speaking after the "Listening..." prompt
2. Stop speaking when done
3. M.O.L.O.C.H. detects silence and processes
4. Response is spoken back to you

**Vision Mode:**
Use commands like:
- "Take a photo"
- "What do you see?"
- "Analyze this image"
- "Read the text in the image"

### Common Commands

M.O.L.O.C.H. understands natural language, but here are some useful patterns:

#### File Operations
```
"Read the file /home/pi/config.txt"
"List all Python files in this directory"
"Create a file called notes.txt with..."
"Search for the word 'config' in all files"
```

#### System Operations
```
"Check the CPU temperature"
"Show disk usage"
"What processes are running?"
"Check network connectivity"
```

#### Web Search
```
"Search the web for Raspberry Pi 5 specs"
"What's the current weather in Berlin?"
"Find the latest Python documentation"
```

#### Memory & History
```
"What did we talk about yesterday?"
"Search my memory for conversations about AI"
"Show me statistics for this week"
"What was the first thing I asked you?"
```

#### Vision Commands (Unified/Vision Mode)
```
"Take a picture and describe it"
"What objects are in the image?"
"Read any text you can see"
"Compare this to the last image"
```

---

## Features Deep Dive

### Voice Interaction

M.O.L.O.C.H. uses advanced voice processing for natural conversation:

**Speech Recognition:**
- Whisper STT (OpenAI) - highly accurate
- Multiple language support
- Noise filtering

**Speech Synthesis:**
- Multiple TTS engines (pyttsx3, espeak, festival)
- Adjustable voice speed and volume
- Different voice profiles

**Silence Detection:**
- Automatic end-of-speech detection
- Configurable silence threshold
- No need to press buttons

**Tips for Best Results:**
- Speak clearly at normal pace
- Minimize background noise
- Position microphone 6-12 inches away
- Test audio levels first

---

### Vision Capabilities

Use your camera for visual understanding:

**What M.O.L.O.C.H. Can See:**
- Objects and their positions
- Text in images (OCR)
- Scenes and environments
- People (with privacy considerations)
- Colors, shapes, patterns

**Vision Memory:**
- All captured images are stored
- Timestamped and contextualized
- Can be referenced in future conversations
- Search through past images

**Example Use Cases:**
- "What's in my fridge?" (point camera)
- "Read this printed document"
- "Identify this plant/object"
- "Is anyone at the door?"
- "What time does this clock show?"

---

### Memory System

M.O.L.O.C.H. remembers everything:

**Short-Term Memory:**
- Current conversation (last 100k tokens)
- Recent interactions and context
- Active themes and topics

**Long-Term Memory:**
- All conversations stored in SQLite
- Efficient retrieval and search
- Context-aware recall
- Never forgets (unless you delete it)

**Memory Features:**
- Full-text search
- Date/time filtering
- Theme-based organization
- Statistics and analytics

**Viewing Your Memory:**
```bash
# View memory database
sqlite3 moloch_3.0/data/memory.db "SELECT * FROM conversations LIMIT 10;"

# Search memory
sqlite3 moloch_3.0/data/memory.db "SELECT * FROM conversations WHERE content LIKE '%raspberry%';"
```

---

### Personality & Autonomy

M.O.L.O.C.H. has adaptive personality characteristics:

**Personality Traits:**
- Formality level
- Verbosity (detail level)
- Creativity
- Emotional tone

**Zeit-Awareness:**
- Always knows current date/time
- Tracks session duration
- Understands temporal context
- Time-based behaviors

**Mood Detection:**
- Analyzes conversation sentiment
- Adapts responses accordingly
- Maintains conversation flow
- Context-appropriate behavior

---

## Configuration During Use

### Adjusting Settings

While running, you can ask M.O.L.O.C.H. to:

- "Speak faster/slower"
- "Be more concise"
- "Give more details"
- "Use a different voice"
- "Save the current conversation"

### Checking Status

Ask about system status:

- "What's your current configuration?"
- "Show me statistics"
- "How much memory are you using?"
- "What's the CPU temperature?"
- "How long have we been talking?"

---

## Advanced Usage

### Tool Integration

M.O.L.O.C.H. can execute bash commands safely:

```
"Run htop and show me the output"
"Check GPIO pin 17 status"
"Download a file from this URL"
"Compress this directory"
```

**Safety Features:**
- Dangerous commands are filtered
- Confirmation for destructive operations
- Error handling and recovery
- Logged for audit

### Automation

Create custom workflows:

```
"Every morning at 8am, check the weather and tell me"
"Monitor the CPU temperature and alert if over 75°C"
"Take a photo every hour and describe changes"
```

(Note: Scheduler feature planned for future release)

---

## Best Practices

### For Voice Mode

✅ **Do:**
- Test audio before extended use
- Use quality microphone
- Minimize background noise
- Speak naturally
- Let M.O.L.O.C.H. finish speaking

❌ **Don't:**
- Interrupt during speech synthesis
- Use in very noisy environments
- Speak too quietly or too far away
- Forget to check audio levels

### For Vision Mode

✅ **Do:**
- Ensure adequate lighting
- Hold camera steady
- Point at subject clearly
- Wait for capture confirmation
- Review captured images

❌ **Don't:**
- Use in very dark conditions
- Move camera during capture
- Point at sensitive/private content without consideration
- Exceed storage limits

### For Performance

✅ **Do:**
- Monitor CPU temperature
- Close unused applications
- Use appropriate mode for task
- Regular system updates
- Clean up old logs

❌ **Don't:**
- Run all features on low-RAM Pi
- Neglect cooling
- Fill up storage
- Use Opus model on Pi 3B+
- Forget to check API usage

---

## Stopping M.O.L.O.C.H.

To gracefully exit:

**Text Mode:**
Type: `exit`, `quit`, or press `Ctrl+C`

**Voice Mode:**
Say: "Exit", "Quit", "Goodbye" or press `Ctrl+C`

**Emergency Stop:**
Press `Ctrl+C` twice quickly

**From Another Terminal:**
```bash
pkill -f moloch3
# or
killall python3
```

---

## Next Steps

- **[Voice Commands](/docs/usage/voice.md)** - Detailed voice interaction guide
- **[Vision Guide](/docs/usage/vision.md)** - Master camera features
- **[Memory Management](/docs/usage/memory.md)** - Work with memory system
- **[Configuration](/docs/configuration/basic.md)** - Customize settings
- **[Troubleshooting](/docs/use/troubleshooting/diagnostics.md)** - Fix issues

---

**Need help?** Join the discussion on [GitHub Issues](https://github.com/moloch00464-bit/documentation/issues).
