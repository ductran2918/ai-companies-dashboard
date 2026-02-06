# AI Companies Dashboard

Interactive dashboard showcasing AI companies founded by Chinese entrepreneurs in Singapore. Features company logos, founder profile images, responsive design, and comprehensive company information.

🔗 **[View Live Dashboard](https://ductran2918.github.io/ai-companies-dashboard/)**

## Features

### NEW Dashboard (v3.0 - Simplified Static Version)
- 🏢 **Company logos** displayed prominently
- 👤 **Founder profile images** with LinkedIn URL matching
- 💰 **Funding information** with badges (amount, stage, year)
- 📊 **Clean card layout** with organized sections
- 📱 **Fully responsive** design (mobile, tablet, desktop)
- ⚡ **Zero dependencies** - Pure HTML/CSS/JavaScript
- 🚀 **Static hosting ready** - No backend required
- 🎨 **Modern, minimalist** black & white design

### Data Features
- Company logos from high-quality sources
- 12 founder profile images matched via LinkedIn URLs
- 7 companies with complete information
- Funding details (amount, stage, founding year)
- Investor information
- Founder backgrounds

## Quick Start

### Simplified Dashboard (Recommended)

1. **Start Local Server:**
   ```bash
   python3 -m http.server 8000
   ```

2. **Open Dashboard:**
   - Navigate to: http://localhost:8000/dashboard.html
   - Data loads automatically from CSV files

3. **View Company Information:**
   - Company logos displayed at top of each card
   - Founder avatars shown with names and LinkedIn links
   - Funding badges show amount, stage, and year
   - Full descriptions and investor lists

### Legacy Dashboard (Google Sheets Integration)

For the older version with Google Sheets integration:
- Dashboard: http://localhost:8000/index.html
- Editor: http://localhost:8000/editor.html

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

## Data Format

### Company Data (`final_dataset/final_dataset_corrected.csv`)

The dashboard loads data from a CSV file with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Name | Company name | ChemLex |
| Company linkedIn | LinkedIn company URL | https://linkedin.com/company/chemlex |
| Company logo | Image URL for company logo | https://cdn.techinasia.com/data/images/... |
| Founders | Names with LinkedIn URLs | Sean Lin (https://sg.linkedin.com/in/linsen986), Peng Wang (...) |
| Founders background | Founder experience text | Sean Lin was the youngest global project manager... |
| Total funding (in US$ million) | Funding amount | 71 |
| Funding stage | Latest funding round | Series B |
| Year founded | Year company started | 2022 |
| Investors | Investor list | Granite Asia (Singapore), Qiming Venture Partners... |
| Description | What company does | Founded in 2022 in Shanghai, ChemLex uses AI... |

### Founder Images (`final_dataset/profile_images.csv`)

Profile images are matched via LinkedIn URLs:

| Column | Description | Example |
|--------|-------------|---------|
| Person Name | Founder name | Sean Lin |
| LinkedIn Profile URL | LinkedIn profile URL | https://sg.linkedin.com/in/linsen986 |
| Image URL | Profile image URL | https://cdn.techinasia.com/wp-content/uploads/... |

**Matching Logic:**
- Founders field is parsed to extract LinkedIn URLs
- URLs are matched against profile_images.csv
- Matching founders get their profile image displayed

## Files

### Main Dashboard (NEW v3.0)
- `dashboard.html` - **Simplified static dashboard** with logos and images (~400 lines)
  - Zero dependencies
  - Loads data directly from CSV files
  - Company logos and founder avatars
  - No backend required

### Data Files
- `final_dataset/final_dataset_corrected.csv` - Company data (7 companies)
- `final_dataset/profile_images.csv` - Founder profile images (12 images)

### Legacy Files (Old Versions)
- `index.html` - Legacy dashboard with Google Sheets integration
- `editor.html` - Data editor interface
- `mobile-test.html` - Mobile viewport testing page
- `js/api-client.js` - API client for backend communication
- `js/editor.js` - Editor application logic
- `backend/` - Flask backend for data editor
- `sample-data.csv` - Old data format

### Configuration
- `.gitignore` - Git ignore rules for temporary and sensitive files

## Updating Content

### Simplified Dashboard (v3.0)

**Edit CSV files directly:**

1. **Update company data:**
   - Edit `final_dataset/final_dataset_corrected.csv`
   - Add/remove companies or update information
   - Keep CSV format intact (headers on first row)

2. **Add founder images:**
   - Add rows to `final_dataset/profile_images.csv`
   - Format: `Person Name,LinkedIn Profile URL,Image URL`
   - LinkedIn URL must match exactly with Founders field

3. **Refresh dashboard:**
   - Save CSV files
   - Reload http://localhost:8000/dashboard.html
   - Changes appear immediately

**Note:** The dashboard loads data directly from CSV files on each page load. No database or backend required.

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

### Simplified Dashboard (v3.0)
- **Framework:** Pure HTML/CSS/JavaScript (zero dependencies)
- **Architecture:** Modular class-based design
- **Data Source:** CSV files loaded via fetch API
- **Image Matching:** LinkedIn URL-based founder image matching
- **Styling:** Pure CSS with CSS variables (design tokens)
- **Responsive:** Mobile-first design with flexible grid
- **Performance:** Loads all data on page load (7 companies, 12 images)
- **Error Handling:** Graceful fallback for missing images
- **Browser Support:** Modern browsers (Chrome, Firefox, Safari, Edge)
- **File Size:** ~400 lines in single HTML file

### Data Loading Process
1. Parse both CSV files (companies + profile images)
2. Build founder image lookup map (LinkedIn URL → Image URL)
3. Parse Founders field to extract names and URLs
4. Match founders to images via LinkedIn URL
5. Render company cards with logos and avatars

### Security
- **XSS Prevention:** HTML escaping via textContent
- **No External Dependencies:** All code in single HTML file
- **Static Assets:** Images loaded from trusted CDN sources

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

**v3.0 (January 2026) - Simplified Static Dashboard**
- 🎯 **Major Simplification:** Removed backend complexity, pure static HTML
- 🏢 **Company Logos:** Display company logos from image URLs
- 👤 **Founder Avatars:** Show founder profile images matched via LinkedIn URLs
- 💰 **Funding Badges:** Display funding amount, stage, and founding year
- 📊 **Card Layout:** Clean, organized sections for each company
- ⚡ **Zero Dependencies:** Single HTML file, no build process
- 🚀 **Static Hosting:** Deploy anywhere (GitHub Pages, Netlify, S3, etc.)
- 📁 **CSV Data Source:** Load directly from `final_dataset/` folder
- 🔗 **LinkedIn Integration:** Clickable founder names link to profiles

**Key Benefits of v3.0:**
- No backend server required
- No database setup needed
- Just edit CSV files and refresh
- Faster page loads
- Easier maintenance
- Simpler deployment

**Previous Versions:**
- v2.2: Data editor with Flask backend (legacy)
- v2.1: Google Sheets integration with fallback
- v2.0: Refactored modular architecture

## License

MIT License - Free for personal and commercial use

---

**Last Updated:** January 2026
