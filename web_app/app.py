"""
Flask web application for AI Editor - Visual interface for testing scrapes.
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_editor.crawlers import FirecrawlClient
from ai_editor.utils import setup_logging
from ai_editor.config import settings
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Setup logging
setup_logging(log_level=settings.log_level)

# Load news sources
sources_file = Path(__file__).parent.parent / "config" / "sources.yaml"
with open(sources_file, 'r') as f:
    sources_data = yaml.safe_load(f)
    NEWS_SOURCES = sources_data['sources']

# Store scrape results in memory (for simple demo)
# In production, this would be in a database
scrape_results = {}
article_cache = {}


@app.route('/')
def index():
    """Homepage with scrape controls."""
    return render_template('index.html', sources=NEWS_SOURCES)


@app.route('/scrape', methods=['POST'])
def scrape():
    """Execute a scrape for a selected source."""
    source_name = request.form.get('source')

    # Find the source config
    source_config = next((s for s in NEWS_SOURCES if s['name'] == source_name), None)
    if not source_config:
        return jsonify({'error': 'Invalid source'}), 400

    try:
        # Initialize Firecrawl client
        client = FirecrawlClient()

        # Scrape homepage
        stories = client.scrape_homepage(
            url=source_config['homepage_url'],
            source_name=source_name
        )

        # Store results
        scrape_id = f"{source_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        scrape_results[scrape_id] = {
            'source': source_name,
            'url': source_config['homepage_url'],
            'scraped_at': datetime.now().isoformat(),
            'story_count': len(stories),
            'stories': [
                {
                    'headline': story.headline,
                    'url': str(story.url),
                    'source': story.source,
                    'scraped_at': story.scraped_at.isoformat()
                }
                for story in stories
            ]
        }

        return redirect(url_for('results', scrape_id=scrape_id))

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/results/<scrape_id>')
def results(scrape_id):
    """Display scrape results."""
    if scrape_id not in scrape_results:
        return "Scrape not found", 404

    result = scrape_results[scrape_id]
    return render_template('results.html', result=result, scrape_id=scrape_id)


@app.route('/article/<scrape_id>/<int:story_index>')
def article(scrape_id, story_index):
    """Display full article content."""
    if scrape_id not in scrape_results:
        return "Scrape not found", 404

    result = scrape_results[scrape_id]
    if story_index >= len(result['stories']):
        return "Story not found", 404

    story = result['stories'][story_index]

    # Check if we already scraped this article
    article_key = f"{scrape_id}_{story_index}"
    if article_key not in article_cache:
        try:
            # Scrape the full article
            client = FirecrawlClient()
            article_obj = client.scrape_article(
                url=story['url'],
                source_name=story['source']
            )

            if article_obj:
                article_cache[article_key] = {
                    'url': str(article_obj.url),
                    'title': article_obj.title,
                    'author': article_obj.author,
                    'word_count': article_obj.word_count,
                    'is_paywalled': article_obj.is_paywalled,
                    'published_at': article_obj.published_at.isoformat() if article_obj.published_at else None,
                    'content': article_obj.content,
                    'extracted_at': article_obj.extracted_at.isoformat()
                }
            else:
                article_cache[article_key] = None

        except Exception as e:
            article_cache[article_key] = {'error': str(e)}

    article_data = article_cache.get(article_key)
    return render_template('article.html',
                         story=story,
                         article=article_data,
                         scrape_id=scrape_id,
                         story_index=story_index)


@app.route('/history')
def history():
    """Show scrape history."""
    history_items = [
        {
            'scrape_id': scrape_id,
            'source': data['source'],
            'scraped_at': data['scraped_at'],
            'story_count': data['story_count']
        }
        for scrape_id, data in sorted(scrape_results.items(),
                                      key=lambda x: x[1]['scraped_at'],
                                      reverse=True)
    ]
    return render_template('history.html', history=history_items)


@app.route('/api/sources')
def api_sources():
    """API endpoint to get available sources."""
    return jsonify(NEWS_SOURCES)


if __name__ == '__main__':
    print("\n" + "="*70)
    print("AI Editor - Web Interface")
    print("="*70)
    print(f"Starting server at http://localhost:5000")
    print(f"Sources configured: {len(NEWS_SOURCES)}")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
