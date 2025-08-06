'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function WeeklyReportPage() {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReport = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/weekly-report');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Weekly report data:', data);
      console.log('Highlights:', data.highlights);
      console.log('Most quoted expert:', data.highlights?.most_quoted_expert);
      setReport(data);
      setError(null);
    } catch (error) {
      console.error('Error fetching weekly report:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch weekly report');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">Genereren van wekelijks rapport...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="max-w-md p-6 border rounded-lg">
          <h2 className="text-xl font-bold text-red-600 mb-4">Error</h2>
          <p className="text-muted-foreground mb-4">{error}</p>
          <button 
            onClick={fetchReport} 
            className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Opnieuw proberen
          </button>
        </div>
      </div>
    );
  }

  if (!report) return null;

  const reportDate = new Date(report.report_date);
  const year = reportDate.getFullYear();

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link href="/">
            <button className="flex items-center gap-2 px-4 py-2 border rounded hover:bg-gray-100">
              ← Terug naar Dashboard
            </button>
          </Link>
          <div className="h-6 w-px bg-border"></div>
          <div>
            <h1 className="text-3xl font-bold">
              📅 Wekelijks Rapport - Week {report.week_number} van {year}
            </h1>
            <p className="text-muted-foreground">
              Gegenereerd op {reportDate.toLocaleDateString('nl-NL', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              })}
            </p>
          </div>
        </div>

        {/* Statistics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="p-6 border rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium">Trending Topics</h3>
              <span className="text-2xl">📈</span>
            </div>
            <div className="text-2xl font-bold text-blue-600">{report.statistics.trending_topics_count}</div>
            <p className="text-xs text-muted-foreground">AI onderwerpen geïdentificeerd</p>
          </div>

          <div className="p-6 border rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium">Experts</h3>
              <span className="text-2xl">👥</span>
            </div>
            <div className="text-2xl font-bold text-blue-600">{report.statistics.identified_experts_count}</div>
            <p className="text-xs text-muted-foreground">Potentiële podcast gasten</p>
          </div>

          <div className="p-6 border rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium">Podcast Suggesties</h3>
              <span className="text-2xl">💡</span>
            </div>
            <div className="text-2xl font-bold text-blue-600">{report.statistics.topic_suggestions_count}</div>
            <p className="text-xs text-muted-foreground">Onderwerp ideeën voor AIToday Live</p>
          </div>
        </div>

        {/* Highlights Section */}
        <div className="border rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">📊 Week Highlights</h2>
          <p className="text-muted-foreground mb-6">De meest opvallende ontwikkelingen van deze week</p>
          
          {/* Top Trending Topic */}
          {report.highlights.top_trending_topic && (
            <div className="mb-6">
              <h3 className="font-semibold text-lg mb-2"># Meest Trending Topic</h3>
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-lg">
                    {report.highlights.top_trending_topic.topic}
                  </span>
                  <span className={`px-2 py-1 rounded text-sm ${
                    report.highlights.top_trending_topic.sentiment === 'positive' ? 'bg-green-100 text-green-800' :
                    report.highlights.top_trending_topic.sentiment === 'negative' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {report.highlights.top_trending_topic.sentiment}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground mb-2">
                  {report.highlights.top_trending_topic.mentions} vermeldingen in {report.highlights.top_trending_topic.sources.length} bronnen
                </p>
                <p className="text-sm">
                  <strong>Suggested angle:</strong> {report.highlights.top_trending_topic.suggested_angle}
                </p>
              </div>
            </div>
          )}

          {/* Most Quoted Expert */}
          {report.highlights.most_quoted_expert && (
            <div className="mb-6">
              <h3 className="font-semibold text-lg mb-2">💬 Meest Geciteerde Expert</h3>
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium">{report.highlights.most_quoted_expert.name || 'Onbekende expert'}</h4>
                {(report.highlights.most_quoted_expert.title || report.highlights.most_quoted_expert.organization) && (
                  <p className="text-sm text-muted-foreground">
                    {report.highlights.most_quoted_expert.title || 'Expert'} 
                    {report.highlights.most_quoted_expert.organization && ` bij ${report.highlights.most_quoted_expert.organization}`}
                  </p>
                )}
                <p className="text-sm mt-2">
                  {report.highlights.most_quoted_expert.quote_count || report.highlights.most_quoted_expert.recent_quotes || 0} quotes in media deze week
                </p>
                {(report.highlights.most_quoted_expert.expertise_areas || report.highlights.most_quoted_expert.expertise) && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {(report.highlights.most_quoted_expert.expertise_areas || report.highlights.most_quoted_expert.expertise || []).slice(0, 5).map((area: string, index: number) => (
                      <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                        {area}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Trending Topics */}
        <div className="border rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">📈 Trending Topics ({(report.trends && report.trends.topics && report.trends.topics.length) || 0})</h2>
          <p className="text-muted-foreground mb-6">AI onderwerpen die deze week opvielen</p>
          
          {report.trends && report.trends.topics && report.trends.topics.length > 0 ? (
            <div className="space-y-4">
              {report.trends.topics.slice(0, 5).map((topic: any, index: number) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">{topic.topic || 'Onbekend onderwerp'}</span>
                    <span className={`px-2 py-1 rounded text-sm ${
                      topic.sentiment === 'positive' ? 'bg-green-100 text-green-800' :
                      topic.sentiment === 'negative' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {topic.sentiment || 'neutral'}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">
                    {topic.mentions || 0} vermeldingen • {(topic.sources && topic.sources.length) || 0} bronnen
                  </p>
                  <p className="text-sm">{topic.suggested_angle || 'Geen suggestie beschikbaar'}</p>
                  {topic.key_articles && topic.key_articles.length > 0 && (
                    <div className="mt-2">
                      <p className="text-xs font-medium">Belangrijkste artikel:</p>
                      <a 
                        href={topic.key_articles[0].url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-xs text-blue-600 hover:underline"
                      >
                        {topic.key_articles[0].title || 'Artikel titel niet beschikbaar'} ↗
                      </a>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-muted-foreground py-8">
              Geen trending topics beschikbaar
            </p>
          )}
        </div>

        {/* Experts */}
        <div className="border rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">👥 Top Experts</h2>
          <p className="text-muted-foreground mb-6">Potentiële gasten voor AIToday Live</p>
          
          {report.experts && report.experts.experts ? (
            <div className="space-y-4">
              {Array.isArray(report.experts.experts) ? (
                report.experts.experts.slice(0, 5).map((expert: any, index: number) => (
                  <div key={index} className="border rounded-lg p-4">
                    <h4 className="font-medium">{String(expert.name || 'Onbekende expert')}</h4>
                    {(expert.title || expert.organization) && (
                      <p className="text-sm text-muted-foreground">
                        {String(expert.title || 'Expert')}
                        {expert.organization && ` bij ${String(expert.organization)}`}
                      </p>
                    )}
                    <p className="text-sm mt-1">
                      {Number(expert.quote_count || expert.recent_quotes || 0)} quotes deze week
                    </p>
                    {(expert.expertise_areas || expert.expertise) && Array.isArray(expert.expertise_areas || expert.expertise) && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {(expert.expertise_areas || expert.expertise || []).slice(0, 3).map((area: any, areaIndex: number) => (
                          <span key={areaIndex} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                            {String(area)}
                          </span>
                        ))}
                      </div>
                    )}
                    {expert.quotes && Array.isArray(expert.quotes) && expert.quotes.length > 0 && (
                      <div className="mt-2 p-2 bg-gray-100 rounded text-xs italic">
                        "{String(expert.quotes[0].text || expert.quotes[0].quote || 'Quote niet beschikbaar')}"
                      </div>
                    )}
                  </div>
                ))
              ) : (
                // Handle single expert object
                <div className="border rounded-lg p-4">
                  <h4 className="font-medium">{String(report.experts.experts.name || 'Onbekende expert')}</h4>
                  {(report.experts.experts.title || report.experts.experts.organization) && (
                    <p className="text-sm text-muted-foreground">
                      {String(report.experts.experts.title || 'Expert')}
                      {report.experts.experts.organization && ` bij ${String(report.experts.experts.organization)}`}
                    </p>
                  )}
                  <p className="text-sm mt-1">
                    {Number(report.experts.experts.quote_count || report.experts.experts.recent_quotes || 0)} quotes deze week
                  </p>
                  {(report.experts.experts.expertise_areas || report.experts.experts.expertise) && Array.isArray(report.experts.experts.expertise_areas || report.experts.experts.expertise) && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {(report.experts.experts.expertise_areas || report.experts.experts.expertise || []).slice(0, 5).map((area: any, areaIndex: number) => (
                        <span key={areaIndex} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                          {String(area)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <p className="text-center text-muted-foreground py-8">
              Geen experts beschikbaar
            </p>
          )}
        </div>

        {/* Topic Suggestions */}
        <div className="border rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">💡 Podcast Topic Suggesties ({(report.suggestions && report.suggestions.suggestions && report.suggestions.suggestions.length) || 0})</h2>
          <p className="text-muted-foreground mb-6">Concrete ideeën voor AIToday Live afleveringen</p>
          
          {report.suggestions && report.suggestions.suggestions && report.suggestions.suggestions.length > 0 ? (
            <div className="space-y-6">
              {report.suggestions.suggestions.map((suggestion: any, index: number) => (
                <div key={index} className="border rounded-lg p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-lg">{suggestion.title}</h3>
                      <p className="text-muted-foreground mt-1">{suggestion.description}</p>
                    </div>
                    <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded text-sm">
                      Urgency {suggestion.urgency_score}/10
                    </span>
                  </div>
                  
                  <div className="mb-4">
                    <h4 className="font-medium mb-2">Suggested Angle:</h4>
                    <p className="text-sm bg-gray-100 p-3 rounded">{suggestion.angle}</p>
                  </div>

                  {suggestion.potential_guests && suggestion.potential_guests.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-medium mb-2">Potentiële Gasten:</h4>
                      <div className="flex flex-wrap gap-2">
                        {suggestion.potential_guests.map((guest: string, guestIndex: number) => (
                          <span key={guestIndex} className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                            {guest}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {suggestion.supporting_articles && suggestion.supporting_articles.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-2">Ondersteunende Artikelen:</h4>
                      <div className="space-y-1">
                        {suggestion.supporting_articles.slice(0, 3).map((article: any, articleIndex: number) => (
                          <a
                            key={articleIndex}
                            href={article.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-2 text-sm text-blue-600 hover:underline"
                          >
                            🌍 {article.title} - {article.source} ↗
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-muted-foreground py-8">
              Geen podcast suggesties beschikbaar
            </p>
          )}
        </div>
      </div>
    </div>
  );
}