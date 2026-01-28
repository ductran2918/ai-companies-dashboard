# Data Structure Analysis & Optimization Recommendations

> **Note:** This project currently has multiple CSV files for testing different data structures:
> - `sample-data.csv` - Original structure (used as fallback)
> - `current_data.csv` - Current structure being tested
> - `optimized_data.csv` - Optimized structure being tested

## Current Structure

**Columns:**
1. Company Name
2. Company LinkedIn
3. Founders
4. China Background
5. Current Achievements
6. Investors
7. Description

## Issues Identified

### 1. **Funding Data Embedded in Text** ⚠️
**Problem:** Funding amounts are embedded within "Current Achievements" text, making extraction unreliable.

**Current Format Examples:**
- "Total Capital Raised: $71 million (Series A: $26M, Series A+: $45M)"
- "Total capital raised: US$5 million (Seed round)"
- "Total Capital Raised: $20M"
- "Total capital raised: Not disclosed"

**Issues:**
- Inconsistent formatting (US$ vs $, "million" vs "M")
- Multiple funding rounds mixed together
- Hard to extract for sorting/filtering
- Some companies have "Not disclosed" which breaks extraction

**Impact:** The dashboard's funding sort feature may not work correctly for all companies.

### 2. **Mixed Data Types in Single Field** ⚠️
**Problem:** "Current Achievements" contains multiple types of information:
- Funding amounts
- Founding dates
- User metrics
- Partnerships
- Product launches
- Accelerator programs

**Impact:** Difficult to filter/search by specific criteria (e.g., "show companies founded in 2024").

### 3. **Missing Structured Fields** ⚠️
**Missing fields that would improve functionality:**
- **Total Funding Amount** (numeric, separate field)
- **Funding Stage** (Seed, Series A, Series B, etc.)
- **Founded Date** (for sorting/filtering by age)
- **Industry/Category** (AI, Biotech, Fintech, etc.)
- **Headquarters Location** (though all seem to be Singapore)
- **Number of Employees** (optional)
- **Website URL** (separate from LinkedIn)

### 4. **Founder Data Format** ✅ (Good)
**Current Format:** "Name (URL), Name (URL)"
- Works well with current parser
- Supports both with and without URLs
- **Minor Issue:** Some entries have inconsistent spacing

### 5. **Investor Data Format** ⚠️
**Current Format:** Semicolon-separated list
- "Granite Asia; Qiming Venture Partners; LYFE Capital"
- Some entries have "Not disclosed"
- **Issue:** No way to distinguish lead investors from others

## Recommended Optimizations

### Option A: Add New Columns (Recommended)
Add these columns to your Google Sheet:

```
Company Name | Company LinkedIn | Founders | China Background | 
Total Funding (USD M) | Funding Stage | Founded Year | Industry | 
Current Achievements | Investors | Description
```

**Benefits:**
- Clean separation of structured vs. unstructured data
- Better sorting/filtering capabilities
- More reliable funding extraction
- Can add filters by industry, funding stage, etc.

### Option B: Standardize Current Format (Quick Fix)
Keep current structure but standardize formats:

**Funding Format Standard:**
```
Total Funding: $XXM (Stage: Seed/Series A/etc.)
```
or
```
Total Funding: Not disclosed
```

**Founded Date Format:**
```
Founded: YYYY
```

### Option C: Hybrid Approach (Best Balance)
Keep current columns but add:
- **Total Funding (USD M)** - Numeric field (e.g., 71, 5, 20)
- **Funding Stage** - Dropdown (Seed, Series A, Series A+, Series B, Not disclosed)
- **Founded Year** - Numeric (e.g., 2021, 2024)
- **Industry** - Text (AI, Biotech, Fintech, etc.)

Keep "Current Achievements" for milestones, partnerships, etc.

## Specific Recommendations

### 1. **Fix Funding Extraction**
**Current Code Pattern:**
```javascript
/\$(\d+(?:\.\d+)?)\s*(?:million|M)/i
```

**Issues:**
- Doesn't match "US$5 million"
- Doesn't handle "Total Capital Raised: $71 million"
- Doesn't extract multiple rounds

**Recommended Fix:**
Add a dedicated "Total Funding (USD M)" column with numeric values only.

### 2. **Add Industry/Category Field**
Would enable filtering by:
- AI/ML
- Biotech
- Fintech
- Productivity
- Media/Creative

### 3. **Standardize Date Formats**
Add "Founded Year" column for:
- Sorting by company age
- Filtering by founding period
- Displaying "Founded in YYYY" consistently

### 4. **Improve Investor Data**
Consider adding:
- **Lead Investor** column (separate from other investors)
- Or use format: "Lead Investor; Other Investor 1; Other Investor 2"

## Implementation Priority

### High Priority (Fixes Current Issues)
1. ✅ Add "Total Funding (USD M)" column - numeric field
2. ✅ Add "Funding Stage" column
3. ✅ Standardize funding format in "Current Achievements"

### Medium Priority (Enhances Functionality)
4. Add "Founded Year" column
5. Add "Industry" column
6. Improve investor format (lead vs. others)

### Low Priority (Nice to Have)
7. Add "Website" column (separate from LinkedIn)
8. Add "Number of Employees" column
9. Add "Last Funding Date" column

## Example Optimized Structure

| Company Name | Total Funding (USD M) | Funding Stage | Founded Year | Industry | ... |
|--------------|----------------------|---------------|--------------|----------|-----|
| ChemLex | 71 | Series A+ | 2021 | Biotech | ... |
| ChemT Biotechnology | 3.5 | Seed | 2024 | Biotech | ... |
| Mindverse AI | 5 | Seed | 2022 | AI/ML | ... |
| Video Rebirth | 50 | Seed | 2024 | Media/Creative | ... |

## Next Steps

1. **Immediate:** Add "Total Funding (USD M)" column to fix sorting
2. **Short-term:** Add "Funding Stage" and "Founded Year" columns
3. **Long-term:** Consider adding industry categorization

Would you like me to:
- Update the dashboard code to support new columns?
- Create a migration script to extract funding from current data?
- Add new filtering/sorting capabilities?
