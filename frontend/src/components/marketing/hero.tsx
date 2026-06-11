"use client";

import { motion } from 'framer-motion';
import Link from 'next/link';
import { ArrowRight, ShieldCheck } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden bg-slate-50">
      {/* Background glowing aura */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-indigo-500/10 blur-[100px] rounded-full pointer-events-none" />
      
      {/* Subtle geometric grid background */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjEiIGZpbGw9IiNlNWE1ZmYiLz48L3N2Zz4=')] [mask-image:linear-gradient(to_bottom,white,transparent)] pointer-events-none opacity-50" />

      <div className="max-w-7xl mx-auto px-6 relative z-10 text-center flex flex-col items-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-indigo-100 text-indigo-700 text-sm font-medium mb-8 shadow-sm"
        >
          <ShieldCheck className="w-4 h-4 text-indigo-600" />
          <span>Trusted by Fortune 500 Legal Teams</span>
        </motion.div>
        
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
          className="text-5xl md:text-7xl lg:text-[5rem] font-extrabold text-slate-900 tracking-tight leading-[1.05] mb-6 max-w-4xl mx-auto"
        >
          Enterprise Legal <br className="hidden md:block" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500">
            Intelligence
          </span>
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
          className="text-lg md:text-xl text-slate-600 mb-10 max-w-2xl mx-auto leading-relaxed"
        >
          Automate contract review, extract critical obligations, and ensure compliance with superhuman precision. The operating system for modern legal teams.
        </motion.p>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 w-full sm:w-auto"
        >
          <Link 
            href="/login" 
            className="group relative inline-flex items-center justify-center gap-2 px-8 py-4 bg-slate-900 text-white font-semibold rounded-full overflow-hidden transition-all hover:scale-105 hover:shadow-2xl hover:shadow-indigo-500/25 w-full sm:w-auto"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-blue-500 opacity-0 group-hover:opacity-10 transition-opacity" />
            <span>Get Started Now</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link 
            href="#demo" 
            className="inline-flex items-center justify-center px-8 py-4 bg-white text-slate-900 font-semibold rounded-full border border-slate-200 shadow-sm transition-all hover:bg-slate-50 hover:border-slate-300 w-full sm:w-auto"
          >
            Book a Demo
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
