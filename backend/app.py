"""
Flask REST API for AI Companies Editor.
Provides CRUD endpoints for managing company data in CSV format.
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import traceback
import logging
from io import StringIO

from config import (
    DEBUG, PORT, HOST, CORS_ORIGINS, MAX_UPLOAD_SIZE,
    FUNDING_STAGES, INDUSTRIES
)
from models import CSVModel
from validators import ValidationError

# Initialize Flask app
app = Flask(__name__)

# Configure CORS with specific origins
CORS(app, origins=CORS_ORIGINS, supports_credentials=True)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set max upload size
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE


# Error handlers
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    """Handle validation errors with 400 Bad Request."""
    logger.warning(f"Validation error: {str(e)}")
    return jsonify({
        'success': False,
        'error': str(e)
    }), 400


@app.errorhandler(IOError)
def handle_io_error(e):
    """Handle file I/O errors with 500 Internal Server Error."""
    logger.error(f"I/O error: {str(e)}")
    return jsonify({
        'success': False,
        'error': 'File operation failed. Please try again.'
    }), 500


@app.errorhandler(413)
def handle_file_too_large(e):
    """Handle file size errors."""
    return jsonify({
        'success': False,
        'error': f'File too large. Maximum size is {MAX_UPLOAD_SIZE // (1024*1024)}MB.'
    }), 413


@app.errorhandler(Exception)
def handle_unexpected_error(e):
    """Handle unexpected errors with 500 Internal Server Error."""
    logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
    return jsonify({
        'success': False,
        'error': 'An unexpected error occurred. Please try again.'
    }), 500


# API endpoints

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'AI Companies Editor API is running'
    })


@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Get configuration data (dropdown options, etc.).

    Returns:
        JSON with funding stages and industries
    """
    return jsonify({
        'success': True,
        'config': {
            'fundingStages': FUNDING_STAGES,
            'industries': INDUSTRIES
        }
    })


@app.route('/api/companies', methods=['GET'])
def get_companies():
    """
    Get all companies.

    Returns:
        JSON array of companies with auto-generated IDs
    """
    try:
        companies = CSVModel.get_all()
        logger.info(f"Retrieved {len(companies)} companies")

        return jsonify({
            'success': True,
            'companies': companies,
            'count': len(companies)
        })

    except Exception as e:
        raise  # Let error handler deal with it


@app.route('/api/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """
    Get a single company by ID.

    Args:
        company_id: Row index of company (0-indexed)

    Returns:
        JSON with company data or 404 if not found
    """
    try:
        company = CSVModel.get_by_id(company_id)

        if company is None:
            return jsonify({
                'success': False,
                'error': f'Company with ID {company_id} not found'
            }), 404

        logger.info(f"Retrieved company ID {company_id}")

        return jsonify({
            'success': True,
            'company': company
        })

    except Exception as e:
        raise


@app.route('/api/companies', methods=['POST'])
def create_company():
    """
    Create a new company.

    Request body:
        JSON object with company data (all 11 fields)

    Returns:
        JSON with created company (including new ID)
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        # Create company (validation happens in model)
        company = CSVModel.create(data)

        logger.info(f"Created company: {company.get('Company Name')} (ID: {company['id']})")

        return jsonify({
            'success': True,
            'company': company,
            'message': 'Company created successfully'
        }), 201

    except ValidationError:
        raise  # Let validation error handler deal with it
    except Exception as e:
        raise


@app.route('/api/companies/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    """
    Update an existing company.

    Args:
        company_id: Row index of company to update (0-indexed)

    Request body:
        JSON object with updated company data

    Returns:
        JSON with updated company data
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        # Update company (validation happens in model)
        company = CSVModel.update(company_id, data)

        logger.info(f"Updated company ID {company_id}: {company.get('Company Name')}")

        return jsonify({
            'success': True,
            'company': company,
            'message': 'Company updated successfully'
        })

    except ValidationError:
        raise
    except Exception as e:
        raise


@app.route('/api/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """
    Delete a company.

    Args:
        company_id: Row index of company to delete (0-indexed)

    Returns:
        JSON with success message
    """
    try:
        CSVModel.delete(company_id)

        logger.info(f"Deleted company ID {company_id}")

        return jsonify({
            'success': True,
            'message': 'Company deleted successfully'
        })

    except ValidationError:
        raise
    except Exception as e:
        raise


@app.route('/api/import', methods=['POST'])
def import_csv():
    """
    Import companies from uploaded CSV file.

    Request:
        multipart/form-data with 'file' field containing CSV

    Returns:
        JSON with import results (count, errors)
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400

        file = request.files['file']

        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        # Check file extension
        if not file.filename.endswith('.csv'):
            return jsonify({
                'success': False,
                'error': 'File must be a CSV (.csv extension required)'
            }), 400

        # Read file content
        file_content = file.read().decode('utf-8')

        # Import CSV (validation happens in model)
        result = CSVModel.import_csv(file_content)

        if result['success']:
            logger.info(f"Imported {result['imported']} companies from {file.filename}")
            return jsonify({
                'success': True,
                'imported': result['imported'],
                'message': f"Successfully imported {result['imported']} companies"
            }), 201
        else:
            logger.warning(f"Import failed with {len(result['errors'])} errors")
            return jsonify({
                'success': False,
                'imported': 0,
                'errors': result['errors'],
                'error': f"Import failed with {len(result['errors'])} validation errors"
            }), 400

    except ValidationError:
        raise
    except Exception as e:
        raise


@app.route('/api/export', methods=['GET'])
def export_csv():
    """
    Export all companies as CSV file.

    Returns:
        CSV file download
    """
    try:
        # Get CSV content
        csv_content = CSVModel.export_csv()

        # Create file-like object
        csv_file = StringIO(csv_content)

        logger.info("Exported companies to CSV")

        # Return as downloadable file
        return send_file(
            StringIO(csv_content),
            mimetype='text/csv',
            as_attachment=True,
            download_name='companies-export.csv'
        )

    except Exception as e:
        raise


# Run server
if __name__ == '__main__':
    logger.info(f"Starting AI Companies Editor API on {HOST}:{PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"CORS origins: {CORS_ORIGINS}")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
