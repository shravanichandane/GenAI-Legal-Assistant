"use client";

import React, { useState } from 'react';
import { Search, Filter, FileText, CheckCircle, AlertTriangle, Clock, MoreVertical, Plus } from 'lucide-react';
import Link from 'next/link';

// Mock Contract Data
const mockContracts = [
  { id: "1029", name: "Meridian SaaS Enterprise Agreement", vendor: "Meridian Tech", status: "Critical Risk", score: 72, date: "Oct 12, 2026", type: "SaaS" },
  { id: "1028", name: "Apex Vendor API License V2", vendor: "Apex Corp", status: "Approved", score: 12, date: "Oct 11, 2026", type: "Vendor" },
  { id: "1027", name: "GlobalTech Mutual NDA", vendor: "GlobalTech", status: "Pending Review", score: 45, date: "Oct 10, 2026", type: "NDA" },
  { id: "1026", name: "Horizon Cloud Infrastructure Services", vendor: "Horizon", status: "Warning", score: 58, date: "Oct 09, 2026", type: "Infrastructure" },
  { id: "1025", name: "Stark Industries Data Processing Addendum", vendor: "Stark Ind.", status: "Approved", score: 8, date: "Oct 08, 2026", type: "DPA" },
];

export default function ContractsRepository() {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredContracts = mockContracts.filter(c => 
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    c.vendor.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getStatusStyle = (status: string) => {
    switch(status) {
      case "Critical Risk": return "bg-rose-50 text-rose-700 border-rose-200";
      case "Warning": return "bg-amber-50 text-amber-700 border-amber-200";
      case "Approved": return "bg-emerald-50 text-emerald-700 border-emerald-200";
      default: return "bg-indigo-50 text-indigo-700 border-indigo-200";
    }
  };

  const getStatusIcon = (status: string) => {
    switch(status) {
      case "Critical Risk": return <AlertTriangle className="w-3.5 h-3.5 mr-1.5" />;
      case "Warning": return <AlertTriangle className="w-3.5 h-3.5 mr-1.5" />;
      case "Approved": return <CheckCircle className="w-3.5 h-3.5 mr-1.5" />;
      default: return <Clock className="w-3.5 h-3.5 mr-1.5" />;
    }
  };

  return (
    <div className="flex flex-col gap-8 p-8 min-h-screen bg-slate-50">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex flex-col gap-1">
          <h1 className="text-3xl font-extrabold tracking-tight text-indigo-950">Contract Repository</h1>
          <p className="text-slate-500 font-medium">Browse, filter, and manage all documents processed by the AI pipeline.</p>
        </div>
        <Link href="/contracts/upload" className="flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-lg font-medium transition-all shadow-sm shadow-indigo-200">
          <Plus className="w-5 h-5" />
          Upload New Contract
        </Link>
      </div>

      {/* Main Container */}
      <div className="flex flex-col rounded-2xl border border-slate-200/60 bg-white shadow-sm overflow-hidden">
        {/* Toolbar */}
        <div className="flex items-center justify-between p-5 border-b border-slate-100 bg-white">
          <div className="relative max-w-md w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search by contract name or vendor..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all text-slate-700"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-slate-600 bg-slate-50 border border-slate-200 rounded-lg hover:bg-slate-100 transition-colors">
            <Filter className="w-4 h-4" />
            Filter Status
          </button>
        </div>

        {/* Data Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 text-slate-500 text-xs uppercase tracking-wider font-semibold">
                <th className="px-6 py-4 border-b border-slate-100">Document Name</th>
                <th className="px-6 py-4 border-b border-slate-100">Counterparty</th>
                <th className="px-6 py-4 border-b border-slate-100">Type</th>
                <th className="px-6 py-4 border-b border-slate-100">AI Risk Score</th>
                <th className="px-6 py-4 border-b border-slate-100">Status</th>
                <th className="px-6 py-4 border-b border-slate-100">Date Uploaded</th>
                <th className="px-6 py-4 border-b border-slate-100 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {filteredContracts.map((contract) => (
                <tr key={contract.id} className="hover:bg-slate-50/80 transition-colors group cursor-pointer">
                  <td className="px-6 py-4">
                    <Link href={`/contracts/${contract.id}`} className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600 shrink-0">
                        <FileText className="w-4 h-4" />
                      </div>
                      <span className="font-semibold text-indigo-950 hover:text-indigo-600 transition-colors">{contract.name}</span>
                    </Link>
                  </td>
                  <td className="px-6 py-4 text-slate-600 font-medium">{contract.vendor}</td>
                  <td className="px-6 py-4 text-slate-500">{contract.type}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-16 bg-slate-100 rounded-full h-2 overflow-hidden">
                        <div 
                          className={`h-full rounded-full ${contract.score > 60 ? 'bg-rose-500' : contract.score > 30 ? 'bg-amber-400' : 'bg-emerald-500'}`} 
                          style={{ width: `${contract.score}%` }}
                        />
                      </div>
                      <span className="text-xs font-bold text-slate-700">{contract.score}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold border ${getStatusStyle(contract.status)}`}>
                      {getStatusIcon(contract.status)}
                      {contract.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-500">{contract.date}</td>
                  <td className="px-6 py-4 text-right">
                    <button className="p-1.5 text-slate-400 hover:text-indigo-600 rounded-md hover:bg-indigo-50 transition-colors opacity-0 group-hover:opacity-100">
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {/* Pagination mock */}
        <div className="flex items-center justify-between p-5 border-t border-slate-100 bg-slate-50/50">
          <span className="text-sm text-slate-500">Showing <span className="font-medium text-slate-700">1</span> to <span className="font-medium text-slate-700">{filteredContracts.length}</span> of <span className="font-medium text-slate-700">124</span> results</span>
          <div className="flex gap-1">
            <button className="px-3 py-1 text-sm border border-slate-200 text-slate-400 rounded-md cursor-not-allowed bg-white">Previous</button>
            <button className="px-3 py-1 text-sm border border-slate-200 text-slate-600 rounded-md hover:bg-slate-50 bg-white transition-colors">1</button>
            <button className="px-3 py-1 text-sm border border-slate-200 text-slate-600 rounded-md hover:bg-slate-50 bg-white transition-colors">2</button>
            <button className="px-3 py-1 text-sm border border-slate-200 text-slate-600 rounded-md hover:bg-slate-50 bg-white transition-colors">3</button>
            <span className="px-2 py-1 text-slate-400">...</span>
            <button className="px-3 py-1 text-sm border border-slate-200 text-slate-600 rounded-md hover:bg-slate-50 bg-white transition-colors">Next</button>
          </div>
        </div>
      </div>
    </div>
  );
}
