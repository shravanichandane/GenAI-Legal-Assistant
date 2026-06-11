# ⚖️ LegalSight AI: Enterprise Legal Intelligence OS

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)
![Next.js](https://img.shields.io/badge/Next.js-14.0-black.svg)
![Tailwind](https://img.shields.io/badge/Tailwind-3.3-38B2AC.svg)

**LegalSight AI** is a production-grade, end-to-end Enterprise Legal Intelligence Operating System. 

It transcends traditional "AI Chatbots" by providing a complete, deterministic pipeline that shatters complex legal PDFs, classifies clauses using **Legal-BERT**, retrieves precedents via **FAISS Vector Search**, reranks context using **Cross-Encoders**, and synthesizes risk using **GenAI (LLMs)**—all wrapped in a strictly governed, multi-tenant SaaS architecture.

## 🧠 The End-to-End Mental Model

```text
User Uploads Contract ➔ NLP (Legal-BERT) ➔ Semantic Structuring (Parser) ➔ Playbook Matching ➔ Vector Retrieval (FAISS) ➔ Reranking (Cross Encoder) ➔ LLM Reasoning (Gemini) ➔ Risk Engine (Data Science) ➔ Explainability Layer ➔ Human Review (Lawyer) ➔ Feedback Loop (MLOps) ➔ Analytics Dashboard
```

---

## 🏗️ Core Architecture & Subsystems

### 1. NLP Layer (Clause Intelligence)
Instead of forcing lawyers to read 50-page PDFs line-by-line, LegalSight utilizes a fine-tuned **Legal-BERT** Transformer model to semantically segment text into 40+ legal categories (e.g., Liability, Indemnification). 
* **UI Mapping:** The Frontend binds semantic segmentation to UI navigation. Clicking "Liability Caps" in the Clause Index instantly scrolls and highlights the exact paragraph in the Document Viewer.

### 2. RAG + Retrieval Layer (FAISS + Cross-Encoder + Gemini)
When a clause is extracted, it undergoes a complex Retrieval-Augmented Generation pipeline:
* `FAISS` retrieves the Top-20 similar historical precedents.
* A `Cross-Encoder` reranks the precedents for strict semantic relevance.
* `Gemini` evaluates the clause against the firm's strict Playbook parameters.
* **UI Mapping (Evidence Trace):** To build *trust-by-design*, the UI exposes the exact FAISS ID, Rerank Score, and Playbook Rule violated, replacing black-box AI with mathematical and legal explainability.

### 3. Risk Engine (Data Science Layer)
Aggregates clause-level risk into a holistic contract-level score using a weighted deterministic model:
`Risk Score = (0.3 × clause severity) + (0.2 × playbook violation) + (0.2 × missing clauses) + (0.3 × historical risk)`
* **UI Mapping:** A Partner-level Analytics Dashboard visualizing risk distribution over time and clause heatmaps.

### 4. Playbook System (Enterprise Knowledge)
A dynamic control plane where Senior Partners can modify clause rules, update financial thresholds (e.g., Liability Caps), and define fallback language. This turns the system into an AI that strictly adapts to law firm policy.

### 5. Human-in-the-Loop Learning (MLOps)
The system creates a continuous learning loop. When a lawyer modifies an AI output and clicks "Approve with Edits," the delta is stored and logged, feeding directly into a future RLHF (Reinforcement Learning from Human Feedback) training dataset.

### 6. Enterprise Security & Multi-Tenancy
* Stateless JWT Authentication & Role-Based Access Control (RBAC).
* PostgreSQL (Neon) strict tenant isolation.

---

## 💻 Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy, Celery, Redis.
* **AI / ML:** HuggingFace Transformers (Legal-BERT, Cross-Encoders), FAISS, LangChain, Google Gemini API.
* **Frontend:** Next.js 14 (App Router), React, Tailwind CSS, Framer Motion, Shadcn UI.
* **Database:** PostgreSQL (Neon Serverless).

## 🚀 Getting Started

### Backend Setup
```bash
# Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
# Install dependencies and run Next.js
cd frontend
npm install
npm run dev
```