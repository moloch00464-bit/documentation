---
title: System Requirements
description: "Hardware and software requirements for M.O.L.O.C.H. 3.0 on Raspberry Pi"
---

# System Requirements

This page outlines the hardware and software requirements for running M.O.L.O.C.H. 3.0 on Raspberry Pi.

## Hardware Requirements

### Minimum Specifications

- **Raspberry Pi Model**: 3B+ or newer
- **RAM**: 2GB minimum
- **Storage**: 16GB SD card minimum
- **Audio**: USB microphone or audio HAT
- **Network**: WiFi or Ethernet connection

!!! warning
    While M.O.L.O.C.H. 3.0 can run on a Raspberry Pi 3B+ with 2GB RAM, performance will be limited. You may experience slower response times and need to reduce context window size.

### Recommended Specifications

- **Raspberry Pi Model**: 4 (4GB+) or Raspberry Pi 5 (8GB)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 64GB+ SD card (Class 10 or UHS-I)
- **Audio**:
  - USB microphone with noise cancellation
  - Quality speakers or headphones
  - Optional: HiFiBerry or similar audio HAT
- **Camera**: Raspberry Pi Camera Module v2/v3 or USB webcam
- **Network**: Gigabit Ethernet or 5GHz WiFi
- **Optional**: Active cooling (fan or heatsink)

### Performance Comparison

| Model | RAM | Voice Mode | Vision Mode | Unified Mode | Notes |
|-------|-----|------------|-------------|--------------|-------|
| Pi 3B+ | 1GB | ❌ Not recommended | ❌ Not recommended | ❌ Not recommended | Insufficient RAM |
| Pi 3B+ | 2GB | ⚠️ Limited | ❌ Not recommended | ❌ Not recommended | Text mode only recommended |
| Pi 4 | 2GB | ⚠️ Limited | ⚠️ Limited | ❌ Not recommended | Reduce context size |
| Pi 4 | 4GB | ✅ Good | ✅ Good | ⚠️ Limited | Recommended minimum |
| Pi 4 | 8GB | ✅ Excellent | ✅ Excellent | ✅ Good | Recommended |
| Pi 5 | 4GB | ✅ Excellent | ✅ Excellent | ✅ Good | Fast performance |
| Pi 5 | 8GB | ✅ Excellent | ✅ Excellent | ✅ Excellent | Best performance |

## Software Requirements

### Operating System

- **Raspberry Pi OS Bookworm** (Debian 12) or newer
- **Architecture**: 64-bit recommended (32-bit supported but limited)
- **Desktop**: Not required (can run headless)

### Python Environment

- **Python Version**: 3.9 or newer (3.11+ recommended)
- **Virtual Environment**: Required (venv or conda)
- **Pip**: Latest version

### System Packages

Required system packages (installed via apt):

```
portaudio19-dev
python3-pyaudio
espeak
ffmpeg
libcamera-apps
python3-picamera2
git
```

Optional packages for enhanced features:

```
festival
festvox-kallpc16k
pulseaudio
alsa-utils
```

## API Requirements

### Required API Access

- **Anthropic API Key** - For Claude AI access
  - Minimum: Claude Sonnet access
  - Recommended: Claude Opus access
  - Get your key: [console.anthropic.com](https://console.anthropic.com/)

### Optional API Access

- **OpenAI API Key** - For Whisper STT
  - Alternative: Use local Whisper model (requires more RAM)
  - Get your key: [platform.openai.com](https://platform.openai.com/)

### API Credit Recommendations

Based on typical usage patterns:

| Usage Level | Daily Interactions | Monthly API Cost (Estimated) |
|-------------|-------------------|------------------------------|
| Light | 10-20 exchanges | $5-15 (Sonnet) / $15-30 (Opus) |
| Medium | 50-100 exchanges | $20-40 (Sonnet) / $50-100 (Opus) |
| Heavy | 200+ exchanges | $50-100 (Sonnet) / $150-300 (Opus) |

!!! note
    Vision features consume more API credits. Each image analysis can cost 2-5x a text-only exchange.

## Network Requirements

### Bandwidth

- **Minimum**: 1 Mbps down / 512 Kbps up
- **Recommended**: 10 Mbps down / 2 Mbps up
- **With Vision**: 25 Mbps down / 5 Mbps up

### Connectivity

- **Latency**: <200ms to api.anthropic.com recommended
- **Reliability**: Stable connection required (no data caps recommended)
- **Ports**: HTTPS (443) outbound access required

### Whitelisted Domains

Ensure your network allows access to:

- `api.anthropic.com` (Claude API)
- `api.openai.com` (Optional: Whisper STT)
- `pypi.org` (Package installation)

## Storage Requirements

### Minimum Storage Breakdown

- **System + OS**: 4GB
- **M.O.L.O.C.H. 3.0**: 500MB
- **Python Environment**: 1GB
- **Memory Database**: 500MB (grows over time)
- **Logs**: 200MB
- **Free Space Buffer**: 2GB

**Total Minimum**: 16GB SD card

### Recommended Storage Breakdown

- **System + OS**: 8GB
- **M.O.L.O.C.H. 3.0**: 1GB (with models)
- **Python Environment**: 2GB
- **Memory Database**: 5GB (extensive history)
- **Logs & Debugging**: 1GB
- **Vision Cache**: 2GB
- **Free Space Buffer**: 10GB

**Total Recommended**: 64GB SD card

### Storage Growth Over Time

The memory database grows based on your usage:

- **Text-only**: ~1MB per day
- **Voice interactions**: ~5MB per day
- **Vision features**: ~20MB per day (with cached images)

## Audio Hardware

### Microphone Requirements

**Minimum**:
- USB microphone with basic audio input
- 16kHz+ sampling rate

**Recommended**:
- USB microphone with noise cancellation
- 44.1kHz sampling rate
- Cardioid or unidirectional pickup pattern
- Examples:
  - Blue Snowball
  - Samson Meteor
  - Rode NT-USB Mini

**Budget Options**:
- PlayStation Eye Camera (good built-in mic array)
- USB webcam with integrated mic

### Speaker/Output Requirements

**Minimum**:
- 3.5mm headphones or speakers
- Basic audio output

**Recommended**:
- USB speakers or DAC
- Quality headphones for clear TTS output
- HiFiBerry DAC+ for audiophile quality

## Camera Hardware (Optional)

Required only if using vision features:

### Raspberry Pi Camera Module

- **V2**: 8MP, good quality
- **V3**: 12MP, excellent quality with autofocus
- **HQ Camera**: 12MP, interchangeable lens support

### USB Webcam

- Minimum 720p resolution
- USB 2.0 or better
- Auto-focus recommended
- Examples:
  - Logitech C270
  - Logitech C920
  - Microsoft LifeCam

## Power Requirements

Proper power supply is critical for stable operation:

| Model | Minimum PSU | Recommended PSU | Notes |
|-------|-------------|-----------------|-------|
| Pi 3B+ | 2.5A (12.5W) | 3A (15W) | USB-C or micro-USB |
| Pi 4 | 3A (15W) | 5A (25W) | USB-C with e-marker |
| Pi 5 | 5A (25W) | 5A (27W) | USB-C PD required |

!!! danger
    Insufficient power can cause:
    - Random crashes and reboots
    - Audio glitches and distortion
    - SD card corruption
    - USB device failures

    Always use the official Raspberry Pi power supply or a quality alternative.

## Thermal Considerations

M.O.L.O.C.H. 3.0 can be CPU-intensive, especially with voice and vision processing:

### Cooling Solutions

**Passive (Minimum)**:
- Aluminum heatsinks on CPU, RAM, USB controller
- Open-air case design

**Active (Recommended)**:
- 30mm or 40mm cooling fan (5V)
- Official Raspberry Pi Active Cooler
- Argon ONE or similar cases with integrated cooling

### Temperature Limits

- **Idle**: 35-45°C acceptable
- **Under Load**: 50-70°C acceptable
- **Throttling**: Begins at 80°C (performance reduced)
- **Critical**: 85°C (automatic shutdown protection)

Monitor temperature with:

```bash
vcgencmd measure_temp
```

## Comparison: Raspberry Pi vs. Termux

| Feature | Raspberry Pi | Termux (Android) |
|---------|--------------|------------------|
| Performance | Better (dedicated hardware) | Limited (shared resources) |
| Audio Quality | Excellent (dedicated I/O) | Variable (device dependent) |
| Camera | Better (Pi Camera or USB) | Good (device camera) |
| Power Usage | 5-15W constant | Battery-dependent |
| Portability | Stationary | Highly portable |
| GPIO Access | Yes | No |
| 24/7 Operation | Ideal | Not recommended |
| Setup Complexity | Moderate | Easy |

## Next Steps

Once you've verified your system meets these requirements:

1. **[Installation Guide](/docs/installation/raspberry-pi.md)** - Begin the setup process
2. **[Configuration](/docs/configuration/basic.md)** - Configure API keys and preferences
3. **[Usage Guide](/docs/usage/index.md)** - Start using M.O.L.O.C.H.

---

**Questions?** Check the [FAQ](/docs/faq/index.md) or [open an issue](https://github.com/moloch00464-bit/documentation/issues).
