"""
Vercel Serverless Function for scraping news homepages.
"""
import sys
import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from firecrawl import FirecrawlApp
except ImportError:
    # Fallback for local testing
    FirecrawlApp = None


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)

            source_name = data.get('source')
            if not source_name:
                self.send_error_response(400, 'Source name required')
                return

            # Get Firecrawl API key from environment
            api_key = os.environ.get('FIRECRAWL_API_KEY')
            if not api_key:
                self.send_error_response(500, 'FIRECRAWL_API_KEY not configured')
                return

            # Map source names to URLs
            SOURCE_URLS = {
                'TechCrunch': 'https://techcrunch.com',
                'The Verge': 'https://www.theverge.com',
                'Wired': 'https://www.wired.com',
                'Ars Technica': 'https://arstechnica.com',
                'CNBC': 'https://www.cnbc.com',
                'Reuters': 'https://www.reuters.com',
                'Bloomberg': 'https://www.bloomberg.com',
                'VentureBeat': 'https://venturebeat.com',
            }

            source_url = SOURCE_URLS.get(source_name)
            if not source_url:
                self.send_error_response(400, f'Unknown source: {source_name}')
                return

            # Initialize Firecrawl
            client = FirecrawlApp(api_key=api_key)

            # Scrape homepage
            result = client.scrape_url(
                source_url,
                params={
                    'formats': ['markdown', 'links'],
                    'onlyMainContent': True,
                    'timeout': 30000
                }
            )

            if not result or 'links' not in result:
                self.send_error_response(500, 'Failed to scrape homepage')
                return

            # Extract article links
            links = result.get('links', [])
            stories = []

            for link in links[:20]:  # Limit to first 20
                url_str = str(link)
                if self._looks_like_article_url(url_str):
                    stories.append({
                        'headline': self._extract_headline(url_str),
                        'url': url_str,
                        'source': source_name,
                        'scraped_at': datetime.utcnow().isoformat()
                    })

            # Generate scrape ID
            scrape_id = f"{source_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Prepare response
            response_data = {
                'scrape_id': scrape_id,
                'source': source_name,
                'url': source_url,
                'scraped_at': datetime.utcnow().isoformat(),
                'story_count': len(stories),
                'stories': stories
            }

            self.send_json_response(200, response_data)

        except Exception as e:
            self.send_error_response(500, str(e))

    def _looks_like_article_url(self, url: str) -> bool:
        """Check if URL looks like an article."""
        skip_patterns = [
            '/tag/', '/category/', '/author/', '/search/', '/page/',
            'facebook.com', 'twitter.com', 'linkedin.com',
            '.pdf', '.jpg', '.png', '.gif',
            '/about', '/contact', '/privacy', '/terms'
        ]

        url_lower = url.lower()
        if any(pattern in url_lower for pattern in skip_patterns):
            return False

        article_indicators = ['/20', '/article', '/news', '/story', '/post', '-', '_']
        return any(indicator in url_lower for indicator in article_indicators)

    def _extract_headline(self, url: str) -> str:
        """Extract headline from URL slug."""
        try:
            slug = url.split('/')[-1].replace('-', ' ').replace('_', ' ')
            return slug[:100]
        except:
            return "Article"

    def send_json_response(self, status_code: int, data: dict):
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def send_error_response(self, status_code: int, message: str):
        """Send error response."""
        self.send_json_response(status_code, {'error': message})
