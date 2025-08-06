import { NextRequest, NextResponse } from 'next/server';
import { database } from '@/lib/database';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = parseInt(searchParams.get('offset') || '0');
    const hours = searchParams.get('hours');

    let articles;
    if (hours) {
      articles = await database.getArticlesSince(parseInt(hours));
    } else {
      articles = await database.getArticles(limit, offset);
    }

    return NextResponse.json(articles);
  } catch (error) {
    console.error('Error fetching articles:', error);
    return NextResponse.json(
      { error: 'Failed to fetch articles' },
      { status: 500 }
    );
  }
}