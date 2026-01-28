# AutoShorts AI - Quick Setup Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd C:\Users\hp\.gemini\antigravity\scratch\autoshorts_ai
pip install -r requirements.txt
```

### Step 2: Configure API Keys

1. Copy the example environment file:
```bash
copy config\.env.example .env
```

2. Edit `.env` and add your API keys:

**Required (Minimum to test):**
```env
OPENAI_API_KEY=sk-your-key-here
```

**Optional (for full functionality):**
```env
# Text-to-Speech (alternative to OpenAI)
ELEVENLABS_API_KEY=your-key-here
ELEVENLABS_VOICE_ID=your-voice-id

# Stock Footage
PEXELS_API_KEY=your-key-here
PIXABAY_API_KEY=your-key-here

# AI Image Generation
STABILITY_AI_API_KEY=your-key-here

# Social Media Publishing
YOUTUBE_CLIENT_ID=your-client-id
YOUTUBE_CLIENT_SECRET=your-client-secret
YOUTUBE_REFRESH_TOKEN=your-refresh-token

INSTAGRAM_ACCESS_TOKEN=your-access-token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your-account-id
```

### Step 3: Test the System

```bash
# Test with example script
python example_usage.py

# Or generate a single video
python main.py generate --niche self-improvement
```

---

## 📖 Usage Examples

### Generate a Single Video

```bash
python main.py generate --niche finance --topic "5 Ways to Save Money"
```

### Batch Generate Multiple Videos

```bash
python main.py batch --count 5 --niche technology
```

### Run in Continuous Mode

```bash
# Daily automation (posts at 12pm and 6pm)
python main.py run --frequency daily --niche self-improvement --publish

# Hourly automation
python main.py run --frequency hourly --videos-per-run 1

# Weekly automation (Mondays at 10am)
python main.py run --frequency weekly --videos-per-run 3
```

### Check System Status

```bash
python main.py status
```

---

## 🎯 What Works Now

✅ **Fully Functional:**
- Complete 9-agent system
- OpenAI TTS voiceover generation
- LLM script & metadata generation
- Video assembly with MoviePy
- Continuous scheduling (hourly/daily/weekly)
- Error handling & retry logic
- Memory & learning system

⚠️ **Needs API Keys:**
- Stock footage fetching (Pexels/Pixabay)
- AI image generation (Stability AI)
- Social media publishing (YouTube/Instagram)
- Platform scraping (YouTube/Instagram/TikTok)

---

## 🔧 Troubleshooting

### MoviePy Issues

If you get font errors with MoviePy:
```bash
# Install ImageMagick
# Download from: https://imagemagick.org/script/download.php
# Or use Chocolatey:
choco install imagemagick
```

### Missing Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### API Rate Limits

Adjust in `.env`:
```env
MAX_CONCURRENT_AGENTS=3
COST_LIMIT_DAILY=10.00
```

---

## 📊 Cost Estimates

With OpenAI API only (1 video/day):

| Component | Cost/Video | Cost/Month |
|-----------|-----------|------------|
| Script (GPT-4) | $0.05 | $1.50 |
| Voiceover (TTS) | $0.10 | $3.00 |
| Metadata (GPT-4) | $0.02 | $0.60 |
| **Total** | **$0.17** | **$5.10** |

For 2 videos/day: ~$10/month
For 5 videos/day: ~$25/month

---

## 🎓 Next Steps

1. **Test with OpenAI only** (no other APIs needed)
2. **Add stock footage APIs** for better visuals
3. **Configure social media** for publishing
4. **Run in continuous mode** for automation
5. **Monitor analytics** and optimize

---

## 📁 Project Structure

```
autoshorts_ai/
├── agents/           # 9 specialized agents
├── core/             # Framework + video assembler
├── workflows/        # Pipeline + scheduler
├── config/           # Settings + logging
├── data/             # Generated content
├── main.py           # CLI entry point
└── .env              # Your API keys (create this)
```

---

## 🆘 Need Help?

1. Check logs in `data/logs/`
2. Review `walkthrough.md` for architecture details
3. See `example_usage.py` for code examples
4. Read `README.md` for full documentation

---

## ⚡ Quick Commands Reference

```bash
# Generate single video
python main.py generate --niche [NICHE]

# Batch generate
python main.py batch --count [N] --niche [NICHE]

# Continuous mode
python main.py run --frequency [hourly|daily|weekly]

# System status
python main.py status

# Test system
python example_usage.py
```

---

**You're all set! Start with `python main.py generate --niche self-improvement` to create your first video! 🎬**
