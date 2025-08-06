import { NextRequest, NextResponse } from 'next/server';
import { logManager } from '@/lib/logs';

export async function GET(
  request: NextRequest,
  { params }: { params: { filename: string } }
) {
  try {
    const { filename } = params;

    if (!filename) {
      return NextResponse.json(
        { error: 'Filename is required' },
        { status: 400 }
      );
    }

    const content = await logManager.getLogContent(filename);

    if (content === null) {
      return NextResponse.json(
        { error: 'Log file not found or could not be read' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      filename,
      content,
      lines: content.split('\n').length,
      size: Buffer.byteLength(content, 'utf8')
    });
  } catch (error) {
    console.error('Error fetching log content:', error);
    return NextResponse.json(
      { error: 'Failed to fetch log content' },
      { status: 500 }
    );
  }
}