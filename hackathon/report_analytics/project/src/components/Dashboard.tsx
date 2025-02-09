import React, { useEffect, useState } from 'react';
import { ArrowUpRight, Users, IndianRupee, Target, Download } from 'lucide-react';
import { 
  fetchDashboardData, 
  fetchCampaigns, 
  exportPDF,
  createCampaign 
} from '../lib/api';
import type { Campaign } from '../types';

const stats = [
  { name: 'Total Campaigns', value: '0', icon: Target },
  { name: 'Total Donations', value: '₹0', icon: IndianRupee },
  { name: 'Lives Impacted', value: '0', icon: Users },
];

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState({
    total_campaigns: 0,
    total_funds_raised: 0,
    total_tax_savings: 0,
    lives_impacted: 0
  });
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setIsLoading(true);
        const [dashData, campaignsData] = await Promise.all([
          fetchDashboardData(),
          fetchCampaigns()
        ]);
        
        setDashboardData(dashData);
        setCampaigns(campaignsData);
        setError(null);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Dashboard loading error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  const handleExportPDF = async () => {
    try {
      await exportPDF();
    } catch (err) {
      console.error('PDF export error:', err);
      setError('Failed to export PDF');
    }
  };

  const handleCampaignClick = (campaign: Campaign) => {
    // TODO: Implement campaign details view
    console.log('Campaign clicked:', campaign);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-rose-500" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 px-4 py-2 bg-rose-500 text-white rounded-md hover:bg-rose-600"
        >
          Retry
        </button>
      </div>
    );
  }

  const updatedStats = [
    { 
      name: 'Total Campaigns', 
      value: dashboardData.total_campaigns.toString(), 
      icon: Target 
    },
    { 
      name: 'Total Donations', 
      value: `₹${(dashboardData.total_funds_raised / 100000).toFixed(1)}L`, 
      icon: IndianRupee 
    },
    { 
      name: 'Lives Impacted', 
      value: dashboardData.lives_impacted.toLocaleString(), 
      icon: Users 
    },
  ];

  return (
    <div className="md:ml-64">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <button
          onClick={handleExportPDF}
          className="flex items-center px-4 py-2 bg-rose-500 text-white rounded-md hover:bg-rose-600"
        >
          <Download className="h-4 w-4 mr-2" />
          Export Report
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {updatedStats.map((stat) => (
          <div
            key={stat.name}
            className="relative overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:px-6 sm:py-6"
          >
            <dt>
              <div className="absolute rounded-md bg-rose-500 p-3">
                <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">
                {stat.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline">
              <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
              <p className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                <ArrowUpRight 
                  className="h-5 w-5 flex-shrink-0 self-center text-green-500" 
                  aria-hidden="true" 
                />
                <span className="sr-only">Increased by</span>
                12%
              </p>
            </dd>
          </div>
        ))}
      </div>

      <div className="mt-8">
        <h2 className="text-lg font-medium text-gray-900">Active Campaigns</h2>
        <div className="mt-4 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {campaigns.map((campaign) => (
            <div
              key={campaign.campaign_id}
              className="relative overflow-hidden rounded-lg bg-white shadow cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => handleCampaignClick(campaign)}
            >
              <div className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <Target className="h-6 w-6 text-rose-500" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-medium text-gray-900">
                      {campaign.title}
                    </h3>
                    <p className="text-sm text-gray-500">{campaign.company_name}</p>
                  </div>
                </div>
                <div className="mt-4">
                  <div className="relative pt-1">
                    <div className="overflow-hidden h-2 text-xs flex rounded bg-rose-100">
                      <div
                        style={{
                          width: `${(campaign.amount_raised / campaign.goal_amount) * 100}%`,
                        }}
                        className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-rose-500"
                      />
                    </div>
                  </div>
                  <div className="mt-2 flex justify-between text-sm text-gray-600">
                    <span>₹{(campaign.amount_raised / 100000).toFixed(1)}L raised</span>
                    <span>₹{(campaign.goal_amount / 100000).toFixed(1)}L goal</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}