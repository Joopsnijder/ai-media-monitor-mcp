import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function GET() {
  try {
    // Create a simple Python script that only outputs JSON
    const scriptPath = path.join(process.cwd(), '..', 'api_weekly_report.py');
    
    const promise = new Promise((resolve, reject) => {
      const python = spawn('python', [scriptPath], {
        cwd: path.join(process.cwd(), '..'),
        env: { ...process.env }
      });

      let stdout = '';
      let stderr = '';

      python.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      python.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      python.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(`Weekly report script failed: ${stderr}`));
        } else {
          try {
            // Parse the JSON output from the script
            const report = JSON.parse(stdout);
            resolve(report);
          } catch (error) {
            reject(new Error(`Failed to parse weekly report JSON: ${stdout}\nError: ${error}`));
          }
        }
      });

      python.on('error', (error) => {
        reject(new Error(`Failed to start weekly report script: ${error}`));
      });
    });

    const report = await promise;
    return NextResponse.json(report);

  } catch (error) {
    console.error('Error generating weekly report:', error);
    return NextResponse.json(
      { error: 'Failed to generate weekly report', details: error.message },
      { status: 500 }
    );
  }
}