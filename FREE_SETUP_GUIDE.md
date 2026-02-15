# 🆓 100% FREE Setup Guide

## 🎯 Run AutoShorts AI Completely FREE!

No credit card, no paid APIs, 100% open-source alternatives!
---
## 📋 What You Need (All FREE!)
### **1. Ollama (Local LLM) - 100% FREE**
- **Cost**: FREE forever
- **What it does**: Replaces OpenAI for script generation
- **Quality**: Very good (Llama 3.2, Mistral, etc.)
- **Setup time**: 5 minutes
### **2. Edge-TTS - 100% FREE**
- **Cost**: FREE forever
- **What it does**: Replaces OpenAI TTS for voiceovers
- **Quality**: Natural Microsoft voices
- **Setup time**: 1 minute (just install)

### **3. Pexels API - 100% FREE**
- **Cost**: FREE forever
- **What it does**: Stock footage
- **Limit**: 200 requests/hour (plenty!)
- **Setup time**: 2 minutes

---

## 🚀 Quick Setup (15 Minutes)

### **Step 1: Install Ollama (5 min)**

**Windows:**
```bash
# Download and install from:
https://ollama.com/download

# After installation, open PowerShell and run:
ollama pull llama3.2

# Verify it's running:
ollama list
```

**What this does**: Downloads a free, local AI model (about 2GB)

### **Step 2: Install Free Dependencies (2 min)**

```bash
# Make sure you're in the project directory
cd C:\Users\hp\.gemini\antigravity\scratch\autoshorts_ai

# Activate virtual environment
venv\Scripts\activate.bat

# Install free alternatives
pip install edge-tts ollama groq huggingface-hub
```

### **Step 3: Get Free API Keys (5 min)**

**Pexels (Stock Footage):**
1. Go to: https://www.pexels.com/api/
2. Sign up (free)
3. Get your API key

**Optional - Groq (Faster than local):**
1. Go to: https://console.groq.com/
2. Sign up (free)
3. Get your API key (free tier: 30 requests/minute)

### **Step 4: Configure .env (2 min)**

```bash
# Copy the config file
copy config\.env.example .env

# Edit .env and add:
```

**Minimal (Ollama local):**
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

TTS_PROVIDER=edge-tts

PEXELS_API_KEY=your-free-pexels-key-here
```

**Or use Groq (faster, still free):**
```env
LLM_PROVIDER=groq
GROQ_API_KEY=your-free-groq-key-here

TTS_PROVIDER=edge-tts

PEXELS_API_KEY=your-free-pexels-key-here
```

### **Step 5: Run! (1 min)**

```bash
python main.py generate --niche self-improvement
```

**That's it!** 🎉

---

## 💰 Cost Comparison

| Setup | Cost/Video | Cost/Month (30 videos) |
|-------|-----------|----------------------|
| **OpenAI** | $0.15-0.20 | $5-6 |
| **100% Free (Ollama + Edge-TTS)** | **$0.00** | **$0.00** |
| **Free Cloud (Groq + Edge-TTS)** | **$0.00** | **$0.00** |

---

## 🎭 Free LLM Options

### **Option 1: Ollama (Recommended for Privacy)**
- ✅ 100% local, no internet needed
- ✅ No rate limits
- ✅ Complete privacy
- ⚠️ Requires ~2-4GB disk space
- ⚠️ Slower than cloud (but still fast enough)

**Best models:**
- `llama3.2` - Best quality (2GB)
- `mistral` - Fast and good (4GB)
- `phi3` - Smallest, fastest (2GB)

### **Option 2: Groq (Recommended for Speed)**
- ✅ Very fast (faster than OpenAI!)
- ✅ Free tier: 30 requests/minute
- ✅ No local installation needed
- ⚠️ Requires internet
- ⚠️ Rate limited (but generous)

### **Option 3: Hugging Face**
- ✅ Free tier available
- ✅ Many models to choose from
- ⚠️ Slower than Groq
- ⚠️ Rate limited

---

## 🎤 Free TTS: Edge-TTS

**Available Voices:**
- `en-US-GuyNeural` - Male US (energetic)
- `en-US-AriaNeural` - Female US (warm)
- `en-GB-RyanNeural` - Male UK (authoritative)
- `en-GB-SoniaNeural` - Female UK (professional)

**Quality**: Very natural, comparable to paid services!

---

## 📸 Free Stock Footage

### **Pexels**
- **Cost**: FREE
- **Limit**: 200 requests/hour
- **Quality**: High-quality videos and images
- **Get key**: https://www.pexels.com/api/

### **Pixabay**
- **Cost**: FREE
- **Quality**: Good quality
- **Get key**: https://pixabay.com/api/docs/

---

## 🔧 Troubleshooting

### **"Ollama not found"**
```bash
# Make sure Ollama is running
ollama serve

# In another terminal, pull a model
ollama pull llama3.2
```

### **"Edge-TTS not installed"**
```bash
pip install edge-tts
```

### **"Groq API error"**
- Check your API key is correct
- Verify you're within rate limits (30 req/min)

---

## 📊 Performance Comparison

| Provider | Speed | Quality | Cost |
|----------|-------|---------|------|
| **OpenAI GPT-4** | Fast | Excellent | $0.15/video |
| **Groq (Llama 3.3)** | Very Fast | Very Good | FREE |
| **Ollama (Llama 3.2)** | Medium | Very Good | FREE |
| **Ollama (Phi3)** | Fast | Good | FREE |

---

## 🎯 Recommended Setup

**For Best Quality (Still Free):**
```env
LLM_PROVIDER=groq
GROQ_API_KEY=your-free-groq-key
TTS_PROVIDER=edge-tts
PEXELS_API_KEY=your-free-pexels-key
```

**For Complete Privacy:**
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
TTS_PROVIDER=edge-tts
PEXELS_API_KEY=your-free-pexels-key
```

---

## ✅ Final Checklist

- [ ] Install Ollama (or get Groq API key)
- [ ] Install Edge-TTS: `pip install edge-tts`
- [ ] Get Pexels API key (2 min signup)
- [ ] Copy and edit `.env` file
- [ ] Run: `python main.py generate --niche self-improvement`

---

## 🎉 You're Ready!

**Total Cost**: $0.00
**Total Time**: 15 minutes
**Videos per month**: Unlimited!

Run your first free video:
```bash
python main.py generate --niche self-improvement
```

Enjoy creating unlimited videos for FREE! 🚀
