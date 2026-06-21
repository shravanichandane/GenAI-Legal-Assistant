"use client";

import { motion } from "framer-motion";
import { FileText, BookOpen, BarChart3, Settings, Bell, Search, Menu, Cpu, SquareTerminal, Loader2 } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import { DemoBanner } from "@/components/DemoBanner";
import { api } from "@/lib/api";

const navItems = [
  { icon: SquareTerminal, label: "Dashboard", href: "/home" },
  { icon: FileText, label: "Review", href: "/contracts/upload" },
  { icon: BookOpen, label: "Playbooks", href: "/playbooks" },
  { icon: BarChart3, label: "Analytics", href: "/analytics" },
  { icon: Cpu, label: "Research", href: "/research" },
  { icon: Settings, label: "Settings", href: "/settings" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const router = useRouter();
  const [userEmail, setUserEmail] = useState("Managing Partner");
  const [isAuthChecked, setIsAuthChecked] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const user = await api.getMe();
        setUserEmail(user.email || "Managing Partner");
        setIsAuthChecked(true);
      } catch {
        // Not authenticated — redirect to login
        router.push('/login');
      }
    };
    checkAuth();
  }, [router]);

  const handleLogout = async () => {
    try {
      await api.logout();
    } catch {
      // Even if logout API fails, redirect to login
    }
    router.push('/login');
  };

  // Show a centered loading spinner while auth is being verified
  if (!isAuthChecked) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#FDFBF7]">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-10 h-10 animate-spin text-amber-600" />
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400">Verifying Session</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-white overflow-hidden">
      {/* Sidebar - Envato Legal Luxury Style */}
      <motion.aside 
        initial={{ width: 260 }}
        animate={{ width: isSidebarOpen ? 260 : 80 }}
        className="bg-slate-950 border-r border-slate-800 flex flex-col relative z-20"
      >
        <div className="h-20 flex items-center justify-between px-6 border-b border-slate-800">
          {isSidebarOpen ? (
            <div className="flex items-center gap-3 font-serif font-bold text-2xl text-white tracking-wide">
              <div className="border border-amber-600 p-1">
                <div className="bg-amber-600 p-1.5">
                  <ScaleIcon className="w-5 h-5 text-slate-950" />
                </div>
              </div>
              LegalSight
            </div>
          ) : (
            <div className="mx-auto border border-amber-600 p-1">
              <div className="bg-amber-600 p-1.5">
                <ScaleIcon className="w-5 h-5 text-slate-950" />
              </div>
            </div>
          )}
        </div>

        <div className="flex-1 py-10 px-4 space-y-2">
          {navItems.map((item) => {
            // Because the 'contracts/upload' path maps to Review, 
            // we will consider it active if the path starts with /contracts
            const isActive = item.href === '/contracts/upload' 
              ? pathname.startsWith('/contracts') 
              : pathname === item.href;
              
            return (
              <Link key={item.label} href={item.href}>
                <div
                  className={`flex items-center gap-4 px-4 py-3 transition-colors group border-l-2 ${
                    isActive
                      ? "border-amber-600 bg-white/5 text-amber-600"
                      : "border-transparent text-slate-400 hover:border-slate-500 hover:bg-white/5 hover:text-white"
                  }`}
                >
                  <item.icon className={`w-4 h-4 ${isActive ? "text-amber-600" : "text-slate-500 group-hover:text-white"}`} />
                  {isSidebarOpen && <span className="text-[11px] font-bold uppercase tracking-[0.15em]">{item.label}</span>}
                </div>
              </Link>
            );
          })}
        </div>

        <div className="p-6 border-t border-slate-800 bg-slate-950/50">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-slate-800 border border-slate-700 flex items-center justify-center text-amber-600 font-serif text-lg flex-shrink-0">
              {userEmail.charAt(0).toUpperCase() || 'J'}
            </div>
            {isSidebarOpen && (
              <div className="overflow-hidden">
                <p className="text-xs font-bold uppercase tracking-widest text-white truncate" title={userEmail}>
                  {userEmail.split('@')[0]}
                </p>
                <p className="text-[10px] text-slate-400 font-mono truncate">Managing Partner</p>
              </div>
            )}
          </div>
        </div>
      </motion.aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-[#FDFBF7]">
        {/* Top Navbar */}
        <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-8 z-10 relative">
          <div className="flex items-center gap-6">
            <button 
              onClick={() => setSidebarOpen(!isSidebarOpen)}
              className="p-2 text-slate-400 hover:text-slate-950 transition-colors border border-transparent hover:border-slate-200"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="hidden md:flex relative group">
              <Search className="w-4 h-4 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
              <input 
                type="text" 
                placeholder="SEARCH REPOSITORIES..." 
                className="pl-12 pr-4 py-3 w-96 bg-slate-50 border border-slate-200 focus:bg-white focus:border-amber-600 text-[10px] font-bold uppercase tracking-[0.15em] transition-colors outline-none rounded-none"
              />
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button className="relative p-2 text-slate-400 hover:text-slate-950 transition-colors border border-transparent hover:border-slate-200">
              <Bell className="w-5 h-5" />
              <span className="absolute top-2 right-2 w-2 h-2 bg-amber-600 rounded-full"></span>
            </button>
            <button 
              onClick={handleLogout}
              className="px-4 py-2 border border-slate-200 text-xs font-bold uppercase tracking-widest text-slate-500 hover:bg-slate-50 transition-colors"
            >
              Sign Out
            </button>
          </div>
        </header>

        {/* Persistent Demo Banner */}
        <DemoBanner />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-8 md:p-12">
          {children}
        </main>
      </div>
    </div>
  );
}

function ScaleIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z" />
      <path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z" />
      <path d="M7 21h10" />
      <path d="M12 3v18" />
      <path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2" />
    </svg>
  )
}
