import { NextRequest, NextResponse } from 'next/server';
import { logManager } from '@/lib/logs';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const type = searchParams.get('type'); // 'recent', 'stats', or null for all
    const count = parseInt(searchParams.get('count') || '10');

    if (type === 'stats') {
      const stats = await logManager.getLogStats();
      return NextResponse.json(stats);
    }

    if (type === 'recent') {
      const recentLogs = await logManager.getRecentLogs(count);
      return NextResponse.json(recentLogs);
    }

    // Default: return all log files
    const logs = await logManager.getLogFiles();
    return NextResponse.json(logs);
  } catch (error) {
    console.error('Error fetching logs:', error);
    return NextResponse.json(
      { error: 'Failed to fetch logs' },
      { status: 500 }
    );
  }
}