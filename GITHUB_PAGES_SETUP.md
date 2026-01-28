# GitHub Pages Setup Instructions

## Enable GitHub Pages (One-time Setup)

Since the repository is now created, you need to enable GitHub Pages manually:

### Steps:

1. **Go to Repository Settings**
   - Visit: https://github.com/ductran2918/ai-companies-dashboard
   - Click **Settings** tab (top right)

2. **Navigate to Pages Section**
   - Scroll down left sidebar
   - Click **Pages** under "Code and automation"

3. **Configure Source**
   - Under "Build and deployment"
   - **Source:** Deploy from a branch
   - **Branch:** Select `master` (or `main`)
   - **Folder:** Select `/ (root)`
   - Click **Save**

4. **Wait for Deployment**
   - GitHub will build and deploy your site
   - Takes 1-2 minutes
   - Refresh the page to see the live URL

5. **Access Your Dashboard**
   - Your live dashboard will be at:
   - **https://ductran2918.github.io/ai-companies-dashboard/**

---

## Update README with Live URL

After GitHub Pages is enabled, update the README.md:

1. Open `README.md` in the repository
2. Replace this line:
   ```
   🔗 **[View Live Dashboard](https://yourusername.github.io/ai-companies-dashboard/)**
   ```
   
   With:
   ```
   🔗 **[View Live Dashboard](https://ductran2918.github.io/ai-companies-dashboard/)**
   ```

3. Commit and push the change

---

## Troubleshooting

**Pages option not visible?**
- Make sure the repository is public
- Check that you have admin access to the repository

**404 Error on live URL?**
- Wait 2-3 minutes after enabling Pages
- Check that `index.html` exists in the root directory
- Verify the branch name is correct (master or main)

**Dashboard shows "Error Loading Data"?**
- You still need to configure your Google Sheet ID in `index.html`
- Follow the setup instructions in README.md

---

## Next Steps

1. ✅ Repository created: https://github.com/ductran2918/ai-companies-dashboard
2. ⏳ Enable GitHub Pages (follow steps above)
3. ⏳ Configure Google Sheet ID in `index.html`
4. ⏳ Push changes to see live updates

---

**Repository URL:** https://github.com/ductran2918/ai-companies-dashboard  
**Live Dashboard URL (after Pages enabled):** https://ductran2918.github.io/ai-companies-dashboard/
