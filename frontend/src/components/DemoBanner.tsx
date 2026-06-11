"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { UploadCloud } from 'lucide-react';

export function DemoBanner() {
  const [isDemo, setIsDemo] = useState(false);

  useEffect(() => {
    const checkDemo = () => {
      setIsDemo(localStorage.getItem('legalsight_demo_mode') !== 'false');
    };
    
    // Check initially
    checkDemo();
    
    // Check periodically to stay synced with the WelcomePopup dismissing
    const interval = setInterval(checkDemo, 1000);
    return () => clearInterval(interval);
  }, []);

  if (!isDemo) return null;

  return (
    <div className="bg-indigo-600 text-white px-6 py-2.5 flex items-center justify-between text-sm shadow-sm z-20 relative">
      <div className="flex items-center gap-3 font-medium">
        <span className="flex h-2.5 w-2.5 relative">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
        </span>
        You are currently exploring the Demo Workspace. Mock data is active.
      </div>
      <Link 
        href="/contracts/upload" 
        onClick={() => localStorage.setItem('legalsight_demo_mode', 'false')}
        className="flex items-center gap-2 bg-white/20 hover:bg-white/30 px-4 py-1.5 rounded-lg font-semibold transition-colors"
      >
        <UploadCloud className="w-4 h-4" />
        Exit Demo & Upload Live Data
      </Link>
    </div>
  );
}
