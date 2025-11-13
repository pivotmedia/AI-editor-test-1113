# AI Editor - Business of AI Daily Brief

A lightweight automated system that scans major US-centric business and tech news homepages, identifies AI-related stories, extracts the relevant articles, ranks them by business impact, and produces 5 high-quality summaries each morning.

## Overview

The AI Editor system:
- Crawls 15-20 major news homepages daily
- Filters stories for AI-business relevance using LLM classification
- Extracts full article content from top candidates
- Ranks articles by business impact
- Generates concise summaries (1 headline + 3 bullets per story)
- Outputs structured JSON for publishing workflows

**Target Audience**: Busy US professionals (ages 20-50) who need high-signal AI news focused on business impact, not technical deep-dives.

## Project Status

**Phase 1: Foundation & Core Infrastructure** ✅ COMPLETE

- [x] Project structure initialized
- [x] Configuration management (Pydantic Settings)
- [x] Firecrawl integration working
- [x] Data models defined
- [x] Test script verified

**Next Phases**:
- Phase 2: Multi-source homepage crawling
- Phase 3: AI relevance filtering
- Phase 4: Full article extraction pipeline
- Phase 5: Business impact ranking
- Phase 6: Summarization engine
- Phase 7: Orchestration & scheduling
- Phase 8: API & integration layer
- Phase 9: Testing & optimization
- Phase 10: Deployment

## Quick Start

### Prerequisites

- Python 3.11+
- Firecrawl API key
- Anthropic Claude API key (for later phases)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Run the test script:
```bash
python test_scrape.py
```

This will:
- Scrape TechCrunch homepage
- Extract article links
- Download one full article
- Save results to `output/` directory

## Project Structure

```
test/
├── src/ai_editor/           # Main application code
│   ├── crawlers/            # Firecrawl client and scraping logic
│   ├── models/              # Pydantic data models
│   ├── filters/             # AI relevance filtering (Phase 3)
│   ├── rankers/             # Business impact ranking (Phase 5)
│   ├── summarizers/         # Summary generation (Phase 6)
│   └── utils/               # Logging and utilities
├── config/                  # Configuration files
│   └── sources.yaml         # News source definitions
├── tests/                   # Unit and integration tests
├── logs/                    # Application logs
├── output/                  # Generated summaries and reports
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
└── test_scrape.py          # Test script for Firecrawl
```

## Configuration

### Environment Variables

Key configuration in `.env`:

```bash
# API Keys
FIRECRAWL_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Thresholds
AI_RELEVANCE_THRESHOLD=40        # Min score for AI relevance (0-100)
MIN_ARTICLE_WORD_COUNT=200       # Min words for valid article

# Scheduling
DAILY_RUN_TIME=05:00             # Daily execution time (HH:MM)
TIMEZONE=America/New_York        # Timezone for scheduling

# Output
OUTPUT_DIR=output                # Where to save results
```

### News Sources

Configured in `config/sources.yaml`. Currently includes:

**Top-Tier Business News**: CNBC, Reuters, AP News, Bloomberg, Yahoo Finance, Business Insider, Forbes

**Tech/AI Focused**: TechCrunch, The Verge, Wired, Ars Technica, VentureBeat, Semafor, Axios

**General News**: CNN Business, ABC News Tech, NBC News Tech

## Data Models

### Story
Basic story metadata from homepage:
- `source`: News source name
- `headline`: Story headline
- `summary`: Short summary (if available)
- `url`: Full article URL
- `category`: Story category
- `scraped_at`: Timestamp

### Article
Full article content:
- `url`: Article URL
- `source`: Source name
- `title`: Article title
- `content`: Full text (markdown)
- `author`: Article author
- `published_at`: Publication timestamp
- `word_count`: Number of words
- `is_paywalled`: Whether content is behind paywall
- `extracted_at`: Extraction timestamp

### ScoredArticle
Article with AI scores:
- `article`: Full Article object
- `relevance_score`: AI relevance (0-100)
- `impact_score`: Business impact (0-100)
- `reasoning`: Explanation of scores

### DailySummary
Final output format:
- `date`: Date (YYYY-MM-DD)
- `stories`: List of 5 StoryBullets
- `generated_at`: Generation timestamp

### StoryBullets
Individual story summary:
- `source`: Source name
- `url`: Original article URL
- `headline`: Generated headline (10-14 words)
- `bullets`: List of exactly 3 bullet points

## Test Results

**Test Date**: 2025-11-13

**Test Source**: TechCrunch

**Results**:
- ✅ Homepage scrape successful
- ✅ Extracted 9 article links
- ✅ Full article extraction working
- ✅ Content word count: 2,531 words
- ✅ Markdown formatting preserved
- ✅ Metadata extraction functional

**Output Files**:
- `output/test_scrape_techcrunch.json` - Homepage stories
- `output/test_article_full.json` - Full article content

## Usage

### Test Single Homepage Scrape

```bash
python test_scrape.py
```

### Run Full Pipeline (Coming in Phase 7)

```bash
python -m ai_editor.pipeline
```

### Manual Scraping

```python
from ai_editor.crawlers import FirecrawlClient

client = FirecrawlClient()

# Scrape homepage
stories = client.scrape_homepage(
    url="https://techcrunch.com",
    source_name="TechCrunch"
)

# Scrape full article
article = client.scrape_article(
    url="https://techcrunch.com/2025/11/12/...",
    source_name="TechCrunch"
)
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
ruff check src/
```

### Type Checking

```bash
mypy src/
```

## Architecture

### Phase 1 (Current): Foundation
- Firecrawl integration
- Data models
- Configuration management
- Basic scraping functionality

### Phase 2: Homepage Crawling
- Multi-source parallel crawling
- Data normalization
- SQLite storage
- Error handling and retries

### Phase 3: AI Relevance Filtering
- LLM integration (Anthropic Claude)
- Relevance scoring (0-100)
- Candidate selection
- Prompt engineering

### Phase 4: Article Extraction
- Full text extraction
- Content quality validation
- Paywall detection
- Metadata extraction

### Phase 5: Business Impact Ranking
- Impact scoring model
- Top 5 selection
- Diversity filtering
- Novelty detection

### Phase 6: Summarization
- Headline generation
- 3-bullet summaries
- Fact-checking
- Quality assurance

### Phase 7: Orchestration
- Daily scheduling (5 AM ET)
- Pipeline automation
- Error recovery
- Monitoring

### Phase 8: API & Integration
- REST API (FastAPI)
- Multiple output formats
- Webhook support
- Email delivery

## Technical Stack

- **Language**: Python 3.11+
- **Web Scraping**: Firecrawl API
- **LLM**: Anthropic Claude API
- **Data Validation**: Pydantic
- **Configuration**: Pydantic Settings
- **Database**: SQLite (dev) → PostgreSQL (prod)
- **Scheduling**: APScheduler
- **Testing**: pytest
- **Logging**: Python logging + structlog

## Error Handling

The system includes:
- Exponential backoff retries (2s, 4s, 8s intervals)
- Graceful degradation if sources fail
- Paywall detection and handling
- Rate limiting compliance
- Detailed error logging

## Output Format

Final daily brief JSON:

```json
{
  "date": "2025-11-13",
  "stories": [
    {
      "source": "Reuters",
      "url": "https://reuters.com/article/12345",
      "headline": "Microsoft Expands Azure AI Services with New Enterprise Tools",
      "bullets": [
        "Microsoft announced Azure AI Studio with custom model training for enterprises",
        "The move positions Microsoft to compete directly with AWS and Google Cloud AI offerings",
        "Early access customers report 40% reduction in AI deployment time"
      ]
    }
    // ... 4 more stories
  ],
  "generated_at": "2025-11-13T05:15:00Z"
}
```

## Roadmap

- [x] **Phase 1**: Foundation & Firecrawl integration
- [ ] **Phase 2**: Multi-source crawling (Week 2)
- [ ] **Phase 3**: AI relevance filtering (Week 3)
- [ ] **Phase 4**: Article extraction pipeline (Week 4)
- [ ] **Phase 5**: Business impact ranking (Week 5)
- [ ] **Phase 6**: Summarization engine (Week 6)
- [ ] **Phase 7**: Orchestration & scheduling (Week 7)
- [ ] **Phase 8**: API & integration (Week 8)
- [ ] **Phase 9**: Testing & optimization (Week 9)
- [ ] **Phase 10**: Production deployment (Week 10)

## Contributing

This is an internal project. For questions or issues, contact the development team.

## License

Proprietary - All rights reserved.

## Support

For issues or questions:
1. Check the logs in `logs/`
2. Review test output in `output/`
3. Contact the development team

---

**Last Updated**: 2025-11-13
**Version**: 0.1.0 (Phase 1 Complete)
