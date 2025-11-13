# Vercel Deployment Guide for AI Editor

This repository contains a Next.js application in the `nextjs-app/` subdirectory that needs to be deployed to Vercel.

## 🎯 Critical: Root Directory Configuration

**The #1 most important step** is to configure Vercel to use `nextjs-app` as the Root Directory.

### Option 1: Configure in Vercel Dashboard (Recommended)

1. **Go to your Vercel project**
   - Navigate to https://vercel.com/dashboard
   - Select your project: `ai-editor-test-1113`

2. **Configure Root Directory**
   - Click **Settings** (top navigation)
   - Click **General** (left sidebar)
   - Scroll down to **Root Directory** section
   - Click **Edit**
   - Enter: `nextjs-app`
   - Click **Save**

3. **Configure Environment Variables**
   - Click **Environment Variables** (left sidebar)
   - Click **Add New**
   - Key: `FIRECRAWL_API_KEY`
   - Value: `fc-6ad923d22340481d976f1d78493e2f4e`
   - Select all environments (Production, Preview, Development)
   - Click **Save**

4. **Redeploy**
   - Go to **Deployments** tab
   - Click on the latest deployment
   - Click **⋯** (three dots menu)
   - Click **Redeploy**

### Option 2: Deploy via Vercel CLI

```bash
cd nextjs-app
vercel --prod
```

When prompted, answer:
- Set up and deploy: **Y**
- Which scope: (select your account)
- Link to existing project: **Y** (if exists) or **N** (if new)
- Project name: `ai-editor`
- In which directory is your code located: `.` (current directory)

Then add environment variable:
```bash
vercel env add FIRECRAWL_API_KEY production
# Paste: fc-6ad923d22340481d976f1d78493e2f4e
```

## 📁 Repository Structure

```
/
├── src/                    # Python backend (Phase 1 infrastructure)
├── web_app/               # Flask app (alternative, not for Vercel)
└── nextjs-app/            # ← DEPLOY THIS FOLDER
    ├── app/               # Next.js pages
    ├── api/               # Python serverless functions
    ├── package.json       # Node dependencies
    ├── requirements.txt   # Python dependencies
    └── vercel.json        # Vercel config (Python runtime)
```

## 🔧 What Vercel Will Do

When properly configured with Root Directory = `nextjs-app`, Vercel will:

1. ✅ Detect Next.js 15 from `package.json`
2. ✅ Run `npm install` (installs React, Next.js, etc.)
3. ✅ Run `next build` (builds the app)
4. ✅ Install Python dependencies from `requirements.txt`
5. ✅ Configure Python 3.9 runtime for `api/**/*.py` files
6. ✅ Deploy serverless functions

## 🐛 Troubleshooting

### Error: "No Next.js version detected"

**Cause**: Root Directory is not set correctly in Vercel project settings.

**Solution**:
1. Go to Project Settings → General → Root Directory
2. Set to: `nextjs-app`
3. Click Save
4. Redeploy

### Error: "No flask entrypoint found"

**Cause**: Vercel is looking at the repository root (where `web_app/` Flask app exists) instead of `nextjs-app/`.

**Solution**: Same as above - set Root Directory to `nextjs-app`

### Error: "FIRECRAWL_API_KEY not configured"

**Cause**: Environment variable not set in Vercel.

**Solution**:
1. Settings → Environment Variables
2. Add `FIRECRAWL_API_KEY` = `fc-6ad923d22340481d976f1d78493e2f4e`
3. Redeploy

### Build succeeds but Python functions fail

**Cause**: Python dependencies not installing or wrong runtime.

**Solution**:
- Check `nextjs-app/requirements.txt` exists
- Check `nextjs-app/vercel.json` has Python runtime config
- Check Vercel Function Logs for Python errors

## 📦 Dependencies

**Node.js (Next.js frontend)**:
- Next.js 15.0.3
- React 18.3.1
- Tailwind CSS 3.4.1
- TypeScript 5

**Python (Serverless functions)**:
- firecrawl-py 1.5.0
- httpx 0.27.2
- Python 3.9 runtime

## 🌐 After Deployment

Once deployed successfully, Vercel will give you a URL like:
```
https://ai-editor-xxxxx.vercel.app
```

Test the deployment:
1. Visit the homepage
2. Select "TechCrunch" from the dropdown
3. Click "Start Scraping"
4. Wait 10-30 seconds
5. View results showing extracted articles

## 📚 Additional Resources

- [Vercel Next.js Deployment Docs](https://vercel.com/docs/frameworks/nextjs)
- [Vercel Python Serverless Functions](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Vercel Monorepo Guide](https://vercel.com/docs/monorepos)

## ✅ Verification Checklist

Before redeploying, verify:

- [ ] Root Directory is set to `nextjs-app` in Vercel settings
- [ ] Environment variable `FIRECRAWL_API_KEY` is added
- [ ] Latest code is pushed to GitHub branch `claude/ai-editor-daily-brief-011CV66BK8idtfeh752UoWPf`
- [ ] `nextjs-app/package.json` has Next.js in dependencies
- [ ] `nextjs-app/package-lock.json` exists
- [ ] `nextjs-app/requirements.txt` exists

---

**Need Help?**

If issues persist after following this guide:
1. Check Vercel build logs for specific errors
2. Check Vercel Function Logs for runtime errors
3. Verify all files are committed to git
4. Try deploying via Vercel CLI instead of dashboard

**Last Updated**: 2025-11-13
