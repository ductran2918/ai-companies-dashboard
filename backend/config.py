"""
Configuration settings for the AI Companies Editor backend.
"""

import os

# CSV file path - points to the main data file in project root
CSV_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample-data.csv')

# Backup directory for automatic CSV backups
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')

# Maximum number of backups to keep (auto-cleanup old ones)
MAX_BACKUPS = 10

# Maximum file size for CSV uploads (5MB in bytes)
MAX_UPLOAD_SIZE = 5 * 1024 * 1024

# CORS settings
# Development: Allow localhost origins
CORS_ORIGINS_DEV = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:5500',  # VSCode Live Server
]

# Production: Replace with actual deployed domain
CORS_ORIGINS_PROD = [
    'https://ductran2918.github.io',
]

# Determine environment
ENV = os.getenv('FLASK_ENV', 'development')
CORS_ORIGINS = CORS_ORIGINS_DEV if ENV == 'development' else CORS_ORIGINS_PROD

# Flask settings
DEBUG = ENV == 'development'
PORT = int(os.getenv('PORT', 5000))
HOST = '0.0.0.0'  # Allow external connections

# Expected CSV column headers (11-column optimized structure)
REQUIRED_HEADERS = [
    'Company Name',
    'Company LinkedIn',
    'Founders',
    'China Background',
    'Total Funding (USD M)',
    'Funding Stage',
    'Founded Year',
    'Industry',
    'Current Achievements',
    'Investors',
    'Description'
]

# Validation rules
VALIDATION = {
    'company_name_max_length': 200,
    'description_max_length': 1000,
    'founders_max_length': 500,
    'china_background_max_length': 500,
    'achievements_max_length': 500,
    'investors_max_length': 500,
    'min_founded_year': 1900,
    'max_founded_year': 2099,
    'min_funding': 0,
    'max_funding': 10000,  # $10 billion max
}

# Dropdown options
FUNDING_STAGES = [
    'Pre-seed',
    'Seed',
    'Angel',
    'Series A',
    'Series A+',
    'Series B',
    'Series C+',
    'Growth',
    'IPO',
    'Acquired',
    'Not disclosed'
]

INDUSTRIES = [
    'AI/ML',
    'Biotech',
    'Creative AI',
    'Data Infrastructure',
    'DevTools',
    'Enterprise AI',
    'Fintech',
    'Healthcare',
    'Media/Creative',
    'Productivity',
    'Security',
    'Other'
]
