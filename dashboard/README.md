# AI Media Monitor Dashboard

A modern web dashboard for monitoring the AI Media Monitor system's database content and log file status in real-time.

## Features

### 📊 Database Monitoring
- Real-time article count and statistics
- Source distribution and activity metrics
- AI topics analysis and trending content
- Historical data visualization

### 📋 Log File Monitoring  
- Latest collection run status and health indicators
- Error detection and alert system
- Processing statistics timeline
- Log file health and size monitoring

### 🎨 Modern UI
- Dark theme with orange accent colors
- Responsive design for desktop and mobile
- Professional shadcn/ui components
- Real-time data updates every 30 seconds

## Quick Start

### Prerequisites
- Node.js 18+ installed
- Access to the parent project's `data/articles.db` SQLite database
- Access to the parent project's `logs/` directory

### Installation

1. **Navigate to dashboard directory:**
   ```bash
   cd dashboard
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Development

### Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Create production build
- `npm run start` - Start production server
- `npm run lint` - Run ESLint checks

### Project Structure

```
dashboard/
├── src/
│   ├── app/
│   │   ├── api/           # API routes for data fetching
│   │   │   ├── articles/  # Article data endpoints
│   │   │   ├── stats/     # Statistics endpoints
│   │   │   └── logs/      # Log monitoring endpoints
│   │   ├── globals.css    # Global styles with dark theme
│   │   ├── layout.tsx     # Root layout component
│   │   └── page.tsx       # Main dashboard page
│   └── components/
│       └── ui/            # shadcn/ui components
├── lib/
│   ├── database.ts        # SQLite database connection utilities
│   ├── logs.ts           # Log file parsing utilities
│   └── utils.ts          # General utility functions
├── components.json        # shadcn/ui configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── package.json          # Project dependencies
```

### API Endpoints

#### `/api/articles`
- **GET** - Fetch articles with optional filtering
- Query parameters:
  - `limit` - Number of articles to return (default: 50)
  - `offset` - Pagination offset (default: 0)  
  - `hours` - Filter articles from last N hours

#### `/api/stats`
- **GET** - Get comprehensive statistics
- Query parameters:
  - `hoursBack` - Timeframe for statistics (default: 168 hours / 7 days)
- Returns: database stats, sources breakdown, topics analysis

#### `/api/logs`
- **GET** - Fetch log file information
- Query parameters:
  - `type` - "recent", "stats", or null for all logs
  - `count` - Number of recent logs to return (default: 10)

## Configuration

### Database Connection
The dashboard automatically connects to the parent project's SQLite database at `../data/articles.db`. No additional configuration is required.

### Log Monitoring
Log files are read from `../logs/` directory. The system automatically parses:
- Daily collection logs (`daily_collection_YYYYMMDD_HHMMSS.log`)
- Weekly report logs (`weekly_report_YYYYMMDD_HHMMSS.log`)

### Theme Customization
The dark theme with orange highlights is configured in:
- `src/app/globals.css` - CSS custom properties
- `tailwind.config.js` - Tailwind theme configuration
- `components.json` - shadcn/ui theme settings

## Deployment

### Local Production Build
```bash
npm run build
npm run start
```

### Port Configuration
By default, the development server runs on port 3000. To change this:
```bash
npm run dev -- -p 3001
```

## Monitoring Features

### System Health Indicators
- 🟢 **Healthy** - No recent errors, collections running successfully
- 🟡 **Warning** - Some errors but more successful runs than failures  
- 🔴 **Critical** - More errors than successful runs

### Real-time Updates
- Data refreshes automatically every 30 seconds
- Manual refresh button available in header
- Last update timestamp displayed

### Error Detection
- Automatic parsing of log files for error patterns
- Error count tracking and display
- Recent error logs prominently displayed

## Troubleshooting

### Database Connection Issues
- Ensure `../data/articles.db` exists and is readable
- Check SQLite database permissions
- Verify Node.js has access to parent directory

### Log Parsing Issues  
- Ensure `../logs/` directory exists
- Check log file naming conventions
- Verify read permissions on log files

### Development Server Issues
- Ensure Node.js 18+ is installed
- Clear `node_modules` and run `npm install` again
- Check for port conflicts (default: 3000)

## Technology Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Database**: SQLite (read-only access)
- **Icons**: Lucide React
- **Charts**: Recharts (for future data visualization)
