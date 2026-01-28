/**
 * Company Editor Application
 * Manages the data editor interface for CRUD operations.
 */

class CompanyEditor {
    constructor() {
        // Initialize API client
        this.api = new APIClient();

        // State
        this.companies = [];
        this.config = null;
        this.editingCompanyId = null;

        // DOM elements
        this.elements = {
            // Alerts
            alert: document.getElementById('alert'),

            // Loading/Empty states
            loading: document.getElementById('loading'),
            tableWrapper: document.getElementById('table-wrapper'),
            emptyState: document.getElementById('empty-state'),

            // Stats
            totalCount: document.getElementById('total-count'),
            lastUpdated: document.getElementById('last-updated'),

            // Table
            tableBody: document.getElementById('table-body'),

            // Buttons
            addBtn: document.getElementById('add-btn'),
            importBtn: document.getElementById('import-btn'),
            exportBtn: document.getElementById('export-btn'),
            fileInput: document.getElementById('file-input'),

            // Company Modal
            companyModal: document.getElementById('company-modal'),
            modalTitle: document.getElementById('modal-title'),
            closeModal: document.getElementById('close-modal'),
            cancelBtn: document.getElementById('cancel-btn'),
            saveBtn: document.getElementById('save-btn'),
            companyForm: document.getElementById('company-form'),

            // Delete Modal
            deleteModal: document.getElementById('delete-modal'),
            closeDeleteModal: document.getElementById('close-delete-modal'),
            cancelDeleteBtn: document.getElementById('cancel-delete-btn'),
            confirmDeleteBtn: document.getElementById('confirm-delete-btn'),
            deleteCompanyName: document.getElementById('delete-company-name'),

            // Form Fields
            companyId: document.getElementById('company-id'),
            companyName: document.getElementById('company-name'),
            companyLinkedin: document.getElementById('company-linkedin'),
            founders: document.getElementById('founders'),
            chinaBackground: document.getElementById('china-background'),
            totalFunding: document.getElementById('total-funding'),
            fundingStage: document.getElementById('funding-stage'),
            foundedYear: document.getElementById('founded-year'),
            industry: document.getElementById('industry'),
            achievements: document.getElementById('achievements'),
            investors: document.getElementById('investors'),
            description: document.getElementById('description')
        };

        this.init();
    }

    /**
     * Initialize the editor application
     */
    async init() {
        // Set up event listeners
        this.setupEventListeners();

        // Load configuration (dropdown options)
        await this.loadConfig();

        // Load companies data
        await this.loadCompanies();
    }

    /**
     * Set up all event listeners
     */
    setupEventListeners() {
        // Add company button
        this.elements.addBtn.addEventListener('click', () => this.showAddForm());

        // Import/Export buttons
        this.elements.importBtn.addEventListener('click', () => this.elements.fileInput.click());
        this.elements.exportBtn.addEventListener('click', () => this.exportCSV());
        this.elements.fileInput.addEventListener('change', (e) => this.importCSV(e));

        // Company modal
        this.elements.closeModal.addEventListener('click', () => this.closeCompanyModal());
        this.elements.cancelBtn.addEventListener('click', () => this.closeCompanyModal());
        this.elements.companyForm.addEventListener('submit', (e) => this.saveCompany(e));

        // Delete modal
        this.elements.closeDeleteModal.addEventListener('click', () => this.closeDeleteModal());
        this.elements.cancelDeleteBtn.addEventListener('click', () => this.closeDeleteModal());
        this.elements.confirmDeleteBtn.addEventListener('click', () => this.confirmDelete());

        // Close modals on outside click
        this.elements.companyModal.addEventListener('click', (e) => {
            if (e.target === this.elements.companyModal) {
                this.closeCompanyModal();
            }
        });

        this.elements.deleteModal.addEventListener('click', (e) => {
            if (e.target === this.elements.deleteModal) {
                this.closeDeleteModal();
            }
        });
    }

    /**
     * Load configuration (dropdown options)
     */
    async loadConfig() {
        try {
            this.config = await this.api.getConfig();

            // Populate funding stage dropdown
            this.config.fundingStages.forEach(stage => {
                const option = document.createElement('option');
                option.value = stage;
                option.textContent = stage;
                this.elements.fundingStage.appendChild(option);
            });

            // Populate industry dropdown
            this.config.industries.forEach(industry => {
                const option = document.createElement('option');
                option.value = industry;
                option.textContent = industry;
                this.elements.industry.appendChild(option);
            });

        } catch (error) {
            console.error('Failed to load config:', error);
            this.showAlert('Failed to load dropdown options', 'error');
        }
    }

    /**
     * Load all companies from API
     */
    async loadCompanies() {
        try {
            this.showLoading(true);
            this.companies = await this.api.getCompanies();
            this.renderTable();
            this.updateStats();
            this.showLoading(false);

        } catch (error) {
            console.error('Failed to load companies:', error);
            this.showAlert(error.message, 'error');
            this.showLoading(false);
        }
    }

    /**
     * Render companies table
     */
    renderTable() {
        const tbody = this.elements.tableBody;
        tbody.innerHTML = '';

        if (this.companies.length === 0) {
            this.elements.tableWrapper.style.display = 'none';
            this.elements.emptyState.style.display = 'block';
            return;
        }

        this.elements.tableWrapper.style.display = 'block';
        this.elements.emptyState.style.display = 'none';

        this.companies.forEach(company => {
            const row = document.createElement('tr');

            // Company Name
            const nameCell = document.createElement('td');
            nameCell.innerHTML = `<span class="company-name">${this.escapeHtml(company['Company Name'])}</span>`;
            row.appendChild(nameCell);

            // Industry
            const industryCell = document.createElement('td');
            if (company['Industry']) {
                industryCell.innerHTML = `<span class="badge badge-industry">${this.escapeHtml(company['Industry'])}</span>`;
            } else {
                industryCell.textContent = '—';
            }
            row.appendChild(industryCell);

            // Funding Stage
            const stageCell = document.createElement('td');
            if (company['Funding Stage']) {
                stageCell.innerHTML = `<span class="badge badge-stage">${this.escapeHtml(company['Funding Stage'])}</span>`;
            } else {
                stageCell.textContent = '—';
            }
            row.appendChild(stageCell);

            // Total Funding
            const fundingCell = document.createElement('td');
            if (company['Total Funding (USD M)']) {
                fundingCell.textContent = `$${company['Total Funding (USD M)']}M`;
            } else {
                fundingCell.textContent = '—';
            }
            row.appendChild(fundingCell);

            // Founded Year
            const yearCell = document.createElement('td');
            yearCell.textContent = company['Founded Year'] || '—';
            row.appendChild(yearCell);

            // Actions
            const actionsCell = document.createElement('td');
            actionsCell.innerHTML = `
                <div class="actions">
                    <button class="btn btn-secondary btn-icon" onclick="editor.editCompany(${company.id})">Edit</button>
                    <button class="btn btn-danger btn-icon" onclick="editor.deleteCompany(${company.id})">Delete</button>
                </div>
            `;
            row.appendChild(actionsCell);

            tbody.appendChild(row);
        });
    }

    /**
     * Update statistics display
     */
    updateStats() {
        this.elements.totalCount.textContent = this.companies.length;
        this.elements.lastUpdated.textContent = new Date().toLocaleTimeString();
    }

    /**
     * Show loading state
     */
    showLoading(show) {
        this.elements.loading.style.display = show ? 'block' : 'none';
        if (!show) {
            this.renderTable();
        }
    }

    /**
     * Show add company form
     */
    showAddForm() {
        this.editingCompanyId = null;
        this.elements.modalTitle.textContent = 'Add Company';
        this.elements.companyForm.reset();
        this.elements.companyId.value = '';
        this.clearFormErrors();
        this.openCompanyModal();
    }

    /**
     * Edit existing company
     */
    async editCompany(id) {
        try {
            const company = this.companies.find(c => c.id === id);
            if (!company) {
                this.showAlert('Company not found', 'error');
                return;
            }

            this.editingCompanyId = id;
            this.elements.modalTitle.textContent = 'Edit Company';

            // Populate form fields
            this.elements.companyId.value = id;
            this.elements.companyName.value = company['Company Name'] || '';
            this.elements.companyLinkedin.value = company['Company LinkedIn'] || '';
            this.elements.founders.value = company['Founders'] || '';
            this.elements.chinaBackground.value = company['China Background'] || '';
            this.elements.totalFunding.value = company['Total Funding (USD M)'] || '';
            this.elements.fundingStage.value = company['Funding Stage'] || '';
            this.elements.foundedYear.value = company['Founded Year'] || '';
            this.elements.industry.value = company['Industry'] || '';
            this.elements.achievements.value = company['Current Achievements'] || '';
            this.elements.investors.value = company['Investors'] || '';
            this.elements.description.value = company['Description'] || '';

            this.clearFormErrors();
            this.openCompanyModal();

        } catch (error) {
            console.error('Failed to edit company:', error);
            this.showAlert(error.message, 'error');
        }
    }

    /**
     * Save company (create or update)
     */
    async saveCompany(e) {
        e.preventDefault();

        // Collect form data
        const data = {
            'Company Name': this.elements.companyName.value.trim(),
            'Company LinkedIn': this.elements.companyLinkedin.value.trim(),
            'Founders': this.elements.founders.value.trim(),
            'China Background': this.elements.chinaBackground.value.trim(),
            'Total Funding (USD M)': this.elements.totalFunding.value.trim(),
            'Funding Stage': this.elements.fundingStage.value,
            'Founded Year': this.elements.foundedYear.value.trim(),
            'Industry': this.elements.industry.value,
            'Current Achievements': this.elements.achievements.value.trim(),
            'Investors': this.elements.investors.value.trim(),
            'Description': this.elements.description.value.trim()
        };

        try {
            if (this.editingCompanyId !== null) {
                // Update existing company
                await this.api.updateCompany(this.editingCompanyId, data);
                this.showAlert('Company updated successfully', 'success');
            } else {
                // Create new company
                await this.api.createCompany(data);
                this.showAlert('Company created successfully', 'success');
            }

            this.closeCompanyModal();
            await this.loadCompanies();

        } catch (error) {
            console.error('Failed to save company:', error);
            this.showAlert(error.message, 'error');
        }
    }

    /**
     * Delete company (show confirmation)
     */
    deleteCompany(id) {
        const company = this.companies.find(c => c.id === id);
        if (!company) {
            this.showAlert('Company not found', 'error');
            return;
        }

        this.editingCompanyId = id;
        this.elements.deleteCompanyName.textContent = company['Company Name'];
        this.openDeleteModal();
    }

    /**
     * Confirm delete action
     */
    async confirmDelete() {
        if (this.editingCompanyId === null) return;

        try {
            await this.api.deleteCompany(this.editingCompanyId);
            this.showAlert('Company deleted successfully', 'success');
            this.closeDeleteModal();
            await this.loadCompanies();

        } catch (error) {
            console.error('Failed to delete company:', error);
            this.showAlert(error.message, 'error');
        }
    }

    /**
     * Import CSV file
     */
    async importCSV(e) {
        const file = e.target.files[0];
        if (!file) return;

        if (!file.name.endsWith('.csv')) {
            this.showAlert('Please select a CSV file', 'error');
            return;
        }

        try {
            const result = await this.api.importCSV(file);

            if (result.success) {
                this.showAlert(`Successfully imported ${result.imported} companies`, 'success');
                await this.loadCompanies();
            } else {
                this.showAlert(`Import failed: ${result.error}`, 'error');
            }

        } catch (error) {
            console.error('Failed to import CSV:', error);
            this.showAlert(error.message, 'error');
        } finally {
            // Reset file input
            this.elements.fileInput.value = '';
        }
    }

    /**
     * Export CSV file
     */
    async exportCSV() {
        try {
            await this.api.exportCSV();
            this.showAlert('CSV exported successfully', 'success');

        } catch (error) {
            console.error('Failed to export CSV:', error);
            this.showAlert(error.message, 'error');
        }
    }

    /**
     * Show alert message
     */
    showAlert(message, type = 'success') {
        const alert = this.elements.alert;
        alert.className = `alert alert-${type} active`;
        alert.textContent = message;

        // Auto-hide after 5 seconds
        setTimeout(() => {
            alert.classList.remove('active');
        }, 5000);
    }

    /**
     * Open company modal
     */
    openCompanyModal() {
        this.elements.companyModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    /**
     * Close company modal
     */
    closeCompanyModal() {
        this.elements.companyModal.classList.remove('active');
        document.body.style.overflow = '';
        this.elements.companyForm.reset();
        this.clearFormErrors();
    }

    /**
     * Open delete modal
     */
    openDeleteModal() {
        this.elements.deleteModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    /**
     * Close delete modal
     */
    closeDeleteModal() {
        this.elements.deleteModal.classList.remove('active');
        document.body.style.overflow = '';
        this.editingCompanyId = null;
    }

    /**
     * Clear form validation errors
     */
    clearFormErrors() {
        // Remove any error styling
        const inputs = this.elements.companyForm.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.style.borderColor = '';
        });
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize editor when DOM is ready
let editor;
document.addEventListener('DOMContentLoaded', () => {
    editor = new CompanyEditor();
});
