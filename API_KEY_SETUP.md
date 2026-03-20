# 🗝️ API Keys Procurement Guide

This guide provides step-by-step instructions for obtaining the API keys required for AutoShorts AI.

--
## 🚀 1. OpenAI (Essential/Recommended)
**Used for**: Scripts, Metadata, and High-Quality TTS.
1. Go to [OpenAI Platform](https://platform.openai.com/).
2. Sign up or Log in.
3. Navigate to **API Keys** in the left sidebar (under "Dashboards" or project settings).
4. Click **+ Create new secret key**.
5. Copy the key immediately and paste it into your `.env` file as `OPENAI_API_KEY`.
6. **Note**: New accounts usually get $5 free credit. If you run out, you'll need to add a payment method (it's pay-as-you-go).
---


## 🆓 2. Pexels (Free Stock Video/Images)
**Used for**: Automatic background footage.
1. Visit [Pexels API](https://www.pexels.com/api/).
2. Click **Get Started** or **Sign Up**.
3. Fill in the application form (Just say "building an AI video automation tool").
4. Once approved (usually instant), go to your [API dashboard](https://www.pexels.com/api/new/).
5. Copy your **API Key** and paste it as `PEXELS_API_KEY`.
---


## ⚡ 3. Groq (Fast Free Cloud AI)
**Used for**: 100% Free script/metadata generation (alternative to OpenAI).
1. Go to [Groq Console](https://console.groq.com/).
2. Sign up with Google or Email.
3. Navigate to **API Keys** on the left.
4. Click **Create API Key**.
5. Copy and paste as `GROQ_API_KEY`.

---

## 📺 4. YouTube (Automated Publishing)
**Used for**: Auto-uploading to YouTube Shorts.
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a **New Project** named "AutoShorts".
3. Search for "YouTube Data API v3" and click **Enable**.
4. Go to **Credentials** -> **Create Credentials** -> **OAuth client ID**.
   - You may need to "Configure Consent Screen" first (Internal/External).
5. Set Application type to **Desktop app**.
6. Download the `client_secrets.json` or copy the **Client ID** and **Client Secret**.
7. Paste into `.env` as `YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET`.

---

## 📸 5. Instagram (Automated Publishing)
**Used for**: Auto-uploading to Instagram Reels.
1. Go to [Meta for Developers](https://developers.facebook.com/).
2. Create a New App (Type: Business).
3. Add the **Instagram Graph API** product.
4. You will need a **Facebook Page** linked to an **Instagram Business/Creator Account**.
5. Use the **Graph API Explorer** to generate a **Short-lived Access Token**.
6. Exchange it for a **Long-lived Access Token**.
7. Copy your **Instagram Business Account ID** (found in App Settings or via Graph API).
8. Paste as `INSTAGRAM_ACCESS_TOKEN` and `INSTAGRAM_BUSINESS_ACCOUNT_ID`.

---

## 🎨 6. Stability AI (AI Image Generation)
**Used for**: Creating custom visuals for scenes.
1. Go to [DreamStudio](https://dreamstudio.ai/) or [Stability AI Platform](https://platform.stability.ai/).
2. Sign up and go to your **Account/API** section.
3. Copy your API key.
4. Paste as `STABILITY_AI_API_KEY`.

---

## 🛠️ Summary Table

| Service | Key Name | Cost | Link |
|---------|----------|------|------|
| OpenAI | `OPENAI_API_KEY` | Paid (Free credits) | [Link](https://platform.openai.com/) |
| Pexels | `PEXELS_API_KEY` | **Free** | [Link](https://www.pexels.com/api/) |
| Groq | `GROQ_API_KEY` | **Free** | [Link](https://console.groq.com/) |
| YouTube | `YOUTUBE_ID/SECRET`| **Free** | [Link](https://console.cloud.google.com/) |
| Stability | `STABILITY_API_KEY`| Paid | [Link](https://platform.stability.ai/) |

---

### 💡 Pro Tip
If you want to keep it **100% free**, use **Groq** for thinking and **Pexels** for footage. You won't pay a single cent!
