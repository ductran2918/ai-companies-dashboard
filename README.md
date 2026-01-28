# AI Companies Dashboard

Interactive dashboard showcasing AI companies founded by Chinese entrepreneurs in Singapore. Features real-time data sync with Google Sheets, responsive design, minimalist styling, and a powerful data editor.

🔗 **[View Live Dashboard](https://ductran2918.github.io/ai-companies-dashboard/)**

## Features

### Dashboard
- ✅ Real-time Google Sheets integration (auto-refreshes every 5 minutes)
- ✅ Fully responsive design (mobile, tablet, desktop) with mobile-optimized UI
- ✅ Search and filter functionality
- ✅ Sort by name or funding amount
- ✅ Grid and table view options
- ✅ Minimalist black & white design
- ✅ Fully customizable fonts and styling via CSS variables
- ✅ Mobile test page for responsive design testing
- ✅ Modern, refactored codebase with modular architecture
- ✅ Industry, funding stage, and year badges for quick insights

### Data Editor (NEW in v2.2)
- ✏️ Web-based form editor for adding/editing companies
- 🔒 Input validation and security (XSS prevention, CSV injection protection)
- 📤 Import/Export CSV functionality
- 🔄 Automatic backups before every change
- 🎯 No manual CSV editing required!

## Quick Start

### Option 1: Use the Data Editor (Easiest)

1. **Start Backend Server:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
   Backend runs at http://localhost:5000

2. **Start Frontend:**
   ```bash
   # From project root
   python3 -m http.server 8000
   ```
   - Dashboard: http://localhost:8000/index.html
   - Editor: http://localhost:8000/editor.html

3. **Edit Data:**
   - Open the editor at http://localhost:8000/editor.html
   - Add, edit, or delete companies using the form interface
   - Changes save automatically to `sample-data.csv`

### Option 2: Google Sheets Integration

1. **Create Google Sheet:**
   - Go to [Google Sheets](https://sheets.google.com)
   - Create new spreadsheet
   - Import `sample-data.csv` (File → Import → Upload)
   - Share publicly: Click Share → "Anyone with the link" → Viewer
   - Copy Sheet ID from URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`

2. **Configure Dashboard:**
   - Open `index.html` in text editor
   - Find the `CONFIG` object (around line 714)
   - Replace `GOOGLE_SHEET_ID` with your Sheet ID

3. **Deploy:**
   - **GitHub Pages:** Push to master branch
   - **Local:** Run `python3 -m http.server 8000`
   - **Embed:** Use iframe in your website

## Mobile Testing

Use the included `mobile-test.html` file to test the dashboard's responsive design:

1. Start local server: `python3 -m http.server 8000`
2. Open `mobile-test.html` in browser
3. Select different device presets (iPhone SE, iPhone 12 Pro, etc.)
4. Verify mobile UI and responsive behavior

## Customization

### Change Fonts

Edit CSS variables in `index.html` (lines 11-42):

```css
:root {
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --font-size-base: 16px;
    --font-size-xxl: 32px;
    --line-height: 1.6;
}
```

For CJK characters (Chinese, Japanese, Korean), use:
```css
--font-family: 'Noto Sans CJK SC', 'Segoe UI', sans-serif;
```

### Change Colors

Edit color variables in `index.html`:

```css
:root {
    --color-primary: #000000;
    --color-secondary: #666666;
    --color-border: #cccccc;
    /* ... */
}
```

### Modify Auto-Refresh Interval

Edit the `CONFIG` object in `index.html`:

```javascript
const CONFIG = {
    AUTO_REFRESH_INTERVAL: 300000, // 5 minutes (in milliseconds)
    // Change to 60000 for 1 minute, 600000 for 10 minutes
};
```

## Data Format (11-Column Structure)

**NEW in v2.2:** Data structure upgraded from 7 columns to 11 columns for better organization.

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| Company Name | ✅ | Company name | ChemLex |
| Company LinkedIn | | LinkedIn URL | https://sg.linkedin.com/company/chemlex |
| Founders | | Names with URLs | Felix Tao (https://...), Kisson Lin (https://...) |
| China Background | | Chinese heritage/experience | Worked at Alibaba... |
| **Total Funding (USD M)** | | **Funding in millions** | **71** |
| **Funding Stage** | | **Latest funding round** | **Series A+** |
| **Founded Year** | | **Year founded** | **2020** |
| **Industry** | | **Industry category** | **Biotech** |
| Current Achievements | | Recent milestones | Launched global HQ in Singapore... |
| Investors | | Semicolon separated | Qiming; Sequoia; Ant Group |
| Description | ✅ | What company does | ChemLex is an AI-for-science company... |

**Format Notes:**
- Founders: `Name (URL), Name (URL)` or just `Name, Name`
- Investors: Separate multiple investors with semicolons `;`
- Funding stages: Pre-seed, Seed, Angel, Series A, Series A+, Series B, Series C+, Growth, IPO, Acquired
- Industries: AI/ML, Biotech, Creative AI, Data Infrastructure, DevTools, Enterprise AI, Fintech, Healthcare, Media/Creative, Productivity, Security, Other

**Migration Note:**
Old 7-column CSVs are automatically backed up to `sample-data-backup-7col-*.csv`. Run `python3 migrate_data.py` to convert legacy data.

## Files

### Frontend
- `index.html` - Main dashboard file (refactored with modular architecture)
- `editor.html` - Data editor interface (NEW in v2.2)
- `mobile-test.html` - Mobile viewport testing page
- `js/api-client.js` - API client for backend communication (NEW)
- `js/editor.js` - Editor application logic (NEW)

### Backend (NEW in v2.2)
- `backend/app.py` - Flask REST API server
- `backend/models.py` - CSV data operations (CRUD)
- `backend/validators.py` - Input validation & security
- `backend/config.py` - Configuration settings
- `backend/requirements.txt` - Python dependencies
- `backend/backups/` - Automatic CSV backups

### Data
- `sample-data.csv` - Main data file (11-column format)
- `sample-data-backup-7col-*.csv` - Legacy 7-column backups
- `migrate_data.py` - Migration script (7-col → 11-col)
- `current_data.csv` - Test data file
- `optimized_data.csv` - Optimized structure reference

### Configuration
- `.gitignore` - Git ignore rules for temporary and sensitive files

## Updating Content

### Option 1: Use the Data Editor (Recommended)

1. **Start the backend server:**
   ```bash
   cd backend
   python app.py
   ```

2. **Open the editor:** http://localhost:8000/editor.html

3. **Make changes:**
   - Click "Add Company" to create new entries
   - Click "Edit" to modify existing companies
   - Click "Delete" to remove companies
   - Use "Import CSV" to bulk upload data
   - Use "Export CSV" to download current data

4. **Changes are immediate:**
   - Automatic backup created before every change
   - Data saved to `sample-data.csv`
   - Refresh dashboard to see updates

### Option 2: Edit Google Sheet Directly

1. Edit your Google Sheet directly
2. Changes appear automatically:
   - Auto-refresh: Every 5 minutes (only when tab is visible)
   - Manual refresh: Press F5 or Cmd+R

No code changes needed! Just edit the Google Sheet and refresh the page.

**Fallback Mode:**
If Google Sheets is unavailable, the dashboard automatically falls back to loading `sample-data.csv`. This ensures the dashboard always works, even offline.

## Troubleshooting

**Dashboard shows error?**
1. Check Google Sheet ID is correct in `CONFIG` object
2. Verify sheet is shared publicly ("Anyone with the link can view")
3. Ensure first row has exact column headers
4. Check browser console (F12) for detailed error messages
5. If Google Sheets fails, dashboard will automatically load `sample-data.csv` as fallback

**Data not updating?**
1. Wait 5 minutes for auto-refresh (only refreshes when tab is visible)
2. Manually refresh page (Ctrl+R or Cmd+R)
3. Clear browser cache if needed
4. Check if you're seeing fallback data (console will show warning)

**Mobile UI issues?**
1. Ensure viewport meta tag is present (already included)
2. Test using `mobile-test.html` page
3. Check responsive breakpoints in CSS (768px and 480px)

## Technical Details

### Frontend
- **Framework:** Vanilla JavaScript (zero dependencies)
- **Architecture:** Modular class-based design
- **Data Source:** Google Sheets CSV export (no API key required) with local CSV fallback
- **Styling:** Pure CSS with CSS variables (design tokens)
- **Responsive:** Mobile-first design with safe-area support
- **Auto-refresh:** Configurable interval (default: 5 minutes), only when tab is visible
- **Performance:** Search debouncing (150ms) to reduce re-renders
- **Error Recovery:** Automatic fallback to local CSV if Google Sheets fails
- **Browser Support:** Modern browsers (Chrome, Firefox, Safari, Edge)

### Backend (NEW in v2.2)
- **Framework:** Flask (Python 3.7+)
- **API:** RESTful endpoints (CRUD operations)
- **Storage:** CSV file with automatic backups
- **Security:**
  - Input validation (required fields, data types, length limits)
  - XSS prevention (HTML sanitization, script tag removal)
  - CSV injection prevention (formula character escaping)
  - File upload security (size limits, extension validation)
  - CORS configuration (restricted origins)
- **Backup Strategy:** Automatic backup before every write, keeps last 10 backups
- **Dependencies:** Flask, Flask-CORS, python-dotenv

## Deployment

### Frontend Deployment
Already deployed to GitHub Pages at https://ductran2918.github.io/ai-companies-dashboard/

### Backend Deployment Options

**Option 1: PythonAnywhere (Free Tier Available)**
```bash
# 1. Create account at pythonanywhere.com
# 2. Upload backend/ folder via Files tab
# 3. Create new Web App → Flask
# 4. Configure WSGI file to point to app.py
# 5. Set working directory to backend/
# 6. Reload web app
# Backend URL: https://yourusername.pythonanywhere.com/api
```

**Option 2: Railway**
```bash
npm install -g @railway/cli
railway login
railway init
railway up
# Railway provides HTTPS URL automatically
```

**Option 3: Heroku**
```bash
# Add Procfile: web: cd backend && python app.py
heroku create your-app-name
git push heroku master
```

**After Deployment:**
Update `js/api-client.js` with production backend URL:
```javascript
const API_BASE_URL = 'https://yourusername.pythonanywhere.com/api';
```

## Recent Updates

**v2.2 (January 2026) - Data Editor Release**
- ✏️ **NEW: Web-based data editor** - Add/edit/delete companies via form interface
- 🔒 **Security:** Input validation, XSS prevention, CSV injection protection
- 📤 **Import/Export:** Bulk CSV operations with validation
- 🔄 **Auto-backup:** Automatic backups before every change
- 📊 **Enhanced data structure:** Upgraded from 7 to 11 columns
  - New fields: Total Funding (USD M), Funding Stage, Founded Year, Industry
  - Structured data for better filtering and visualization
- 🎨 **Dashboard badges:** Industry, funding stage, funding amount, founding year
- 🔧 **Backend API:** Flask REST API for data operations
- 📝 **Migration script:** Automated 7-column to 11-column conversion

**v2.1 (January 2026)**
- ✅ Added .gitignore for better version control
- ⚡ Performance: Added search debouncing (150ms) to reduce re-renders
- 🔄 Smart auto-refresh: Only refreshes when tab is visible (saves API calls)
- 🛡️ Error recovery: Automatic fallback to local CSV if Google Sheets fails
- 📝 Better code documentation with inline comments for magic numbers
- 🔧 Fixed mobile-test.html to use relative path (works in production)

**v2.0 (January 2026)**
- ✨ Complete codebase refactoring with modular architecture
- 🎨 Improved mobile UI with proper alignment and tag wrapping
- 📱 Added mobile test page for responsive design testing
- 🔧 Enhanced CSS organization with design tokens
- 📱 Safe-area support for modern mobile devices
- 🎯 Better responsive breakpoints and mobile optimization

## License

MIT License - Free for personal and commercial use

---

**Last Updated:** January 2026
