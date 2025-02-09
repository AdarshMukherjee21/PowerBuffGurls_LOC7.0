// Initialize Lucide icons
lucide.createIcons();

// API Configuration
const API_URL = 'http://localhost:5000/api';

// DOM Elements
const totalCampaigns = document.getElementById('totalCampaigns');
const totalDonations = document.getElementById('totalDonations');
const livesImpacted = document.getElementById('livesImpacted');
const campaignsGrid = document.getElementById('campaignsGrid');
const createCampaignBtn = document.getElementById('createCampaignBtn');
const createCampaignModal = document.getElementById('createCampaignModal');
const campaignForm = document.getElementById('campaignForm');
const closeBtn = document.querySelector('.close-btn');
const cancelBtn = document.getElementById('cancelBtn');
const exportPdfBtn = document.getElementById('exportPdfBtn');

// Fetch Dashboard Data
async function fetchDashboardData() {
  try {
    const response = await fetch(`${API_URL}/dashboard`);
    if (!response.ok) {
      throw new Error('Failed to fetch dashboard data');
    }
    const data = await response.json();

    // Format numbers properly
    totalCampaigns.textContent = data.total_campaigns || 0;
    totalDonations.textContent = formatAmount(data.total_funds_raised || 0);
    livesImpacted.textContent = (data.lives_impacted || 0).toLocaleString();
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    showError('Error loading dashboard data');
  }
}

// Format amount in Lakhs
function formatAmount(amount) {
  // Convert to Lakhs (1 Lakh = 100,000)
  const amountInLakhs = amount / 100000;
  return `₹${amountInLakhs.toFixed(1)}L`;
}

// Fetch and Display Campaigns
async function fetchCampaigns() {
  try {
    const response = await fetch(`${API_URL}/campaigns`);
    if (!response.ok) {
      throw new Error('Failed to fetch campaigns');
    }
    const campaigns = await response.json();

    campaignsGrid.innerHTML = campaigns.map(campaign => {
      // Ensure amounts are numbers
      const goalAmount = parseFloat(campaign.goal_amount) || 0;
      const amountRaised = parseFloat(campaign.amount_raised) || 0;
      const progressPercentage = goalAmount > 0 ? (amountRaised / goalAmount) * 100 : 0;

      return `
        <div class="campaign-card">
          <div class="campaign-header">
            <i data-lucide="target" class="campaign-icon"></i>
            <div>
              <h3 class="campaign-title">${campaign.title}</h3>
              <p class="campaign-company">${campaign.company_name}</p>
            </div>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${progressPercentage}%"></div>
          </div>
          <div class="campaign-stats">
            <span>${formatAmount(amountRaised)}</span>
            <span>${formatAmount(goalAmount)}</span>
          </div>
        </div>
      `;
    }).join('');

    // Reinitialize icons for new content
    lucide.createIcons();
  } catch (error) {
    console.error('Error fetching campaigns:', error);
    showError('Error loading campaigns');
  }
}

// Create Campaign
async function createCampaign(formData) {
  try {
    const data = Object.fromEntries(formData);
    // Convert goal_amount to a number
    data.goal_amount = parseFloat(data.goal_amount) || 0;

    const response = await fetch(`${API_URL}/create_campaign`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to create campaign');
    }

    // Refresh dashboard and campaigns
    await Promise.all([fetchDashboardData(), fetchCampaigns()]);
    closeModal();
    showSuccess('Campaign created successfully');
  } catch (error) {
    console.error('Error creating campaign:', error);
    showError('Failed to create campaign');
  }
}

// Modal Functions
function openModal() {
  createCampaignModal.classList.add('active');
}

function closeModal() {
  createCampaignModal.classList.remove('active');
  campaignForm.reset();
}

// Notifications
function showSuccess(message) {
  const notification = document.createElement('div');
  notification.className = 'notification success';
  notification.textContent = message;
  showNotification(notification);
}

function showError(message) {
  const notification = document.createElement('div');
  notification.className = 'notification error';
  notification.textContent = message;
  showNotification(notification);
}

function showNotification(notification) {
  document.body.appendChild(notification);
  setTimeout(() => {
    notification.remove();
  }, 3000);
}

// Event Listeners
createCampaignBtn.addEventListener('click', openModal);
closeBtn.addEventListener('click', closeModal);
cancelBtn.addEventListener('click', closeModal);

campaignForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(campaignForm);
  await createCampaign(formData);
});

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
  fetchDashboardData();
  fetchCampaigns();
});