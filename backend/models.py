"""
CSV data model for CRUD operations on companies data.
Handles reading, writing, and backup of CSV file.
"""

import csv
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from config import CSV_FILE_PATH, BACKUP_DIR, MAX_BACKUPS, REQUIRED_HEADERS
from validators import validate_company_data, ValidationError


class CSVModel:
    """Model for managing company data in CSV format."""

    @staticmethod
    def _ensure_backup_dir():
        """Create backup directory if it doesn't exist."""
        os.makedirs(BACKUP_DIR, exist_ok=True)

    @staticmethod
    def _create_backup() -> str:
        """
        Create a backup of the current CSV file.

        Returns:
            Path to the backup file

        Raises:
            IOError: If backup creation fails
        """
        CSVModel._ensure_backup_dir()

        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'sample-data_{timestamp}.csv'
        backup_path = os.path.join(BACKUP_DIR, backup_filename)

        # Copy current CSV to backup
        if os.path.exists(CSV_FILE_PATH):
            shutil.copy2(CSV_FILE_PATH, backup_path)
        else:
            raise IOError(f"CSV file not found: {CSV_FILE_PATH}")

        # Cleanup old backups (keep only MAX_BACKUPS most recent)
        CSVModel._cleanup_old_backups()

        return backup_path

    @staticmethod
    def _cleanup_old_backups():
        """Remove old backup files, keeping only MAX_BACKUPS most recent."""
        if not os.path.exists(BACKUP_DIR):
            return

        # Get all backup files sorted by modification time (newest first)
        backups = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith('sample-data_') and filename.endswith('.csv'):
                filepath = os.path.join(BACKUP_DIR, filename)
                backups.append((filepath, os.path.getmtime(filepath)))

        backups.sort(key=lambda x: x[1], reverse=True)

        # Remove old backups beyond MAX_BACKUPS
        for filepath, _ in backups[MAX_BACKUPS:]:
            try:
                os.remove(filepath)
            except OSError:
                pass  # Ignore errors during cleanup

    @staticmethod
    def _read_csv() -> List[Dict]:
        """
        Read all companies from CSV file.

        Returns:
            List of company dictionaries (each row as dict with column headers as keys)

        Raises:
            IOError: If CSV file cannot be read
        """
        if not os.path.exists(CSV_FILE_PATH):
            # Create empty CSV with headers if file doesn't exist
            CSVModel._write_csv([])
            return []

        companies = []

        with open(CSV_FILE_PATH, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)

            # Verify headers match expected structure
            if reader.fieldnames and set(reader.fieldnames) != set(REQUIRED_HEADERS):
                # Check if it's close enough (allow extra columns)
                missing = set(REQUIRED_HEADERS) - set(reader.fieldnames)
                if missing:
                    raise IOError(
                        f"CSV file has invalid headers. Missing: {', '.join(missing)}"
                    )

            for row in reader:
                companies.append(dict(row))

        return companies

    @staticmethod
    def _write_csv(companies: List[Dict]):
        """
        Write companies list to CSV file.

        Args:
            companies: List of company dictionaries

        Raises:
            IOError: If CSV file cannot be written
        """
        with open(CSV_FILE_PATH, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=REQUIRED_HEADERS)
            writer.writeheader()
            writer.writerows(companies)

    @staticmethod
    def get_all() -> List[Dict]:
        """
        Get all companies with auto-generated IDs.

        Returns:
            List of companies with 'id' field (0-indexed row number)
        """
        companies = CSVModel._read_csv()

        # Add auto-generated ID (row index)
        for i, company in enumerate(companies):
            company['id'] = i

        return companies

    @staticmethod
    def get_by_id(company_id: int) -> Optional[Dict]:
        """
        Get a single company by its ID (row index).

        Args:
            company_id: Row index of company (0-indexed)

        Returns:
            Company dictionary with 'id' field, or None if not found
        """
        companies = CSVModel.get_all()

        if 0 <= company_id < len(companies):
            return companies[company_id]

        return None

    @staticmethod
    def create(data: Dict) -> Dict:
        """
        Create a new company record.

        Args:
            data: Company data dictionary

        Returns:
            Created company with 'id' field

        Raises:
            ValidationError: If data validation fails
            IOError: If file operations fail
        """
        # Validate and sanitize input
        validated_data = validate_company_data(data)

        # Create backup before modifying
        CSVModel._create_backup()

        # Read existing companies
        companies = CSVModel._read_csv()

        # Ensure all required fields are present
        new_company = {header: validated_data.get(header, '') for header in REQUIRED_HEADERS}

        # Append new company
        companies.append(new_company)

        # Write back to CSV
        CSVModel._write_csv(companies)

        # Return created company with ID
        new_company['id'] = len(companies) - 1
        return new_company

    @staticmethod
    def update(company_id: int, data: Dict) -> Dict:
        """
        Update an existing company record.

        Args:
            company_id: Row index of company to update (0-indexed)
            data: Updated company data

        Returns:
            Updated company with 'id' field

        Raises:
            ValidationError: If data validation fails or company not found
            IOError: If file operations fail
        """
        # Validate and sanitize input
        validated_data = validate_company_data(data)

        # Create backup before modifying
        CSVModel._create_backup()

        # Read existing companies
        companies = CSVModel._read_csv()

        # Check if company exists
        if not (0 <= company_id < len(companies)):
            raise ValidationError(f"Company with ID {company_id} not found")

        # Update company data
        updated_company = {header: validated_data.get(header, '') for header in REQUIRED_HEADERS}
        companies[company_id] = updated_company

        # Write back to CSV
        CSVModel._write_csv(companies)

        # Return updated company with ID
        updated_company['id'] = company_id
        return updated_company

    @staticmethod
    def delete(company_id: int) -> bool:
        """
        Delete a company record.

        Args:
            company_id: Row index of company to delete (0-indexed)

        Returns:
            True if deleted successfully

        Raises:
            ValidationError: If company not found
            IOError: If file operations fail
        """
        # Create backup before modifying
        CSVModel._create_backup()

        # Read existing companies
        companies = CSVModel._read_csv()

        # Check if company exists
        if not (0 <= company_id < len(companies)):
            raise ValidationError(f"Company with ID {company_id} not found")

        # Remove company
        del companies[company_id]

        # Write back to CSV
        CSVModel._write_csv(companies)

        return True

    @staticmethod
    def import_csv(file_content: str) -> Dict:
        """
        Import companies from CSV file content.

        Args:
            file_content: CSV file content as string

        Returns:
            Dictionary with import results (count, errors)

        Raises:
            ValidationError: If CSV structure is invalid
            IOError: If file operations fail
        """
        # Parse CSV content
        lines = file_content.strip().split('\n')
        if len(lines) < 2:  # Need at least header + 1 data row
            raise ValidationError("CSV file is empty or has no data rows")

        # Read CSV from string
        reader = csv.DictReader(lines)

        # Verify headers
        if not reader.fieldnames:
            raise ValidationError("CSV file has no headers")

        missing_headers = set(REQUIRED_HEADERS) - set(reader.fieldnames)
        if missing_headers:
            raise ValidationError(
                f"CSV file is missing required headers: {', '.join(missing_headers)}"
            )

        # Parse and validate all rows
        companies = []
        errors = []
        row_num = 1  # Start at 1 (header is row 0)

        for row in reader:
            row_num += 1
            try:
                # Validate each row
                validated = validate_company_data(row)
                company = {header: validated.get(header, '') for header in REQUIRED_HEADERS}
                companies.append(company)
            except ValidationError as e:
                errors.append(f"Row {row_num}: {str(e)}")

        if errors:
            # Return errors without importing
            return {
                'success': False,
                'imported': 0,
                'errors': errors
            }

        # Create backup before replacing
        CSVModel._create_backup()

        # Replace entire CSV with imported data
        CSVModel._write_csv(companies)

        return {
            'success': True,
            'imported': len(companies),
            'errors': []
        }

    @staticmethod
    def export_csv() -> str:
        """
        Export all companies as CSV string.

        Returns:
            CSV content as string
        """
        companies = CSVModel._read_csv()

        # Write to string buffer
        output = []
        output.append(','.join(REQUIRED_HEADERS))

        for company in companies:
            row = []
            for header in REQUIRED_HEADERS:
                value = company.get(header, '')
                # Escape quotes and wrap in quotes if contains comma, quote, or newline
                if ',' in value or '"' in value or '\n' in value:
                    value = '"' + value.replace('"', '""') + '"'
                row.append(value)
            output.append(','.join(row))

        return '\n'.join(output)
