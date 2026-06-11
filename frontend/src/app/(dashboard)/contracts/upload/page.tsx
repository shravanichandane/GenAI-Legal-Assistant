"use client";

import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { UploadCloud, FileText, CheckCircle2, Loader2, Server, BrainCircuit, Search, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";

const PIPELINE_STEPS = [
  { id: "parsing", label: "Parsing Document", icon: FileText, desc: "Extracting text & layout structures" },
  { id: "classifying", label: "Classifying Clauses", icon: Server, desc: "Identifying legal entities & provisions" },
  { id: "retrieval", label: "Semantic Retrieval", icon: Search, desc: "Matching against playbook standards" },
  { id: "scoring", label: "Risk Scoring", icon: BrainCircuit, desc: "Applying AI risk models & scoring" }
];

export default function UploadPage() {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [currentStep, setCurrentStep] = useState(-1);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileUpload(e.target.files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    setCurrentStep(0); // Uploading & Parsing
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Execute live API request to FastAPI
      const { api } = await import("@/lib/api");
      const uploadData = await api.uploadContract(formData);

      // Activate live data across the application dashboard
      localStorage.setItem('app_mode', 'live');

      // Read file content to pass it to the workspace via localStorage
      const reader = new FileReader();
      reader.onload = (event) => {
        const text = event.target?.result;
        if (text) {
          localStorage.setItem('latest_uploaded_contract_text', text.toString());
        }
      };
      reader.readAsText(file);
      
      const contractId = uploadData.contract_id;
      
      // Poll for status
      let isComplete = false;
      while (!isComplete) {
        const statusData = await api.getContractStatus(contractId);
        
        if (statusData.status === "failed") {
            throw new Error(statusData.error || "Analysis failed");
        }
        
        if (statusData.status === "analyzed") {
            isComplete = true;
            setCurrentStep(3); // Scoring complete
            setTimeout(() => {
                router.push(`/contracts/${contractId}`);
            }, 1000);
            break;
        }
        
        // Update step based on progress
        if (statusData.progress >= 25 && currentStep < 1) setCurrentStep(1);
        if (statusData.progress >= 50 && currentStep < 2) setCurrentStep(2);
        
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
    } catch (error) {
      console.error("Error uploading document:", error);
      alert("Failed to upload document to FastAPI backend. Is the server running?");
      setIsUploading(false);
      setCurrentStep(-1);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-[#FDFBF7] p-8 flex flex-col items-center justify-center">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-12">
          <span className="text-xs font-bold uppercase tracking-[0.2em] text-amber-600 mb-4 block">New Intake</span>
          <h1 className="text-4xl font-serif text-slate-950 tracking-tight mb-4">
            Upload Agreement
          </h1>
          <p className="text-sm text-slate-500 font-medium">
            Securely process your agreements through the intelligence pipeline.
          </p>
        </div>

        {!isUploading ? (
          <>
            <input 
              type="file" 
              ref={fileInputRef} 
              className="hidden" 
              onChange={handleFileSelect} 
              accept=".pdf,.docx,.txt" 
            />
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`relative group border border-dashed p-16 transition-all duration-500 ease-in-out cursor-pointer flex flex-col items-center justify-center min-h-[450px] bg-white rounded-none shadow-sm ${
                isDragging 
                  ? "border-amber-600 bg-amber-600/5" 
                  : "border-slate-300 hover:border-amber-600 hover:shadow-2xl hover:shadow-amber-600/10"
              }`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <motion.div 
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex flex-col items-center pointer-events-none"
              >
                <div className={`p-6 mb-8 border transition-all duration-500 ${
                  isDragging ? "border-amber-600 text-amber-600 bg-white shadow-lg shadow-amber-600/20" : "border-slate-200 text-slate-400 group-hover:border-amber-600 group-hover:text-amber-600"
                }`}>
                  <UploadCloud className="w-10 h-10" strokeWidth={1} />
                </div>
                <h3 className="text-2xl font-serif text-slate-950 mb-4">
                  Drag & Drop or Click to Upload
                </h3>
                <p className="text-slate-400 text-sm mb-10 max-w-sm text-center font-mono">
                  Supports PDF, DOCX, and TXT files up to 50MB. All files are securely encrypted.
                </p>
                
                <div className="bg-slate-950 text-white px-8 py-4 text-xs font-bold uppercase tracking-[0.15em] hover:bg-slate-800 transition-colors flex items-center gap-3 pointer-events-auto border border-slate-950">
                  Select File
                  <ArrowRight className="w-4 h-4 text-amber-600" />
                </div>
              </motion.div>
            </motion.div>
          </>
        ) : (
          <motion.div 
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white shadow-2xl border border-slate-200 p-12 min-h-[450px] flex flex-col justify-center rounded-none relative overflow-hidden"
          >
            <div className="absolute top-0 left-0 w-full h-1 bg-slate-100">
              <motion.div 
                className="h-full bg-amber-600"
                initial={{ width: "0%" }}
                animate={{ width: `${((currentStep + 1) / PIPELINE_STEPS.length) * 100}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>

            <div className="flex items-center justify-center mb-12">
              <div className="relative">
                <div className="w-20 h-20 bg-slate-950 flex items-center justify-center border border-amber-600/30">
                  <BrainCircuit className="w-8 h-8 text-amber-600 animate-pulse" />
                </div>
                <motion.div 
                  animate={{ rotate: 360 }}
                  transition={{ repeat: Infinity, duration: 8, ease: "linear" }}
                  className="absolute inset-[-4px] border border-dashed border-amber-600/50"
                />
              </div>
            </div>
            
            <h3 className="text-2xl font-serif text-center text-slate-950 mb-10">
              Processing Document Intelligence
            </h3>

            <div className="space-y-8 max-w-md mx-auto w-full">
              {PIPELINE_STEPS.map((step, index) => {
                const isActive = currentStep === index;
                const isCompleted = currentStep > index;
                const Icon = step.icon;

                return (
                  <div key={step.id} className="flex items-center gap-6">
                    <div className={`flex-shrink-0 w-10 h-10 border flex items-center justify-center transition-all duration-500 ${
                      isCompleted ? "border-amber-600 bg-amber-600 text-white" :
                      isActive ? "border-slate-950 bg-slate-950 text-amber-600" :
                      "border-slate-200 bg-white text-slate-300"
                    }`}>
                      {isCompleted ? (
                        <CheckCircle2 className="w-5 h-5" />
                      ) : isActive ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                      ) : (
                        <Icon className="w-5 h-5" />
                      )}
                    </div>
                    
                    <div className="flex-1">
                      <h4 className={`text-xs font-bold uppercase tracking-[0.1em] transition-colors ${
                        isActive ? "text-slate-950" :
                        isCompleted ? "text-slate-600" :
                        "text-slate-400"
                      }`}>
                        {step.label}
                      </h4>
                      <p className={`text-xs font-mono transition-colors mt-1 ${
                        isActive || isCompleted ? "text-slate-500" : "text-slate-300"
                      }`}>
                        {step.desc}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
