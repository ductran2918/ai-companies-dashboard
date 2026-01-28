# AI Companies Dashboard - Setup & Customization Guide

## Overview

This is a fully responsive, minimalist HTML dashboard that displays AI company data pulled directly from a Google Sheet. Changes made to the Google Sheet will automatically appear in the dashboard (refreshes every 5 minutes).

**Features:**
- ✓ Responsive design (works on desktop, tablet, mobile)
- ✓ Minimalist black & white design
- ✓ Real-time data sync from Google Sheets
- ✓ Search and filter functionality
- ✓ Sort by company name or funding
- ✓ Grid and table view options
- ✓ Expandable company cards with detailed information
- ✓ Fully customizable fonts and styling

---

## Step 1: Create Google Sheet

### 1.1 Create a New Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Click **"+ New"** → **"Spreadsheet"**
3. Name it: **"AI Companies Dashboard Data"**

### 1.2 Set Up the Data Structure

Your Google Sheet should have these column headers in the first row:

```
Company Name | Company LinkedIn | Founders | China Background | Current Achievements | Investors | Description
```

**Column Descriptions:**

- **Company Name** (required): Name of the company
- **Company LinkedIn** (required): Full LinkedIn company page URL
- **Founders** (required): Format: `Name (URL), Name (URL)` or just names
  - Example: `Felix Tao (https://linkedin.com/in/felix-tao), Kisson Lin (https://linkedin.com/in/kisson-lin)`
- **China Background** (required): Achievements/experience in China
- **Current Achievements** (required): Company metrics and milestones
  - Include funding amounts like: `Total Raised: $50M`
- **Investors** (required): Investor names separated by semicolons
  - Example: `Qiming Venture Partners; Actoz Soft`
- **Description** (required): What the company does

### 1.3 Add Your Data

Copy and paste the data from the provided CSV file, or manually enter company information.

**Important:** The first row MUST contain the headers exactly as shown above.

---

## Step 2: Share Google Sheet Publicly

### 2.1 Get Share Link

1. Click the **"Share"** button (top right)
2. Click **"Change"** next to "Restricted"
3. Select **"Anyone with the link"** → **"Viewer"**
4. Copy the share link

### 2.2 Extract Sheet ID

From the share link, extract the Sheet ID:
```
https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit?usp=sharing
                                        ^^^^^^^^^^^^^^^^
                                        Copy this part
```

---

## Step 3: Configure the HTML File

### 3.1 Open the HTML File

Open `ai_companies_dashboard.html` in a text editor (VS Code, Sublime Text, Notepad++, etc.)

### 3.2 Add Your Google Sheet ID

Find this line (around line 456):

```javascript
const GOOGLE_SHEET_ID = 'YOUR_GOOGLE_SHEET_ID_HERE';
```

Replace `YOUR_GOOGLE_SHEET_ID_HERE` with your actual Sheet ID:

```javascript
const GOOGLE_SHEET_ID = '1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t';
```

### 3.3 (Optional) Change Sheet Name

If your sheet is not named "Sheet1", update this line:

```javascript
const SHEET_NAME = 'Sheet1';  // Change if your sheet has a different name
```

---

## Step 4: Deploy the Dashboard

### Option A: Embed in Website

Add this code to your website where you want the dashboard to appear:

```html
<iframe 
    src="path/to/ai_companies_dashboard.html" 
    width="100%" 
    height="1200px" 
    frameborder="0"
    style="border: none;">
</iframe>
```

### Option B: Standalone Page

Simply open the HTML file in a browser:
```
File → Open → ai_companies_dashboard.html
```

Or upload to your web server and access via URL.

### Option C: GitHub Pages (Free Hosting)

1. Create a GitHub repository
2. Upload the HTML file
3. Enable GitHub Pages in Settings
4. Access at: `https://yourusername.github.io/repository-name/ai_companies_dashboard.html`

---

## Customization Guide

### Font Styling

The dashboard uses a CSS variable system for easy font customization. Find this section in the HTML file:

```css
:root {
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --font-family-mono: 'Courier New', monospace;
    --font-size-base: 16px;
    --font-size-small: 14px;
    --font-size-large: 18px;
    --font-size-xl: 24px;
    --font-size-xxl: 32px;
    --line-height: 1.6;
}
```

#### Change Font Family

Replace the font names:

```css
/* For serif fonts */
--font-family: 'Georgia', 'Times New Roman', serif;

/* For sans-serif fonts */
--font-family: 'Arial', 'Helvetica', sans-serif;

/* For modern fonts */
--font-family: 'Inter', 'Helvetica Neue', sans-serif;

/* For CJK characters (Chinese, Japanese, Korean) */
--font-family: 'Noto Sans CJK SC', 'Segoe UI', sans-serif;  /* Simplified Chinese */
--font-family: 'Noto Sans CJK TC', 'Segoe UI', sans-serif;  /* Traditional Chinese */
--font-family: 'Noto Sans CJK JP', 'Segoe UI', sans-serif;  /* Japanese */
--font-family: 'Noto Sans CJK KR', 'Segoe UI', sans-serif;  /* Korean */
```

#### Change Font Sizes

Adjust the base font sizes:

```css
--font-size-base: 18px;      /* Larger base text */
--font-size-small: 16px;     /* Larger small text */
--font-size-large: 20px;     /* Larger large text */
--font-size-xl: 28px;        /* Larger headings */
--font-size-xxl: 36px;       /* Larger main title */
```

#### Change Line Height

Adjust spacing between lines:

```css
--line-height: 1.8;  /* More spacious */
--line-height: 1.4;  /* More compact */
```

### Color Customization

To add colors (if you want to deviate from minimalist black & white):

Find the color definitions and modify:

```css
body {
    background-color: #ffffff;  /* Change background */
    color: #000000;             /* Change text color */
}

.company-card {
    border: 1px solid #cccccc;  /* Change border color */
}

.company-card:hover {
    border-color: #000000;      /* Change hover border */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);  /* Change shadow */
}
```

### Spacing & Layout

Adjust padding and margins:

```css
.container {
    padding: 40px 20px;  /* Change container padding */
}

.companies-grid {
    gap: 30px;  /* Change spacing between cards */
}

.company-card {
    padding: 25px;  /* Change card padding */
}
```

### Grid Columns

Change the number of columns in grid view:

```css
.companies-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    /* Change 350px to adjust card width */
    /* Smaller = more columns, Larger = fewer columns */
}
```

### Mobile Breakpoints

Customize responsive behavior at different screen sizes:

```css
/* Tablet and below */
@media (max-width: 768px) {
    /* Styles for tablets and smaller */
}

/* Mobile phones */
@media (max-width: 480px) {
    /* Styles for phones */
}
```

---

## Data Format Examples

### Founders Column Format

**With LinkedIn URLs:**
```
Felix Tao (https://linkedin.com/in/felix-tao), Kisson Lin (https://linkedin.com/in/kisson-lin)
```

**Without URLs:**
```
Felix Tao, Kisson Lin
```

### Investors Column Format

Separate multiple investors with semicolons:
```
Qiming Venture Partners; Sequoia Capital; Ant Group
```

### Achievements Column Format

Include funding amounts for automatic sorting:
```
Total Raised: $50M; Founded in 2024; 100K users; Partnerships with major companies
```

---

## Troubleshooting

### Dashboard Shows "Error Loading Data"

**Problem:** "Failed to fetch data from Google Sheets"

**Solutions:**
1. Verify your Sheet ID is correct
2. Make sure the Google Sheet is shared publicly (Anyone with the link)
3. Check that the sheet name matches `SHEET_NAME` in the code
4. Ensure the first row contains the exact headers

### Data Not Updating

**Problem:** Changes to Google Sheet don't appear in dashboard

**Solutions:**
1. The dashboard auto-refreshes every 5 minutes
2. Manually refresh the page (Ctrl+R or Cmd+R)
3. Clear browser cache
4. Check browser console for errors (F12 → Console tab)

### Fonts Not Displaying Correctly

**Problem:** CJK characters (Chinese/Japanese/Korean) appear as boxes

**Solutions:**
1. Change the font family to a CJK-supporting font:
   ```css
   --font-family: 'Noto Sans CJK SC', 'Segoe UI', sans-serif;
   ```
2. Make sure the font is installed or use a web font:
   ```html
   <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+CJK+SC&display=swap" rel="stylesheet">
   ```

### Mobile Layout Issues

**Problem:** Dashboard doesn't look right on mobile

**Solutions:**
1. Check that viewport meta tag is present:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   ```
2. Test in mobile browser or use browser DevTools (F12 → Device Toggle)
3. Adjust mobile breakpoints in CSS if needed

---

## Advanced Customization

### Add Custom CSS

You can add custom CSS at the end of the `<style>` section:

```css
/* Your custom styles here */
.company-card {
    border-radius: 8px;  /* Add rounded corners */
}

.company-name {
    text-transform: uppercase;  /* Make titles uppercase */
}
```

### Modify Auto-Refresh Interval

Change how often the dashboard updates from Google Sheets:

```javascript
// Auto-refresh every 5 minutes (300000 ms)
setInterval(fetchDataFromGoogleSheets, 300000);

// Change to 1 minute (60000 ms)
setInterval(fetchDataFromGoogleSheets, 60000);

// Change to 10 minutes (600000 ms)
setInterval(fetchDataFromGoogleSheets, 600000);
```

### Add More Columns to Google Sheet

To add new columns to your Google Sheet:

1. Add the column header to your sheet
2. No code changes needed - the dashboard will automatically display the new data in expandable sections

---

## Performance Tips

1. **Keep data clean:** Remove empty rows from your Google Sheet
2. **Limit rows:** Dashboard works best with 50-100 companies
3. **Optimize images:** If adding images, keep file sizes small
4. **Cache:** Browser caches data, so updates may take up to 5 minutes to appear

---

## Security Notes

- The dashboard uses Google Sheets API with a public API key
- Only publicly shared sheets can be accessed
- No sensitive data should be stored in the sheet
- The API key is visible in the code (this is intentional for public sheets)

---

## Support & Questions

For issues or questions:

1. Check the Troubleshooting section above
2. Open browser console (F12) to see error messages
3. Verify Google Sheet is properly formatted and shared
4. Test with sample data to isolate issues

---

## Version History

- **v1.0** (Jan 2026): Initial release
  - Grid and table views
  - Search and sort functionality
  - Google Sheets integration
  - Responsive design
  - Minimalist styling

---

## License

This dashboard is provided as-is for personal and commercial use.

---

## Quick Reference

| Task | Location |
|------|----------|
| Change Google Sheet ID | Line ~456 in JavaScript section |
| Change Sheet Name | Line ~457 in JavaScript section |
| Modify Fonts | Lines 5-14 in CSS `:root` section |
| Change Colors | Search for color values in CSS |
| Adjust Spacing | Search for `padding`, `margin`, `gap` in CSS |
| Change Grid Columns | Line ~180 in CSS |
| Modify Auto-Refresh | Line ~550 in JavaScript section |

---

**Happy customizing! 🎨**
