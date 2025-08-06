'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Database, FileText, Activity, AlertTriangle, CheckCircle, Clock, ExternalLink } from 'lucide-react';

interface DatabaseStats {
  total_articles: number;
  unique_sources: number;
  earliest_article: string;
  latest_article: string;
  sources: { [key: string]: number };
}

interface LogStats {
  totalLogs: number;
  recentSuccessful: number;
  recentErrors: number;
  lastCollection: LogInfo | null;
  errorLogs: LogInfo[];
}

interface LogInfo {
  filename: string;
  date: string;
  type: string;
  status: string;
  summary?: string;
}

interface StatsData {
  database: DatabaseStats;
  sources: { [key: string]: number };
  topics: { [key: string]: number };
  timeframe: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [logStats, setLogStats] = useState<LogStats | null>(null);
  const [recentLogs, setRecentLogs] = useState<LogInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const fetchData = async () => {
    try {
      const [statsResponse, logsResponse, recentLogsResponse] = await Promise.all([
        fetch('/api/stats'),
        fetch('/api/logs?type=stats'),
        fetch('/api/logs?type=recent&count=10')
      ]);

      if (statsResponse.ok && logsResponse.ok && recentLogsResponse.ok) {
        const statsData = await statsResponse.json();
        const logsData = await logsResponse.json();
        const recentLogsData = await recentLogsResponse.json();
        
        setStats(statsData);
        setLogStats(logsData);
        setRecentLogs(recentLogsData);
        setLastUpdate(new Date());
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const topSources = stats?.sources ? Object.entries(stats.sources)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5) : [];

  const topTopics = stats?.topics ? Object.entries(stats.topics)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 8) : [];

  const systemHealth = logStats ? 
    (logStats.recentErrors === 0 ? 'healthy' : 
     logStats.recentSuccessful > logStats.recentErrors ? 'warning' : 'critical') : 'unknown';

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-foreground">AI Media Monitor</h1>
            <p className="text-muted-foreground">Real-time system monitoring dashboard</p>
          </div>
          <div className="flex items-center gap-4">
            <Badge variant="outline" className="text-xs">
              Last update: {lastUpdate.toLocaleTimeString()}
            </Badge>
            <Button 
              onClick={fetchData} 
              size="sm"
              className="bg-primary hover:bg-primary/90"
            >
              Refresh
            </Button>
          </div>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Articles</CardTitle>
              <Database className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">{stats?.database.total_articles || 0}</div>
              <p className="text-xs text-muted-foreground">
                From {stats?.database.unique_sources || 0} sources
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">System Health</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                {systemHealth === 'healthy' && (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                )}
                {systemHealth === 'warning' && (
                  <AlertTriangle className="h-5 w-5 text-yellow-500" />
                )}
                {systemHealth === 'critical' && (
                  <AlertTriangle className="h-5 w-5 text-red-500" />
                )}
                <span className="text-2xl font-bold capitalize">{systemHealth}</span>
              </div>
              <p className="text-xs text-muted-foreground">
                {logStats?.recentSuccessful || 0} successful, {logStats?.recentErrors || 0} errors
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Recent Activity</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">
                {Object.values(stats?.sources || {}).reduce((a, b) => a + b, 0)}
              </div>
              <p className="text-xs text-muted-foreground">
                Articles last 7 days
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Log Files</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">{logStats?.totalLogs || 0}</div>
              <p className="text-xs text-muted-foreground">
                Collection logs available
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Top Sources */}
          <Card>
            <CardHeader>
              <CardTitle>Top Sources (Last 7 Days)</CardTitle>
              <CardDescription>Most active article sources</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topSources.map(([source, count], index) => (
                  <div key={source} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary">{index + 1}</Badge>
                      <span className="text-sm font-medium">{source}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-muted-foreground">{count} articles</span>
                      <Progress 
                        value={(count / Math.max(...Object.values(stats?.sources || {}))) * 100} 
                        className="w-20"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Top AI Topics */}
          <Card>
            <CardHeader>
              <CardTitle>Trending AI Topics</CardTitle>
              <CardDescription>Most mentioned topics in recent articles</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {topTopics.map(([topic, count]) => (
                  <Badge key={topic} variant="outline" className="text-xs">
                    {topic} ({count})
                  </Badge>
                ))}
              </div>
              {topTopics.length === 0 && (
                <p className="text-sm text-muted-foreground">No topic data available</p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Recent Log Files */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Log Files</CardTitle>
            <CardDescription>All recent collection and report logs</CardDescription>
          </CardHeader>
          <CardContent>
            {recentLogs.length > 0 ? (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Log File</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Date</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Summary</TableHead>
                    <TableHead></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {recentLogs.map((log) => (
                    <TableRow key={log.filename}>
                      <TableCell className="font-medium">
                        {log.filename}
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">
                          {log.type === 'daily_collection' ? 'Daily Collection' : 'Weekly Report'}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {new Date(log.lastModified).toLocaleString()}
                      </TableCell>
                      <TableCell>
                        <Badge 
                          variant={
                            log.status === 'success' ? 'default' : 
                            log.status === 'error' ? 'destructive' : 'secondary'
                          }
                        >
                          {log.status}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-sm max-w-xs truncate">
                        {log.summary || 'No summary available'}
                      </TableCell>
                      <TableCell>
                        <Link href={`/logs/${log.filename}`}>
                          <Button variant="ghost" size="sm">
                            <ExternalLink className="w-4 h-4" />
                          </Button>
                        </Link>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            ) : (
              <p className="text-sm text-muted-foreground">No log files available</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
