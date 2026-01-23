# Analytics Setup Guide

## Google Analytics 4 (GA4) Setup Instructions

I've added Google Analytics tracking code to all your HTML files. To start tracking visitors and their countries, follow these steps:

### Step 1: Create a Google Analytics Account

1. Go to [Google Analytics](https://analytics.google.com/)
2. Sign in with your Google account
3. Click "Start measuring" or "Admin" (if you already have an account)

### Step 2: Create a Property

1. In the Admin section, click "Create Property"
2. Enter your website name (e.g., "Engineering Hub")
3. Select your timezone and currency
4. Click "Next" and complete the business information
5. Click "Create"

### Step 3: Get Your Measurement ID

1. After creating the property, you'll see a "Data Streams" section
2. Click "Add stream" → "Web"
3. Enter your website URL
4. You'll receive a **Measurement ID** that looks like: `G-XXXXXXXXXX`

### Step 4: Add Your Measurement ID to Your Website

1. Open each HTML file in your project
2. Find the line that says: `gtag('config', 'G-XXXXXXXXXX');`
3. Replace `G-XXXXXXXXXX` with your actual Measurement ID
4. Also replace it in the script src URL: `https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX`

**Files that need updating:**
- `index.html`
- `video-scripts.html`
- `streamlit-apps.html`
- `reinforced_concrete.html`
- `steel.html`
- `resources.html`

### Step 5: View Your Analytics

1. After adding your Measurement ID, wait 24-48 hours for data to start appearing
2. Visit [Google Analytics](https://analytics.google.com/)
3. Navigate to **Reports** → **Realtime** to see current visitors
4. Navigate to **Reports** → **User** → **Demographics details** to see country data

## What You'll Be Able to Track

- **Total visitors** and page views
- **Countries** visitors are from
- **Cities** visitors are from
- **Devices** used (desktop, mobile, tablet)
- **Browsers** used
- **Traffic sources** (direct, search, social media, etc.)
- **Most popular pages**
- **User behavior** and engagement

## Alternative Analytics Options

If you prefer privacy-focused alternatives:

### 1. Plausible Analytics
- Privacy-friendly, GDPR compliant
- Simple dashboard
- Paid service (~$9/month)
- Website: https://plausible.io/

### 2. GoatCounter
- Free for personal use
- Open source
- Privacy-friendly
- Website: https://www.goatcounter.com/

### 3. Simple Analytics
- Privacy-focused
- GDPR compliant
- Paid service
- Website: https://simpleanalytics.com/

## Need Help?

If you need assistance setting up Google Analytics or prefer a different analytics solution, let me know!
