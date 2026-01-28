# AI Companies Dashboard

Interactive dashboard showcasing AI companies founded by Chinese entrepreneurs in Singapore. Features real-time data sync with Google Sheets, responsive design, and minimalist styling.

🔗 **[View Live Dashboard](https://yourusername.github.io/ai-companies-dashboard/)**

## Features

- ✅ Real-time Google Sheets integration
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Search and filter functionality
- ✅ Sort by name or funding amount
- ✅ Grid and table view options
- ✅ Minimalist black & white design
- ✅ Fully customizable fonts and styling

## Quick Start

### 1. Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create new spreadsheet
3. Import `sample-data.csv` (File → Import → Upload)
4. Share publicly: Click Share → "Anyone with the link" → Viewer
5. Copy Sheet ID from URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`

### 2. Configure Dashboard

1. Open `index.html` in text editor
2. Find line ~456: `const GOOGLE_SHEET_ID = 'YOUR_GOOGLE_SHEET_ID_HERE';`
3. Replace with your Sheet ID
4. Save file

### 3. Deploy

**Option A: GitHub Pages (Recommended)**
- Already configured in this repo
- Push changes to main branch
- Access at: `https://yourusername.github.io/ai-companies-dashboard/`

**Option B: Local**
- Open `index.html` in browser

**Option C: Embed in Website**
```html
<iframe src="path/to/index.html" width="100%" height="1200px" frameborder="0"></iframe>
```

## Customization

### Change Fonts

Edit CSS variables in `index.html` (lines 5-14):

```css
:root {
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --font-size-base: 16px;
    --font-size-xxl: 32px;
    --line-height: 1.6;
}
```

For detailed customization guide, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)

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

## Files

- `index.html` - Main dashboard file
- `sample-data.csv` - Sample data for Google Sheets import
- `SETUP_GUIDE.md` - Detailed setup and customization guide

## Troubleshooting

**Dashboard shows error?**
1. Check Google Sheet ID is correct
2. Verify sheet is shared publicly
3. Ensure first row has exact column headers

**Data not updating?**
1. Wait 5 minutes for auto-refresh
2. Manually refresh page (Ctrl+R)

For more help, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)

## Technical Details

- **Framework:** Vanilla JavaScript (no dependencies)
- **Data Source:** Google Sheets API v4
- **Styling:** Pure CSS with CSS variables
- **Responsive:** Mobile-first design
- **Auto-refresh:** Every 5 minutes

## License

MIT License - Free for personal and commercial use

---

**Last Updated:** January 2026
