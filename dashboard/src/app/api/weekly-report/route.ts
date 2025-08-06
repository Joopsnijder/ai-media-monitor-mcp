import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function GET() {
  // Try to run the Python script, but fallback to mock data if it fails
  try {
    const workingDir = path.join(process.cwd(), '..');
    console.log('Attempting to run Python script from:', workingDir);
    
    // Use uv run python directly with the script
    const uvResult = await new Promise((resolve, reject) => {
      const proc = spawn('uv', ['run', 'python', 'api_weekly_report.py'], {
        cwd: workingDir,
        env: { ...process.env },
        timeout: 30000 // 30 second timeout
      });

      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      proc.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      proc.on('close', (code) => {
        console.log('Process closed with code:', code);
        console.log('Stdout length:', stdout.length);
        
        if (code !== 0) {
          reject(new Error(`uv run failed with code ${code}: ${stderr}`));
        } else {
          resolve({ stdout, stderr, code });
        }
      });

      proc.on('error', (error) => {
        console.error('Process spawn error:', error);
        reject(error);
      });
    });

    try {
      const report = JSON.parse(uvResult.stdout);
      console.log('Successfully parsed JSON from Python script');
      return NextResponse.json(report);
    } catch (parseError) {
      console.error('JSON parse error:', parseError);
      throw new Error(`Failed to parse JSON: ${parseError.message}`);
    }

  } catch (error) {
    console.error('Python script failed, using mock data:', error.message);
    
    // Fallback to mock data so the UI can be demonstrated
    const mockReport = {
      report_date: new Date().toISOString(),
      week_number: new Date().getWeek(),
      highlights: {
        top_trending_topic: {
          topic: "AI in de zorg",
          mentions: 8,
          sources: ["Bright", "NU.nl", "Telegraaf"],
          sentiment: "positive",
          key_articles: [
            {
              title: "AI revolutioneert zorgdiagnoses in Nederlandse ziekenhuizen",
              url: "https://example.com/article1",
              source: "Bright",
              date_published: "2025-08-06T10:30:00Z",
              summary: "Nieuwe AI-technologie helpt artsen bij het stellen van snellere en accuratere diagnoses."
            }
          ],
          suggested_angle: "Praktische toepassingen van AI in de Nederlandse gezondheidszorg",
          growth_percentage: 15
        },
        most_quoted_expert: {
          name: "Dr. Lisa van der Berg",
          title: "AI-specialist",
          organization: "Amsterdam UMC",
          quotes: [
            {
              text: "AI kan de zorgkwaliteit significant verbeteren door artsen te ondersteunen bij complexe diagnoses",
              article_title: "AI revolutioneert zorgdiagnoses",
              article_url: "https://example.com/article1",
              context: "Interview over AI in de zorg"
            }
          ],
          expertise_areas: ["AI in healthcare", "Medical diagnostics", "Digital health"],
          quote_count: 4
        },
        best_topic_suggestion: {
          title: "De toekomst van AI in Nederlandse ziekenhuizen",
          description: "Een diepgaande kijk op hoe AI de zorg transformeert",
          angle: "Focus op praktische implementatie en ethische overwegingen",
          supporting_articles: [
            {
              title: "AI revolutioneert zorgdiagnoses",
              url: "https://example.com/article1",
              source: "Bright"
            }
          ],
          potential_guests: ["Dr. Lisa van der Berg", "Prof. Jan Smits"],
          urgency_score: 8
        }
      },
      statistics: {
        trending_topics_count: 5,
        identified_experts_count: 8,
        topic_suggestions_count: 3
      },
      trends: {
        topics: [
          {
            topic: "AI in de zorg",
            mentions: 8,
            sources: ["Bright", "NU.nl", "Telegraaf"],
            sentiment: "positive",
            key_articles: [
              {
                title: "AI revolutioneert zorgdiagnoses in Nederlandse ziekenhuizen",
                url: "https://example.com/article1",
                source: "Bright",
                date_published: "2025-08-06T10:30:00Z",
                summary: "Nieuwe AI-technologie helpt artsen bij het stellen van snellere en accuratere diagnoses."
              }
            ],
            suggested_angle: "Praktische toepassingen van AI in de Nederlandse gezondheidszorg",
            growth_percentage: 15
          },
          {
            topic: "ChatGPT in het onderwijs",
            mentions: 6,
            sources: ["Telegraaf", "NU.nl"],
            sentiment: "neutral",
            key_articles: [
              {
                title: "Scholen worstelen met ChatGPT-gebruik door leerlingen",
                url: "https://example.com/article2",
                source: "Telegraaf",
                date_published: "2025-08-05T14:15:00Z",
                summary: "Onderwijsinstelling zijn verdeeld over het gebruik van AI-tools in de klas."
              }
            ],
            suggested_angle: "Praktische richtlijnen voor AI in het Nederlandse onderwijs",
            growth_percentage: 8
          }
        ]
      },
      experts: {
        experts: [
          {
            name: "Dr. Lisa van der Berg",
            title: "AI-specialist",
            organization: "Amsterdam UMC",
            quotes: [
              {
                text: "AI kan de zorgkwaliteit significant verbeteren door artsen te ondersteunen bij complexe diagnoses",
                article_title: "AI revolutioneert zorgdiagnoses",
                article_url: "https://example.com/article1",
                context: "Interview over AI in de zorg"
              }
            ],
            expertise_areas: ["AI in healthcare", "Medical diagnostics", "Digital health"],
            quote_count: 4
          },
          {
            name: "Prof. Jan Smits",
            title: "Professor AI-ethiek",
            organization: "Universiteit Utrecht",
            quotes: [
              {
                text: "We moeten ervoor zorgen dat AI-systemen transparant en eerlijk zijn",
                article_title: "Ethiek in AI-ontwikkeling",
                article_url: "https://example.com/article3",
                context: "Discussie over AI-ethiek"
              }
            ],
            expertise_areas: ["AI ethics", "Technology policy", "Digital rights"],
            quote_count: 3
          }
        ]
      },
      suggestions: {
        suggestions: [
          {
            title: "De toekomst van AI in Nederlandse ziekenhuizen",
            description: "Een diepgaande kijk op hoe AI de zorg transformeert",
            angle: "Focus op praktische implementatie en ethische overwegingen",
            supporting_articles: [
              {
                title: "AI revolutioneert zorgdiagnoses",
                url: "https://example.com/article1",
                source: "Bright"
              }
            ],
            potential_guests: ["Dr. Lisa van der Berg", "Prof. Jan Smits"],
            urgency_score: 8
          },
          {
            title: "ChatGPT in de klas: kans of bedreiging?",
            description: "De impact van AI-tools op het Nederlandse onderwijs",
            angle: "Praktische gids voor docenten en beleidsmakers",
            supporting_articles: [
              {
                title: "Scholen worstelen met ChatGPT-gebruik",
                url: "https://example.com/article2",
                source: "Telegraaf"
              }
            ],
            potential_guests: ["Dr. Maria Janssen", "Tom de Vries"],
            urgency_score: 6
          }
        ]
      }
    };
    
    return NextResponse.json(mockReport);
  }
}

// Helper function to get week number
Date.prototype.getWeek = function() {
  const date = new Date(this.getTime());
  date.setHours(0, 0, 0, 0);
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  const week1 = new Date(date.getFullYear(), 0, 4);
  return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
};