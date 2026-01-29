# 🚀 How to Run AutoShorts AI

## Quick Start (3 Steps)

### Step 1: Setup Environment

```bash
# Navigate to project directory
cd C:\Users\hp\.gemini\antigravity\scratch\autoshorts_ai

# Create virtual environment (if not already done)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (if not already done)
pip install -r requirements.txt
```

### Step 2: Configure API Keys

```bash
# Copy example environment file
copy config\.env.example .env

# Edit .env file and add your OpenAI API key
notepad .env
```

**Minimum required in `.env`:**
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 3: Run!

```bash
# Generate your first video
python main.py generate --niche self-improvement
```

---

## 📋 All Available Commands

### 1. Generate Single Video

```bash
# Auto-research trending topic
python main.py generate --niche self-improvement

# Specific topic
python main.py generate --niche finance --topic "5 Ways to Save Money"

# With auto-publishing (requires social media API keys)
python main.py generate --niche technology --publish
```

**What happens:**
1. Researches trending topics (or uses your topic)
2. Generates script with GPT-4
3. Plans visuals
4. Generates/fetches media assets
5. Creates voiceover with OpenAI TTS
6. Assembles video with MoviePy
7. Generates SEO-optimized metadata
8. (Optional) Publishes to YouTube/Instagram

### 2. Batch Generate Multiple Videos

```bash
# Create 5 videos
python main.py batch --count 5 --niche self-improvement

# Create 3 videos and publish them
python main.py batch --count 3 --niche finance --publish
```

### 3. Continuous Mode (Automated Scheduling)

```bash
# Daily automation (posts at 12pm and 6pm)
python main.py run --frequency daily --niche self-improvement

# Hourly automation
python main.py run --frequency hourly --videos-per-run 1

# Weekly automation (Mondays at 10am, creates 3 videos)
python main.py run --frequency weekly --videos-per-run 3 --publish
```

**Press Ctrl+C to stop continuous mode**

### 4. Check System Status

```bash
python main.py status
```

### 5. Run Examples (Test System)

```bash
# Run example usage script
python example_usage.py
```

---

## 🎯 Recommended First Run

**Start with this to test everything:**

```bash
# 1. Activate environment
venv\Scripts\activate

# 2. Generate a test video (won't publish)
python main.py generate --niche self-improvement

# 3. Check the output
# Video will be in: data/videos/
# Audio will be in: data/audio/
# Assets will be in: data/assets/
```

---

## 📁 Where to Find Output

After running, check these directories:

```
data/
├── videos/          # Final videos (.mp4)
├── audio/           # Voiceover files (.mp3)
├── assets/          # Visual assets (images/videos)
├── cache/           # Temporary files
└── logs/            # System logs
```

---

## ⚙️ Configuration Options

### Available Niches

You can use any niche, but these are optimized:
- `self-improvement`
- `finance`
- `technology`
- `health`
- `business`
- `motivation`

### Command Line Arguments

**For `generate` command:**
```bash
--niche [NICHE]      # Content niche
--topic [TOPIC]      # Specific topic (optional)
--publish            # Auto-publish after creation
```

**For `batch` command:**
```bash
--count [N]          # Number of videos to create
--niche [NICHE]      # Content niche
--publish            # Auto-publish all videos
```

**For `run` command:**
```bash
--frequency [hourly|daily|weekly]  # Scheduling frequency
--niche [NICHE]                    # Content niche
--videos-per-run [N]               # Videos per scheduled run
--publish                          # Auto-publish videos
```

---

## 🔧 Troubleshooting

### "OpenAI API key not found"

**Solution:** Make sure you've created `.env` file with your API key:
```bash
copy config\.env.example .env
notepad .env
# Add: OPENAI_API_KEY=sk-your-key-here
```

### "MoviePy font errors"

**Solution:** Install ImageMagick:
```bash
# Download from: https://imagemagick.org/script/download.php
# Or use Chocolatey:
choco install imagemagick
```

### "Module not found" errors

**Solution:** Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Videos are just placeholders

**Reason:** Some APIs need keys to work fully:
- Stock footage: Needs Pexels/Pixabay API keys
- AI images: Needs Stability AI key
- Platform scraping: Needs implementation

**Current functionality with OpenAI only:**
- ✅ Script generation
- ✅ Voiceover creation
- ✅ Metadata generation
- ⚠️ Video assembly (works but needs real assets)

---

## 💰 Cost Tracking

With OpenAI API only:
- **Per video:** ~$0.15-0.20
- **Per day (2 videos):** ~$0.40
- **Per month (60 videos):** ~$10-12

Monitor costs in your OpenAI dashboard: https://platform.openai.com/usage

---

## 📊 Example Output

After running `python main.py generate --niche self-improvement`:

```
=== AutoShorts AI - Single Video Generation ===

Step 1/8: Researching trending topics...
✓ Selected topic: "5 Morning Habits That Changed My Life"

Step 2/8: Generating script...
✓ Script generated (45 seconds)

Step 3/8: Planning visuals...
✓ Storyboard created (5 scenes)

Step 4/8: Generating media assets...
✓ Assets prepared

Step 5/8: Generating voiceover...
✓ Voiceover created (data/audio/video_20260129_205500_voiceover.mp3)

Step 6/8: Assembling video...
✓ Video assembled (data/videos/video_20260129_205500_final.mp4)

Step 7/8: Generating captions and metadata...
✓ Metadata generated

Step 8/8: Skipping publishing (auto-publish disabled)

==================================================
VIDEO CREATION RESULT
==================================================
Status: completed
Video ID: video_20260129_205500
Topic: 5 Morning Habits That Changed My Life
Video Path: data/videos/video_20260129_205500_final.mp4

YouTube Title: 5 Morning Habits That Changed My Life 🌅
Instagram Caption: These 5 morning habits transformed everything...
==================================================
```

---

## 🎓 Next Steps

1. **Test basic generation** - `python main.py generate --niche self-improvement`
2. **Review output files** - Check `data/` directory
3. **Add more API keys** - For stock footage, AI images, etc.
4. **Configure publishing** - Add YouTube/Instagram credentials
5. **Run in continuous mode** - Automate video creation

---

## 🆘 Need Help?

- **Logs:** Check `data/logs/autoshorts.log`
- **Documentation:** See `README.md` and `SETUP.md`
- **Examples:** Run `python example_usage.py`
- **Architecture:** Read `walkthrough.md` in brain directory

---

**Ready to create your first video? Run:**
```bash
python main.py generate --niche self-improvement
```

🎬 **Let's go!**
