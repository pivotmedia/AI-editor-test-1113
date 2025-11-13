"""
Vercel Serverless Function for extracting full article content.
"""
import sys
import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler

try:
    from firecrawl import FirecrawlApp
except ImportError:
    FirecrawlApp = None


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)

            article_url = data.get('url')
            source_name = data.get('source', 'Unknown')

            if not article_url:
                self.send_error_response(400, 'Article URL required')
                return

            # Get Firecrawl API key
            api_key = os.environ.get('FIRECRAWL_API_KEY')
            if not api_key:
                self.send_error_response(500, 'FIRECRAWL_API_KEY not configured')
                return

            # Initialize Firecrawl
            client = FirecrawlApp(api_key=api_key)

            # Scrape article
            result = client.scrape_url(
                article_url,
                params={
                    'formats': ['markdown', 'html'],
                    'onlyMainContent': True,
                    'timeout': 30000
                }
            )

            if not result or 'markdown' not in result:
                self.send_error_response(500, 'Failed to extract article content')
                return

            markdown_content = result.get('markdown', '')
            metadata = result.get('metadata', {})

            if len(markdown_content.strip()) < 100:
                self.send_error_response(500, 'Article content too short or empty')
                return

            # Extract metadata
            title = metadata.get('title', metadata.get('ogTitle', 'Untitled'))
            word_count = len(markdown_content.split())
            is_paywalled = self._detect_paywall(markdown_content)

            # Parse publish date
            published_at = None
            if 'publishedTime' in metadata:
                try:
                    published_at = metadata['publishedTime']
                except:
                    pass

            # Prepare response
            article_data = {
                'url': article_url,
                'source': source_name,
                'title': title,
                'content': markdown_content,
                'author': metadata.get('author'),
                'published_at': published_at,
                'word_count': word_count,
                'is_paywalled': is_paywalled,
                'extracted_at': datetime.utcnow().isoformat()
            }

            self.send_json_response(200, article_data)

        except Exception as e:
            self.send_error_response(500, str(e))

    def _detect_paywall(self, content: str) -> bool:
        """Detect if content is paywalled."""
        paywall_indicators = [
            'subscribe to read',
            'subscription required',
            'become a member',
            'sign up to continue',
            'this article is for subscribers'
        ]
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in paywall_indicators)

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
