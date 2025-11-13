# AI Editor - Next.js Web Interface

A modern web interface for the AI Editor project, built with Next.js 15, React 19, TypeScript, and Tailwind CSS. Designed to be deployed on Vercel with Python serverless functions for web scraping.

## Features

✅ **Modern Tech Stack**
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS for styling

✅ **Vercel Deployment Ready**
- Python serverless functions for backend
- Optimized for Vercel hosting
- Environment variable configuration

✅ **Core Functionality**
- Select from 8+ news sources
- Scrape homepages using Firecrawl API
- Extract full article content
- View results with clean UI
- Mobile responsive design

## Prerequisites

- Node.js 18+ and npm/yarn
- Firecrawl API key ([Get one here](https://firecrawl.dev))
- Vercel account (for deployment)

## Local Development

### 1. Install Dependencies

```bash
cd nextjs-app
npm install
```

### 2. Configure Environment Variables

Create a `.env.local` file:

```bash
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
nextjs-app/
├── app/                          # Next.js App Router
│   ├── page.tsx                  # Homepage (scrape launcher)
│   ├── results/[id]/page.tsx    # Results page
│   ├── article/[...]/page.tsx   # Article view page
│   ├── layout.tsx                # Root layout
│   └── globals.css               # Global styles
├── api/                          # Python serverless functions
│   ├── scrape.py                 # Homepage scraping endpoint
│   └── article.py                # Article extraction endpoint
├── public/                       # Static assets
├── package.json                  # Node dependencies
├── requirements.txt              # Python dependencies (for Vercel)
├── vercel.json                   # Vercel configuration
├── tsconfig.json                 # TypeScript config
├── tailwind.config.ts            # Tailwind CSS config
└── README.md                     # This file
```

## Deployment to Vercel

### Option 1: Deploy via Vercel CLI

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Deploy**:
```bash
vercel
```

4. **Set Environment Variable**:
```bash
vercel env add FIRECRAWL_API_KEY
# Enter your Firecrawl API key when prompted
```

5. **Redeploy with env vars**:
```bash
vercel --prod
```

### Option 2: Deploy via Vercel Dashboard

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai-editor.git
git push -u origin main
```

2. **Import to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Project"
   - Select your GitHub repository
   - Root directory: `nextjs-app`
   - Click "Deploy"

3. **Add Environment Variable**:
   - Go to Project Settings → Environment Variables
   - Add `FIRECRAWL_API_KEY` with your API key
   - Redeploy the project

### Option 3: One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/ai-editor/tree/main/nextjs-app)

## API Endpoints

### POST /api/scrape

Scrape a news homepage and extract article links.

**Request:**
```json
{
  "source": "TechCrunch"
}
```

**Response:**
```json
{
  "scrape_id": "TechCrunch_20251113_123456",
  "source": "TechCrunch",
  "url": "https://techcrunch.com",
  "scraped_at": "2025-11-13T12:34:56Z",
  "story_count": 15,
  "stories": [
    {
      "headline": "...",
      "url": "https://...",
      "source": "TechCrunch",
      "scraped_at": "2025-11-13T12:34:56Z"
    }
  ]
}
```

### POST /api/article

Extract full article content from a URL.

**Request:**
```json
{
  "url": "https://techcrunch.com/2025/11/12/article-slug",
  "source": "TechCrunch"
}
```

**Response:**
```json
{
  "url": "https://...",
  "source": "TechCrunch",
  "title": "Article Title",
  "content": "Full article content in markdown...",
  "author": "John Doe",
  "published_at": "2025-11-12T10:00:00Z",
  "word_count": 850,
  "is_paywalled": false,
  "extracted_at": "2025-11-13T12:35:00Z"
}
```

## Supported News Sources

- **Tech**: TechCrunch, The Verge, Wired, Ars Technica, VentureBeat
- **Business**: CNBC, Reuters, Bloomberg

More sources can be added in `app/page.tsx` and `api/scrape.py`.

## How It Works

1. **User selects a news source** on the homepage
2. **Frontend sends POST request** to `/api/scrape`
3. **Python serverless function** uses Firecrawl to scrape the homepage
4. **Extracts article links** and returns metadata
5. **User can click "View Article"** to extract full content
6. **Frontend sends POST request** to `/api/article`
7. **Python serverless function** extracts full article text
8. **Results displayed** with formatted content

## Data Storage

Currently uses **localStorage** for storing scrape results (client-side only). This means:
- ✅ No database required for Phase 1
- ✅ Fast and simple
- ⚠️ Data cleared when browser cache is cleared
- ⚠️ Not shared between devices/browsers

**Future phases** will add:
- Database storage (PostgreSQL/MongoDB)
- User authentication
- Persistent scrape history

## Troubleshooting

### "FIRECRAWL_API_KEY not configured"

Make sure you've set the environment variable in Vercel:
1. Go to Project Settings → Environment Variables
2. Add `FIRECRAWL_API_KEY`
3. Redeploy the project

### Python dependencies not installing

Vercel automatically installs Python dependencies from `requirements.txt`. If you see errors:
1. Check `requirements.txt` syntax
2. Ensure Python runtime is `python3.9` in `vercel.json`
3. Check Vercel build logs

### Articles not extracting

Some sites have paywalls or anti-scraping measures:
- Bloomberg often has paywalls
- Some sites block Firecrawl's user agent
- Try different sources to verify functionality

## Development Scripts

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Start production server (after build)
npm start

# Run linter
npm run lint
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FIRECRAWL_API_KEY` | Yes | Your Firecrawl API key |

## Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: Python 3.9 serverless functions
- **Web Scraping**: Firecrawl API
- **Hosting**: Vercel
- **Storage**: localStorage (Phase 1)

## Roadmap

- [x] Phase 1: Basic scraping infrastructure
- [ ] Phase 2: AI relevance filtering
- [ ] Phase 3: Business impact ranking
- [ ] Phase 4: Automated summarization
- [ ] Phase 5: Database integration
- [ ] Phase 6: User authentication
- [ ] Phase 7: Daily scheduling
- [ ] Phase 8: Email delivery

## Contributing

This is an internal project. For issues or questions, contact the development team.

## License

Proprietary - All rights reserved.

---

**Built with ❤️ using Next.js and Vercel**

**Last Updated**: 2025-11-13
**Version**: 0.1.0 (Phase 1)
