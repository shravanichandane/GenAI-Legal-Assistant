"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, UploadCloud, X } from 'lucide-react';
import Link from 'next/link';

export function WelcomePopup() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Only show if the app is in 'empty' mode (just logged in)
    const mode = localStorage.getItem('app_mode');
    if (!mode || mode === 'empty') {
      const timer = setTimeout(() => setIsVisible(true), 1500);
      return () => clearTimeout(timer);
    }
  }, []);

  const dismissPopup = () => {
    setIsVisible(false);
  };

  const startDemoMode = () => {
    localStorage.setItem('app_mode', 'demo');
    setIsVisible(false);
    window.location.reload();
  };

  return (
    <AnimatePresence>
      {isVisible && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm"
            onClick={dismissPopup}
          />

          {/* Modal */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="relative w-full max-w-lg bg-white rounded-none shadow-2xl overflow-hidden border border-slate-200"
          >
            {/* Header pattern */}
            <div className="absolute top-0 left-0 right-0 h-1 bg-amber-600" />
            
            <button 
              onClick={dismissPopup}
              className="absolute top-6 right-6 p-2 text-slate-400 hover:text-slate-950 bg-slate-50 border border-transparent hover:border-slate-200 transition-colors z-10 rounded-none"
            >
              <X className="w-4 h-4" />
            </button>

            <div className="p-10 pt-12">
              <div className="w-12 h-12 bg-slate-950 text-amber-600 flex items-center justify-center mb-8 border border-slate-950">
                <Sparkles className="w-5 h-5" />
              </div>
              
              <h2 className="text-3xl font-serif text-slate-950 mb-4 tracking-tight">
                Demo Workspace
              </h2>
              
              <p className="text-slate-600 mb-8 leading-relaxed font-mono text-sm">
                You are currently exploring LegalSight using synthetic contract data and playbooks. Feel free to explore the Analytics and Risk Engine.
              </p>

              <div className="flex flex-col gap-4">
                <Link 
                  href="/contracts/upload"
                  onClick={dismissPopup}
                  className="w-full bg-slate-950 hover:bg-slate-800 text-white font-bold text-xs uppercase tracking-[0.15em] py-4 transition-all flex items-center justify-center gap-3 rounded-none border border-slate-950"
                >
                  <UploadCloud className="w-4 h-4 text-amber-600" />
                  Upload Live Contract
                </Link>
                <button 
                  onClick={startDemoMode}
                  className="w-full bg-white hover:bg-slate-50 text-slate-950 border border-slate-200 font-bold text-xs uppercase tracking-[0.15em] py-4 transition-all rounded-none"
                >
                  Continue in Demo Mode
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
