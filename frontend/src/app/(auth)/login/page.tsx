"use client";

import React, { useState, useEffect } from "react";
import { Scale, Lock, ArrowRight, Loader2, UserPlus, LogIn } from "lucide-react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [checkingSession, setCheckingSession] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user already has a valid session cookie
    const checkSession = async () => {
      try {
        const { api } = await import("@/lib/api");
        await api.getMe();
        // Session is valid — redirect to dashboard
        router.push('/home');
      } catch {
        // No valid session — stay on login page
        setCheckingSession(false);
      }
    };
    checkSession();
  }, [router]);

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");

    // Validation
    if (password.length < 6) {
      setErrorMsg("Password must be at least 6 characters.");
      return;
    }

    setIsLoading(true);

    try {
      const { api } = await import("@/lib/api");

      if (isSignUp) {
        await api.register({ email, password });
        // Automatically login after successful registration
      }

      const formData = new FormData();
      formData.append("username", email);
      formData.append("password", password);

      await api.login(formData);

      // Cookie is set by the backend automatically via Set-Cookie header
      router.push("/home");
    } catch (err: any) {
      setErrorMsg(err.message || "Authentication failed. Please check your credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  // Show nothing while checking existing session to avoid flash
  if (checkingSession) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-amber-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 flex font-sans">
      
      {/* Left side: Premium Auth Form */}
      <div className="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-16 md:px-24 xl:px-32 relative z-10 bg-white">
        
        <Link href="/" className="absolute top-12 left-8 sm:left-16 md:left-24 xl:left-32 flex items-center gap-3 font-serif font-bold text-2xl text-slate-950">
          <div className="border border-amber-600 p-1">
            <div className="bg-amber-600 p-1.5">
              <Scale className="w-5 h-5 text-slate-950" />
            </div>
          </div>
          LegalSight
        </Link>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md mt-24 lg:mt-0"
        >
          <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-amber-600 mb-4 block">Secure Portal</span>
          <h2 className="text-4xl font-serif text-slate-950 mb-2 tracking-tight">
            {isSignUp ? "Create Account" : "Client Access"}
          </h2>
          <p className="text-slate-500 text-sm mb-8">
            {isSignUp ? "Register to initialize your intelligence workspace." : "Authenticate to access the intelligence workspace."}
          </p>

          <form onSubmit={handleAuth} className="space-y-6">
            <AnimatePresence mode="wait">
              {errorMsg && (
                <motion.div 
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="bg-rose-50 border border-rose-200 text-rose-700 text-xs font-mono p-3"
                >
                  {errorMsg}
                </motion.div>
              )}
            </AnimatePresence>

            <div className="space-y-2">
              <label className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-500 block">Email Address</label>
              <input 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="attorney@example.com"
                className="w-full bg-slate-50 border-b-2 border-slate-200 px-4 py-4 text-slate-950 focus:outline-none focus:bg-white focus:border-amber-600 transition-colors font-mono text-sm"
                required
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-500 block">Master Password</label>
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full bg-slate-50 border-b-2 border-slate-200 px-4 py-4 text-slate-950 focus:outline-none focus:bg-white focus:border-amber-600 transition-colors font-mono text-sm tracking-widest"
                required
              />
            </div>

            {!isSignUp && (
              <div className="flex items-center justify-between pt-2">
                <label className="flex items-center gap-2 cursor-pointer group">
                  <input type="checkbox" defaultChecked className="w-4 h-4 rounded-none border-slate-300 text-slate-950 focus:ring-amber-600" />
                  <span className="text-xs text-slate-500 group-hover:text-slate-950 transition-colors">Remember device</span>
                </label>
                <button type="button" className="text-xs text-amber-600 hover:text-[#A38555] font-bold uppercase tracking-wider">
                  Reset Credentials
                </button>
              </div>
            )}

            <button 
              type="submit" 
              disabled={isLoading}
              className="w-full bg-slate-950 hover:bg-slate-800 text-white font-bold text-xs uppercase tracking-[0.15em] py-5 mt-4 transition-all duration-300 flex items-center justify-center gap-3 border border-slate-950 disabled:opacity-70"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin text-amber-600" />
              ) : (
                <>
                  {isSignUp ? "Initialize Account" : "Authenticate Session"}
                  {isSignUp ? <UserPlus className="w-4 h-4 text-amber-600" /> : <ArrowRight className="w-4 h-4 text-amber-600" />}
                </>
              )}
            </button>
          </form>

          <div className="mt-8 border-t border-slate-200 pt-6 text-center">
            <button 
              type="button" 
              onClick={() => {
                setIsSignUp(!isSignUp);
                setErrorMsg("");
              }}
              className="text-xs font-bold uppercase tracking-wider text-slate-500 hover:text-slate-950 transition-colors flex items-center justify-center gap-2 w-full"
            >
              {isSignUp ? (
                <>
                  <LogIn className="w-4 h-4" /> Already have an account? Sign In
                </>
              ) : (
                <>
                  <UserPlus className="w-4 h-4" /> Fresh user? Create Account
                </>
              )}
            </button>
          </div>
        </motion.div>
      </div>

      {/* Right side: Abstract Brand Image */}
      <div className="hidden lg:flex w-1/2 bg-slate-950 border-l border-slate-800 flex-col items-center justify-center relative overflow-hidden">
        {/* Subtle background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-amber-600/5 rounded-full blur-[100px]" />
        
        <div className="relative z-10 text-center max-w-lg px-12">
          <Lock className="w-16 h-16 text-amber-600 mx-auto mb-8 opacity-80" strokeWidth={1} />
          <h3 className="text-3xl font-serif text-white mb-6 leading-tight">Military-Grade Confidentiality.</h3>
          <p className="text-slate-400 font-mono text-sm leading-relaxed border-l-2 border-amber-600 pl-6 text-left">
            "All intelligence processing occurs within isolated enclaves. No data is used to train foundational models. SOC2 Type II and ISO 27001 Certified."
          </p>
        </div>

        {/* Decorative architectural lines */}
        <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-amber-600/20 to-transparent" />
        <div className="absolute top-0 bottom-0 right-16 w-[1px] bg-slate-800/50" />
        <div className="absolute top-0 bottom-0 right-20 w-[1px] bg-slate-800/30" />
      </div>

    </div>
  );
}
