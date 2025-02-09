// Initialize Lucide icons
lucide.createIcons();

// API Configuration
const API_URL = 'http://localhost:5000/api';

// DOM Elements
const totalContributions = document.getElementById('totalContributions');
const eligibleDeductions = document.getElementById('eligibleDeductions');
const estimatedSavings = document.getElementById('estimatedSavings');
const exportTaxReportBtn = document.getElementById('exportTaxReportBtn');

// Format currency
function formatCurrency(amount) {
    return `₹${(amount).toLocaleString('en-IN', {
        maximumFractionDigits: 2,
        minimumFractionDigits: 2
    })}`;
}

// Fetch Tax Benefits
async function fetchTaxBenefits() {
    try {
        const response = await fetch(`${API_URL}/calculate_tax`);
        if (!response.ok) {
            throw new Error('Failed to calculate tax benefits');
        }
        const data = await response.json();
        
        // Update UI
        totalContributions.textContent = formatCurrency(data.total_contributions);
        eligibleDeductions.textContent = formatCurrency(data.eligible_deductions);
        estimatedSavings.textContent = formatCurrency(data.estimated_tax_savings);
    } catch (error) {
        console.error('Error fetching tax benefits:', error);
        alert('Failed to calculate tax benefits');
    }
}

// Export Tax Report
async function exportTaxReport() {
    try {
        const response = await fetch(`${API_URL}/export_tax_report`);
        if (!response.ok) {
            throw new Error('Failed to generate tax report');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'tax_benefits_report.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error exporting tax report:', error);
        alert('Failed to export tax report');
    }
}

// Event Listeners
exportTaxReportBtn.addEventListener('click', exportTaxReport);

// Initialize
document.addEventListener('DOMContentLoaded', fetchTaxBenefits);