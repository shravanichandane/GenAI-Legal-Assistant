"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  AlertTriangle, 
  Check, 
  ChevronDown, 
  FileText, 
  Info, 
  ShieldAlert, 
  X,
  Search,
  ZoomIn,
  ZoomOut,
  Maximize2,
  BrainCircuit,
  PenTool
} from "lucide-react";

// Mock risk findings
const RISK_FINDINGS = [
  {
    id: "risk-1",
    severity: "high",
    title: "Uncapped Liability Clause",
    description: "The indemnification clause does not specify a maximum liability cap, exposing the company to unlimited damages.",
    playbookRule: "Rule 4.1: All vendor contracts must include a liability cap not exceeding 12 months of contract value.",
    clauseId: "Clause 8.2(a)",
    textSnippet: "...Provider shall indemnify and hold harmless the Client against any and all claims, damages, or losses arising from..."
  },
  {
    id: "risk-2",
    severity: "medium",
    title: "Auto-Renewal Without Notice",
    description: "Contract automatically renews for successive 1-year terms without a requirement for prior written notice.",
    playbookRule: "Rule 2.3: Auto-renewal clauses must require at least 30 days prior written notice to be valid.",
    clauseId: "Clause 3.1",
    textSnippet: "This Agreement shall automatically renew for additional one (1) year periods unless terminated by either party..."
  },
  {
    id: "risk-3",
    severity: "low",
    title: "Non-Standard Governing Law",
    description: "Governing law is set to New York, whereas standard playbook prefers Delaware or California.",
    playbookRule: "Rule 9.1: Preferred governing jurisdictions are DE, CA, or NY in that order of preference.",
    clauseId: "Clause 14.1",
    textSnippet: "This Agreement shall be governed by and construed in accordance with the laws of the State of New York..."
  }
];

// Envato Premium Accordion Component
const RiskAccordion = ({ risk, isOpen, onToggle }: { risk: any, isOpen: boolean, onToggle: () => void }) => {
  return (
    <div className={`border-b transition-all duration-300 ${
      isOpen ? "border-amber-600 bg-white" : "border-slate-200 bg-slate-50 hover:bg-slate-100"
    }`}>
      <button 
        onClick={onToggle}
        className="w-full flex items-center justify-between p-6 focus:outline-none"
      >
        <div className="flex items-center gap-4">
          <div className={`p-2 border ${
            risk.severity === 'high' ? 'border-rose-200 bg-rose-50 text-rose-700' :
            risk.severity === 'medium' ? 'border-amber-200 bg-amber-50 text-amber-700' :
            'border-slate-200 bg-white text-slate-700'
          }`}>
            {risk.severity === 'high' ? <ShieldAlert className="w-4 h-4" /> :
             risk.severity === 'medium' ? <AlertTriangle className="w-4 h-4" /> :
             <Info className="w-4 h-4" />}
          </div>
          <div className="text-left">
            <h4 className="text-slate-950 font-serif text-lg tracking-wide">{risk.title}</h4>
            <span className={`text-[10px] uppercase tracking-widest font-bold ${
              risk.severity === 'high' ? 'text-rose-600' :
              risk.severity === 'medium' ? 'text-amber-600' :
              'text-slate-500'
            }`}>
              {risk.severity} Deviation
            </span>
          </div>
        </div>
        <div className={`text-amber-600 transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`}>
          <ChevronDown className="w-4 h-4" />
        </div>
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <div className="p-6 pt-0 border-t border-slate-100 bg-white">
              <p className="text-sm text-slate-600 mb-6 mt-4 leading-relaxed">
                {risk.description}
              </p>
              
              <div className="mb-6">
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400">Extracted Text</span>
                  <div className="flex-1 h-px bg-slate-100"></div>
                </div>
                <p className="text-sm font-serif text-slate-800 bg-slate-50 p-4 border-l-2 border-amber-600">
                  "{risk.textSnippet}"
                </p>
              </div>

              <div className="flex items-start gap-3 bg-slate-950 text-white p-4">
                <Check className="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" />
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-amber-600 block mb-1">Playbook Rule</span>
                  <p className="text-xs font-mono text-slate-300 leading-relaxed">
                    {risk.playbookRule}
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default function ReviewPage(props: { params: Promise<{ id: string }> }) {
  const params = React.use(props.params);
  const id = params.id;
  
  const [openAccordion, setOpenAccordion] = useState<string | null>(null);
  const [contractText, setContractText] = useState<string | null>(null);
  const [dynamicRisks, setDynamicRisks] = useState<any[]>([]);
  const [zoom, setZoom] = useState(100);
  const [actionStatus, setActionStatus] = useState<string | null>(null);
  const [appMode, setAppMode] = useState('demo');

  const [overallScore, setOverallScore] = useState(0);

  React.useEffect(() => {
    // Fetch live data from API
    const fetchContractData = async () => {
      try {
        const { api } = await import("@/lib/api");
        
        // 1. Fetch text content
        try {
          const contentData = await api.getContractContent(id);
          if (contentData.content) setContractText(contentData.content);
        } catch (e) {
          console.warn("Failed to fetch contract content");
        }

        // 2. Fetch risks and score
        const risksData = await api.getContractRisks(id);
        const scoreData = await api.getContractRiskScore(id);
        
        if (risksData.findings && Array.isArray(risksData.findings)) {
          setDynamicRisks(risksData.findings);
          if (risksData.findings.length > 0) {
            setOpenAccordion(risksData.findings[0].id);
          }
        }
        
        if (scoreData.score) {
          setOverallScore(scoreData.score);
        } else if (risksData.risk_score) {
          setOverallScore(risksData.risk_score);
        }
      } catch (err) {
        console.error("Failed to fetch contract data:", err);
      }
    };
    
    fetchContractData();
    
    // Poll for updates in case the document is still processing
    const intervalId = setInterval(fetchContractData, 5000);
    return () => clearInterval(intervalId);
  }, [id]);



  const handleAction = async (status: string) => {
    try {
      const { api } = await import("@/lib/api");
      await api.reviewAction(id, status);
      setActionStatus(status);
      setTimeout(() => setActionStatus(null), 3000); // Reset after 3 seconds
    } catch (e) {
      console.error("Failed to submit action", e);
    }
  };



  return (
    <div className="flex h-[calc(100vh-4rem)] bg-white overflow-hidden">
      
      {/* Left Pane: PDF Viewer Mock */}
      <div className="w-1/2 border-r border-slate-200 bg-slate-50 flex flex-col relative">
        {/* Luxury PDF Toolbar */}
        <div className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shadow-sm z-10">
          <div className="flex items-center gap-3">
            <div className="bg-slate-950 text-amber-600 p-2 rounded-none">
              <FileText className="w-4 h-4" />
            </div>
            <span className="font-serif text-slate-950 text-lg truncate max-w-[300px]">
              {contractText ? "Uploaded_Contract.txt" : "MSA_TechCorp_Final_v2.pdf"}
            </span>
          </div>
          
          <div className="flex items-center gap-2 border border-slate-200 p-1 bg-slate-50">
            <button 
              onClick={() => setZoom(z => Math.max(50, z - 10))}
              className="p-1.5 text-slate-400 hover:text-slate-950 hover:bg-white transition-colors"
            >
              <ZoomOut className="w-4 h-4" />
            </button>
            <span className="text-xs font-mono text-slate-500 w-12 text-center">{zoom}%</span>
            <button 
              onClick={() => setZoom(z => Math.min(200, z + 10))}
              className="p-1.5 text-slate-400 hover:text-slate-950 hover:bg-white transition-colors"
            >
              <ZoomIn className="w-4 h-4" />
            </button>
            <div className="w-px h-4 bg-slate-200 mx-2" />
            <button 
              onClick={() => setZoom(100)}
              className="p-1.5 text-slate-400 hover:text-slate-950 hover:bg-white transition-colors"
              title="Reset Zoom"
            >
              <Search className="w-4 h-4" />
            </button>
            <button 
              onClick={() => setZoom(150)}
              className="p-1.5 text-slate-400 hover:text-slate-950 hover:bg-white transition-colors"
              title="Fit to Width"
            >
              <Maximize2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Mock PDF Content */}
        <div className="flex-1 overflow-auto p-12 flex justify-center pb-32">
          <div 
            className="w-full max-w-2xl bg-white shadow-2xl min-h-[1000px] border border-slate-200 p-16 text-slate-800 text-sm leading-relaxed font-serif relative transition-transform duration-300"
            style={{ transform: `scale(${zoom / 100})`, transformOrigin: 'top center' }}
          >
            
            {contractText ? (
              <div className="whitespace-pre-wrap font-serif leading-loose text-slate-900 text-base">
                {contractText}
              </div>
            ) : (
              <>
                <h1 className="text-3xl font-bold text-center mb-12 tracking-wide text-slate-950">MASTER SERVICES AGREEMENT</h1>
                <p className="mb-8 text-justify">This Master Services Agreement ("Agreement") is entered into as of October 1, 2026, by and between TechCorp Inc., a Delaware corporation ("Provider"), and Client LLC ("Client").</p>
                
                <h2 className="font-bold mt-10 mb-4 tracking-widest uppercase text-xs font-sans text-slate-500">3. Term and Termination</h2>
                <p className="mb-6 text-justify">
                  <span className={`transition-all duration-500 ${openAccordion === 'risk-2' ? 'bg-amber-600/20 border-b border-amber-600 text-slate-950' : ''}`}>
                    3.1 Term. This Agreement shall commence on the Effective Date and shall continue for an initial term of one (1) year. This Agreement shall automatically renew for additional one (1) year periods unless terminated by either party.
                  </span>
                </p>
                
                <h2 className="font-bold mt-10 mb-4 tracking-widest uppercase text-xs font-sans text-slate-500">8. Indemnification and Liability</h2>
                <p className="mb-6 text-justify">
                  <span className={`transition-all duration-500 ${openAccordion === 'risk-1' ? 'bg-amber-600/20 border-b border-amber-600 text-slate-950' : ''}`}>
                    8.2 Indemnification. Provider shall indemnify and hold harmless the Client against any and all claims, damages, or losses arising from Provider's performance of services under this Agreement.
                  </span>
                </p>

                <h2 className="font-bold mt-10 mb-4 tracking-widest uppercase text-xs font-sans text-slate-500">14. Miscellaneous</h2>
                <p className="mb-6 text-justify">
                  <span className={`transition-all duration-500 ${openAccordion === 'risk-3' ? 'bg-amber-600/20 border-b border-amber-600 text-slate-950' : ''}`}>
                    14.1 Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of New York, without regard to its conflict of law principles.
                  </span>
                </p>
              </>
            )}
            
            {/* Filler text for scroll */}
            {!contractText && (
              <div className="mt-12 opacity-50 space-y-4">
                <div className="h-2 bg-slate-100 w-full"></div>
                <div className="h-2 bg-slate-100 w-5/6"></div>
                <div className="h-2 bg-slate-100 w-full"></div>
                <div className="h-2 bg-slate-100 w-4/5"></div>
                <div className="h-2 bg-slate-100 w-full mt-8"></div>
                <div className="h-2 bg-slate-100 w-full"></div>
                <div className="h-2 bg-slate-100 w-2/3"></div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Right Pane: AI Risk Dashboard (Luxury) */}
      <div className="w-1/2 flex flex-col bg-white relative">
        <div className="p-8 border-b border-slate-200 bg-slate-950 shadow-xl z-20 flex-shrink-0">
          <div className="flex items-center gap-3 mb-2">
            <div className="bg-amber-600 text-slate-950 p-2">
              <BrainCircuit className="w-5 h-5" />
            </div>
            <h2 className="text-2xl font-serif text-white tracking-wide">Intelligence Review</h2>
          </div>
          <p className="text-sm text-slate-400 ml-12 font-mono">Automated parsing against Master Playbook v4.</p>
          
          <div className="flex gap-8 mt-8 ml-12">
            <div className="flex flex-col">
              <span className="text-[10px] text-amber-600 font-bold uppercase tracking-[0.2em] mb-2">Portfolio Exposure</span>
              <div className="flex items-center gap-3">
                <span className="text-4xl font-serif text-white">{overallScore}</span>
                <span className="text-[10px] text-white font-bold bg-rose-600 px-3 py-1 uppercase tracking-widest border border-rose-500">Critical</span>
              </div>
            </div>
            <div className="w-px h-12 bg-slate-800" />
            <div className="flex flex-col">
              <span className="text-[10px] text-amber-600 font-bold uppercase tracking-[0.2em] mb-2">Anomalies Detected</span>
              <span className="text-4xl font-serif text-white">{dynamicRisks.length}</span>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-auto bg-slate-50 pb-32">
          <div className="px-8 py-4 bg-white border-b border-slate-200 sticky top-0 z-10 flex items-center justify-between">
            <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">
              Deviations Log
            </h3>
            <span className="text-xs font-mono text-amber-600">{dynamicRisks.length} Items</span>
          </div>
          
          <div className="bg-white">
            {dynamicRisks.map(risk => (
              <RiskAccordion 
                key={risk.id} 
                risk={risk} 
                isOpen={openAccordion === risk.id}
                onToggle={() => setOpenAccordion(openAccordion === risk.id ? null : risk.id)}
              />
            ))}
          </div>
        </div>

        {/* Premium Floating Action Menu */}
        <motion.div 
          initial={{ y: 100 }}
          animate={{ y: 0 }}
          transition={{ type: "spring", stiffness: 200, damping: 20 }}
          className="absolute bottom-8 left-8 right-8 bg-white border border-slate-200 shadow-2xl p-4 flex gap-4"
        >
          {actionStatus ? (
            <div className={`flex-1 font-bold text-xs uppercase tracking-[0.15em] py-4 px-6 flex items-center justify-center gap-2 ${
              actionStatus === 'rejected' ? 'bg-rose-50 text-rose-700 border border-rose-200' :
              actionStatus === 'redlined' ? 'bg-slate-900 text-white border border-slate-950' :
              'bg-amber-50 text-amber-700 border border-amber-200'
            }`}>
              {actionStatus === 'rejected' && <X className="w-4 h-4" />}
              {actionStatus === 'redlined' && <PenTool className="w-4 h-4" />}
              {actionStatus === 'approved' && <Check className="w-4 h-4" />}
              Document {actionStatus}
            </div>
          ) : (
            <>
              <button 
                onClick={() => handleAction('rejected')}
                className="flex-1 bg-slate-50 hover:bg-rose-50 border border-slate-200 hover:border-rose-300 text-slate-700 hover:text-rose-700 text-xs font-bold uppercase tracking-[0.15em] py-4 px-6 transition-all duration-300 flex items-center justify-center gap-2 group"
              >
                <X className="w-4 h-4 text-slate-400 group-hover:text-rose-500 transition-colors" />
                Reject
              </button>
              <button 
                onClick={() => handleAction('redlined')}
                className="flex-1 bg-slate-950 hover:bg-slate-800 text-white border border-slate-950 text-xs font-bold uppercase tracking-[0.15em] py-4 px-6 transition-all duration-300 flex items-center justify-center gap-2"
              >
                <PenTool className="w-4 h-4 text-amber-600" />
                Redline
              </button>
              <button 
                onClick={() => handleAction('approved')}
                className="flex-1 bg-amber-600 hover:bg-[#A38555] text-slate-950 font-bold text-xs uppercase tracking-[0.15em] py-4 px-6 shadow-[0_0_20px_rgba(184,151,98,0.3)] transition-all duration-300 flex items-center justify-center gap-2"
              >
                <Check className="w-4 h-4" strokeWidth={3} />
                Approve
              </button>
            </>
          )}
        </motion.div>
      </div>
    </div>
  );
}
