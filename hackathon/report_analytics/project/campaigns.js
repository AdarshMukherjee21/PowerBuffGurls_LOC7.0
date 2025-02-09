// Initialize Lucide icons
lucide.createIcons();

// API Configuration
const API_URL = 'http://localhost:5000/api';

// DOM Elements
const campaignsList = document.getElementById('campaignsList');
const createCampaignBtn = document.getElementById('createCampaignBtn');
const createCampaignModal = document.getElementById('createCampaignModal');
const campaignForm = document.getElementById('campaignForm');
const searchInput = document.getElementById('searchInput');
const causeFilter = document.getElementById('causeFilter');
const statusFilter = document.getElementById('statusFilter');
const closeBtns = document.querySelectorAll('.close-btn, .close-modal');

let campaigns = [];

// Fetch and Display Campaigns
async function fetchCampaigns() {
  try {
    const response = await fetch(`${API_URL}/campaigns`);
    if (!response.ok) {
      throw new Error('Failed to fetch campaigns');
    }
    campaigns = await response.json();
    filterAndDisplayCampaigns();
  } catch (error) {
    console.error('Error fetching campaigns:', error);
    showError('Failed to load campaigns');
  }
}

function filterAndDisplayCampaigns() {
  const searchTerm = searchInput.value.toLowerCase();
  const selectedCause = causeFilter.value;
  const selectedStatus = statusFilter.value;

  const filteredCampaigns = campaigns.filter(campaign => {
    const matchesSearch = 
      campaign.title.toLowerCase().includes(searchTerm) ||
      campaign.company_name.toLowerCase().includes(searchTerm) ||
      campaign.description.toLowerCase().includes(searchTerm);
    const matchesCause = !selectedCause || campaign.cause === selectedCause;
    const matchesStatus = !selectedStatus || campaign.status === selectedStatus;
    return matchesSearch && matchesCause && matchesStatus;
  });

  displayCampaigns(filteredCampaigns);
}

function displayCampaigns(campaignsToShow) {
  campaignsList.innerHTML = campaignsToShow.map(campaign => {
    const goalAmount = parseFloat(campaign.goal_amount) || 0;
    const amountRaised = parseFloat(campaign.amount_raised) || 0;
    const progressPercentage = goalAmount > 0 ? (amountRaised / goalAmount) * 100 : 0;
    
    return `
    <div class="campaign-card">
      <div class="campaign-header">
        <div class="campaign-info">
          <h3 class="campaign-title">${campaign.title}</h3>
          <p class="campaign-company">${campaign.company_name}</p>
          <span class="campaign-cause">${campaign.cause}</span>
          <span class="campaign-status ${campaign.status.toLowerCase()}">${campaign.status}</span>
        </div>
      </div>
      <p class="campaign-description">${campaign.description}</p>
      <div class="campaign-progress">
        <div class="progress-stats">
          <span>₹${(amountRaised / 100000).toFixed(1)}L raised</span>
          <span>₹${(goalAmount / 100000).toFixed(1)}L goal</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" style="width: ${progressPercentage}%"></div>
        </div>
        <div class="campaign-dates">
          <span>Started: ${new Date(campaign.start_date).toLocaleDateString()}</span>
          <span>Ends: ${new Date(campaign.end_date).toLocaleDateString()}</span>
        </div>
      </div>
    </div>
  `}).join('');

  // Reinitialize icons
  lucide.createIcons();
}

// Create Campaign
async function createCampaign(formData) {
  try {
    const data = Object.fromEntries(formData);
    data.goal_amount = parseFloat(data.goal_amount);

    const response = await fetch(`${API_URL}/create_campaign`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to create campaign');
    }

    await fetchCampaigns();
    closeModal(createCampaignModal);
    showSuccess('Campaign created successfully');
  } catch (error) {
    console.error('Error creating campaign:', error);
    showError(error.message || 'Failed to create campaign');
  }
}

// Modal Functions
function openModal(modal) {
  modal.classList.add('active');
}

function closeModal(modal) {
  modal.classList.remove('active');
  const form = modal.querySelector('form');
  if (form) form.reset();
}

// Notifications
function showSuccess(message) {
  alert(message); // Replace with a better notification system
}

function showError(message) {
  alert(message); // Replace with a better notification system
}

// Event Listeners
createCampaignBtn.addEventListener('click', () => openModal(createCampaignModal));

closeBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const modal = btn.closest('.modal');
    closeModal(modal);
  });
});

campaignForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(campaignForm);
  await createCampaign(formData);
});

searchInput.addEventListener('input', filterAndDisplayCampaigns);
causeFilter.addEventListener('change', filterAndDisplayCampaigns);
statusFilter.addEventListener('change', filterAndDisplayCampaigns);

// Initialize
document.addEventListener('DOMContentLoaded', fetchCampaigns);