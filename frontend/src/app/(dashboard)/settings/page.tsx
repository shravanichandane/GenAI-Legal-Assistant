"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Settings, Shield, Key, Bell, Users, Database } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div className="max-w-5xl mx-auto pb-12">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-6 border-b border-slate-200 pb-8 mb-12">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
          <span className="text-xs font-bold uppercase tracking-[0.2em] text-amber-600 mb-3 block">Workspace</span>
          <h1 className="text-4xl md:text-5xl font-serif text-slate-950 tracking-tight">Settings</h1>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="flex items-center gap-4">
          <button className="px-8 py-3 bg-slate-950 text-white text-xs font-bold uppercase tracking-[0.15em] hover:bg-slate-800 transition-colors rounded-none">
            Save Changes
          </button>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        
        {/* Settings Navigation */}
        <div className="md:col-span-1 space-y-2">
          {[
            { icon: Settings, label: "General", active: true },
            { icon: Shield, label: "Security", active: false },
            { icon: Key, label: "API Keys", active: false },
            { icon: Users, label: "Team", active: false },
            { icon: Database, label: "Data Retention", active: false },
            { icon: Bell, label: "Notifications", active: false },
          ].map((item, idx) => (
            <button key={idx} className={`w-full flex items-center gap-3 px-4 py-3 text-left transition-colors border-l-2 ${
              item.active 
                ? "border-amber-600 bg-white text-slate-950 shadow-sm" 
                : "border-transparent text-slate-500 hover:bg-white hover:text-slate-800"
            }`}>
              <item.icon className={`w-4 h-4 ${item.active ? "text-amber-600" : "text-slate-400"}`} />
              <span className="text-xs font-bold uppercase tracking-[0.1em]">{item.label}</span>
            </button>
          ))}
        </div>

        {/* Settings Content */}
        <div className="md:col-span-3 space-y-8">
          
          <div className="bg-white border border-slate-200 p-8">
            <h3 className="text-xl font-serif text-slate-950 mb-6 pb-4 border-b border-slate-100">Profile Information</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-400 block">First Name</label>
                <input type="text" defaultValue="John" className="w-full bg-slate-50 border border-slate-200 px-4 py-3 text-slate-950 focus:outline-none focus:border-amber-600 transition-colors font-mono text-sm" />
              </div>
              <div className="space-y-2">
                <label className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-400 block">Last Name</label>
                <input type="text" defaultValue="Doe" className="w-full bg-slate-50 border border-slate-200 px-4 py-3 text-slate-950 focus:outline-none focus:border-amber-600 transition-colors font-mono text-sm" />
              </div>
              <div className="space-y-2 md:col-span-2">
                <label className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-400 block">Email Address</label>
                <input type="email" defaultValue="john@company.com" className="w-full bg-slate-50 border border-slate-200 px-4 py-3 text-slate-950 focus:outline-none focus:border-amber-600 transition-colors font-mono text-sm" />
              </div>
              <div className="space-y-2 md:col-span-2">
                <label className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-400 block">Role</label>
                <input type="text" defaultValue="Managing Partner" disabled className="w-full bg-slate-100 border border-slate-200 px-4 py-3 text-slate-500 font-mono text-sm cursor-not-allowed" />
              </div>
            </div>
          </div>

          <div className="bg-white border border-slate-200 p-8">
            <h3 className="text-xl font-serif text-slate-950 mb-6 pb-4 border-b border-slate-100">System Preferences</h3>
            
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-950">Strict Playbook Enforcement</h4>
                  <p className="text-xs text-slate-500 mt-1">Automatically flag low-risk deviations as critical.</p>
                </div>
                <button className="w-12 h-6 bg-slate-200 rounded-full relative transition-colors">
                  <div className="w-4 h-4 bg-white rounded-full absolute left-1 top-1 shadow-sm" />
                </button>
              </div>
              
              <div className="h-px bg-slate-100 w-full" />
              
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-950">Enable Cross-Encoder Reranking</h4>
                  <p className="text-xs text-slate-500 mt-1">Improves accuracy but adds ~150ms latency per query.</p>
                </div>
                <button className="w-12 h-6 bg-amber-600 rounded-full relative transition-colors">
                  <div className="w-4 h-4 bg-white rounded-full absolute right-1 top-1 shadow-sm" />
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
