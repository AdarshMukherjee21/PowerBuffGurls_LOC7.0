// Initialize Lucide icons
lucide.createIcons();

// API Configuration
const API_URL = 'http://localhost:5000/api';

// DOM Elements
const totalLivesImpacted = document.getElementById('totalLivesImpacted');
const volunteerHours = document.getElementById('volunteerHours');
const avgImpact = document.getElementById('avgImpact');
const resourcesList = document.getElementById('resourcesList');
const sroiRatio = document.getElementById('sroiRatio');
const exportImpactReportBtn = document.getElementById('exportImpactReportBtn');

// Fetch Impact Analytics
async function fetchImpactAnalytics() {
    try {
        const response = await fetch(`${API_URL}/impact_analytics`);
        if (!response.ok) {
            throw new Error('Failed to fetch impact analytics');
        }
        const data = await response.json();
        
        // Update UI
        totalLivesImpacted.textContent = data.total_lives_impacted.toLocaleString();
        volunteerHours.textContent = data.volunteer_hours.toLocaleString();
        avgImpact.textContent = `₹${data.average_funding_per_beneficiary.toLocaleString()}`;
        
        // Display resources
        displayResources(data.resources_distributed);
        
        // Calculate and display SROI
        const sroi = calculateSROI(data);
        sroiRatio.textContent = `${sroi}:1`;
    } catch (error) {
        console.error('Error fetching impact analytics:', error);
        showError('Failed to load impact analytics');
    }
}

// Display Resources
function displayResources(resources) {
    resourcesList.innerHTML = resources.map(resource => `
        <div class="resource-card">
            <div class="resource-icon">
                <i data-lucide="package"></i>
            </div>
            <div class="resource-content">
                <h3>${resource}</h3>
            </div>
        </div>
    `).join('');
    
    // Reinitialize icons
    lucide.createIcons();
}

// Calculate SROI
function calculateSROI(data) {
    const socialValue = data.total_lives_impacted * data.average_funding_per_beneficiary;
    const totalInvestment = data.total_lives_impacted * data.average_funding_per_beneficiary;
    return (socialValue / totalInvestment).toFixed(2);
}

// Export Impact Report
async function exportImpactReport() {
    try {
        const response = await fetch(`${API_URL}/export_impact_report`);
        if (!response.ok) {
            throw new Error('Failed to generate impact report');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'impact_report.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error exporting impact report:', error);
        showError('Failed to export impact report');
    }
}

// Error Handling
function showError(message) {
    alert(message); // Replace with a better notification system
}

// Event Listeners
exportImpactReportBtn.addEventListener('click', exportImpactReport);

// Initialize
document.addEventListener('DOMContentLoaded', fetchImpactAnalytics);