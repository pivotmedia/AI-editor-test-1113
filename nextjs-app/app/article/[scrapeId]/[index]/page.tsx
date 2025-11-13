'use client';

import { use, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Article {
  url: string;
  source: string;
  title: string;
  content: string;
  author?: string;
  published_at?: string;
  word_count: number;
  is_paywalled: boolean;
  extracted_at: string;
}

export default function ArticlePage({ params }: { params: Promise<{ scrapeId: string; index: string }> }) {
  const { scrapeId, index } = use(params);
  const router = useRouter();
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchArticle = async () => {
      // Get the scrape result from localStorage
      const stored = localStorage.getItem(`scrape_${scrapeId}`);
      if (!stored) {
        setError('Scrape result not found');
        setLoading(false);
        return;
      }

      const scrapeResult = JSON.parse(stored);
      const storyIndex = parseInt(index);
      const story = scrapeResult.stories[storyIndex];

      if (!story) {
        setError('Story not found');
        setLoading(false);
        return;
      }

      // Check if article is already cached
      const cachedArticle = localStorage.getItem(`article_${scrapeId}_${index}`);
      if (cachedArticle) {
        setArticle(JSON.parse(cachedArticle));
        setLoading(false);
        return;
      }

      // Fetch article content
      try {
        const response = await fetch('/api/article', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            url: story.url,
            source: story.source,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || 'Failed to extract article');
        }

        // Cache the article
        localStorage.setItem(`article_${scrapeId}_${index}`, JSON.stringify(data));
        setArticle(data);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [scrapeId, index]);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            <p className="mt-4 text-slate-300">Extracting article content... This may take 10-30 seconds.</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-red-900/30 border border-red-700 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-red-300">❌ Extraction Failed</h2>
          <p className="text-red-200 mt-2">{error}</p>
          <button
            onClick={() => router.push(`/results/${scrapeId}`)}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
          >
            ← Back to Results
          </button>
        </div>
      </div>
    );
  }

  if (!article) return null;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-slate-100">📄 Full Article</h1>
        <button
          onClick={() => router.push(`/results/${scrapeId}`)}
          className="bg-slate-700 text-slate-200 px-4 py-2 rounded hover:bg-slate-600 transition-colors"
        >
          ← Back to Results
        </button>
      </div>

      <div className="bg-green-900/30 border border-green-700 rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold text-green-300 mb-3">✅ Successfully Extracted</h2>
        <h3 className="text-2xl font-bold text-slate-100 mb-4">{article.title}</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-200">
          <div>
            <p><strong>Source:</strong> <span className="bg-blue-900/50 text-blue-300 px-2 py-1 rounded border border-blue-700">{article.source}</span></p>
            <p className="mt-2"><strong>Author:</strong> {article.author || 'N/A'}</p>
            <p className="mt-2"><strong>Word Count:</strong> <strong className="text-slate-100">{article.word_count}</strong> words</p>
          </div>
          <div>
            <p><strong>Published:</strong> {article.published_at ? new Date(article.published_at).toLocaleString() : 'Unknown'}</p>
            <p className="mt-2"><strong>Extracted:</strong> {new Date(article.extracted_at).toLocaleString()}</p>
            <p className="mt-2">
              <strong>Paywalled:</strong>{' '}
              <span className={`px-2 py-1 rounded border ${article.is_paywalled ? 'bg-yellow-900/40 text-yellow-300 border-yellow-700' : 'bg-green-900/40 text-green-300 border-green-700'}`}>
                {article.is_paywalled ? 'Yes' : 'No'}
              </span>
            </p>
          </div>
        </div>

        <p className="mt-4 text-sm break-all">
          <strong>URL:</strong>{' '}
          <a href={article.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
            {article.url} ↗
          </a>
        </p>
      </div>

      <div className="bg-slate-800 rounded-lg shadow-xl mb-6 border border-slate-700">
        <div className="border-b border-slate-700 p-4">
          <h3 className="font-semibold text-slate-100">
            📝 Article Content{' '}
            <span className="text-sm font-normal bg-slate-700 text-slate-300 px-2 py-1 rounded ml-2">Markdown Format</span>
          </h3>
        </div>
        <div className="p-6">
          <div className="max-h-96 overflow-y-auto bg-slate-900 p-4 rounded border border-slate-600 font-mono text-sm">
            <pre className="whitespace-pre-wrap text-slate-200">{article.content}</pre>
          </div>
        </div>
        <div className="border-t border-slate-700 p-4 text-xs text-slate-400">
          ℹ️ Content extracted using Firecrawl&apos;s mainContent mode. Scroll to read the full article.
        </div>
      </div>

      {article.word_count < 200 && (
        <div className="bg-yellow-900/30 border border-yellow-700 rounded-lg p-4 mb-6">
          <p className="text-yellow-200">
            ⚠️ <strong>Low word count detected.</strong> This article may be incomplete or behind a paywall.
            Minimum recommended: 200 words.
          </p>
        </div>
      )}

      <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
        <h3 className="font-semibold text-slate-100 mb-3">📊 Data Quality Notes</h3>
        <ul className="list-disc list-inside space-y-1 text-sm text-slate-300">
          <li><strong className="text-slate-200">Title:</strong> Extracted from page metadata or content</li>
          <li><strong className="text-slate-200">Content:</strong> Main article text in markdown format</li>
          <li><strong className="text-slate-200">Metadata:</strong> Author, publish date, and word count</li>
          <li><strong className="text-slate-200">Paywall Detection:</strong> Heuristic-based detection</li>
        </ul>
        <hr className="my-3 border-slate-600" />
        <p className="text-xs text-slate-400">
          Future phases will score this content for AI relevance and business impact, then summarize it into headlines and bullet points.
        </p>
      </div>
    </div>
  );
}
