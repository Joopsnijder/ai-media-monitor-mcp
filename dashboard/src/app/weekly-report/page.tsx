'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { 
  ArrowLeft, 
  TrendingUp, 
  Users, 
  Lightbulb, 
  Calendar, 
  ExternalLink,
  BarChart3,
  MessageSquote,
  Globe,
  Hash
} from 'lucide-react';

interface TrendingTopic {
  topic: string;
  mentions: number;
  sources: string[];
  sentiment: string;
  key_articles: Array<{
    title: string;
    url: string;
    source: string;
    date_published: string;
    summary: string;
  }>;
  suggested_angle: string;
  growth_percentage: number | null;
}

interface Expert {
  name: string;
  title: string;
  organization: string;
  quotes: Array<{
    text: string;
    article_title: string;
    article_url: string;
    context: string;
  }>;
  expertise_areas: string[];
  quote_count: number;
}

interface TopicSuggestion {
  title: string;
  description: string;
  angle: string;
  supporting_articles: Array<{
    title: string;
    url: string;
    source: string;
  }>;
  potential_guests: string[];
  urgency_score: number;
}

interface WeeklyReport {
  report_date: string;
  week_number: number;
  highlights: {
    top_trending_topic: TrendingTopic | null;
    most_quoted_expert: Expert | null;
    best_topic_suggestion: TopicSuggestion | null;
  };
  statistics: {
    trending_topics_count: number;
    identified_experts_count: number;
    topic_suggestions_count: number;
  };
  trends: {
    topics: TrendingTopic[];
  };
  experts: {
    experts: Expert[];
  };
  suggestions: {
    suggestions: TopicSuggestion[];
  };
}

export default function WeeklyReportPage() {
  const [report, setReport] = useState<WeeklyReport | null>(null);
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
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle className="text-destructive">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">{error}</p>
            <Button onClick={fetchReport} className="w-full">
              Opnieuw proberen
            </Button>
          </CardContent>
        </Card>
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
            <Button variant="ghost" size="sm">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Terug naar Dashboard
            </Button>
          </Link>
          <div className="h-6 w-px bg-border"></div>
          <div>
            <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
              <Calendar className="w-8 h-8" />
              Wekelijks Rapport - Week {report.week_number} van {year}
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
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Trending Topics</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">{report.statistics.trending_topics_count}</div>
              <p className="text-xs text-muted-foreground">AI onderwerpen geïdentificeerd</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Experts</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">{report.statistics.identified_experts_count}</div>
              <p className="text-xs text-muted-foreground">Potentiële podcast gasten</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Podcast Suggesties</CardTitle>
              <Lightbulb className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">{report.statistics.topic_suggestions_count}</div>
              <p className="text-xs text-muted-foreground">Onderwerp ideeën voor AIToday Live</p>
            </CardContent>
          </Card>
        </div>

        {/* Highlights Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5" />
              Week Highlights
            </CardTitle>
            <CardDescription>De meest opvallende ontwikkelingen van deze week</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Top Trending Topic */}
            {report.highlights.top_trending_topic && (
              <div>
                <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                  <Hash className="w-4 h-4" />
                  Meest Trending Topic
                </h3>
                <div className="bg-muted p-4 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <Badge variant="outline" className="text-lg">
                      {report.highlights.top_trending_topic.topic}
                    </Badge>
                    <Badge variant={
                      report.highlights.top_trending_topic.sentiment === 'positive' ? 'default' :
                      report.highlights.top_trending_topic.sentiment === 'negative' ? 'destructive' : 'secondary'
                    }>
                      {report.highlights.top_trending_topic.sentiment}
                    </Badge>
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
              <div>
                <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                  <MessageSquote className="w-4 h-4" />
                  Meest Geciteerde Expert
                </h3>
                <div className="bg-muted p-4 rounded-lg">
                  <h4 className="font-medium">{report.highlights.most_quoted_expert.name}</h4>
                  <p className="text-sm text-muted-foreground">
                    {report.highlights.most_quoted_expert.title} bij {report.highlights.most_quoted_expert.organization}
                  </p>
                  <p className="text-sm mt-2">
                    {report.highlights.most_quoted_expert.quote_count} quotes in media deze week
                  </p>
                  <div className="flex flex-wrap gap-1 mt-2">
                    {report.highlights.most_quoted_expert.expertise_areas.map((area, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {area}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Best Topic Suggestion */}
            {report.highlights.best_topic_suggestion && (
              <div>
                <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                  <Lightbulb className="w-4 h-4" />
                  Top Podcast Suggestie
                </h3>
                <div className="bg-muted p-4 rounded-lg">
                  <h4 className="font-medium">{report.highlights.best_topic_suggestion.title}</h4>
                  <p className="text-sm text-muted-foreground mt-1">
                    {report.highlights.best_topic_suggestion.description}
                  </p>
                  <p className="text-sm mt-2">
                    <strong>Angle:</strong> {report.highlights.best_topic_suggestion.angle}
                  </p>
                  <Badge variant="outline" className="mt-2">
                    Urgency: {report.highlights.best_topic_suggestion.urgency_score}/10
                  </Badge>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Detailed Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Trending Topics */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Trending Topics ({report.trends.topics.length})
              </CardTitle>
              <CardDescription>AI onderwerpen die deze week opvielen</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {report.trends.topics.slice(0, 5).map((topic, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <Badge variant="outline">{topic.topic}</Badge>
                      <Badge variant={
                        topic.sentiment === 'positive' ? 'default' :
                        topic.sentiment === 'negative' ? 'destructive' : 'secondary'
                      }>
                        {topic.sentiment}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">
                      {topic.mentions} vermeldingen • {topic.sources.length} bronnen
                    </p>
                    <p className="text-sm">{topic.suggested_angle}</p>
                    {topic.key_articles.length > 0 && (
                      <div className="mt-2">
                        <p className="text-xs font-medium">Belangrijkste artikel:</p>
                        <a 
                          href={topic.key_articles[0].url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-xs text-blue-600 hover:underline flex items-center gap-1"
                        >
                          {topic.key_articles[0].title}
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Top Experts */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5" />
                Top Experts ({report.experts.experts.length})
              </CardTitle>
              <CardDescription>Potentiële gasten voor AIToday Live</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {report.experts.experts.slice(0, 5).map((expert, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <h4 className="font-medium">{expert.name}</h4>
                    <p className="text-sm text-muted-foreground">
                      {expert.title} bij {expert.organization}
                    </p>
                    <p className="text-sm mt-1">
                      {expert.quote_count} quotes deze week
                    </p>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {expert.expertise_areas.slice(0, 3).map((area, areaIndex) => (
                        <Badge key={areaIndex} variant="outline" className="text-xs">
                          {area}
                        </Badge>
                      ))}
                    </div>
                    {expert.quotes.length > 0 && (
                      <div className="mt-2 p-2 bg-muted rounded text-xs italic">
                        "{expert.quotes[0].text}"
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Topic Suggestions */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Lightbulb className="w-5 h-5" />
              Podcast Topic Suggesties ({report.suggestions.suggestions.length})
            </CardTitle>
            <CardDescription>Concrete ideeën voor AIToday Live afleveringen</CardDescription>
          </CardHeader>
          <CardContent>
            {report.suggestions.suggestions.length > 0 ? (
              <div className="grid gap-4">
                {report.suggestions.suggestions.map((suggestion, index) => (
                  <div key={index} className="border rounded-lg p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="font-semibold text-lg">{suggestion.title}</h3>
                        <p className="text-muted-foreground mt-1">{suggestion.description}</p>
                      </div>
                      <Badge variant="outline">
                        Urgency {suggestion.urgency_score}/10
                      </Badge>
                    </div>
                    
                    <div className="mb-4">
                      <h4 className="font-medium mb-2">Suggested Angle:</h4>
                      <p className="text-sm bg-muted p-3 rounded">{suggestion.angle}</p>
                    </div>

                    {suggestion.potential_guests.length > 0 && (
                      <div className="mb-4">
                        <h4 className="font-medium mb-2">Potentiële Gasten:</h4>
                        <div className="flex flex-wrap gap-2">
                          {suggestion.potential_guests.map((guest, guestIndex) => (
                            <Badge key={guestIndex} variant="secondary">
                              {guest}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {suggestion.supporting_articles.length > 0 && (
                      <div>
                        <h4 className="font-medium mb-2">Ondersteunende Artikelen:</h4>
                        <div className="space-y-1">
                          {suggestion.supporting_articles.slice(0, 3).map((article, articleIndex) => (
                            <a
                              key={articleIndex}
                              href={article.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center gap-2 text-sm text-blue-600 hover:underline"
                            >
                              <Globe className="w-3 h-3" />
                              {article.title} - {article.source}
                              <ExternalLink className="w-3 h-3" />
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
          </CardContent>
        </Card>
      </div>
    </div>
  );
}