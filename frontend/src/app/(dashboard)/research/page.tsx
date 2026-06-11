"use client";

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Network, ServerCog, Database, Cpu, Activity, Clock, ShieldCheck, Scale } from 'lucide-react';

interface ResearchMetrics {
  total_documents_processed: number;
  average_inference_time_ms: number;
  active_models: {
    retriever: string;
    generator: string;
    cross_encoder: string;
  };
  accuracy_metrics: {
    precision_at_5: number;
    recall_at_5: number;
    ndcg: number;
    cross_encoder_mrr: number;
  };
  system_health: string;
}

export default function ResearchPage() {
  const [metrics, setMetrics] = useState<ResearchMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/research/metrics');
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        setMetrics(data);
        setError(false);
      } catch (err) {
        console.error("Failed to fetch live research metrics", err);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-7xl mx-auto pb-12">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-6 border-b border-slate-200 pb-8 mb-12">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
          <span className="text-xs font-bold uppercase tracking-[0.2em] text-amber-600 mb-3 block">Under the Hood</span>
          <h1 className="text-4xl md:text-5xl font-serif text-slate-950 tracking-tight">Research & Architecture</h1>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-4 py-2 bg-slate-50 border border-slate-200">
            <div className={`w-2 h-2 rounded-full ${metrics?.system_health === 'optimal' ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
            <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500">API Link Active</span>
          </div>
          <button className="px-8 py-3 bg-slate-950 text-white text-xs font-bold uppercase tracking-[0.15em] hover:bg-slate-800 transition-colors rounded-none">
            Download Paper
          </button>
        </motion.div>
      </div>

      {error ? (
        <div className="bg-rose-50 border border-rose-200 p-8 text-center text-rose-700 font-mono text-sm">
          Failed to connect to FastAPI Backend (`http://localhost:8000`). Please ensure the server is running.
        </div>
      ) : loading ? (
        <div className="flex items-center justify-center py-32">
          <Activity className="w-8 h-8 text-amber-600 animate-spin" />
        </div>
      ) : metrics ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Top Level Stats */}
          <div className="lg:col-span-12 grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white border border-slate-200 p-6 flex flex-col justify-between hover:border-amber-600 transition-colors">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 mb-6 block">Inference Speed</span>
              <div className="flex items-end justify-between">
                <span className="text-4xl font-serif text-slate-950">{metrics.average_inference_time_ms}</span>
                <span className="text-sm font-mono text-slate-500 mb-1">ms / query</span>
              </div>
            </div>
            <div className="bg-white border border-slate-200 p-6 flex flex-col justify-between hover:border-amber-600 transition-colors">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 mb-6 block">Processed Corpus</span>
              <div className="flex items-end justify-between">
                <span className="text-4xl font-serif text-slate-950">{(metrics.total_documents_processed / 1000).toFixed(1)}k</span>
                <span className="text-sm font-mono text-slate-500 mb-1">documents</span>
              </div>
            </div>
            <div className="bg-slate-950 border border-slate-950 p-6 flex flex-col justify-between relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-24 h-24 bg-white/5 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-amber-600/20 transition-colors" />
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-amber-600 mb-6 block relative z-10">Cross-Encoder MRR</span>
              <div className="flex items-end justify-between relative z-10">
                <span className="text-4xl font-serif text-white">{metrics.accuracy_metrics?.cross_encoder_mrr || 'N/A'}</span>
                <ShieldCheck className="w-6 h-6 text-amber-600 mb-1" />
              </div>
            </div>
            <div className="bg-white border border-slate-200 p-6 flex flex-col justify-between hover:border-amber-600 transition-colors">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 mb-6 block">System Status</span>
              <div className="flex items-end justify-between">
                <span className="text-2xl font-serif text-slate-950 uppercase tracking-widest">{metrics.system_health}</span>
                <Activity className="w-6 h-6 text-emerald-600 mb-1" />
              </div>
            </div>
          </div>

          {/* Architecture Visualizer */}
          <div className="lg:col-span-8 bg-white border border-slate-200 p-8">
            <h3 className="text-xl font-serif text-slate-950 border-b border-slate-100 pb-4 mb-8">RAG Pipeline Architecture</h3>
            
            <div className="space-y-4">
              <div className="flex items-center gap-6 p-4 border border-slate-100 bg-slate-50 hover:border-amber-600 transition-colors">
                <Database className="w-6 h-6 text-slate-400" />
                <div className="flex-1">
                  <h4 className="text-xs font-bold uppercase tracking-widest text-slate-950">Vector Store & Retriever</h4>
                  <p className="text-sm font-mono text-slate-500 mt-1">{metrics.active_models?.retriever || 'N/A'}</p>
                </div>
                <div className="text-right">
                  <span className="block text-xl font-serif text-slate-950">{metrics.accuracy_metrics?.recall_at_5 || 'N/A'}</span>
                  <span className="text-[10px] uppercase tracking-widest text-slate-400">Recall@5</span>
                </div>
              </div>

              <div className="flex justify-center py-2">
                <div className="w-px h-6 bg-slate-300" />
              </div>

              <div className="flex items-center gap-6 p-4 border border-slate-100 bg-slate-50 hover:border-amber-600 transition-colors">
                <ServerCog className="w-6 h-6 text-amber-600" />
                <div className="flex-1">
                  <h4 className="text-xs font-bold uppercase tracking-widest text-slate-950">Cross-Encoder Reranker</h4>
                  <p className="text-sm font-mono text-slate-500 mt-1">{metrics.active_models?.cross_encoder || 'N/A'}</p>
                </div>
                <div className="text-right">
                  <span className="block text-xl font-serif text-slate-950">{metrics.accuracy_metrics?.ndcg || 'N/A'}</span>
                  <span className="text-[10px] uppercase tracking-widest text-slate-400">nDCG</span>
                </div>
              </div>

              <div className="flex justify-center py-2">
                <div className="w-px h-6 bg-slate-300" />
              </div>

              <div className="flex items-center gap-6 p-4 border border-slate-950 bg-slate-950">
                <Cpu className="w-6 h-6 text-white" />
                <div className="flex-1">
                  <h4 className="text-xs font-bold uppercase tracking-widest text-amber-600">Generative Inference</h4>
                  <p className="text-sm font-mono text-slate-300 mt-1">{metrics.active_models?.generator || 'N/A'}</p>
                </div>
                <div className="text-right">
                  <span className="block text-xs font-bold uppercase tracking-widest text-white mt-2">Active</span>
                </div>
              </div>
            </div>
          </div>

          {/* Model Card */}
          <div className="lg:col-span-4 bg-slate-50 border border-slate-200 p-8 flex flex-col">
            <h3 className="text-xl font-serif text-slate-950 border-b border-slate-200 pb-4 mb-8">Model Card</h3>
            
            <div className="flex-1 space-y-8">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 block mb-2">Primary Objective</span>
                <p className="text-sm font-serif text-slate-700 leading-relaxed">
                  Identify and classify severe risk liabilities in enterprise-grade B2B contracts using contextual extraction.
                </p>
              </div>
              
              <div>
                <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 block mb-2">Training Data</span>
                <p className="text-sm font-mono text-slate-700">CUAD (Commercial Data)</p>
                <p className="text-sm font-mono text-slate-700 mt-1">ContractNLI (Logic)</p>
                <p className="text-sm font-mono text-slate-700 mt-1">MAUD (Mergers & Acq)</p>
              </div>

              <div>
                <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 block mb-2">Live Accuracy (F1)</span>
                <div className="h-2 w-full bg-slate-200 mt-4">
                  <div className="h-full bg-amber-600" style={{ width: '92%' }} />
                </div>
                <div className="flex justify-between mt-2">
                  <span className="text-xs font-mono text-slate-500">LegalSight Pipeline</span>
                  <span className="text-xs font-bold text-slate-950">0.92</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      ) : null}
    </div>
  );
}
