"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { WelcomePopup } from "@/components/WelcomePopup";
import { 
  FileText, 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  ArrowUpRight, 
  ArrowDownRight,
  MoreVertical,
  Download,
  Eye,
  Scale
} from "lucide-react";

// Premium StatCard Component
const StatCard = ({ 
  title, 
  value, 
  change, 
  trend, 
  icon: Icon, 
  delay 
}: { 
  title: string; 
  value: string; 
  change: string; 
  trend: 'up' | 'down' | 'neutral'; 
  icon: React.ElementType; 
  delay: number 
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay, ease: "easeOut" }}
      className="bg-white p-6 border border-slate-200 shadow-sm hover:shadow-lg transition-all duration-300 group rounded-none"
    >
      <div className="flex justify-between items-start mb-6">
        <div className="p-2 border border-slate-100 bg-slate-50 group-hover:bg-slate-900 group-hover:border-slate-900 transition-colors">
          <Icon className="w-5 h-5 text-slate-700 group-hover:text-white transition-colors" strokeWidth={1.5} />
        </div>
        <div className={`flex items-center gap-1 text-xs font-bold px-2 py-1 uppercase tracking-wider ${
          trend === 'up' ? 'text-emerald-700 bg-emerald-50' : 
          trend === 'down' ? 'text-rose-700 bg-rose-50' : 
          'text-slate-600 bg-slate-100'
        }`}>
          {trend === 'up' && <ArrowUpRight className="w-3 h-3" />}
          {trend === 'down' && <ArrowDownRight className="w-3 h-3" />}
          {change}
        </div>
      </div>
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">{title}</p>
        <h3 className="text-4xl font-serif text-slate-950 tracking-tight">{value}</h3>
      </div>
    </motion.div>
  );
};

// Premium RecentActivityTable Component
const RecentActivityTable = ({ appMode }: { appMode: string }) => {
  let activities: any[] = [];
  
  if (appMode === 'demo') {
    activities = [
      { id: 1, name: "Acme Corp NDA.pdf", type: "NDA", status: "Review", date: "Today, 2:30 PM", risk: "Low" },
      { id: 2, name: "GlobalTech MSA - Draft v2.docx", type: "MSA", status: "Approved", date: "Today, 11:15 AM", risk: "Medium" },
      { id: 3, name: "Stark Industries Vendor Agreement", type: "Vendor", status: "Pending", date: "Yesterday", risk: "High" },
      { id: 4, name: "Wayne Ent Employment Contract", type: "HR", status: "Review", date: "Yesterday", risk: "Low" },
    ];
  } else if (appMode === 'live') {
    // Show the newly uploaded contract as the only activity
    activities = [
      { id: 999, name: "Uploaded_Contract.txt", type: "Custom", status: "Review", date: "Just now", risk: "High" }
    ];
  }

  const hasData = appMode !== 'empty';

  return (
    <div className="bg-white border border-slate-200 shadow-sm flex flex-col h-full rounded-none">
      <div className="p-8 border-b border-slate-200 flex justify-between items-center bg-slate-50/50">
        <div>
          <h3 className="text-xl font-serif text-slate-950">Recent Activity</h3>
          <p className="text-sm text-slate-500 mt-1">Contracts awaiting your attention</p>
        </div>
        <button className="text-sm font-semibold text-slate-950 hover:text-indigo-700 uppercase tracking-wider transition-colors border-b border-transparent hover:border-indigo-700">
          View Ledger
        </button>
      </div>
      <div className="flex-1 overflow-auto relative">
        {!hasData && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-white z-10 text-center p-8">
            <FileText className="w-12 h-12 text-slate-200 mb-4" />
            <h4 className="text-lg font-serif text-slate-950 mb-2">No Contracts Processed</h4>
            <p className="text-sm text-slate-500 mb-6 max-w-sm">Upload your first contract to initialize the intelligence pipeline and populate the ledger.</p>
            <Link href="/contracts/upload" className="px-6 py-2 border border-amber-600 text-amber-700 hover:bg-amber-50 text-xs font-bold uppercase tracking-widest transition-colors">
              Upload Document
            </Link>
          </div>
        )}
        <table className="w-full text-left border-collapse">
          <thead>
            <tr>
              <th className="px-8 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-200">Document</th>
              <th className="px-8 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-200 hidden sm:table-cell">Type</th>
              <th className="px-8 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-200">Status</th>
              <th className="px-8 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-200 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {activities.map((activity) => (
              <tr key={activity.id} className="hover:bg-slate-50 transition-colors group">
                <td className="px-8 py-5">
                  <div className="flex items-center gap-4">
                    <div className="p-2 bg-slate-100 text-slate-500">
                      <FileText className="w-4 h-4" />
                    </div>
                    <span className="font-medium text-slate-950">{activity.name}</span>
                  </div>
                </td>
                <td className="px-8 py-5 hidden sm:table-cell">
                  <span className="text-sm font-mono text-slate-500">{activity.type}</span>
                </td>
                <td className="px-8 py-5">
                  <div className="flex items-center gap-2 text-sm">
                    {activity.status === 'Approved' && <CheckCircle2 className="w-4 h-4 text-emerald-600" />}
                    {activity.status === 'Review' && <Clock className="w-4 h-4 text-amber-600" />}
                    {activity.status === 'Pending' && <AlertTriangle className="w-4 h-4 text-slate-400" />}
                    <span className={`font-medium ${
                      activity.status === 'Approved' ? 'text-emerald-700' :
                      activity.status === 'Review' ? 'text-amber-700' :
                      'text-slate-600'
                    }`}>{activity.status}</span>
                  </div>
                </td>
                <td className="px-8 py-5 text-right">
                  <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Link href={`/contracts/${activity.id}`} className="p-2 text-slate-400 hover:text-white hover:bg-slate-900 transition-colors">
                      <Eye className="w-4 h-4" />
                    </Link>
                    <button className="p-2 text-slate-400 hover:text-slate-900 hover:bg-slate-100 transition-colors">
                      <Download className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Premium RiskDistribution Chart Mockup
const RiskDistribution = ({ appMode }: { appMode: string }) => {
  const hasData = appMode !== 'empty';
  
  // Custom widths based on mode
  const standardWidth = appMode === 'demo' ? "65%" : appMode === 'live' ? "10%" : "0%";
  const deviationsWidth = appMode === 'demo' ? "25%" : appMode === 'live' ? "30%" : "0%";
  const criticalWidth = appMode === 'demo' ? "10%" : appMode === 'live' ? "60%" : "0%";
  const exposureScore = appMode === 'demo' ? '8.4' : appMode === 'live' ? '9.8' : '0.0';
  const exposureTrend = appMode === 'demo' ? '+1.2 v. Prev Quarter' : appMode === 'live' ? 'New baseline set' : 'No prior data';

  return (
    <div className="bg-slate-950 border border-slate-800 p-8 text-white h-full relative flex flex-col justify-between rounded-none shadow-2xl overflow-hidden">
      {!hasData && (
        <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm z-10 flex flex-col items-center justify-center p-8 text-center border border-slate-800">
          <Scale className="w-10 h-10 text-slate-700 mb-4" />
          <p className="text-sm font-mono text-slate-500 uppercase tracking-widest">Awaiting Data</p>
        </div>
      )}
      <div>
        <div className="flex items-center gap-3 mb-8">
          <Scale className="w-5 h-5 text-slate-400" />
          <h3 className="text-xl font-serif tracking-wide text-white">Portfolio Risk Analysis</h3>
        </div>
        
        <div className="space-y-6">
          <div className="space-y-2">
            <div className="flex justify-between text-xs font-mono tracking-widest text-slate-400 uppercase">
              <span>Standard (Low Risk)</span>
              <span className="text-white">{standardWidth}</span>
            </div>
            <div className="h-1 bg-slate-800 w-full">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: standardWidth }}
                transition={{ duration: 1, delay: 0.5, ease: "circOut" }}
                className="h-full bg-white"
              />
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-xs font-mono tracking-widest text-slate-400 uppercase">
              <span>Deviations (Medium)</span>
              <span className="text-slate-300">{deviationsWidth}</span>
            </div>
            <div className="h-1 bg-slate-800 w-full">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: deviationsWidth }}
                transition={{ duration: 1, delay: 0.7, ease: "circOut" }}
                className="h-full bg-slate-400"
              />
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-xs font-mono tracking-widest text-slate-400 uppercase">
              <span>Critical (High Risk)</span>
              <span className="text-rose-400">{criticalWidth}</span>
            </div>
            <div className="h-1 bg-slate-800 w-full">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: criticalWidth }}
                transition={{ duration: 1, delay: 0.9, ease: "circOut" }}
                className="h-full bg-rose-500"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="mt-10 pt-8 border-t border-slate-800 flex items-end justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-1">Portfolio Exposure</p>
          <p className="text-5xl font-serif text-white tracking-tight">{exposureScore}<span className="text-2xl text-slate-500 font-sans">/10</span></p>
        </div>
        <div className="text-right">
          <p className="text-sm font-mono text-slate-500">{exposureTrend}</p>
        </div>
      </div>
    </div>
  );
};

export default function DashboardHomePage() {
  const [appMode, setAppMode] = useState('demo');
  
  useEffect(() => {
    const mode = localStorage.getItem('app_mode');
    if (mode) {
      setAppMode(mode);
    }
  }, []);

  return (
    <div className="max-w-7xl mx-auto space-y-10 pb-12">
      <WelcomePopup />
      
      {/* Premium Header section */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-6 border-b border-slate-200 pb-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl font-serif text-slate-950 tracking-tight">Executive Dashboard</h1>
          <p className="text-slate-500 text-sm mt-2 font-medium">Systemic risk overview and active review queue.</p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="flex items-center gap-3"
        >
          <button className="px-6 py-2.5 bg-white border border-slate-200 text-slate-950 text-sm font-bold uppercase tracking-wider hover:bg-slate-50 transition-colors rounded-none">
            Generate Report
          </button>
          <Link href="/contracts/upload" className="px-6 py-2.5 bg-slate-950 text-white text-sm font-bold uppercase tracking-wider hover:bg-slate-800 transition-colors flex items-center gap-2 rounded-none">
            <FileText className="w-4 h-4" />
            New Analysis
          </Link>
        </motion.div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Total Contracts" 
          value={appMode === 'demo' ? "1,248" : appMode === 'live' ? "1" : "0"} 
          change={appMode === 'demo' ? "+12%" : "0%"} 
          trend={appMode === 'demo' ? "up" : "neutral"} 
          icon={FileText} 
          delay={0.1} 
        />
        <StatCard 
          title="Pending Review" 
          value={appMode === 'demo' ? "42" : appMode === 'live' ? "1" : "0"} 
          change={appMode === 'demo' ? "-5%" : "0%"} 
          trend={appMode === 'demo' ? "down" : "neutral"} 
          icon={Clock} 
          delay={0.2} 
        />
        <StatCard 
          title="Critical Alerts" 
          value={appMode === 'demo' ? "3" : appMode === 'live' ? "2" : "0"} 
          change="0%" 
          trend={appMode === 'live' ? "up" : "neutral"} 
          icon={AlertTriangle} 
          delay={0.3} 
        />
        <StatCard 
          title="Processed Today" 
          value={appMode === 'demo' ? "156" : appMode === 'live' ? "1" : "0"} 
          change={appMode === 'demo' ? "+24%" : "0%"} 
          trend={appMode === 'demo' ? "up" : "neutral"} 
          icon={CheckCircle2} 
          delay={0.4} 
        />
      </div>

      {/* Bento Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-auto lg:h-[450px]">
        {/* Recent Activity takes up 2 columns */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="lg:col-span-2 h-full"
        >
          <RecentActivityTable appMode={appMode} />
        </motion.div>
        
        {/* Risk Distribution takes 1 column */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="h-full"
        >
          <RiskDistribution appMode={appMode} />
        </motion.div>
      </div>

    </div>
  );
}
