"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, ShieldAlert, Scale, CheckCircle2, ChevronRight, FileJson, ArrowRight, Settings2, Code2, Users, ArrowDownRight } from 'lucide-react';

// Playbook Data
const DEMO_PLAYBOOKS = [
  {
    id: "pb-01",
    title: "Master Services Agreement (MSA)",
    department: "Enterprise Sales",
    rules: 42,
    strictness: "High",
    lastUpdated: "2 days ago",
    active: true
  },
  {
    id: "pb-02",
    title: "Vendor NDA (Standard)",
    department: "Procurement",
    rules: 15,
    strictness: "Medium",
    lastUpdated: "1 week ago",
    active: true
  },
  {
    id: "pb-03",
    title: "Employment Contract v4",
    department: "Human Resources",
    rules: 28,
    strictness: "Critical",
    lastUpdated: "3 weeks ago",
    active: true
  }
];

const LIVE_PLAYBOOKS = [
  {
    id: "pb-live-01",
    title: "Corporate Indemnification Standards",
    department: "Legal & Compliance",
    rules: 1,
    strictness: "Critical",
    lastUpdated: "Just now",
    active: true
  }
];

export default function PlaybooksPage() {
  const [appMode, setAppMode] = useState('demo');
  const [selectedPlaybook, setSelectedPlaybook] = useState<any>(DEMO_PLAYBOOKS[0]);

  useEffect(() => {
    const mode = localStorage.getItem('app_mode');
    if (mode === 'empty') {
      setAppMode('empty');
      setSelectedPlaybook(null);
    } else if (mode === 'live') {
      setAppMode('live');
      setSelectedPlaybook(LIVE_PLAYBOOKS[0]);
    } else {
      setAppMode('demo');
      setSelectedPlaybook(DEMO_PLAYBOOKS[0]);
    }
  }, []);

  const currentPlaybooks = appMode === 'demo' ? DEMO_PLAYBOOKS : appMode === 'live' ? LIVE_PLAYBOOKS : [];
  const hasData = appMode !== 'empty';

  return (
    <div className="max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-6 border-b border-slate-200 pb-6 mb-10">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <h1 className="text-4xl font-serif text-slate-950 tracking-tight">Legal Playbooks</h1>
          <p className="text-slate-500 text-sm mt-2 font-medium">Deterministic rules engines that govern the AI risk scoring.</p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-3"
        >
          <button className="px-6 py-2.5 bg-slate-950 text-white text-sm font-bold uppercase tracking-wider hover:bg-slate-800 transition-colors flex items-center gap-2 rounded-none">
            <BookOpen className="w-4 h-4" />
            Create Playbook
          </button>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Playbook List */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="lg:col-span-5 flex flex-col gap-4 relative"
        >
          <div className="bg-white border border-slate-200 rounded-none shadow-sm overflow-hidden flex-1">
            <div className="px-6 py-4 bg-slate-50 border-b border-slate-200">
              <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Active Repositories</h3>
            </div>
            {!hasData && (
              <div className="p-12 text-center text-slate-500 flex flex-col items-center">
                <BookOpen className="w-8 h-8 text-slate-300 mb-4" />
                <p className="text-sm font-mono uppercase tracking-widest">No playbooks found</p>
                <p className="text-xs mt-2">Initialize your first playbook to start automated reviews.</p>
              </div>
            )}
            <div className="divide-y divide-slate-100">
              {currentPlaybooks.map((pb) => (
                <button 
                  key={pb.id}
                  onClick={() => setSelectedPlaybook(pb)}
                  className={`w-full text-left p-6 transition-colors flex items-center justify-between group ${
                    selectedPlaybook?.id === pb.id ? "bg-slate-950" : "hover:bg-slate-50"
                  }`}
                >
                  <div>
                    <h4 className={`text-lg font-serif mb-1 ${
                      selectedPlaybook?.id === pb.id ? "text-white" : "text-slate-950"
                    }`}>{pb.title}</h4>
                    <div className="flex items-center gap-3">
                      <span className={`text-xs font-mono tracking-widest uppercase ${
                        selectedPlaybook?.id === pb.id ? "text-slate-400" : "text-slate-500"
                      }`}>{pb.department}</span>
                      <span className={`text-xs px-2 py-0.5 border ${
                        selectedPlaybook?.id === pb.id ? "border-slate-800 text-slate-400" : "border-slate-200 text-slate-500"
                      }`}>{pb.rules} Rules</span>
                    </div>
                  </div>
                  <ChevronRight className={`w-5 h-5 transition-transform ${
                    selectedPlaybook?.id === pb.id ? "text-white translate-x-1" : "text-slate-300 group-hover:text-slate-600"
                  }`} />
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Right Column: Rule Extraction Visualizer */}
        <motion.div 
          key={selectedPlaybook?.id || 'empty'}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="lg:col-span-7"
        >
          {selectedPlaybook ? (
            <div className="bg-white border border-slate-200 shadow-sm rounded-none h-full flex flex-col">
              <div className="p-8 border-b border-slate-200 flex items-start justify-between bg-slate-50">
                <div>
                  <h2 className="text-2xl font-serif text-slate-950 mb-2">{selectedPlaybook.title}</h2>
                  <div className="flex items-center gap-4 text-sm font-medium text-slate-500">
                    <span className="flex items-center gap-1.5"><ShieldAlert className="w-4 h-4 text-rose-500"/> {selectedPlaybook.strictness} Strictness</span>
                    <span className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-emerald-500"/> Active Enforcement</span>
                  </div>
                </div>
                <button className="p-2 border border-slate-200 text-slate-600 hover:bg-white hover:text-slate-950 transition-colors">
                  <Settings2 className="w-5 h-5" />
                </button>
              </div>

              <div className="p-8 flex-1">
                <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-6 flex items-center gap-2">
                  <Code2 className="w-4 h-4"/> AI Rule Extraction Engine
                </h3>

                {/* Translation Visualization */}
                <div className="relative">
                  {/* Human Plain Text Rule */}
                  <div className="bg-slate-50 border border-slate-200 p-6 mb-8 relative z-10 shadow-sm">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs font-bold uppercase tracking-widest text-slate-500">Human Instruction (Natural Language)</span>
                      <span className="text-xs font-mono text-slate-400">Rule_ID: {appMode === 'live' ? '82' : '104'}</span>
                    </div>
                    <p className="text-lg font-serif text-slate-900 leading-relaxed border-l-2 border-indigo-600 pl-4">
                      {appMode === 'live' 
                        ? '"We will not accept aggregate liability greater than $50,000 USD or the total fees paid in the preceding 3 months under any indemnification provision."'
                        : '"Under no circumstances should we accept uncapped liability. The absolute maximum liability cap we can accept in this agreement is 12 months of paid fees. Anything else is a critical violation."'}
                    </p>
                  </div>

                  {/* Arrow Connector */}
                  <div className="absolute left-8 top-[120px] bottom-[100px] w-px bg-indigo-200 z-0">
                    <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-6 h-6 bg-white border border-indigo-200 rounded-full flex items-center justify-center">
                      <ArrowDownRight className="w-3 h-3 text-indigo-600" />
                    </div>
                  </div>

                  {/* AI JSON Rule */}
                  <div className="bg-slate-950 border border-slate-800 p-6 relative z-10 shadow-xl ml-4">
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-xs font-bold uppercase tracking-widest text-slate-400">Machine Translation (JSON Logic)</span>
                      <FileJson className="w-4 h-4 text-emerald-400" />
                    </div>
                    <pre className="text-sm font-mono text-emerald-400 overflow-x-auto">
{appMode === 'live' ? `{
  "clause_target": "Indemnification",
  "enforcement_level": "CRITICAL",
  "conditions": {
    "aggregate_liability_max_usd": 50000,
    "alternative_max_months": 3
  },
  "deterministic_penalty": 50.0,
  "fallback_resolution": "Reject and enforce $50k or 3-month fee cap."
}` : `{
  "clause_target": "Liability",
  "enforcement_level": "CRITICAL",
  "conditions": {
    "has_cap": true,
    "cap_value_max_months": 12,
    "uncapped_allowed": false
  },
  "deterministic_penalty": 40.0,
  "fallback_resolution": "Reject and redline cap to 12 months."
}`}
                    </pre>
                  </div>
                </div>

              </div>
            </div>
          ) : (
            <div className="bg-slate-50 border border-slate-200 shadow-sm rounded-none h-full flex flex-col items-center justify-center p-12 text-center min-h-[400px]">
              <FileJson className="w-12 h-12 text-slate-300 mb-6" />
              <h3 className="text-xl font-serif text-slate-950 mb-2">Rule Engine Inactive</h3>
              <p className="text-slate-500 max-w-sm">No playbooks selected. Upload a contract or create a playbook to view the deterministic AI extraction logic.</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
