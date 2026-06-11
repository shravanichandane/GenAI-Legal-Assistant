# LegalSight AI: System Design & Architecture

This document serves as the formal architectural blueprint and system design rationale for LegalSight AI. It is structured to meet the rigorous standards of Big Tech (Google/Meta) system design interviews and academic research program (e.g., MBZUAI) evaluations.

---

## 1. Problem Statement

Design an **Enterprise Legal Document Intelligence System** that can:
* Ingest large legal contracts (PDF / text)
* Extract and classify clauses
* Retrieve relevant legal precedents
* Apply company-specific legal policies (playbooks)
* Generate risk assessments
* Support human review + feedback learning loop
* Operate in a secure multi-tenant SaaS environment

---

## 2. High-Level Architecture Diagram

```text
                    ┌────────────────────────────┐
                    │     Next.js Frontend       │
                    │  (Lawyer / Partner UI)     │
                    └────────────┬───────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │   FastAPI Gateway Layer    │
                    │ JWT + RBAC + Tenant Guard  │
                    └────────────┬───────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Document NLP │     │ Playbook Engine  │     │ Audit Logger     │
│ Legal-BERT   │     │ Firm Policies    │     │ Compliance Log   │
└──────┬───────┘     └────────┬─────────┘     └──────────────────┘
       │                      │
       ▼                      ▼
┌────────────────────────────────────────────┐
│        Clause Representation Layer         │
│     (Structured Legal Clause Nodes)       │
└────────────────────┬───────────────────────┘
                     ▼
        ┌──────────────────────────────┐
        │  Retrieval System (FAISS)    │
        │  + Embedding Encoder         │
        └────────────┬─────────────────┘
                     ▼
        ┌──────────────────────────────┐
        │ Cross-Encoder Reranker       │
        │ (DeBERTa / MiniLM CE)        │
        └────────────┬─────────────────┘
                     ▼
        ┌──────────────────────────────┐
        │ Context Builder (RAG Layer)  │
        │ + Evidence Selector          │
        └────────────┬─────────────────┘
                     ▼
        ┌──────────────────────────────┐
        │ Gemini LLM Generator         │
        │ (Grounded Recommendations)   │
        └────────────┬─────────────────┘
                     ▼
        ┌──────────────────────────────┐
        │ Risk Intelligence Engine     │
        │ (Deterministic + ML scoring) │
        └────────────┬─────────────────┘
                     ▼
        ┌──────────────────────────────┐
        │ Explainability Layer         │
        │ (Traceability Graph Engine)  │
        └────────────┬─────────────────┘
                     ▼
        ┌──────────────────────────────┐
        │ Human Review System          │
        │ Approve / Reject / Modify    │
        └────────────┬─────────────────┘
                     ▼
        ┌──────────────────────────────┐
        │ PostgreSQL (Neon SaaS DB)    │
        │ Multi-tenant + Audit Logs    │
        └──────────────────────────────┘
```

---

## 3. Key System Design Decisions

### 3.1. Why a Multi-Stage Pipeline instead of a Single LLM?
We intentionally avoided an “LLM-only design” (e.g., just passing the PDF to GPT-4). Legal systems require **determinism, auditability, and absolute truth**. A hybrid system (Symbolic + Neural + Generative AI) allows us to enforce institutional policy constraints *before* the LLM hallucinates legal judgments.

### 3.2. Two-Stage Retrieval (FAISS + Cross Encoder)
We split retrieval to balance speed and accuracy:
* **Bi-Encoder (MiniLM / Legal-BERT):** Fast vector retrieval (Top-K candidates).
* **Cross-Encoder (DeBERTa):** High-precision reranking to ensure strict semantic relevance before passing context to the LLM.

### 3.3. The Playbook Engine (Pre-LLM Conditioning)
Instead of letting the LLM act as the final authority on law, we inject firm-specific constraints (e.g., Liability Caps, missing mandatory clauses) into the prompt context. The LLM acts as an assistant synthesizing the rule against the text, not the judge.

### 3.4. Hybrid Risk Scoring
We utilize a hybrid deterministic/statistical scoring system:
`Final Score = Rule Violations + Retrieval Similarity + ML Clause Severity + Missing Penalties`
This ensures risk scores are mathematically reproducible.

### 3.5. Explainability Layer (Trust-by-Design)
Every output requires an Evidence Trace:
1. Clause Source ID
2. Playbook Rule Violated
3. Retrieval Evidence (FAISS IDs)
4. Confidence Scores
This makes the AI defensible and enterprise-ready for legal professionals.

### 3.6. MLOps Feedback Loop
We built a pipeline to support RLHF-style feedback ingestion. When a lawyer clicks "Approve with Edits," the delta between the AI's redline and the lawyer's edit is logged. While continuous training is scoped for future work, the data pipeline to capture this signal is fully operational.
