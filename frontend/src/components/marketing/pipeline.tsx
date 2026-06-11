"use client";

import { motion } from 'framer-motion';
import { FileText, Cpu, Network, ShieldCheck, ArrowRight } from 'lucide-react';

const steps = [
  {
    id: "01",
    title: "Hierarchical Parser",
    description: "PDFs are shattered into granular, structured JSON arrays while maintaining the original document hierarchy and context.",
    icon: FileText,
    color: "from-blue-500 to-indigo-500",
    bg: "bg-blue-50",
    text: "text-blue-600"
  },
  {
    id: "02",
    title: "Legal-BERT Classification",
    description: "Fine-tuned Transformer model analyzes and categorizes each clause (e.g., Liability, Indemnity, Force Majeure).",
    icon: Cpu,
    color: "from-indigo-500 to-violet-500",
    bg: "bg-indigo-50",
    text: "text-indigo-600"
  },
  {
    id: "03",
    title: "Semantic RAG & FAISS",
    description: "Vector similarity search instantly cross-references extracted clauses against your firm's historical playbooks and precedents.",
    icon: Network,
    color: "from-violet-500 to-purple-500",
    bg: "bg-violet-50",
    text: "text-violet-600"
  },
  {
    id: "04",
    title: "Deterministic Risk Engine",
    description: "Cross-encoder reranking feeds into our deterministic rule engine to assign a final 0-100 risk score and generate the Evidence Trace.",
    icon: ShieldCheck,
    color: "from-emerald-500 to-teal-500",
    bg: "bg-emerald-50",
    text: "text-emerald-600"
  }
];

export function Pipeline() {
  return (
    <section className="py-24 bg-white border-t border-slate-100 overflow-hidden relative">
      <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] opacity-[0.3]" />
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="mb-16 md:text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 tracking-tight mb-4">
            How It Works
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl md:mx-auto">
            Our proprietary pipeline leverages four discrete AI models to process complex legal agreements in milliseconds.
          </p>
        </div>

        <div className="relative">
          {/* Connecting Line */}
          <div className="hidden md:block absolute top-[45px] left-[10%] right-[10%] h-0.5 bg-slate-100 z-0" />
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative z-10">
            {steps.map((step, index) => (
              <motion.div
                key={step.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                className="flex flex-col items-start md:items-center relative"
              >
                {/* Number Badge */}
                <div className="hidden md:flex absolute -top-4 -right-2 text-[100px] font-black text-slate-50/50 -z-10 select-none">
                  {step.id}
                </div>

                <motion.div 
                  className={`w-24 h-24 rounded-2xl flex items-center justify-center mb-6 bg-gradient-to-br ${step.color} shadow-lg shadow-indigo-100/50 text-white relative`}
                  whileHover={{ scale: 1.05, rotate: 5 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <step.icon className="w-10 h-10" />
                </motion.div>

                <h3 className="text-lg font-bold text-slate-900 mb-3 md:text-center tracking-tight">
                  {step.title}
                </h3>
                <p className="text-slate-500 text-sm md:text-center leading-relaxed font-medium">
                  {step.description}
                </p>

                {/* Arrow for mobile */}
                {index !== steps.length - 1 && (
                  <div className="md:hidden mt-6 text-slate-300 ml-8">
                    <ArrowRight className="w-6 h-6 rotate-90" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
