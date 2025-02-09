// Initialize Lucide icons
lucide.createIcons();

// API Configuration
const API_URL = 'http://localhost:5000/api';

// DOM Elements
const totalFunds = document.getElementById('totalFunds');
const allocatedFunds = document.getElementById('allocatedFunds');
const pendingFunds = document.getElementById('pendingFunds');
const transactionsBody = document.getElementById('transactionsBody');
const searchTransactions = document.getElementById('searchTransactions');
const typeFilter = document.getElementById('typeFilter');
const exportReportBtn = document.getElementById('exportReportBtn');

let transactions = [];

// Fetch Financial Reports
async function fetchFinancialReports() {
  try {
    const response = await fetch(`${API_URL}/financial_reports`);
    const data = await response.json();
    
    // Update summary
    totalFunds.textContent = formatCurrency(data.total_funds_received);
    allocatedFunds.textContent = formatCurrency(data.total_funds_allocated);
    pendingFunds.textContent = formatCurrency(data.pending_distribution);
    
    // Store transactions and display them
    transactions = data.transactions;
    filterAndDisplayTransactions();
  } catch (error) {
    console.error('Error fetching financial reports:', error);
    showError('Failed to load financial reports');
  }
}

// Filter and Display Transactions
function filterAndDisplayTransactions() {
  const searchTerm = searchTransactions.value.toLowerCase();
  const selectedType = typeFilter.value;

  const filteredTransactions = transactions.filter(transaction => {
    const matchesSearch = 
      transaction.transaction_id.toLowerCase().includes(searchTerm) ||
      transaction.donor_name.toLowerCase().includes(searchTerm) ||
      transaction.campaign_id.toLowerCase().includes(searchTerm);
    const matchesType = !selectedType || transaction.type === selectedType;
    return matchesSearch && matchesType;
  });

  displayTransactions(filteredTransactions);
}

// Display Transactions
function displayTransactions(transactionsToShow) {
  transactionsBody.innerHTML = transactionsToShow.map(transaction => `
    <tr>
      <td>${transaction.transaction_id}</td>
      <td>${transaction.campaign_id}</td>
      <td>${transaction.donor_name}</td>
      <td class="amount">${formatCurrency(transaction.amount)}</td>
      <td>
        <span class="transaction-type ${transaction.type.toLowerCase()}">
          ${transaction.type}
        </span>
      </td>
      <td>${formatDate(transaction.timestamp)}</td>
    </tr>
  `).join('');
}

// Export Financial Report
async function exportFinancialReport() {
  try {
    const response = await fetch(`${API_URL}/export_financial_report`);
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'financial_report.pdf';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error exporting report:', error);
    showError('Failed to export report');
  }
}

// Utility Functions
function formatCurrency(amount) {
  return `₹${(amount / 100000).toFixed(1)}L`;
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function showError(message) {
  // Implement error notification
  console.error(message);
}

// Event Listeners
searchTransactions.addEventListener('input', filterAndDisplayTransactions);
typeFilter.addEventListener('change', filterAndDisplayTransactions);
exportReportBtn.addEventListener('click', exportFinancialReport);

// Initialize
document.addEventListener('DOMContentLoaded', fetchFinancialReports);