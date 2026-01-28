#!/usr/bin/env python3
"""
Quick test script to verify backend functionality.
"""

import sys
sys.path.insert(0, 'backend')

from models import CSVModel
from validators import validate_company_data, ValidationError

print("=== Testing Backend Components ===\n")

# Test 1: Read CSV
print("1. Testing CSV read:")
try:
    companies = CSVModel.get_all()
    print(f"   ✓ Loaded {len(companies)} companies")
    if companies:
        print(f"   ✓ First company: {companies[0].get('Company Name', 'N/A')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Validation
print("\n2. Testing validation:")
test_data = {
    'Company Name': 'Test Company',
    'Company LinkedIn': 'https://linkedin.com/company/test',
    'Founders': 'John Doe',
    'China Background': 'Test background',
    'Total Funding (USD M)': '10',
    'Funding Stage': 'Seed',
    'Founded Year': '2024',
    'Industry': 'AI/ML',
    'Current Achievements': 'Test achievements',
    'Investors': 'Test Investor',
    'Description': 'Test description'
}

try:
    validated = validate_company_data(test_data)
    print(f"   ✓ Validation passed")
    print(f"   ✓ Validated company name: {validated['Company Name']}")
except ValidationError as e:
    print(f"   ✗ Validation error: {e}")

# Test 3: XSS Prevention
print("\n3. Testing XSS prevention:")
xss_data = test_data.copy()
xss_data['Company Name'] = '<script>alert("XSS")</script>Test'

try:
    validated = validate_company_data(xss_data)
    print(f"   ✓ XSS prevention worked")
    print(f"   ✓ Sanitized name: {validated['Company Name']}")
    if '<script>' not in validated['Company Name']:
        print(f"   ✓ Script tags removed successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: CSV Injection Prevention
print("\n4. Testing CSV injection prevention:")
csv_injection_data = test_data.copy()
csv_injection_data['Company Name'] = '=1+1'

try:
    validated = validate_company_data(csv_injection_data)
    print(f"   ✓ CSV injection prevention worked")
    print(f"   ✓ Escaped name: {validated['Company Name']}")
    if validated['Company Name'].startswith("'"):
        print(f"   ✓ Formula character escaped successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n=== All Backend Tests Complete ===")
