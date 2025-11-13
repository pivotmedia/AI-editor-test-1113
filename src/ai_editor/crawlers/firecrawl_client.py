"""
Firecrawl client wrapper for scraping news homepages and articles.
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

from firecrawl import FirecrawlApp
from pydantic import HttpUrl

from ..models import Story, Article
from ..config import settings

logger = logging.getLogger(__name__)


class FirecrawlClient:
    """
    Wrapper around Firecrawl API for scraping news sources.
    Handles retries, error handling, and data normalization.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Firecrawl client."""
        self.api_key = api_key or settings.firecrawl_api_key
        self.client = FirecrawlApp(api_key=self.api_key)
        self.timeout = settings.firecrawl_timeout
        self.max_retries = settings.firecrawl_max_retries
        logger.info("Firecrawl client initialized")

    def scrape_homepage(self, url: str, source_name: str) -> List[Story]:
        """
        Scrape a news homepage and extract story links with metadata.

        Args:
            url: Homepage URL to scrape
            source_name: Name of the news source

        Returns:
            List of Story objects extracted from the homepage
        """
        logger.info(f"Scraping homepage: {source_name} ({url})")

        for attempt in range(self.max_retries):
            try:
                # Use Firecrawl's scrape endpoint with extract mode
                result = self.client.scrape_url(
                    url,
                    params={
                        'formats': ['markdown', 'links'],
                        'onlyMainContent': True,
                        'timeout': self.timeout * 1000  # Convert to milliseconds
                    }
                )

                if not result or 'markdown' not in result:
                    logger.warning(f"No content returned from {source_name}")
                    return []

                # Extract stories from the result
                stories = self._parse_homepage_result(result, source_name, url)
                logger.info(f"Extracted {len(stories)} stories from {source_name}")
                return stories

            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{self.max_retries} failed for {source_name}: {e}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All retries exhausted for {source_name}")
                    return []

        return []

    def scrape_article(self, url: str, source_name: str) -> Optional[Article]:
        """
        Scrape full article content from a URL.

        Args:
            url: Article URL to scrape
            source_name: Name of the news source

        Returns:
            Article object with full content, or None if failed
        """
        logger.info(f"Scraping article: {url}")

        for attempt in range(self.max_retries):
            try:
                # Use Firecrawl's scrape endpoint for article extraction
                result = self.client.scrape_url(
                    url,
                    params={
                        'formats': ['markdown', 'html'],
                        'onlyMainContent': True,
                        'timeout': self.timeout * 1000
                    }
                )

                if not result or 'markdown' not in result:
                    logger.warning(f"No content returned from article: {url}")
                    return None

                # Parse article content
                article = self._parse_article_result(result, url, source_name)
                if article:
                    logger.info(f"Successfully extracted article: {article.title[:50]}...")
                return article

            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{self.max_retries} failed for article {url}: {e}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All retries exhausted for article: {url}")
                    return None

        return None

    def _parse_homepage_result(self, result: Dict[str, Any], source_name: str, base_url: str) -> List[Story]:
        """
        Parse Firecrawl homepage result and extract stories.

        Args:
            result: Raw result from Firecrawl
            source_name: Name of the source
            base_url: Base URL of the homepage

        Returns:
            List of Story objects
        """
        stories = []

        # Get the markdown content
        markdown_content = result.get('markdown', '')

        # Get extracted links
        links = result.get('links', [])

        # For now, we'll extract article links that look like news articles
        # This is a simple heuristic - in production, you'd want more sophisticated parsing
        for link in links[:20]:  # Limit to first 20 links to avoid noise
            try:
                # Basic heuristic: article links usually have dates or article IDs in path
                url_str = str(link)
                if self._looks_like_article_url(url_str):
                    story = Story(
                        source=source_name,
                        headline=self._extract_headline_from_link(link, markdown_content),
                        summary=None,  # We'll get this when we scrape the full article
                        url=HttpUrl(url_str),
                        category=None,
                        scraped_at=datetime.utcnow()
                    )
                    stories.append(story)
            except Exception as e:
                logger.debug(f"Skipping link {link}: {e}")
                continue

        return stories

    def _parse_article_result(self, result: Dict[str, Any], url: str, source_name: str) -> Optional[Article]:
        """
        Parse Firecrawl article result and create Article object.

        Args:
            result: Raw result from Firecrawl
            url: Article URL
            source_name: Name of the source

        Returns:
            Article object or None
        """
        markdown_content = result.get('markdown', '')
        metadata = result.get('metadata', {})

        if not markdown_content or len(markdown_content.strip()) < 100:
            logger.warning(f"Article content too short or empty: {url}")
            return None

        # Extract title from metadata or markdown
        title = metadata.get('title', metadata.get('ogTitle', 'Untitled'))

        # Count words
        word_count = len(markdown_content.split())

        # Check if paywalled (heuristic)
        is_paywalled = self._detect_paywall(markdown_content)

        # Extract publish date if available
        published_at = None
        if 'publishedTime' in metadata:
            try:
                published_at = datetime.fromisoformat(metadata['publishedTime'].replace('Z', '+00:00'))
            except:
                pass

        article = Article(
            url=HttpUrl(url),
            source=source_name,
            title=title,
            content=markdown_content,
            author=metadata.get('author'),
            published_at=published_at,
            word_count=word_count,
            is_paywalled=is_paywalled,
            extracted_at=datetime.utcnow()
        )

        return article

    def _looks_like_article_url(self, url: str) -> bool:
        """
        Simple heuristic to detect if a URL is likely an article.

        Args:
            url: URL to check

        Returns:
            True if URL looks like an article
        """
        # Skip common non-article patterns
        skip_patterns = [
            '/tag/', '/category/', '/author/', '/search/', '/page/',
            'facebook.com', 'twitter.com', 'linkedin.com',
            'instagram.com', 'youtube.com',
            '.pdf', '.jpg', '.png', '.gif',
            '/about', '/contact', '/privacy', '/terms'
        ]

        url_lower = url.lower()
        if any(pattern in url_lower for pattern in skip_patterns):
            return False

        # Look for positive indicators
        article_indicators = [
            '/20', '/article', '/news', '/story', '/post',
            '-', '_'  # Often in article slugs
        ]

        return any(indicator in url_lower for indicator in article_indicators)

    def _extract_headline_from_link(self, link: str, markdown_content: str) -> str:
        """
        Extract headline associated with a link from markdown content.
        This is a placeholder - in production you'd use more sophisticated parsing.

        Args:
            link: The article URL
            markdown_content: Full markdown content

        Returns:
            Extracted headline or URL slug
        """
        # Fallback: use URL slug as headline
        try:
            slug = link.split('/')[-1].replace('-', ' ').replace('_', ' ')
            return slug[:100]  # Truncate if too long
        except:
            return "Article"

    def _detect_paywall(self, content: str) -> bool:
        """
        Detect if content is behind a paywall (heuristic).

        Args:
            content: Article content

        Returns:
            True if likely paywalled
        """
        paywall_indicators = [
            'subscribe to read',
            'subscription required',
            'become a member',
            'sign up to continue',
            'this article is for subscribers'
        ]

        content_lower = content.lower()
        return any(indicator in content_lower for indicator in paywall_indicators)
