# M.O.L.O.C.H. 3.0 - Raspberry Pi Documentation

**Multi-Operational Learning & Optimization Cognitive Holographic System**

This repository contains the documentation for M.O.L.O.C.H. 3.0 - Autonomous Edition, specifically adapted for **Raspberry Pi** hardware.

## About M.O.L.O.C.H. 3.0

M.O.L.O.C.H. 3.0 is an advanced autonomous AI system featuring:

- 🎤 **Voice Interaction** - Natural conversation with Whisper STT
- 👁️ **Vision Capabilities** - Camera integration with Claude Vision API
- 🧠 **Persistent Memory** - Long-term context storage
- 🤖 **Autonomous Personality** - Adaptive behavioral characteristics
- ⏰ **Zeit-Awareness** - Complete temporal consciousness
- 🛠️ **Tool Integration** - Bash, files, web search, and more

## Documentation

The documentation is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and hosted on GitHub Pages.

**View the documentation:** [https://moloch00464-bit.github.io/documentation](https://moloch00464-bit.github.io/documentation)

## Quick Start

See the [Raspberry Pi Installation Guide](source/docs/installation/raspberry-pi.md) to get started.

## Building the Documentation Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Serve locally
mkdocs serve

# Build static site
mkdocs build
```

## Repository Structure

```
documentation/
├── source/               # Documentation source files
│   ├── docs/            # Main documentation content
│   │   ├── installation/    # Installation guides
│   │   ├── features/        # Feature documentation
│   │   ├── configuration/   # Configuration guides
│   │   └── ...
│   ├── assets/          # Images, stylesheets
│   └── index.md         # Homepage
├── mkdocs.yml           # MkDocs configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Links

- **Main Repository**: [github.com/moloch00464-bit/documentation](https://github.com/moloch00464-bit/documentation)
- **M.O.L.O.C.H. 3.0 PR**: [Pull Request #1](https://github.com/moloch00464-bit/documentation/pull/1)
- **Documentation Site**: [moloch00464-bit.github.io/documentation](https://moloch00464-bit.github.io/documentation)

## License

See [LICENSE](LICENSE) file for details.

---

**Note**: This repository was originally forked from [hacs/documentation](https://github.com/hacs/documentation) and repurposed for the M.O.L.O.C.H. 3.0 project.