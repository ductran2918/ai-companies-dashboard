# AI Companies Dashboard

Interactive dashboard showcasing AI companies founded by Chinese entrepreneurs in Singapore. Features real-time data sync with Google Sheets, responsive design, and minimalist styling.

🔗 **[View Live Dashboard](https://ductran2918.github.io/ai-companies-dashboard/)**

## Features

- ✅ Real-time Google Sheets integration (auto-refreshes every 5 minutes)
- ✅ Fully responsive design (mobile, tablet, desktop) with mobile-optimized UI
- ✅ Search and filter functionality
- ✅ Sort by name or funding amount
- ✅ Grid and table view options
- ✅ Minimalist black & white design
- ✅ Fully customizable fonts and styling via CSS variables
- ✅ Mobile test page for responsive design testing
- ✅ Modern, refactored codebase with modular architecture

## Quick Start

### 1. Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create new spreadsheet
3. Import `sample-data.csv` (File → Import → Upload)
4. Share publicly: Click Share → "Anyone with the link" → Viewer
5. Copy Sheet ID from URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`

### 2. Configure Dashboard

1. Open `index.html` in text editor
2. Find the `CONFIG` object (around line 568):
   ```javascript
   const CONFIG = {
       GOOGLE_SHEET_ID: 'YOUR_GOOGLE_SHEET_ID_HERE',
       SHEET_NAME: 'Sheet1',
       ...
   };
   ```
3. Replace `YOUR_GOOGLE_SHEET_ID_HERE` with your Sheet ID
4. Save file

### 3. Deploy

**Option A: GitHub Pages (Recommended)**
- Already configured in this repo
- Push changes to master branch
- Access at: `https://ductran2918.github.io/ai-companies-dashboard/`

**Option B: Local Development**
- Start local server: `python3 -m http.server 8000`
- Open `http://localhost:8000` in browser
- For mobile testing, open `mobile-test.html`

**Option C: Embed in Website**
```html
<iframe src="path/to/index.html" width="100%" height="1200px" frameborder="0"></iframe>
```

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

## Google Sheet Format

Required columns:

| Column | Description | Example |
|--------|-------------|---------|
| Company Name | Company name | ChemLex |
| Company LinkedIn | LinkedIn URL | https://sg.linkedin.com/company/chemlex |
| Founders | Names with URLs | Felix Tao (https://...), Kisson Lin (https://...) |
| China Background | Achievements in China | Senior Manager at Alibaba... |
| Current Achievements | Metrics & milestones | Total Raised: $50M; Founded 2024... |
| Investors | Semicolon separated | Qiming; Sequoia; Ant Group |
| Description | What company does | ChemLex is an AI-for-science company... |

**Format Notes:**
- Founders: `Name (URL), Name (URL)` or just `Name, Name`
- Investors: Separate multiple investors with semicolons `;`
- Funding amounts: Include `$X million` or `$XM` in Current Achievements for sorting

## Files

- `index.html` - Main dashboard file (refactored with modular architecture)
- `mobile-test.html` - Mobile viewport testing page
- `sample-data.csv` - Sample data for Google Sheets import (also used as fallback)
- `current_data.csv` - Current data structure being tested
- `optimized_data.csv` - Optimized data structure being tested
- `.gitignore` - Git ignore rules for temporary and sensitive files

## Updating Content

**To update dashboard content:**
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

- **Framework:** Vanilla JavaScript (no dependencies)
- **Architecture:** Modular class-based design
- **Data Source:** Google Sheets CSV export (no API key required) with local CSV fallback
- **Styling:** Pure CSS with CSS variables (design tokens)
- **Responsive:** Mobile-first design with safe-area support
- **Auto-refresh:** Configurable interval (default: 5 minutes), only when tab is visible
- **Performance:** Search debouncing (150ms) to reduce re-renders
- **Error Recovery:** Automatic fallback to local CSV if Google Sheets fails
- **Browser Support:** Modern browsers (Chrome, Firefox, Safari, Edge)

## Recent Updates

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
