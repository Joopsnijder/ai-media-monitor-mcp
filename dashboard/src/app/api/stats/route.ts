import { NextRequest, NextResponse } from 'next/server';
import { database } from '@/lib/database';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const hoursBack = parseInt(searchParams.get('hoursBack') || '168'); // Default 7 days

    const [databaseStats, sourcesStats, topicStats] = await Promise.all([
      database.getDatabaseStats(),
      database.getSourcesStats(hoursBack),
      database.getTopicStats(hoursBack)
    ]);

    return NextResponse.json({
      database: databaseStats,
      sources: sourcesStats,
      topics: topicStats,
      timeframe: hoursBack
    });
  } catch (error) {
    console.error('Error fetching stats:', error);
    return NextResponse.json(
      { error: 'Failed to fetch statistics' },
      { status: 500 }
    );
  }
}