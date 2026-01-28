#!/usr/bin/env python3
"""
Data migration script: Convert 7-column CSV to 11-column optimized structure.

This script:
1. Reads current sample-data.csv (7 columns)
2. Extracts funding amount and stage from "Current Achievements" text
3. Adds structured fields: Total Funding (USD M), Funding Stage, Founded Year, Industry
4. Backs up original as sample-data-backup-7col.csv
5. Writes new 11-column format to sample-data.csv
"""

import csv
import re
import shutil
from datetime import datetime

# File paths
INPUT_FILE = 'sample-data.csv'
BACKUP_FILE = f'sample-data-backup-7col-{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
OUTPUT_FILE = 'sample-data.csv'

# New column headers (11 columns)
NEW_HEADERS = [
    'Company Name',
    'Company LinkedIn',
    'Founders',
    'China Background',
    'Total Funding (USD M)',  # NEW: Extracted from achievements
    'Funding Stage',           # NEW: Extracted from achievements
    'Founded Year',            # NEW: Manually categorized
    'Industry',                # NEW: Manually categorized
    'Current Achievements',    # EXISTING: Cleaned version
    'Investors',
    'Description'
]

# Manual industry categorization based on company descriptions
INDUSTRY_MAPPING = {
    'ChemLex': 'Biotech',
    'ChemT Biotechnology': 'Biotech',
    'LlamaGen.Ai': 'Creative AI',
    'Mindverse AI': 'AI/ML',
    'Orion Arm': 'Productivity',
    'RockFlow': 'Fintech',
    'Singdata Cloud PTE LTD': 'Data Infrastructure',
    'Tanka AI': 'Productivity',
    'Video Rebirth': 'Media/Creative'
}

# Manual founded year (researched from data)
FOUNDED_YEAR_MAPPING = {
    'ChemLex': '2020',  # From context
    'ChemT Biotechnology': '2024',  # Explicitly stated "Founded October 2024"
    'LlamaGen.Ai': '2023',  # Explicitly stated "Launched in 2023"
    'Mindverse AI': '2022',  # Explicitly stated "Founded early 2022"
    'Orion Arm': '2023',  # Explicitly stated "Founded May 2023"
    'RockFlow': '2021',  # Explicitly stated "Founded July 2021"
    'Singdata Cloud PTE LTD': '2021',  # Explicitly stated "Founded 2021"
    'Tanka AI': '2024',  # From context
    'Video Rebirth': '2024'  # Explicitly stated "Founded 2024"
}


def extract_funding_amount(achievements_text):
    """
    Extract total funding amount from achievements text.

    Args:
        achievements_text: Text containing funding information

    Returns:
        String representing funding in millions USD, or empty string if not found
    """
    if not achievements_text:
        return ''

    # Pattern 1: "Total Capital Raised: $XX million" or "Total capital raised: $3-4 million"
    pattern1 = re.search(r'Total [Cc]apital [Rr]aised:\s*\$?(\d+(?:\.\d+)?(?:-\d+)?)\s*million', achievements_text)
    if pattern1:
        # Handle ranges like "3-4" - take the higher number
        amount = pattern1.group(1)
        if '-' in amount:
            amount = amount.split('-')[1]
        return amount

    # Pattern 2: "Raised US$XX million" or "Raised $XXM"
    pattern2 = re.search(r'[Rr]aised\s+(?:US\s*)?\$(\d+(?:\.\d+)?)\s*(?:million|M)', achievements_text)
    if pattern2:
        return pattern2.group(1)

    # Pattern 3: Generic "$XXM" or "$XX million" (as fallback)
    pattern3 = re.search(r'\$(\d+(?:\.\d+)?)\s*(?:million|M)\b', achievements_text, re.IGNORECASE)
    if pattern3:
        return pattern3.group(1)

    return ''


def extract_funding_stage(achievements_text):
    """
    Extract funding stage from achievements text.

    Args:
        achievements_text: Text containing funding stage information

    Returns:
        Funding stage string (e.g., "Series A", "Seed"), or empty string if not found
    """
    if not achievements_text:
        return ''

    # Check for specific funding stages
    stages = [
        'Series C+',
        'Series C',
        'Series B+',
        'Series B',
        'Series A+',
        'Series A',
        'Seed',
        'Pre-seed',
        'Angel',
        'Growth',
        'IPO',
        'Acquired'
    ]

    for stage in stages:
        if re.search(rf'\b{re.escape(stage)}\b', achievements_text, re.IGNORECASE):
            return stage

    return ''


def clean_achievements_text(achievements_text, extracted_funding, extracted_stage):
    """
    Remove extracted funding info from achievements text to avoid duplication.

    Args:
        achievements_text: Original achievements text
        extracted_funding: Funding amount that was extracted
        extracted_stage: Funding stage that was extracted

    Returns:
        Cleaned achievements text
    """
    if not achievements_text:
        return ''

    # Remove "Total Capital Raised: $XXM" patterns
    text = re.sub(r'Total [Cc]apital [Rr]aised:\s*\$?\d+(?:\.\d+)?\s*million[^;]*;?\s*', '', achievements_text)

    # Remove "Raised $XXM" patterns
    text = re.sub(r'[Rr]aised\s+(?:US\s*)?\$\d+(?:\.\d+)?\s*(?:million|M)[^;]*;?\s*', '', text)

    # Remove series round details like "(Series A: $26M, Series A+: $45M)"
    text = re.sub(r'\([^)]*Series [A-Z]\+?:[^)]*\)', '', text)

    # Clean up multiple semicolons
    text = re.sub(r';\s*;', ';', text)

    # Remove leading/trailing semicolons and whitespace
    text = text.strip('; ')

    return text


def migrate_data():
    """
    Main migration function.
    """
    print("=== Data Migration: 7-column → 11-column ===\n")

    # Step 1: Backup original file
    print(f"1. Backing up original file to: {BACKUP_FILE}")
    shutil.copy2(INPUT_FILE, BACKUP_FILE)
    print("   ✓ Backup created\n")

    # Step 2: Read current CSV
    print(f"2. Reading current CSV: {INPUT_FILE}")
    companies = []

    with open(INPUT_FILE, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        companies = list(reader)

    print(f"   ✓ Read {len(companies)} companies\n")

    # Step 3: Transform data
    print("3. Transforming data to 11-column format:")
    migrated = []

    for company in companies:
        company_name = company.get('Company Name', '')
        achievements = company.get('Current Achievements', '')

        # Extract funding info
        total_funding = extract_funding_amount(achievements)
        funding_stage = extract_funding_stage(achievements)

        # Get manually categorized data
        industry = INDUSTRY_MAPPING.get(company_name, '')
        founded_year = FOUNDED_YEAR_MAPPING.get(company_name, '')

        # Clean achievements text (remove extracted funding info)
        cleaned_achievements = clean_achievements_text(achievements, total_funding, funding_stage)

        # Create new row
        new_row = {
            'Company Name': company.get('Company Name', ''),
            'Company LinkedIn': company.get('Company LinkedIn', ''),
            'Founders': company.get('Founders', ''),
            'China Background': company.get('China Background', ''),
            'Total Funding (USD M)': total_funding,
            'Funding Stage': funding_stage,
            'Founded Year': founded_year,
            'Industry': industry,
            'Current Achievements': cleaned_achievements,
            'Investors': company.get('Investors', ''),
            'Description': company.get('Description', '')
        }

        migrated.append(new_row)

        # Print extraction results
        print(f"   - {company_name}:")
        print(f"     Funding: ${total_funding}M, Stage: {funding_stage}, Year: {founded_year}, Industry: {industry}")

    print(f"\n   ✓ Transformed {len(migrated)} companies\n")

    # Step 4: Write new CSV
    print(f"4. Writing new CSV: {OUTPUT_FILE}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=NEW_HEADERS)
        writer.writeheader()
        writer.writerows(migrated)

    print(f"   ✓ Wrote {len(migrated)} companies to new format\n")

    # Step 5: Summary
    print("=== Migration Summary ===")
    print(f"✓ Original file backed up: {BACKUP_FILE}")
    print(f"✓ New 11-column CSV created: {OUTPUT_FILE}")
    print(f"✓ Total companies migrated: {len(migrated)}")
    print("\nNew columns added:")
    print("  - Total Funding (USD M): Extracted from achievements text")
    print("  - Funding Stage: Extracted from achievements text")
    print("  - Founded Year: Manually categorized based on research")
    print("  - Industry: Manually categorized based on company focus")
    print("\nMigration complete! ✓")


if __name__ == '__main__':
    try:
        migrate_data()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
