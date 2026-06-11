"use client";

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, TrendingDown, Scale, ShieldAlert, FileText, CheckCircle2 } from 'lucide-react';

export default function AnalyticsPage() {
  const [appMode, setAppMode] = useState('demo');

  useEffect(() => {
    const mode = localStorage.getItem('app_mode');
    if (mode) {
      setAppMode(mode);
    }
  }, []);

  const mockHeights = [40, 65, 80, 55, 90, 75, 100, 85, 120, 95, 110, 130];
  const liveHeights = [0, 0, 0, 0, 0, 1]; // Just 1 doc in June (current month)
  
  const heights = appMode === 'demo' ? mockHeights : appMode === 'live' ? [...new Array(11).fill(0), 1] : new Array(12).fill(0);
  const hasData = appMode !== 'empty';

  return (
    <div className="max-w-7xl mx-auto pb-12">
      {/* Envato Luxury Legal Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-6 border-b border-slate-200 pb-8 mb-12">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <span className="text-xs font-bold uppercase tracking-[0.2em] text-amber-600 mb-3 block">Firm Intelligence</span>
          <h1 className="text-4xl md:text-5xl font-serif text-slate-950 tracking-tight">Analytics & Insights</h1>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-4"
        >
          <button className="px-8 py-3 bg-white border border-slate-200 text-slate-950 text-xs font-bold uppercase tracking-[0.15em] hover:bg-slate-50 hover:border-amber-600 transition-colors rounded-none">
            Export Report
          </button>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        
        {/* Metric 1 */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white border border-slate-200 p-8 rounded-none hover:border-amber-600 transition-colors group relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-24 h-24 bg-slate-50 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none group-hover:bg-amber-600/10 transition-colors duration-500" />
          <div className="flex justify-between items-start mb-12">
            <h3 className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">Total Liability Exposure</h3>
            <Scale className="w-5 h-5 text-amber-600" />
          </div>
          <div>
            <p className="text-5xl font-serif text-slate-950 tracking-tight mb-2">
              {appMode === 'demo' ? '$42.5M' : appMode === 'live' ? '$50,000' : '$0'}
            </p>
            <div className="flex items-center gap-2 text-sm">
              <TrendingDown className="w-4 h-4 text-emerald-600" />
              <span className="font-semibold text-emerald-700">
                {appMode === 'demo' ? '-14% vs Last Quarter' : appMode === 'live' ? 'Baseline Identified' : 'No previous data'}
              </span>
            </div>
          </div>
        </motion.div>

        {/* Metric 2 */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-slate-950 p-8 rounded-none border border-slate-950 group relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none group-hover:bg-amber-600/20 transition-colors duration-500" />
          <div className="flex justify-between items-start mb-12 relative z-10">
            <h3 className="text-xs font-bold uppercase tracking-[0.15em] text-amber-600">Contracts Analyzed</h3>
            <FileText className="w-5 h-5 text-white" />
          </div>
          <div className="relative z-10">
            <p className="text-5xl font-serif text-white tracking-tight mb-2">
              {appMode === 'demo' ? '1,248' : appMode === 'live' ? '1' : '0'}
            </p>
            <div className="flex items-center gap-2 text-sm">
              <TrendingUp className="w-4 h-4 text-amber-600" />
              <span className="font-medium text-slate-300">
                {appMode === 'demo' ? 'Target Exceeded' : appMode === 'live' ? 'First Analysis' : 'Awaiting processing'}
              </span>
            </div>
          </div>
        </motion.div>

        {/* Metric 3 */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white border border-slate-200 p-8 rounded-none hover:border-amber-600 transition-colors group relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-24 h-24 bg-slate-50 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none group-hover:bg-amber-600/10 transition-colors duration-500" />
          <div className="flex justify-between items-start mb-12">
            <h3 className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">Critical Violations</h3>
            <ShieldAlert className="w-5 h-5 text-rose-500" />
          </div>
          <div>
            <p className="text-5xl font-serif text-slate-950 tracking-tight mb-2">
              {appMode === 'demo' ? '42' : appMode === 'live' ? '2' : '0'}
            </p>
            <div className="flex items-center gap-2 text-sm">
              <TrendingUp className="w-4 h-4 text-rose-600" />
              <span className="font-semibold text-rose-700">
                {appMode === 'demo' ? '+3 Needs Immediate Review' : appMode === 'live' ? 'Active Deviations' : '0 pending review'}
              </span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Large Chart Area Mockup */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white border border-slate-200 rounded-none p-10 h-auto relative"
      >
        {!hasData && (
          <div className="absolute inset-0 bg-white/80 backdrop-blur-[2px] z-20 flex items-center justify-center border border-slate-200">
            <p className="text-sm font-mono text-slate-500 uppercase tracking-widest bg-white py-2 px-6 border border-slate-200 shadow-sm">Waiting for Intelligence Pipeline</p>
          </div>
        )}

        <div className="flex justify-between items-center border-b border-slate-100 pb-6 mb-8">
          <div>
            <h3 className="text-2xl font-serif text-slate-950">Risk Detection Velocity</h3>
            <p className="text-sm text-slate-500 mt-1">AI throughput vs Human reviewer bandwidth</p>
          </div>
          <div className="flex gap-2">
            <button className="px-4 py-2 bg-slate-100 text-xs font-bold uppercase tracking-widest text-slate-500">Weekly</button>
            <button className="px-4 py-2 bg-slate-950 text-xs font-bold uppercase tracking-widest text-white">Monthly</button>
          </div>
        </div>

        {/* Abstract Visualization using Tailwind */}
        <div className="h-64 flex items-end justify-between gap-2 px-4 mt-8 border-b border-slate-200 pb-1 relative">
          {/* Mock Y-Axis lines */}
          <div className="absolute left-0 right-0 top-0 border-t border-slate-100 border-dashed w-full" />
          <div className="absolute left-0 right-0 top-1/2 border-t border-slate-100 border-dashed w-full" />
          
          {heights.map((height, i) => (
            <div key={i} className="w-full flex justify-center group relative z-10">
              {/* Tooltip on hover */}
              <div className="absolute -top-10 opacity-0 group-hover:opacity-100 transition-opacity bg-slate-950 text-white text-xs px-2 py-1 rounded">
                {appMode === 'demo' ? height * 10 : height} docs
              </div>
              <motion.div 
                initial={{ height: 0 }}
                animate={{ height: `${(height / 130) * 100}%` }}
                transition={{ duration: 1, delay: 0.5 + (i * 0.05), ease: "circOut" }}
                className="w-full max-w-[2rem] bg-slate-200 group-hover:bg-amber-600 transition-colors"
              />
            </div>
          ))}
        </div>
        <div className="flex justify-between px-6 mt-4 text-xs font-mono text-slate-400">
          <span>Jan</span>
          <span>Feb</span>
          <span>Mar</span>
          <span>Apr</span>
          <span>May</span>
          <span>Jun</span>
          <span>Jul</span>
          <span>Aug</span>
          <span>Sep</span>
          <span>Oct</span>
          <span>Nov</span>
          <span>Dec</span>
        </div>
      </motion.div>

    </div>
  );
}
