import Link from "next/link";
import { Scale, ArrowRight, ShieldCheck, Zap, Database } from "lucide-react";

export const metadata = {
  title: "LegalSight AI | Premium Legal Intelligence",
  description: "Automate contract review and risk detection with superhuman precision.",
};

export default function MarketingPage() {
  return (
    <div className="min-h-screen bg-[#FDFBF7] flex flex-col font-sans selection:bg-amber-600 selection:text-white">
      
      {/* Luxury Navbar */}
      <header className="h-24 bg-white border-b border-slate-200 flex items-center justify-between px-8 md:px-16 z-10 sticky top-0">
        <div className="flex items-center gap-3 font-serif font-bold text-2xl text-slate-950 tracking-wide">
          <div className="border border-amber-600 p-1">
            <div className="bg-amber-600 p-1.5">
              <Scale className="w-6 h-6 text-slate-950" />
            </div>
          </div>
          LegalSight
        </div>
        
        <div className="hidden md:flex items-center gap-8 text-[11px] font-bold uppercase tracking-[0.15em] text-slate-500">
          <Link href="#features" className="hover:text-slate-950 transition-colors">Features</Link>
          <Link href="#technology" className="hover:text-slate-950 transition-colors">Technology</Link>
          <Link href="#firm" className="hover:text-slate-950 transition-colors">The Firm</Link>
        </div>
        
        <div className="flex items-center gap-4">
          <Link 
            href="/login" 
            className="hidden md:flex text-[11px] font-bold uppercase tracking-[0.15em] text-slate-950 hover:text-amber-600 transition-colors px-4"
          >
            Client Portal
          </Link>
          <Link 
            href="/login" 
            className="bg-slate-950 hover:bg-slate-800 text-white text-[11px] font-bold uppercase tracking-[0.15em] px-8 py-4 transition-all duration-300 border border-slate-950 flex items-center gap-2 group"
          >
            Enter Workspace
            <ArrowRight className="w-4 h-4 text-amber-600 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden bg-slate-950 py-32 px-8 md:px-16 border-b-8 border-amber-600">
          <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            
            <div className="z-10">
              <span className="text-[11px] font-bold uppercase tracking-[0.2em] text-amber-600 mb-6 block">Tier-1 Legal AI</span>
              <h1 className="text-5xl md:text-7xl font-serif text-white tracking-tight leading-[1.1] mb-8">
                Uncompromising <br/> Contract Intelligence.
              </h1>
              <p className="text-slate-400 text-lg md:text-xl font-mono leading-relaxed mb-12 max-w-xl">
                LegalSight autonomously reviews, redlines, and extracts risk from high-stakes corporate agreements using deterministically constrained AI.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Link 
                  href="/login" 
                  className="bg-amber-600 hover:bg-[#A38555] text-slate-950 font-bold text-xs uppercase tracking-[0.15em] py-5 px-10 shadow-[0_0_20px_rgba(184,151,98,0.2)] transition-all flex items-center justify-center gap-3"
                >
                  Request Access
                </Link>
                <Link 
                  href="/research" 
                  className="bg-transparent border border-slate-700 hover:border-amber-600 text-white font-bold text-xs uppercase tracking-[0.15em] py-5 px-10 transition-colors flex items-center justify-center"
                >
                  View Research
                </Link>
              </div>
            </div>

            <div className="relative z-10 hidden lg:block">
              {/* Abstract High-Tech Mockup */}
              <div className="border border-slate-700 bg-slate-900/80 p-8 relative backdrop-blur-sm">
                <div className="absolute top-0 right-0 w-64 h-64 bg-amber-600/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none" />
                <div className="flex justify-between items-center mb-8 border-b border-slate-800 pb-4">
                  <span className="text-white font-serif text-xl">MSA_AlphaCorp.pdf</span>
                  <div className="flex gap-2">
                    <span className="text-[10px] text-slate-950 bg-amber-600 px-2 py-1 font-bold uppercase tracking-widest">High Risk</span>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="h-4 bg-slate-800 w-full" />
                  <div className="h-4 bg-slate-800 w-5/6" />
                  <div className="h-4 bg-slate-800 w-4/5" />
                  <div className="p-4 border-l-2 border-amber-600 bg-amber-600/10 text-slate-300 font-mono text-sm mt-8">
                    "8.2 Indemnification. Provider shall indemnify and hold harmless the Client against any and all claims, damages, or losses..."
                  </div>
                  <div className="text-[10px] uppercase tracking-widest text-amber-600 mt-2">Deviation: Uncapped Liability Detected</div>
                </div>
              </div>
            </div>
            
          </div>
        </section>

        {/* Features Section */}
        <section className="py-24 px-8 md:px-16 bg-white" id="features">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-20">
              <h2 className="text-4xl font-serif text-slate-950 mb-4">Precision Engineering</h2>
              <div className="w-16 h-1 bg-amber-600 mx-auto" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                { icon: ShieldCheck, title: "Absolute Grounding", desc: "Every AI assertion is strictly mapped to extracted contract text. No hallucinations." },
                { icon: Database, title: "Playbook Enforced", desc: "Your firm's unique risk tolerance logic is mapped directly into our vector database." },
                { icon: Zap, title: "Sub-Second Latency", desc: "FAISS-indexed embeddings process 100-page master agreements in milliseconds." }
              ].map((f, i) => (
                <div key={i} className="relative bg-slate-950 border border-slate-800 p-10 group hover:-translate-y-2 transition-all duration-500 hover:shadow-[0_20px_40px_-15px_rgba(217,119,6,0.3)] overflow-hidden">
                  <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-amber-600 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                  <div className="absolute -top-24 -right-24 w-48 h-48 bg-amber-600/5 rounded-full blur-3xl group-hover:bg-amber-600/20 transition-colors duration-700 pointer-events-none" />
                  
                  <div className="relative z-10">
                    <div className="bg-slate-900 border border-slate-700 w-16 h-16 flex items-center justify-center mb-8 group-hover:border-amber-600 group-hover:bg-amber-600/10 transition-colors duration-500 text-amber-600">
                      <f.icon className="w-6 h-6" />
                    </div>
                    <h3 className="text-2xl font-serif text-white mb-4 group-hover:text-amber-500 transition-colors">{f.title}</h3>
                    <p className="text-sm text-slate-400 leading-relaxed font-mono">{f.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>
      
      {/* Footer */}
      <footer className="border-t border-slate-200 bg-slate-950 py-16 px-8 md:px-16">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex items-center gap-3 font-serif font-bold text-xl text-white">
            <div className="border border-amber-600 p-1">
              <div className="bg-amber-600 p-1.5">
                <Scale className="w-4 h-4 text-slate-950" />
              </div>
            </div>
            LegalSight
          </div>
          <p className="text-[10px] text-slate-400 font-bold uppercase tracking-[0.2em]">
            © {new Date().getFullYear()} LegalSight Intelligence. Strictly Confidential.
          </p>
        </div>
      </footer>
    </div>
  );
}
