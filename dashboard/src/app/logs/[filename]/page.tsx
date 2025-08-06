'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, Copy, Download, CheckCircle } from 'lucide-react';

interface LogData {
  filename: string;
  content: string;
  lines: number;
  size: number;
}

export default function LogDetailPage() {
  const params = useParams();
  const router = useRouter();
  const filename = params.filename as string;

  const [logData, setLogData] = useState<LogData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copySuccess, setCopySuccess] = useState(false);

  useEffect(() => {
    if (filename) {
      fetchLogContent();
    }
  }, [filename]);

  const fetchLogContent = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/logs/${filename}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch log content');
      }

      const data = await response.json();
      setLogData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async () => {
    if (!logData) return;

    try {
      await navigator.clipboard.writeText(logData.content);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
    }
  };

  const downloadLog = () => {
    if (!logData) return;

    const blob = new Blob([logData.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const formatDate = (filename: string) => {
    const match = filename.match(/(\d{8}_\d{6})/);
    if (match) {
      const dateStr = match[1];
      const year = dateStr.substring(0, 4);
      const month = dateStr.substring(4, 6);
      const day = dateStr.substring(6, 8);
      const hour = dateStr.substring(9, 11);
      const minute = dateStr.substring(11, 13);
      const second = dateStr.substring(13, 15);
      
      return `${day}/${month}/${year} ${hour}:${minute}:${second}`;
    }
    return filename;
  };

  const getLogType = (filename: string) => {
    if (filename.includes('daily_collection')) return 'Daily Collection';
    if (filename.includes('weekly_report')) return 'Weekly Report';
    return 'Unknown';
  };

  const getLogStatus = (content: string) => {
    const lines = content.toLowerCase();
    if (lines.includes('error') || lines.includes('failed')) return 'error';
    if (lines.includes('=== statistics ===')) return 'success';
    return 'running';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">Loading log content...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background p-4">
        <div className="max-w-4xl mx-auto">
          <Button 
            onClick={() => router.back()} 
            variant="ghost" 
            className="mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
          
          <Card>
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-red-500 text-lg font-medium">Error loading log</p>
                <p className="text-muted-foreground mt-2">{error}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  if (!logData) {
    return null;
  }

  const status = getLogStatus(logData.content);

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <Button 
              onClick={() => router.back()} 
              variant="ghost"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Button>
            
            <div>
              <h1 className="text-2xl font-bold text-foreground">{filename}</h1>
              <p className="text-muted-foreground">
                {getLogType(filename)} • {formatDate(filename)}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Badge 
              variant={status === 'success' ? 'default' : status === 'error' ? 'destructive' : 'secondary'}
            >
              {status}
            </Badge>
            
            <div className="text-sm text-muted-foreground">
              {logData.lines.toLocaleString()} lines • {(logData.size / 1024).toFixed(1)} KB
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2 mb-4">
          <Button onClick={copyToClipboard} variant="outline">
            {copySuccess ? (
              <CheckCircle className="w-4 h-4 mr-2 text-green-500" />
            ) : (
              <Copy className="w-4 h-4 mr-2" />
            )}
            {copySuccess ? 'Copied!' : 'Copy to Clipboard'}
          </Button>
          
          <Button onClick={downloadLog} variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Download Log
          </Button>
        </div>

        {/* Log Content */}
        <Card>
          <CardHeader>
            <CardTitle>Log Content</CardTitle>
            <CardDescription>
              Full log file content with line numbers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative">
              <pre className="bg-muted/30 border rounded-lg p-4 overflow-auto max-h-[70vh] text-sm font-mono">
                {logData.content.split('\n').map((line, index) => (
                  <div key={index} className="flex">
                    <span className="text-muted-foreground select-none w-12 text-right pr-4 border-r border-border/30">
                      {index + 1}
                    </span>
                    <span className="pl-4 flex-1 break-all">
                      {line || '\u00A0'}
                    </span>
                  </div>
                ))}
              </pre>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}