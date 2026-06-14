# Silverback Bridge - Deployment Guide

## 🚀 Professional Deployment with Railway

Railway.app is recommended for professional, mobile-friendly deployment. It supports Python, has a free tier, and auto-scales with usage.

### Step 1: Deploy to Railway (5 minutes)

1. **Go to [Railway.app](https://railway.app)**
2. **Click "Create New Project"**
3. **Select "Deploy from GitHub"**
4. **Connect your GitHub account and authorize**
5. **Select the `silverback-flasher` repository**
6. **Railway auto-detects Python + Procfile**
7. **Add environment variables:**
   ```
   FLASK_SECRET_KEY=silverback-super-secret-key-change-me
   ADMIN_USER=admin
   ADMIN_PASS=Silverback2026
   TELEGRAM_BOT_URL=https://t.me/SilverFlasher_bot
   PORT=5000
   ```
8. **Click Deploy**
9. **Wait 2-3 minutes for build**
10. **Get your public URL from Railway dashboard** (e.g., `https://silverback-xyz.railway.app`)

### Step 2: Configure Custom Domain (Optional)

1. In Railway dashboard, go to **Domains**
2. **Add custom domain**: `hottboiihitzz.cc` (if you own it)
3. **Update DNS to Railway nameservers**
4. **Wait for SSL certificate** (automatic)

### Step 3: Run Telegram Bot

The bot can run:

**Option A: Locally (for testing)**
```powershell
$env:SILVERBACK_BOT_TOKEN="your_telegram_bot_token_here"
$env:SILVERBACK_LANDING_URL="https://your-railway-url.railway.app"
python silverback.py
```

**Option B: On Railway as a Worker**
1. In Railway, create a **New Service**
2. **Deploy from GitHub** (same repo)
3. **Set start command**: `python silverback.py`
4. **Add same env vars**
5. **Deploy**

### Step 4: Update Landing Page Links

Update these environment variables in Railway:

```
TELEGRAM_BOT_URL=https://t.me/SilverFlasher_bot
SILVERBACK_LANDING_URL=https://your-railway-url.railway.app
SILVERBACK_BOT_TOKEN=your_telegram_bot_token_here
SILVERBACK_ADMIN_CHAT_ID=your_admin_chat_id_here
```

---

## 📱 Mobile-Friendly Features Already Built-In

✅ Responsive CSS with Tailwind  
✅ Touch-friendly buttons and forms  
✅ Mobile nav and viewport settings  
✅ Fast load times  
✅ Works on all phones (iOS, Android)  

Test on mobile:
- Open `https://your-railway-url.railway.app` on your phone
- All buttons should work smoothly
- Payment flow should be fast and clear

---

## 🔗 URLs After Deployment

**Web App**: `https://your-railway-url.railway.app`  
**Bridge Page**: `https://your-railway-url.railway.app/bridge`  
**Admin Panel**: `https://your-railway-url.railway.app/admin`  
**Telegram Bot**: `https://t.me/SilverFlasher_bot`  

---

## 💾 Database

SQLite database (`silverback_orders.db`) is stored locally on Railway and persists across restarts.

For production scale, upgrade to PostgreSQL:
1. In Railway: **Add PostgreSQL**
2. Update `app.py` to use PostgreSQL connection string from `DATABASE_URL` env var

---

## 🔐 Security Checklist

- [ ] Change `FLASK_SECRET_KEY` to a long random string
- [ ] Change `ADMIN_PASS` 
- [ ] Use HTTPS only (Railway auto-enables)
- [ ] Rotate bot token if compromised
- [ ] Monitor admin panel for activity

---

## 📊 Monitoring

In Railway dashboard:
- **Logs**: Real-time app output
- **Metrics**: CPU, Memory, Network usage
- **Deployments**: History of all versions
- **Alerts**: Set up notifications for crashes

---

## ✅ Verification

After deployment:

1. **Test landing page** on desktop and mobile
2. **Test bridge flow**:
   - Select amount
   - Choose currency
   - Check receive amount calculates correctly
3. **Test admin panel**: `/admin` with `admin`/`Silverback2026`
4. **Test Telegram bot**: `/start` on @SilverFlasher_bot

All set! 🚀
