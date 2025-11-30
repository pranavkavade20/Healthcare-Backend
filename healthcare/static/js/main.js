// Main JavaScript file for Healthcare System

/**
 * Initialize tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Format currency
 */
function formatCurrency(value, currency = '₹') {
    return currency + parseFloat(value).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

/**
 * Format date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-error',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const alertHTML = `
        <div class="${alertClass} alert animate-fade-in" role="alert">
            <button type="button" class="float-right text-lg">&times;</button>
            ${message}
        </div>
    `;

    // Create container if it doesn't exist
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'fixed top-20 right-4 z-50 max-w-md';
        document.body.appendChild(container);
    }

    const alertDiv = document.createElement('div');
    alertDiv.innerHTML = alertHTML;
    container.appendChild(alertDiv.firstElementChild);

    // Auto remove after 5 seconds
    setTimeout(() => {
        const alert = container.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);

    // Manual close button
    const closeBtn = container.querySelector('.float-right');
    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            this.closest('.alert').remove();
        });
    }
}

/**
 * Validate email
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate phone number
 */
function isValidPhone(phone) {
    const re = /^\+?1?\d{9,15}$/;
    return re.test(phone.replace(/\D/g, ''));
}

/**
 * Load data via AJAX
 */
async function loadData(url) {
    try {
        const response = await fetch(url, {
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error loading data:', error);
        showNotification('Error loading data', 'error');
        return null;
    }
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Search functionality
 */
const search = debounce(async function (query) {
    if (query.length < 2) return;

    // Implementation depends on your search endpoint
    // This is a placeholder
    console.log('Searching for:', query);
}, 300);

/**
 * Form validation
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');

            // Email validation
            if (input.type === 'email' && !isValidEmail(input.value)) {
                input.classList.add('is-invalid');
                isValid = false;
            }

            // Phone validation
            if (input.type === 'tel' && !isValidPhone(input.value)) {
                input.classList.add('is-invalid');
                isValid = false;
            }
        }
    });

    return isValid;
}

/**
 * Copy to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy', 'error');
    });
}

/**
 * Export table to CSV
 */
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvrow = [];
        cols.forEach(col => {
            csvrow.push(col.textContent.trim());
        });
        csv.push(csvrow.join(','));
    });

    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Print element
 */
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const printWindow = window.open('', '', 'width=800,height=600');
    printWindow.document.write('<html><head><title>Print</title>');
    printWindow.document.write('<link rel="stylesheet" href="' + window.location.origin + '/static/css/style.css">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(element.innerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

/**
 * Get CSRF token from cookie
 */
function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Confirm delete action
 */
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

/**
 * Initialize on DOM ready
 */
document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips
    initTooltips();

    // Add CSRF token to all fetch requests
    const csrftoken = getCSRFToken();

    // Highlight invalid form fields
    const invalidInputs = document.querySelectorAll('.is-invalid');
    invalidInputs.forEach(input => {
        input.addEventListener('input', function () {
            this.classList.remove('is-invalid');
        });
    });

    // Initialize form validation if forms exist
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!validateForm(this.id || 'form')) {
                e.preventDefault();
                showNotification('Please fill all required fields correctly', 'warning');
            }
        });
    });

    // Mobile menu toggle
    const menuToggle = document.querySelector('[data-toggle="mobile-menu"]');
    if (menuToggle) {
        menuToggle.addEventListener('click', function () {
            const menu = document.querySelector('.mobile-menu');
            if (menu) {
                menu.classList.toggle('hidden');
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
});

// Log initialization
console.log('Healthcare System JavaScript loaded successfully');
