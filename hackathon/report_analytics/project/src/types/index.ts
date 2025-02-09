export interface Campaign {
  campaign_id: string;
  company_name: string;
  title: string;
  cause: string;
  goal_amount: number;
  amount_raised: number;
  start_date: string;
  end_date: string;
  status: 'Active' | 'Completed';
  description: string;
}

export interface Transaction {
  transaction_id: string;
  campaign_id: string;
  donor_name: string;
  amount: number;
  status: 'Completed' | 'Pending';
  timestamp: string;
}

export interface ImpactMetrics {
  ngo_name: string;
  funds_received: number;
  lives_impacted: number;
  resources_delivered: string[];
}