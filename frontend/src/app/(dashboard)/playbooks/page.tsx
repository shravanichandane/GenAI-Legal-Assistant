"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, ShieldAlert, CheckCircle2, FileJson, Settings2, Code2, ArrowDownRight, Plus, X, Trash2 } from 'lucide-react';

export default function PlaybooksPage() {
  const [rules, setRules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newRule, setNewRule] = useState({ clause_type: '', rule_description: '', is_mandatory: true });
  
  const fetchRules = async () => {
    setLoading(true);
    try {
      const { api } = await import("@/lib/api");
      const data = await api.getPlaybookRules();
      setRules(data);
    } catch (e) {
      console.error("Failed to fetch rules", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRules();
  }, []);

  const handleCreateRule = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { api } = await import("@/lib/api");
      await api.createPlaybookRule(newRule);
      setIsModalOpen(false);
      setNewRule({ clause_type: '', rule_description: '', is_mandatory: true });
      fetchRules();
    } catch (e) {
      console.error("Failed to create rule", e);
    }
  };

  const handleDeleteRule = async (id: string) => {
    if (!confirm("Are you sure you want to delete this rule?")) return;
    try {
      const { api } = await import("@/lib/api");
      await api.deletePlaybookRule(id);
      fetchRules();
    } catch (e) {
      console.error("Failed to delete rule", e);
    }
  };

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
          <button 
            onClick={() => setIsModalOpen(true)}
            className="px-6 py-2.5 bg-slate-950 text-white text-sm font-bold uppercase tracking-wider hover:bg-slate-800 transition-colors flex items-center gap-2 rounded-none"
          >
            <Plus className="w-4 h-4" />
            Create Rule
          </button>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 gap-8">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="flex flex-col gap-4 relative"
        >
          <div className="bg-white border border-slate-200 rounded-none shadow-sm overflow-hidden flex-1">
            <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
              <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Active Organization Policies</h3>
              <span className="text-xs font-mono text-slate-400">{rules.length} Active Rules</span>
            </div>
            
            {loading ? (
              <div className="p-12 text-center text-slate-500">Loading playbook rules...</div>
            ) : rules.length === 0 ? (
              <div className="p-12 text-center text-slate-500 flex flex-col items-center">
                <BookOpen className="w-8 h-8 text-slate-300 mb-4" />
                <p className="text-sm font-mono uppercase tracking-widest">No policies found</p>
                <p className="text-xs mt-2">Initialize your first playbook rule to instruct the AI.</p>
                <button 
                  onClick={() => setIsModalOpen(true)}
                  className="mt-6 px-6 py-2 border border-slate-300 text-slate-600 text-xs font-bold uppercase tracking-wider hover:bg-slate-50 transition-colors"
                >
                  Create Policy
                </button>
              </div>
            ) : (
              <div className="divide-y divide-slate-100">
                {rules.map((rule) => (
                  <div key={rule.id} className="w-full text-left p-6 transition-colors group hover:bg-slate-50">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-[10px] font-bold uppercase tracking-[0.2em] bg-slate-900 text-white px-2 py-1">
                            {rule.clause_type}
                          </span>
                          {rule.is_mandatory && (
                            <span className="flex items-center gap-1 text-[10px] font-bold uppercase tracking-widest text-rose-600 border border-rose-200 bg-rose-50 px-2 py-1">
                              <ShieldAlert className="w-3 h-3" /> Mandatory
                            </span>
                          )}
                        </div>
                      </div>
                      <button 
                        onClick={() => handleDeleteRule(rule.id)}
                        className="text-slate-300 hover:text-rose-600 transition-colors p-2"
                        title="Delete Rule"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    
                    <div className="bg-slate-50 border-l-2 border-indigo-600 p-4">
                      <p className="text-lg font-serif text-slate-900 leading-relaxed">
                        "{rule.rule_description}"
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </motion.div>
      </div>

      {/* Create Rule Modal */}
      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white border border-slate-200 shadow-2xl w-full max-w-2xl overflow-hidden rounded-none flex flex-col"
            >
              <div className="p-6 border-b border-slate-200 flex justify-between items-center bg-slate-50">
                <h2 className="text-xl font-serif text-slate-900">Define New Policy</h2>
                <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                  <X className="w-5 h-5" />
                </button>
              </div>
              
              <form onSubmit={handleCreateRule} className="p-6 flex flex-col gap-6">
                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500 mb-2">
                    Clause Target
                  </label>
                  <input 
                    type="text" 
                    required
                    placeholder="e.g. Liability, Termination, Indemnification"
                    className="w-full border border-slate-200 p-3 text-sm font-medium text-slate-900 focus:outline-none focus:border-amber-600 focus:ring-1 focus:ring-amber-600 transition-all"
                    value={newRule.clause_type}
                    onChange={e => setNewRule({...newRule, clause_type: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500 mb-2">
                    Policy Instruction (Natural Language)
                  </label>
                  <textarea 
                    required
                    rows={4}
                    placeholder="e.g. Under no circumstances should we accept uncapped liability. The absolute maximum liability cap we can accept is $50,000."
                    className="w-full border border-slate-200 p-3 text-sm font-serif text-slate-900 focus:outline-none focus:border-amber-600 focus:ring-1 focus:ring-amber-600 transition-all resize-none"
                    value={newRule.rule_description}
                    onChange={e => setNewRule({...newRule, rule_description: e.target.value})}
                  />
                  <p className="text-xs text-slate-400 mt-2">This instruction will be deterministically injected into the AI reasoning engine.</p>
                </div>
                
                <label className="flex items-center gap-3 cursor-pointer group">
                  <div className="relative flex items-center justify-center w-5 h-5 border border-slate-300 group-hover:border-amber-600 transition-colors">
                    <input 
                      type="checkbox"
                      className="opacity-0 absolute w-full h-full cursor-pointer"
                      checked={newRule.is_mandatory}
                      onChange={e => setNewRule({...newRule, is_mandatory: e.target.checked})}
                    />
                    {newRule.is_mandatory && <CheckCircle2 className="w-4 h-4 text-amber-600" />}
                  </div>
                  <span className="text-sm font-medium text-slate-700">Strict Enforcement (Flag as Critical Violation if breached)</span>
                </label>
                
                <div className="flex justify-end gap-3 mt-4 pt-4 border-t border-slate-100">
                  <button 
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="px-6 py-2 border border-slate-200 text-slate-600 text-xs font-bold uppercase tracking-wider hover:bg-slate-50 transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit"
                    className="px-6 py-2 bg-amber-600 text-slate-950 text-xs font-bold uppercase tracking-wider hover:bg-[#A38555] shadow-[0_0_15px_rgba(184,151,98,0.2)] transition-all"
                  >
                    Deploy Policy
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
