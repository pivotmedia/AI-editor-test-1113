'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

const NEWS_SOURCES = [
  { name: 'TechCrunch', url: 'https://techcrunch.com', category: 'tech', priority: 1 },
  { name: 'The Verge', url: 'https://www.theverge.com', category: 'tech', priority: 1 },
  { name: 'Wired', url: 'https://www.wired.com', category: 'tech', priority: 1 },
  { name: 'Ars Technica', url: 'https://arstechnica.com', category: 'tech', priority: 1 },
  { name: 'CNBC', url: 'https://www.cnbc.com', category: 'business', priority: 1 },
  { name: 'Reuters', url: 'https://www.reuters.com', category: 'business', priority: 1 },
  { name: 'Bloomberg', url: 'https://www.bloomberg.com', category: 'business', priority: 1 },
  { name: 'VentureBeat', url: 'https://venturebeat.com', category: 'tech', priority: 1 },
];

export default function Home() {
  const [selectedSource, setSelectedSource] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleScrape = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSource) return;

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source: selectedSource }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Scraping failed');
      }

      // Store result in localStorage for results page
      localStorage.setItem(`scrape_${data.scrape_id}`, JSON.stringify(data));

      router.push(`/results/${data.scrape_id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setLoading(false);
    }
  };

  const selectedSourceData = NEWS_SOURCES.find(s => s.name === selectedSource);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-slate-800 rounded-lg shadow-xl p-6 mb-6 border border-slate-700">
        <h1 className="text-3xl font-bold text-slate-100 mb-2">
          🚀 Run Homepage Scrape
        </h1>
        <p className="text-slate-300 mb-6">
          Select a news source to scrape its homepage and extract article links.
          This is Phase 1 testing - full pipeline coming soon!
        </p>

        <form onSubmit={handleScrape}>
          <div className="mb-6">
            <label htmlFor="source" className="block text-sm font-medium text-slate-200 mb-2">
              Select News Source:
            </label>
            <select
              id="source"
              value={selectedSource}
              onChange={(e) => setSelectedSource(e.target.value)}
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 text-slate-100 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="">Choose a source...</option>
              {NEWS_SOURCES.map((source) => (
                <option key={source.name} value={source.name}>
                  {source.name} ({source.category}) {source.priority === 1 ? '⭐' : ''}
                </option>
              ))}
            </select>
            <p className="mt-2 text-sm text-slate-400">
              ℹ️ {NEWS_SOURCES.length} sources configured | ⭐ = High priority source
            </p>
          </div>

          {selectedSourceData && (
            <div className="mb-6 p-4 bg-blue-900/30 border border-blue-700 rounded-lg">
              <p className="text-sm text-slate-200"><strong>Selected:</strong> {selectedSourceData.name}</p>
              <p className="text-sm text-slate-200"><strong>URL:</strong> <a href={selectedSourceData.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">{selectedSourceData.url}</a></p>
              <p className="text-sm text-slate-200"><strong>Category:</strong> {selectedSourceData.category}</p>
            </div>
          )}

          {error && (
            <div className="mb-6 p-4 bg-red-900/30 border border-red-700 rounded-lg text-red-300">
              <strong>Error:</strong> {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !selectedSource}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Scraping... (10-30 seconds)
              </span>
            ) : (
              '☁️ Start Scraping'
            )}
          </button>
        </form>
      </div>

      <div className="bg-slate-800 rounded-lg shadow-xl p-6 mb-6 border border-slate-700">
        <h2 className="text-xl font-bold text-slate-100 mb-4">
          ✅ Available Sources
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {['tech', 'business'].map((category) => (
            <div key={category}>
              <h3 className="text-sm font-semibold text-slate-400 uppercase mb-2">{category}</h3>
              <ul className="space-y-2">
                {NEWS_SOURCES.filter(s => s.category === category).map((source) => (
                  <li key={source.name} className="flex items-center text-sm text-slate-300">
                    <span className="text-green-400 mr-2">✓</span>
                    {source.name}
                    {source.priority === 1 && <span className="ml-2 text-xs bg-blue-900/50 text-blue-300 px-2 py-1 rounded border border-blue-700">High Priority</span>}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
        <h2 className="text-lg font-bold text-slate-100 mb-3">
          ℹ️ How It Works
        </h2>
        <ol className="list-decimal list-inside space-y-2 text-sm text-slate-300">
          <li>Select a news source from the dropdown</li>
          <li>Click &quot;Start Scraping&quot; to crawl the homepage</li>
          <li>Firecrawl extracts article links and metadata</li>
          <li>View results with headlines and URLs</li>
          <li>Click on any article to extract full content</li>
        </ol>
        <hr className="my-4 border-slate-600" />
        <p className="text-sm text-slate-400">
          <strong className="text-slate-300">Phase 1 Status:</strong> Basic scraping infrastructure complete.
          AI filtering, ranking, and summarization coming in future phases.
        </p>
      </div>
    </div>
  );
}
