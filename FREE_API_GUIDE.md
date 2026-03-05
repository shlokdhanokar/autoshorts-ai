# 🆓 Free API Keys Guide

## ✅ What You NEED (Only 1 Required!)

### **OpenAI API Key** (Required)
- **Cost**: $5 free credit for new users, then ~$0.15-0.20 per video
- **Get it**: https://platform.openai.com/signup
- **Used for**: Script generation, voiceover (TTS), metadata
- **This is the ONLY required API key!**

- 
---
## 🎁 Free Optional Services

### **Stock Footage**

#### **Pexels** (100% Free)
- **Cost**: FREE forever
- **Limit**: 200 requests/hour
- **Get key**: https://www.pexels.com/api/
- **Quality**: High-quality stock videos and images

#### **Pixabay** (100% Free)
- **Cost**: FREE forever
- **Get key**: https://pixabay.com/api/docs/
- **Quality**: Good quality stock media

### **Text-to-Speech**

#### **OpenAI TTS** (Already included with OpenAI key!)
- **Cost**: ~$0.015 per 1,000 characters (~$0.10/video)
- **Quality**: Very natural voices
- **Already works** - no extra setup needed!

#### **Edge-TTS** (100% Free Alternative)
- **Cost**: FREE forever
- **Setup**: No API key needed, just install: `pip install edge-tts`
- **Quality**: Good Microsoft voices
- **How to use**: I can update the code to use this instead

### **AI Image Generation**

#### **Hugging Face Inference API** (Free Tier)
- **Cost**: FREE tier available
- **Get key**: https://huggingface.co/settings/tokens
- **Models**: Stable Diffusion and others
- **Limit**: Rate limited on free tier

### **Social Media Publishing**

#### **YouTube Data API v3** (100% Free)
- **Cost**: FREE
- **Limit**: 10,000 quota units/day (enough for ~100 uploads)
- **Setup**: https://console.cloud.google.com/
- **Guide**: I can help you set this up

#### **Instagram Graph API** (Free but Complex)
- **Cost**: FREE
- **Requirements**: Facebook Business account
- **Setup**: More complex, requires app review

---

## 💰 Cost Breakdown (Minimal Setup)

### **Option 1: OpenAI Only** (Recommended to start)
```
Setup cost: $0
Per video: ~$0.15-0.20
Monthly (30 videos): ~$5-6
```

**What works:**
- ✅ Script generation
- ✅ Voiceover (OpenAI TTS)
- ✅ Metadata generation
- ✅ Video assembly
- ⚠️ Limited visuals (placeholders until you add stock API)

### **Option 2: OpenAI + Free Stock Footage**
```
Setup cost: $0
Per video: ~$0.15-0.20
Monthly (30 videos): ~$5-6
```

**What works:**
- ✅ Everything from Option 1
- ✅ Real stock footage from Pexels/Pixabay
- ✅ Complete videos ready to publish

### **Option 3: All Free (Edge-TTS + Free Stock)**
```
Setup cost: $0
Per video: ~$0.05 (only OpenAI for script)
Monthly (30 videos): ~$1.50
```

**What works:**
- ✅ Script generation (OpenAI)
- ✅ FREE voiceover (Edge-TTS)
- ✅ FREE stock footage (Pexels/Pixabay)
- ✅ Complete videos at minimal cost

---

## 🚀 Quick Start Guide

### **Minimal Setup (Just OpenAI)**

1. **Get OpenAI API key**: https://platform.openai.com/signup
2. **Copy the .env file**:
   ```bash
   copy config\.env.example .env
   ```
3. **Edit .env and add ONLY this**:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
4. **Run the system**:
   ```bash
   python main.py generate --niche self-improvement
   ```

### **Add Free Stock Footage (Recommended)**

1. **Get Pexels API key**: https://www.pexels.com/api/ (takes 2 minutes)
2. **Add to .env**:
   ```env
   PEXELS_API_KEY=your-pexels-key-here
   ```
3. **Done!** Now you'll get real stock footage

### **Use Free TTS (Optional - Save Money)**

Want to save money on voiceovers? I can update the code to use **Edge-TTS** (100% free):

1. **Install**: `pip install edge-tts`
2. **I'll update the voiceover agent** to use Edge-TTS
3. **Save ~$0.10 per video!**

---

## 📊 Recommended Configuration

**For Testing/Learning:**
```env
OPENAI_API_KEY=sk-your-key-here
AUTO_PUBLISH=false
```

**For Production (Free Stock):**
```env
OPENAI_API_KEY=sk-your-key-here
PEXELS_API_KEY=your-pexels-key-here
AUTO_PUBLISH=false
```

**For Full Automation:**
```env
OPENAI_API_KEY=sk-your-key-here
PEXELS_API_KEY=your-pexels-key-here
YOUTUBE_CLIENT_ID=your-youtube-id
YOUTUBE_CLIENT_SECRET=your-youtube-secret
AUTO_PUBLISH=true
```

---

## ❓ FAQ

**Q: Do I need all the API keys?**
A: No! Only OpenAI is required. Everything else is optional.

**Q: What's the cheapest way to run this?**
A: OpenAI for scripts (~$0.05/video) + Edge-TTS for voice (FREE) + Pexels for footage (FREE) = ~$0.05 per video

**Q: Can I run this completely free?**
A: Almost! You need OpenAI for script generation (~$0.05/video), but everything else can be free.

**Q: Which free services should I add first?**
A: Pexels (stock footage) - it's free, easy to get, and makes a huge difference in video quality.

---

## 🎯 My Recommendation

**Start with this minimal .env:**
```env
OPENAI_API_KEY=your-openai-key-here
PEXELS_API_KEY=your-pexels-key-here
AUTO_PUBLISH=false
```

This gives you:
- ✅ Full script generation
- ✅ Natural voiceovers
- ✅ Real stock footage
- ✅ Complete, publishable videos
- 💰 Cost: ~$0.15-0.20 per video

**Total setup time: 5 minutes**
**Total cost: $0 to start (OpenAI gives $5 free credit)**

---

Want me to help you get the Pexels API key or set up Edge-TTS for free voiceovers?
