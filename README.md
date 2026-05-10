# AutoShorts AI

[![Build Status](https://github.com/shlokdhanokar/autoshorts-ai/actions/workflows/python-app.yml/badge.svg)](https://github.com/shlokdhanokar/autoshorts-ai/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end agentic AI system for automated short-form video creation and publishing.

AutoShorts AI is a fully autonomous multi-agent system that continuously creates, edits, voices, and publishes high-quality Instagram Reels and YouTube Shorts without human intervention.

### Key Features
- **9 Specialized AI Agents** working in coordination
- **Automated Trend Research** from YouTube, Instagram, TikTok, Google Trends
- **LLM-Powered Script Generation** with A/B testing
- **Intelligent Visual Planning** with stock footage and AI generation
- **Natural Voiceovers** using OpenAI TTS or ElevenLabs
- **Automated Video Editing** with captions and transitions
- **SEO-Optimized Metadata** for maximum discoverability
- **Multi-Platform Publishing** to YouTube Shorts and Instagram Reels
- **Continuous Learning** from engagement analytics

## 🚀 Quick Start
### Prerequisites


- Python 3.11+
- OpenAI API key (required)
- Optional: ElevenLabs, Pexels, Stability AI API keys
- YouTube and Instagram API credentials (for publishing)

### Installation

1. Clone or navigate to the project directory:
```bash
cd autoshorts_ai
```
2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
copy config\.env.example .env
# Edit .env with your API keys
```

### Usage

#### Generate a Single Video

```bash
python main.py generate --niche self-improvement --publish
```

#### Generate Multiple Videos (Batch)

```bash
python main.py batch --count 5 --niche finance
```

#### View System Status

```bash
python main.py status
```

## 🧠 Architecture

### Multi-Agent System

1. **Trend Research Agent** - Discovers trending topics
2. **Scriptwriting Agent** - Generates optimized scripts
3. **Visual Planning Agent** - Maps scenes to visuals
4. **Media Generation Agent** - Fetches/generates assets
5. **Voiceover Agent** - Creates natural narration
6. **Video Editing Agent** - Assembles final videos
7. **Caption & Metadata Agent** - Optimizes discoverability
8. **Publishing Agent** - Uploads to platforms
9. **Analytics Agent** - Tracks performance (coming soon)

### Workflow

```
Trend Research → Script Generation → Visual Planning →
Media Generation → Voiceover → Video Editing →
Caption/Metadata → Publishing → Analytics
```

## 📁 Project Structure

```
autoshorts_ai/
├── agents/              # Individual agent implementations
├── core/                # Base classes and orchestrator
├── workflows/           # Pipeline orchestration
├── config/              # Configuration and settings
├── data/                # Generated content and cache
│   ├── videos/          # Final videos
│   ├── assets/          # Visual assets
│   ├── audio/           # Voiceovers
│   └── cache/           # Temporary files
├── tests/               # Unit and integration tests
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

## ⚙️ Configuration

Edit `.env` file to configure:

- **API Keys**: OpenAI, ElevenLabs, Pexels, etc.
- **Social Media**: YouTube and Instagram credentials
- **System Settings**: Niche, posting frequency, cost limits
- **Content Moderation**: Safety filters, human review

## 🔧 Development Status

### ✅ Completed

- Core agent framework with memory and orchestration
- All 8 specialized agents (structure complete)
- Main workflow pipeline
- CLI interface
- Configuration system

### 🚧 In Progress

- Real API integrations (currently using placeholders)
- Actual video editing with MoviePy/FFmpeg
- Analytics and learning agent
- Continuous scheduling system

### 📋 TODO

- Implement real platform scrapers (YouTube, Instagram, TikTok)
- Integrate actual TTS, image generation, and video APIs
- Build video assembly with MoviePy
- Add OAuth flows for social media publishing
- Create web UI dashboard (optional)
- Implement cost tracking and limits
- Add content moderation filters

## 🎓 How It Works

1. **Research**: Scrapes trending topics from multiple platforms
2. **Script**: Uses GPT-4 to generate engaging scripts with hooks
3. **Plan**: Maps script to visual types (stock, AI, text)
4. **Generate**: Fetches stock footage or generates AI visuals
5. **Voice**: Creates natural voiceover with TTS
6. **Edit**: Assembles video with captions and effects
7. **Optimize**: Generates SEO titles, descriptions, hashtags
8. **Publish**: Uploads to YouTube Shorts and Instagram Reels
9. **Learn**: Analyzes performance and improves over time

## 💰 Cost Estimates

Monthly costs (varies by volume):

- **LLM (GPT-4)**: $50-150
- **TTS**: $20-100
- **AI Images**: $30-80 (if using)
- **Total**: ~$200-500/month for daily posting

## 🔒 Safety & Moderation

- Content safety filters (configurable)
- Optional human review queue
- Brand safety checks
- Rate limiting and cost controls

## 📝 License

This project is for educational and personal use.

## 🤝 Contributing

This is an autonomous system - contributions welcome for:
- Real API integrations
- Video editing improvements
- Analytics and learning algorithms
- Platform support expansion

---

**Note**: This system is currently in development. Many features use placeholders and require API integration for full functionality.
