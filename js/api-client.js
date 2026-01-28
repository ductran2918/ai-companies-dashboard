/**
 * API Client for communicating with the Flask backend.
 * Handles all HTTP requests to the REST API.
 */

class APIClient {
    /**
     * Initialize API client.
     * @param {string} baseURL - Base URL for API endpoints (default: http://localhost:5000/api)
     */
    constructor(baseURL = 'http://localhost:5000/api') {
        this.baseURL = baseURL;
    }

    /**
     * Generic fetch wrapper with error handling.
     * @param {string} endpoint - API endpoint path
     * @param {object} options - Fetch options
     * @returns {Promise<object>} - Response JSON
     */
    async _fetch(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        // Set default headers
        const headers = {
            ...options.headers
        };

        // Add Content-Type for JSON requests
        if (options.body && !(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            // Parse JSON response
            const data = await response.json();

            // Check if request was successful
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
            }

            return data;

        } catch (error) {
            // Network errors or parse errors
            if (error instanceof TypeError) {
                throw new Error('Network error: Unable to connect to backend. Is the server running?');
            }
            throw error;
        }
    }

    /**
     * Get all companies.
     * @returns {Promise<Array>} - Array of company objects
     */
    async getCompanies() {
        const data = await this._fetch('/companies');
        return data.companies;
    }

    /**
     * Get a single company by ID.
     * @param {number} id - Company ID (row index)
     * @returns {Promise<object>} - Company object
     */
    async getCompany(id) {
        const data = await this._fetch(`/companies/${id}`);
        return data.company;
    }

    /**
     * Create a new company.
     * @param {object} companyData - Company data object
     * @returns {Promise<object>} - Created company with ID
     */
    async createCompany(companyData) {
        const data = await this._fetch('/companies', {
            method: 'POST',
            body: JSON.stringify(companyData)
        });
        return data.company;
    }

    /**
     * Update an existing company.
     * @param {number} id - Company ID to update
     * @param {object} companyData - Updated company data
     * @returns {Promise<object>} - Updated company object
     */
    async updateCompany(id, companyData) {
        const data = await this._fetch(`/companies/${id}`, {
            method: 'PUT',
            body: JSON.stringify(companyData)
        });
        return data.company;
    }

    /**
     * Delete a company.
     * @param {number} id - Company ID to delete
     * @returns {Promise<object>} - Success response
     */
    async deleteCompany(id) {
        return await this._fetch(`/companies/${id}`, {
            method: 'DELETE'
        });
    }

    /**
     * Import companies from CSV file.
     * @param {File} file - CSV file object
     * @returns {Promise<object>} - Import result (count, errors)
     */
    async importCSV(file) {
        const formData = new FormData();
        formData.append('file', file);

        return await this._fetch('/import', {
            method: 'POST',
            body: formData
        });
    }

    /**
     * Export companies as CSV file.
     * Downloads the file to user's browser.
     */
    async exportCSV() {
        const url = `${this.baseURL}/export`;

        try {
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            // Get CSV content as blob
            const blob = await response.blob();

            // Create download link and trigger download
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = `companies-export-${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            // Clean up blob URL
            window.URL.revokeObjectURL(downloadUrl);

        } catch (error) {
            if (error instanceof TypeError) {
                throw new Error('Network error: Unable to connect to backend');
            }
            throw error;
        }
    }

    /**
     * Get configuration data (dropdown options).
     * @returns {Promise<object>} - Config object with fundingStages and industries
     */
    async getConfig() {
        const data = await this._fetch('/config');
        return data.config;
    }

    /**
     * Health check to verify backend is running.
     * @returns {Promise<boolean>} - True if backend is healthy
     */
    async healthCheck() {
        try {
            const data = await this._fetch('/health');
            return data.status === 'healthy';
        } catch (error) {
            return false;
        }
    }
}
