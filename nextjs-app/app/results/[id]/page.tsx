'use client';

import { use, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Story {
  headline: string;
  url: string;
  source: string;
  scraped_at: string;
}

interface ScrapeResult {
  source: string;
  url: string;
  scraped_at: string;
  story_count: number;
  stories: Story[];
}

export default function ResultsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const [result, setResult] = useState<ScrapeResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would fetch from an API/database
    // For now, we'll use localStorage
    const stored = localStorage.getItem(`scrape_${id}`);
    if (stored) {
      setResult(JSON.parse(stored));
    }
    setLoading(false);
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading results...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-yellow-800">Scrape not found</h2>
          <p className="text-yellow-700 mt-2">The scrape results may have expired or been cleared.</p>
          <button
            onClick={() => router.push('/')}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            ← Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">📊 Scrape Results</h1>
        <button
          onClick={() => router.push('/')}
          className="bg-gray-100 text-gray-700 px-4 py-2 rounded hover:bg-gray-200"
        >
          ← New Scrape
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h2 className="text-2xl font-bold text-blue-600 mb-2">{result.source}</h2>
            <p className="text-sm text-gray-600">
              <strong>Source URL:</strong>{' '}
              <a href={result.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                {result.url}
              </a>
            </p>
          </div>
          <div className="text-right">
            <div className="inline-block bg-green-100 text-green-800 px-4 py-2 rounded-lg">
              <strong>{result.story_count}</strong> stories found
            </div>
            <p className="text-sm text-gray-600 mt-2">Scraped: {new Date(result.scraped_at).toLocaleString()}</p>
          </div>
        </div>
      </div>

      {result.story_count === 0 ? (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <p className="text-yellow-800">
            <strong>No stories found.</strong> The homepage structure may have changed or Firecrawl couldn&apos;t parse the content.
          </p>
        </div>
      ) : (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4">📰 Extracted Stories</h2>
          <div className="space-y-4">
            {result.stories.map((story, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {story.headline || `Article ${index + 1}`}
                    </h3>
                    <p className="text-sm text-gray-600 mb-2">
                      🔗{' '}
                      <a href={story.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                        {story.url.length > 80 ? story.url.substring(0, 80) + '...' : story.url}
                      </a>
                    </p>
                    <p className="text-xs text-gray-500">⏰ {new Date(story.scraped_at).toLocaleString()}</p>
                  </div>
                  <a
                    href={`/article/${id}/${index}`}
                    className="ml-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 whitespace-nowrap"
                  >
                    📄 View Article
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-gray-100 rounded-lg p-6 mt-6">
        <h3 className="font-semibold text-gray-900 mb-2">💡 Next Steps</h3>
        <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
          <li>Click &quot;View Article&quot; to extract complete article text</li>
          <li>Try different news sources to test extraction quality</li>
          <li>Phase 2 will add AI relevance filtering</li>
        </ul>
      </div>
    </div>
  );
}
