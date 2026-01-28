# Claude Code Project Documentation

## Project: AI Companies Dashboard

### Last Updated: 2026-01-28

## Overview
Interactive web dashboard for displaying and filtering AI companies data from Google Sheets. Features automatic data refresh, search functionality, responsive design, and a comprehensive data editor with form-based CRUD operations.

**NEW in v2.2:** Added web-based data editor with Flask backend API, enabling form-based company management without manual CSV editing.

## Project Architecture

### Technology Stack

#### Frontend
- **Framework**: Vanilla JavaScript (zero dependencies)
- **Architecture Pattern**: Modular class-based design
- **Data Source**: Google Sheets CSV export with local CSV fallback
- **Styling**: Pure CSS with CSS variables (design tokens)
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

#### Backend (NEW in v2.2)
- **Framework**: Flask (Python 3.7+)
- **API**: RESTful endpoints for CRUD operations
- **Storage**: CSV file with automatic backup system
- **Security**: Input validation, XSS prevention, CSV injection protection
- **Dependencies**: Flask==3.0.0, Flask-CORS==4.0.0, python-dotenv==1.0.0

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

### Version 2.2 (2026-01-28) - Data Editor Release

**Major New Feature: Web-Based Data Editor**

This release adds a comprehensive data management system with:
- Form-based company editing interface
- Flask REST API backend
- Automatic backup system
- Enhanced security features
- Upgraded data schema (7 → 11 columns)

**New Files:**
1. **editor.html** (~400 lines) - Complete data editor interface with modals
2. **js/api-client.js** (~150 lines) - API client for backend communication
3. **js/editor.js** (~500 lines) - Editor application logic
4. **backend/app.py** (~400 lines) - Flask API with CRUD endpoints
5. **backend/models.py** (~300 lines) - CSV operations with backup
6. **backend/validators.py** (~200 lines) - Input validation & security
7. **backend/config.py** (~90 lines) - Configuration settings
8. **backend/requirements.txt** - Python dependencies
9. **migrate_data.py** (~200 lines) - 7-column to 11-column migration
10. **test_backend.py** (~80 lines) - Backend functionality tests

**Data Schema Upgrade (7 → 11 Columns):**

New structured fields added:
- **Total Funding (USD M)**: Funding amount in millions (extracted from text)
- **Funding Stage**: Pre-seed, Seed, Angel, Series A/B/C+, etc.
- **Founded Year**: Year company was founded
- **Industry**: AI/ML, Biotech, Fintech, etc.

Old achievements text was parsed to extract structured data. All companies migrated automatically with `migrate_data.py`.

**Dashboard Enhancements:**
- Added "Edit Data" button in header linking to editor
- Display industry, funding stage, funding amount, and year as badges on company cards
- Updated funding calculation to use structured field (with fallback to text extraction)
- Added badge styles with color coding (industry = blue, stage = green, funding = orange, year = gray)

**Backend API Endpoints:**
```
GET    /api/health                - Health check
GET    /api/config                - Get dropdown options
GET    /api/companies             - List all companies
GET    /api/companies/:id         - Get single company
POST   /api/companies             - Create new company
PUT    /api/companies/:id         - Update company
DELETE /api/companies/:id         - Delete company
POST   /api/import                - Import CSV file
GET    /api/export                - Export CSV file
```

**Security Features:**
1. **Input Validation:**
   - Required field checks (Company Name, Description)
   - Data type validation (numeric, year format)
   - URL format validation (LinkedIn URLs)
   - Length limits (prevent buffer overflow)
   - Whitelist validation for dropdowns

2. **XSS Prevention:**
   - Frontend: Use `textContent` instead of `innerHTML`
   - Frontend: HTML escape function for user data
   - Backend: Strip `<script>` tags via regex
   - Backend: HTML entity encoding

3. **CSV Injection Prevention:**
   - Detect formula characters (`=`, `+`, `-`, `@`) at start
   - Prefix with single quote to neutralize
   - Prevents code execution in Excel/Sheets

4. **File Upload Security:**
   - Accept only `.csv` files
   - 5MB file size limit
   - Header validation before processing
   - Reject malformed CSVs

5. **Automatic Backups:**
   - Backup created before every write operation
   - Format: `sample-data_YYYYMMDD_HHMMSS.csv`
   - Keep last 10 backups (auto-cleanup)
   - Stored in `backend/backups/`

**Testing:**
All backend functionality tested and verified:
- ✅ CSV read/write operations
- ✅ Input validation (required fields, data types)
- ✅ XSS prevention (script tag removal)
- ✅ CSV injection prevention (formula escaping)
- ✅ Backup creation and cleanup

**Migration Process:**
1. Original 7-column CSV backed up to `sample-data-backup-7col-*.csv`
2. Funding amounts extracted from "Current Achievements" text
3. Funding stages identified (Seed, Series A, etc.)
4. Industries manually categorized based on descriptions
5. Founded years extracted or manually added
6. New 11-column CSV generated
7. All 9 companies migrated successfully

**Updated Files:**
- `index.html`: Added editor link, badge display, structured field usage
- `sample-data.csv`: Migrated to 11-column format
- `README.md`: Comprehensive editor documentation
- `.claude/CLAUDE.md`: This file (full v2.2 documentation)

**Dependencies Added:**
- Backend: Flask==3.0.0, Flask-CORS==4.0.0, python-dotenv==1.0.0
- Frontend: No new dependencies (still zero-dependency)

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
├── editor.html                     # NEW: Data editor interface
├── mobile-test.html               # Mobile viewport testing page
├── js/                            # NEW: JavaScript modules
│   ├── api-client.js              # API client for backend
│   └── editor.js                  # Editor application logic
├── backend/                       # NEW: Flask API backend
│   ├── app.py                     # Main Flask application
│   ├── models.py                  # CSV CRUD operations
│   ├── validators.py              # Input validation & security
│   ├── config.py                  # Configuration settings
│   ├── requirements.txt           # Python dependencies
│   └── backups/                   # Automatic CSV backups
├── sample-data.csv                # Main data file (11-column format)
├── sample-data-backup-7col-*.csv  # Legacy 7-column backups
├── migrate_data.py                # Migration script (7-col → 11-col)
├── test_backend.py                # Backend functionality tests
├── current_data.csv               # Test data file
├── optimized_data.csv             # Optimized structure reference
├── .gitignore                     # Git ignore rules
├── README.md                      # User-facing documentation
├── CSV_STRUCTURE_COMPARISON.md    # Data structure comparison
├── DATA_STRUCTURE_ANALYSIS.md     # Detailed data analysis
└── .claude/
    ├── CLAUDE.md                  # This file (developer documentation)
    └── settings.local.json        # Claude Code local settings
```

## Data Schema (11-Column Structure - NEW in v2.2)

### CSV Columns

| Column | Required | Type | Validation | Description |
|--------|----------|------|------------|-------------|
| Company Name | ✅ | String | Max 200 chars | Company name |
| Company LinkedIn | | URL | Valid URL format | LinkedIn company page |
| Founders | | String | Max 500 chars | Format: Name (URL), Name (URL) |
| China Background | | String | Max 500 chars | Chinese heritage/experience |
| **Total Funding (USD M)** | | **Number** | **0-10000** | **Funding in millions USD** |
| **Funding Stage** | | **Dropdown** | **Whitelist** | **Pre-seed, Seed, Angel, Series A/B/C+, etc.** |
| **Founded Year** | | **Number** | **1900-2099** | **Year founded** |
| **Industry** | | **Dropdown** | **Whitelist** | **AI/ML, Biotech, Fintech, etc.** |
| Current Achievements | | String | Max 500 chars | Recent milestones |
| Investors | | String | Max 500 chars | Semicolon-separated list |
| Description | ✅ | String | Max 1000 chars | What company does |

**NEW in v2.2:** Four new structured fields (Total Funding, Funding Stage, Founded Year, Industry) were added for better data organization and visualization.

### Dropdown Options

**Funding Stages:**
Pre-seed, Seed, Angel, Series A, Series A+, Series B, Series C+, Growth, IPO, Acquired, Not disclosed

**Industries:**
AI/ML, Biotech, Creative AI, Data Infrastructure, DevTools, Enterprise AI, Fintech, Healthcare, Media/Creative, Productivity, Security, Other

### Google Sheets Configuration
- **Sheet ID**: `1m5ghTUb146W0koJ4Hdt8DaugrgVr7NVyrt4cOECVPS0`
- **Sheet Name**: `Sheet1`
- **Sharing**: Must be "Anyone with the link can view"
- **Format**: First row must contain exact column headers (11 columns)

### CSV Export URL Format
```
https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}
```

## Development Workflow

### Local Development

**Option 1: Dashboard Only (No Editor)**
```bash
# Start frontend server
python3 -m http.server 8000

# Open dashboard: http://localhost:8000
# Test mobile: http://localhost:8000/mobile-test.html
```

**Option 2: Full Stack (Dashboard + Editor)**
```bash
# Terminal 1: Start backend
cd backend
pip install -r requirements.txt
python app.py
# Backend runs at http://localhost:5000

# Terminal 2: Start frontend
python3 -m http.server 8000
# Dashboard: http://localhost:8000/index.html
# Editor: http://localhost:8000/editor.html
```

### Testing

**Frontend Testing:**
- **Desktop testing**: Open `index.html` in browser
- **Mobile testing**: Use `mobile-test.html` for viewport simulation
- **Data testing**: Modify `sample-data.csv` or use editor
- **Error testing**: Temporarily break Google Sheets ID to test fallback

**Backend Testing:**
```bash
# Run backend tests
python3 test_backend.py

# Test API manually
curl http://localhost:5000/api/health
curl http://localhost:5000/api/companies
```

**End-to-End Testing:**
1. Start backend server
2. Start frontend server
3. Open editor: http://localhost:8000/editor.html
4. Add new company via form
5. Verify CSV updated: `cat sample-data.csv`
6. Verify backup created: `ls backend/backups/`
7. Open dashboard: http://localhost:8000/index.html
8. Verify new company appears with badges
9. Test edit and delete operations

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
| 2.2 | 2026-01-28 | **Data Editor Release:** Web-based editor, Flask backend API, 11-column schema, badges, security features |
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
