import React from 'react';
import { LayoutDashboard, Users, FileSpreadsheet, Calculator, PieChart } from 'lucide-react';
import Dashboard from './components/Dashboard';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

const navigation = [
  { name: 'Dashboard', icon: LayoutDashboard, href: '#' },
  { name: 'Campaigns', icon: Users, href: '#' },
  { name: 'Financial Reports', icon: FileSpreadsheet, href: '#' },
  { name: 'Tax Calculator', icon: Calculator, href: '#' },
  { name: 'Impact Analytics', icon: PieChart, href: '#' },
];

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="flex">
        <Sidebar navigation={navigation} />
        <main className="flex-1 p-8">
          <Dashboard />
        </main>
      </div>
    </div>
  );
}

export default App;