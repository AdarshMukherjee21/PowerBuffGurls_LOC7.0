import React, { useState } from 'react';
import { Heart } from 'lucide-react';

export default function Navbar() {
  const [isCreatingCampaign, setIsCreatingCampaign] = useState(false);

  const handleCreateCampaign = () => {
    setIsCreatingCampaign(true);
    // TODO: Open campaign creation modal/form
    console.log('Create campaign clicked');
  };

  return (
    <nav className="bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between items-center">
          <div className="flex items-center">
            <Heart className="h-8 w-8 text-rose-500" />
            <span className="ml-2 text-xl font-semibold text-gray-900">CSR Portal</span>
          </div>
          <div className="flex items-center space-x-4">
            <button 
              onClick={handleCreateCampaign}
              disabled={isCreatingCampaign}
              className="rounded-md bg-rose-500 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-rose-600 disabled:opacity-50"
            >
              Create Campaign
            </button>
            <img
              className="h-8 w-8 rounded-full cursor-pointer"
              src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
              alt="User"
              onClick={() => console.log('Profile clicked')}
            />
          </div>
        </div>
      </div>
    </nav>
  );
}