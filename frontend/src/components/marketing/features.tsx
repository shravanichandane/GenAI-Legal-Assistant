"use client";

import { motion } from 'framer-motion';
import { FileSearch, BookOpen, BrainCircuit, ShieldAlert, Zap } from 'lucide-react';

const features = [
  {
    title: "AI-Powered Parsing",
    description: "Instantly ingest complex agreements and extract key clauses, terms, and obligations with 99.9% accuracy.",
    icon: FileSearch,
    className: "md:col-span-2 md:row-span-2 bg-gradient-to-br from-indigo-50 to-white border-indigo-100",
    iconColor: "text-indigo-600",
    iconBg: "bg-indigo-100",
  },
  {
    title: "Dynamic Playbooks",
    description: "Enforce corporate standards automatically against third-party paper.",
    icon: BookOpen,
    className: "md:col-span-1 md:row-span-1 bg-white border-slate-200",
    iconColor: "text-blue-600",
    iconBg: "bg-blue-50",
  },
  {
    title: "Semantic RAG",
    description: "Chat with your entire contract repository instantly.",
    icon: BrainCircuit,
    className: "md:col-span-1 md:row-span-1 bg-white border-slate-200",
    iconColor: "text-purple-600",
    iconBg: "bg-purple-50",
  },
  {
    title: "Risk Mitigation",
    description: "Identify non-standard clauses and compliance risks before you sign.",
    icon: ShieldAlert,
    className: "md:col-span-1 md:row-span-1 bg-white border-slate-200",
    iconColor: "text-rose-600",
    iconBg: "bg-rose-50",
  },
  {
    title: "Lightning Fast",
    description: "Turn around redlines in minutes, not days.",
    icon: Zap,
    className: "md:col-span-1 md:row-span-1 bg-white border-slate-200",
    iconColor: "text-amber-600",
    iconBg: "bg-amber-50",
  }
];

export function Features() {
  return (
    <section id="features" className="py-24 bg-slate-50 relative">
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 tracking-tight mb-4">
            The Complete Toolkit
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl">
            Everything you need to streamline contract negotiations and maintain perfect compliance across your organization.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 md:grid-rows-2 gap-6 auto-rows-[200px] md:auto-rows-[220px]">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className={`group relative overflow-hidden rounded-3xl border p-8 transition-all hover:shadow-xl hover:-translate-y-1 flex flex-col justify-between ${feature.className}`}
            >
              <div>
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center mb-6 ${feature.iconBg}`}>
                  <feature.icon className={`w-6 h-6 ${feature.iconColor}`} />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2 tracking-tight">{feature.title}</h3>
                <p className="text-slate-600 leading-relaxed text-sm md:text-base">{feature.description}</p>
              </div>
              
              {/* Decorative subtle background icon */}
              <feature.icon className="absolute -bottom-6 -right-6 w-32 h-32 opacity-[0.03] text-slate-900 group-hover:scale-110 group-hover:rotate-6 transition-transform duration-500 pointer-events-none" />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
