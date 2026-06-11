"use client";

import Link from 'next/link';

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-50/80 backdrop-blur-md border-b border-slate-200 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-md shadow-indigo-600/20 group-hover:scale-105 transition-transform">
            <span className="text-white font-bold text-xl leading-none">L</span>
          </div>
          <span className="font-bold text-xl text-slate-900 tracking-tight">LegalSight</span>
        </Link>
        
        <div className="flex items-center gap-8">
          <div className="hidden md:flex items-center gap-6">
            <Link href="#features" className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">
              Features
            </Link>
            <Link href="#how-it-works" className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">
              How it Works
            </Link>
          </div>
          <Link 
            href="/login" 
            className="text-sm font-medium bg-slate-900 text-white px-5 py-2.5 rounded-full hover:bg-slate-800 transition-all hover:shadow-lg hover:shadow-slate-900/20 active:scale-95"
          >
            Sign In
          </Link>
        </div>
      </div>
    </nav>
  );
}
