# Claude Code Project Documentation

## Project: AI Companies Dashboard

### Last Updated: 2026-01-28

## Overview
Interactive web dashboard for displaying and filtering AI companies data from Google Sheets. Features automatic data refresh, search functionality, and responsive design optimized for both desktop and mobile viewing.

## Project Architecture

### Technology Stack
- **Frontend Framework**: Vanilla JavaScript (zero dependencies)
- **Architecture Pattern**: Modular class-based design
- **Data Source**: Google Sheets CSV export with local CSV fallback
- **Styling**: Pure CSS with CSS variables (design tokens)
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

### Core Components

#### 1. Configuration (CONFIG object)
```javascript
const CONFIG = {
    GOOGLE_SHEET_ID: '1m5ghTUb146W0koJ4Hdt8DaugrgVr7NVyrt4cOECVPS0',
    SHEET_NAME: 'Sheet1',
    AUTO_REFRESH_INTERVAL: 300000, // 5 minutes in milliseconds
    REQUIRED_FIELD: 'Company Name',
    SEARCH_DEBOUNCE_MS: 150, // Debounce delay for search input
    FALLBACK_CSV: 'sample-data.csv' // Fallback CSV if Google Sheets fails
};
```

#### 2. CSVParser
- Parses CSV text into JavaScript objects
- Handles quoted fields and escaped quotes
- Returns array of company objects with field names as keys

#### 3. DataService
- **fetchFromGoogleSheets()**: Primary data fetching from Google Sheets
- **fetchFromLocalCSV()**: Fallback data fetching from local CSV file
- Error recovery: Automatically falls back to local CSV if Google Sheets fails

#### 4. AppState
- Manages application state (companies data, filters, sort order)
- Methods:
  - `setCompanies()`: Store raw company data
  - `filter(query)`: Filter companies by search query
  - `sort(field)`: Sort companies by specified field

#### 5. UIRenderer
- Renders UI components based on application state
- Methods:
  - `renderCompanies()`: Render company cards grid
  - `renderStats()`: Update statistics display
  - `renderLoading()`: Show loading state
  - `renderError()`: Display error messages

#### 6. DashboardApp (Main Application)
- Orchestrates all components
- Manages application lifecycle
- Handles event listeners and auto-refresh

## Key Features

### Performance Optimizations (v2.1)

#### Search Debouncing
- **Implementation**: 150ms debounce delay on search input
- **Purpose**: Reduces re-renders during typing
- **Code location**: index.html:1210
```javascript
this.searchTimeout = setTimeout(() => {
    this.state.filter(e.target.value);
    this.renderer.renderCompanies();
}, CONFIG.SEARCH_DEBOUNCE_MS);
```

#### Smart Auto-Refresh
- **Implementation**: Only refreshes when tab is visible
- **Purpose**: Saves API calls and reduces unnecessary data fetching
- **Code location**: index.html:1246
```javascript
if (!document.hidden) {
    this.loadData();
}
```

### Error Recovery & Fallback

#### Automatic CSV Fallback
- **Implementation**: Try Google Sheets first, fallback to local CSV on error
- **Purpose**: Ensures dashboard always works, even offline
- **Code location**: index.html:758-779
```javascript
try {
    // Try Google Sheets
    const response = await fetch(googleSheetsUrl);
    // ... process response
} catch (error) {
    console.warn('Google Sheets fetch failed, trying fallback CSV:', error.message);
    return await this.fetchFromLocalCSV();
}
```

### Responsive Design
- **Mobile-first approach**: Optimized for small screens
- **Grid layout**: Auto-adjusts columns based on screen size
- **Touch-friendly**: Large tap targets, proper spacing
- **Safe area support**: Respects iOS notch and Android navigation

## Recent Updates

### Version 2.1 (2026-01-28)

**New Features:**
1. ✅ Added `.gitignore` for better version control
2. ⚡ Search debouncing (150ms) to reduce re-renders during typing
3. 🔄 Smart auto-refresh: Only runs when tab is visible (saves API calls)
4. 🛡️ Error recovery: Automatic fallback to local CSV if Google Sheets fails
5. 📝 Better code documentation with inline comments for magic numbers
6. 🔧 Fixed mobile-test.html to use relative path (works in production)

**Files Changed:**
- `index.html`: Added debouncing, smart refresh, fallback CSV, better comments
- `mobile-test.html`: Changed iframe src from localhost to relative path
- `README.md`: Updated documentation with v2.1 features
- `.gitignore`: Added git ignore rules for common files
- `CSV_STRUCTURE_COMPARISON.md`: Added data structure analysis
- `DATA_STRUCTURE_ANALYSIS.md`: Added detailed data analysis
- `current_data.csv`: Added test data file
- `optimized_data.csv`: Added optimized data structure

**Architecture Changes:**
- Enhanced `DataService` class with fallback mechanism
- Added search debouncing in `DashboardApp` event listeners
- Improved auto-refresh logic with visibility check
- Added inline code comments for clarity

**Dependencies:**
- No new dependencies (still zero-dependency vanilla JavaScript)

### Version 2.0 (Previous)
- ✨ Complete codebase refactoring with modular architecture
- 🎨 Improved mobile UI with proper alignment and tag wrapping
- 📱 Fixed viewport height issues on mobile Safari
- 🔄 Added auto-refresh functionality (5-minute intervals)
- 📊 Enhanced statistics display with proper formatting

## File Structure

```
ai-companies-dashboard/
├── index.html                      # Main dashboard application
├── mobile-test.html               # Mobile viewport testing page
├── sample-data.csv                # Sample data & fallback CSV
├── current_data.csv               # Current data structure for testing
├── optimized_data.csv             # Optimized data structure for testing
├── .gitignore                     # Git ignore rules
├── README.md                      # User-facing documentation
├── CSV_STRUCTURE_COMPARISON.md    # Data structure comparison
├── DATA_STRUCTURE_ANALYSIS.md     # Detailed data analysis
└── .claude/
    ├── CLAUDE.md                  # This file (developer documentation)
    └── settings.local.json        # Claude Code local settings
```

## Data Schema

### Required CSV Columns
- **Company Name** (required)
- **Founders** (optional)
- **Key Investors** (optional)
- **Description** (optional)

### Google Sheets Configuration
- **Sheet ID**: `1m5ghTUb146W0koJ4Hdt8DaugrgVr7NVyrt4cOECVPS0`
- **Sheet Name**: `Sheet1`
- **Sharing**: Must be "Anyone with the link can view"
- **Format**: First row must contain exact column headers

### CSV Export URL Format
```
https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}
```

## Development Workflow

### Local Development
1. **Start local server**:
   ```bash
   python3 -m http.server 8000
   ```
2. **Open dashboard**: http://localhost:8000
3. **Test mobile view**: http://localhost:8000/mobile-test.html

### Testing
- **Desktop testing**: Open `index.html` in browser
- **Mobile testing**: Use `mobile-test.html` for viewport simulation
- **Data testing**: Modify `sample-data.csv` or `current_data.csv`
- **Error testing**: Temporarily break Google Sheets ID to test fallback

### Making Changes

#### Updating Google Sheets Configuration
Edit `CONFIG` object in `index.html`:
```javascript
const CONFIG = {
    GOOGLE_SHEET_ID: 'your-sheet-id-here',
    SHEET_NAME: 'your-sheet-name',
    // ... other config
};
```

#### Adjusting Performance Settings
```javascript
AUTO_REFRESH_INTERVAL: 300000,    // Change refresh interval (ms)
SEARCH_DEBOUNCE_MS: 150,          // Change search debounce delay (ms)
```

#### Modifying Fallback Behavior
```javascript
FALLBACK_CSV: 'sample-data.csv',  // Change fallback CSV file
```

## Deployment

### GitHub Pages (Current)
- **Repository**: https://github.com/ductran2918/ai-companies-dashboard
- **Live URL**: https://ductran2918.github.io/ai-companies-dashboard/
- **Branch**: `master`
- **Automatic deployment**: Pushes to master auto-deploy

### Deployment Checklist
1. ✅ Test locally with `python3 -m http.server`
2. ✅ Verify mobile layout with `mobile-test.html`
3. ✅ Check Google Sheets access (public sharing enabled)
4. ✅ Commit changes to git
5. ✅ Push to master branch
6. ✅ Wait 1-2 minutes for GitHub Pages deployment
7. ✅ Verify live site works correctly

## Common Tasks

### Updating Dashboard Content
1. Edit Google Sheet directly
2. Changes appear automatically within 5 minutes
3. Manual refresh: Press F5 or Cmd+R

### Adding New Features
1. Read existing code in `index.html`
2. Identify relevant class (DataService, AppState, UIRenderer, etc.)
3. Add new methods or modify existing ones
4. Test locally before committing
5. Update this CLAUDE.md with changes

### Fixing Bugs
1. Check browser console (F12) for errors
2. Test with fallback CSV to isolate Google Sheets issues
3. Use mobile-test.html for mobile-specific bugs
4. Verify changes in multiple browsers

## Troubleshooting

### Dashboard Shows Error
1. Verify Google Sheet ID in CONFIG
2. Check sheet is shared publicly
3. Ensure first row has exact column headers
4. Check browser console for detailed errors
5. Dashboard should automatically try fallback CSV

### Data Not Updating
1. Check auto-refresh is working (5-minute intervals)
2. Verify tab is visible (refresh only runs when visible)
3. Manually refresh page (Ctrl+R or Cmd+R)
4. Clear browser cache if needed
5. Check if fallback CSV is being used (console warning)

### Mobile UI Issues
1. Use `mobile-test.html` to debug
2. Check viewport meta tag is present
3. Test on actual mobile device
4. Verify CSS safe-area variables
5. Check for horizontal scrolling issues

### Performance Issues
1. Reduce `SEARCH_DEBOUNCE_MS` if search feels laggy
2. Increase `AUTO_REFRESH_INTERVAL` if too many API calls
3. Check if fallback CSV is smaller/faster to load
4. Verify search debouncing is working (check console logs)

## Code Style Guidelines

### JavaScript
- Use ES6+ features (const, let, arrow functions, classes)
- Modular class-based architecture
- Clear method and variable names
- Add comments for non-obvious logic
- Document magic numbers with inline comments

### CSS
- Use CSS variables for design tokens
- Mobile-first responsive design
- Semantic class names
- Group related properties

### HTML
- Semantic HTML5 elements
- Proper meta tags for mobile
- Accessibility considerations (alt text, labels)

## Security Considerations

### Public Data Only
- Google Sheets must be publicly accessible
- No authentication mechanism
- Suitable for public company data only
- Do not use for sensitive information

### XSS Prevention
- User input is escaped during rendering
- CSV data is treated as plain text
- No eval() or innerHTML with user content

## Future Enhancements

### Potential Features
- [ ] Export to CSV functionality
- [ ] Advanced filtering (by founder, investor, etc.)
- [ ] Dark mode toggle
- [ ] Bookmark/favorite companies
- [ ] Company comparison view
- [ ] Data visualization charts
- [ ] Multi-sheet support
- [ ] Offline mode with service worker

### Performance Improvements
- [ ] Implement virtual scrolling for large datasets
- [ ] Add caching layer with localStorage
- [ ] Lazy load company details
- [ ] Compress CSV data transfer

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1 | 2026-01-28 | Added search debouncing, smart refresh, CSV fallback, .gitignore |
| 2.0 | 2026-01 | Complete refactor with modular architecture, mobile fixes |
| 1.0 | 2025-12 | Initial release with basic functionality |

## Contact & Support

- **Repository Issues**: https://github.com/ductran2918/ai-companies-dashboard/issues
- **Documentation**: README.md (user-facing), CLAUDE.md (developer docs)

## License

[Specify license if applicable]

---

**Last Modified**: 2026-01-28
**Modified By**: Claude Sonnet 4.5
