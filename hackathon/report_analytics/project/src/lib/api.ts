import axios from 'axios';
import type { Campaign, Transaction, ImpactMetrics } from '../types';

const API_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Dashboard
export async function fetchDashboardData() {
  const response = await api.get('/dashboard');
  return response.data;
}

// Campaigns
export async function fetchCampaigns() {
  const response = await api.get('/campaigns');
  return response.data;
}

export async function createCampaign(campaignData: {
  company_name: string;
  title: string;
  cause: string;
  goal_amount: number;
  start_date: string;
  end_date: string;
  description: string;
}) {
  const response = await api.post('/create_campaign', campaignData);
  return response.data;
}

// Financial Reports
export async function fetchFinancialReports() {
  const response = await api.get('/financial_reports');
  return response.data;
}

// Tax Calculator
export async function calculateTax() {
  const response = await api.get('/calculate_tax');
  return response.data;
}

// Impact Analytics
export async function fetchImpactAnalytics() {
  const response = await api.get('/impact_analytics');
  return response.data;
}

// Export PDF
export async function exportPDF() {
  const response = await api.get('/export_pdf', { responseType: 'blob' });
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'csr_report.pdf');
  document.body.appendChild(link);
  link.click();
  link.remove();
}

// Companies
export async function fetchCompanies() {
  const response = await api.get('/companies');
  return response.data;
}

export async function loginCompany(email: string, password: string) {
  const response = await api.post('/companies/login', { email, password });
  return response.data;
}

// NGOs
export async function fetchNGOs() {
  const response = await api.get('/ngos');
  return response.data;
}

export async function loginNGO(email: string, password: string) {
  const response = await api.post('/ngos/login', { email, password });
  return response.data;
}

export async function getMatchingNGOs(companyName: string) {
  const response = await api.get(`/match/${companyName}`);
  return response.data;
}