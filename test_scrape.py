"""
Test script to verify Firecrawl integration by scraping a single homepage.
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_editor.crawlers import FirecrawlClient
from ai_editor.utils import setup_logging
from ai_editor.config import settings

def main():
    """Test scraping TechCrunch homepage."""
    # Setup logging
    setup_logging(log_level=settings.log_level)

    print("=" * 70)
    print("AI Editor - Firecrawl Test Script")
    print("=" * 70)
    print(f"Testing homepage scrape: TechCrunch")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)
    print()

    # Initialize Firecrawl client
    try:
        client = FirecrawlClient()
        print("✓ Firecrawl client initialized successfully")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize Firecrawl client: {e}")
        return 1

    # Test homepage scrape
    print("Scraping TechCrunch homepage...")
    print("This may take 10-30 seconds...")
    print()

    try:
        stories = client.scrape_homepage(
            url="https://techcrunch.com",
            source_name="TechCrunch"
        )

        print(f"✓ Successfully scraped homepage!")
        print(f"  Found {len(stories)} potential article links")
        print()

        if stories:
            print("Sample stories extracted:")
            print("-" * 70)
            for i, story in enumerate(stories[:5], 1):
                print(f"\n{i}. {story.headline}")
                print(f"   URL: {story.url}")
                print(f"   Source: {story.source}")
                print(f"   Scraped: {story.scraped_at.isoformat()}")

            print()
            print("-" * 70)
            print()

            # Save to JSON
            output_dir = Path(settings.output_dir)
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / "test_scrape_techcrunch.json"

            output_data = {
                "source": "TechCrunch",
                "scraped_at": datetime.now().isoformat(),
                "story_count": len(stories),
                "stories": [
                    {
                        "headline": story.headline,
                        "url": str(story.url),
                        "source": story.source,
                        "scraped_at": story.scraped_at.isoformat()
                    }
                    for story in stories
                ]
            }

            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2)

            print(f"✓ Results saved to: {output_file}")
            print()

            # Now test scraping one full article
            if stories:
                print("=" * 70)
                print("Testing full article extraction...")
                print("=" * 70)
                print()

                test_story = stories[0]
                print(f"Extracting article: {test_story.headline}")
                print(f"URL: {test_story.url}")
                print()

                article = client.scrape_article(
                    url=str(test_story.url),
                    source_name=test_story.source
                )

                if article:
                    print("✓ Successfully extracted article!")
                    print()
                    print(f"  Title: {article.title}")
                    print(f"  Author: {article.author or 'N/A'}")
                    print(f"  Word Count: {article.word_count}")
                    print(f"  Paywalled: {article.is_paywalled}")
                    print(f"  Published: {article.published_at or 'N/A'}")
                    print()
                    print("  Content preview (first 300 chars):")
                    print("  " + "-" * 66)
                    print(f"  {article.content[:300]}...")
                    print("  " + "-" * 66)
                    print()

                    # Save article to JSON
                    article_file = output_dir / "test_article_full.json"
                    article_data = {
                        "url": str(article.url),
                        "source": article.source,
                        "title": article.title,
                        "author": article.author,
                        "word_count": article.word_count,
                        "is_paywalled": article.is_paywalled,
                        "published_at": article.published_at.isoformat() if article.published_at else None,
                        "extracted_at": article.extracted_at.isoformat(),
                        "content": article.content
                    }

                    with open(article_file, 'w') as f:
                        json.dump(article_data, f, indent=2)

                    print(f"✓ Full article saved to: {article_file}")
                else:
                    print("✗ Failed to extract article")

        else:
            print("⚠ No stories extracted from homepage")
            print("  This might indicate:")
            print("  - The homepage structure has changed")
            print("  - Firecrawl couldn't parse the content")
            print("  - Rate limiting or network issues")

        print()
        print("=" * 70)
        print("Test completed successfully!")
        print("=" * 70)
        return 0

    except Exception as e:
        print(f"✗ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
