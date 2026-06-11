"""
===========================================================================
MODULE 0.4 — NLP Fundamentals Reference Guide
===========================================================================

This is the most important foundational module.  Every AI/ML concept in
Tier 1-3 builds on these four pillars:

  1. Tokenization  → How computers read text
  2. Embeddings    → How computers understand meaning
  3. NER           → How computers find entities
  4. Classification → How computers make decisions

After reading this, you should be able to answer:

1. What problem does NLP solve?
   → Computers don't understand words.  NLP converts human language
     into numbers that machine learning algorithms can process.

2. Why is this important for Legal AI?
   → Legal contracts are UNSTRUCTURED TEXT.  NLP is the bridge between
     a raw PDF and structured predictions like "this clause is
     INDEMNITY with risk score 8.5".

3. How does it work internally?
   → Text → Tokenisation → Numerical Representation → Model → Prediction

4. What alternatives exist?
   → Rule-based (regex), Statistical (TF-IDF + ML), Neural (Transformers)
     We build all three in this project, starting with the simplest.

5. What metrics evaluate it?
   → Accuracy, Precision, Recall, F1-Score, Confusion Matrix.

6. How would I explain it in an interview?
   → "I built a baseline clause classifier using TF-IDF and Logistic
      Regression to establish performance benchmarks.  The baseline
      achieved X% F1-score, which I later improved to Y% by fine-tuning
      Legal-BERT — a 15% relative improvement that demonstrates the
      value of domain-specific pre-training."

===========================================================================
"""


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 1: TOKENIZATION
# ═══════════════════════════════════════════════════════════════════════════
#
# Tokenization = splitting text into smaller units (tokens).
#
# There are 3 levels of tokenization:
#
# ┌────────────────────────────────────────────────────────────────────┐
# │ Level       │ Input                      │ Output                  │
# ├─────────────┼────────────────────────────┼─────────────────────────┤
# │ Word-level  │ "The Contractor shall"     │ ["The","Contractor",    │
# │             │                            │  "shall"]               │
# │ Subword     │ "indemnification"          │ ["in","dem","ni",       │
# │ (BPE/WP)    │                            │  "fication"]            │
# │ Character   │ "NDA"                      │ ["N","D","A"]           │
# └────────────────────────────────────────────────────────────────────┘
#
# YOUR CURRENT CODE uses word-level tokenization (splitting on spaces
# and periods in clause_extractor.py).
#
# Legal-BERT (Tier 1) will use SUBWORD tokenization (WordPiece).
# This is why "indemnification" gets split into pieces — the model
# has never seen the full word, but it recognises the pieces.
#
# Interview Tip:
#   Q: "Why does BERT use subword tokenization instead of word-level?"
#   A: Word-level creates a huge vocabulary and can't handle unseen words.
#      Character-level loses word meaning.  Subword (WordPiece/BPE) is
#      the sweet spot: small vocabulary (~30k tokens) that can represent
#      ANY word by combining pieces.  Legal terms like "indemnification"
#      become ["in", "##dem", "##ni", "##fication"], letting the model
#      generalise to new legal terms it hasn't been trained on.
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 2: EMBEDDINGS (Text → Numbers)
# ═══════════════════════════════════════════════════════════════════════════
#
# A computer can't multiply the word "indemnify".  We need to convert
# words into VECTORS (lists of numbers).
#
# There are 3 embedding approaches, from simple to advanced:
#
# ┌─────────────────────────────────────────────────────────────────────┐
# │ Method     │ How it works              │ Captures meaning?         │
# ├────────────┼───────────────────────────┼───────────────────────────┤
# │ Bag of     │ Count word frequency      │ No. "dog bites man" =     │
# │ Words      │ Sparse vector             │ "man bites dog"           │
# │            │                           │                           │
# │ TF-IDF     │ Word frequency weighted   │ Slightly. Rare words get  │
# │            │ by rarity (inverse doc    │ higher weight (important  │
# │            │ frequency)                │ for legal jargon!)        │
# │            │                           │                           │
# │ Dense      │ Neural network learns     │ Yes! "indemnify" is close │
# │ (Word2Vec, │ 300-768 dimensional       │ to "hold harmless" in     │
# │ BERT)      │ vectors from context      │ vector space              │
# └─────────────────────────────────────────────────────────────────────┘
#
# OUR BASELINE uses TF-IDF (Tier 0).
# Legal-BERT will use Dense Embeddings (Tier 1).
# FAISS Semantic Search will use Sentence Transformers (Tier 1).
#
# Interview Tip:
#   Q: "Why is TF-IDF good for legal text?"
#   A: Legal contracts have highly domain-specific vocabulary.  Words
#      like "indemnification", "force majeure", "liquidated damages"
#      are RARE in general English but CRITICAL in contracts.  TF-IDF
#      naturally upweights these rare, informative terms because their
#      Inverse Document Frequency (IDF) is high.
#
#   Q: "What's the limitation of TF-IDF?"
#   A: It treats every word independently (bag-of-words assumption).
#      "The contractor shall NOT indemnify" and "The contractor SHALL
#      indemnify" have almost identical TF-IDF vectors, but opposite
#      meanings.  This is why we upgrade to BERT, which understands
#      CONTEXT and word order.
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 3: NAMED ENTITY RECOGNITION (NER)
# ═══════════════════════════════════════════════════════════════════════════
#
# NER finds and classifies named entities in text:
#
#   "Acme Corp shall pay Google Inc $5,000,000 by December 31, 2026"
#    ^^^^^^^^^ ORG             ^^^^^^^^^^ ORG  ^^^^^^^^^^ MONEY
#                                                ^^^^^^^^^^^^^^^^ DATE
#
# For Legal AI, the important entities are:
#   - PARTY:  "Contractor", "Client", "Acme Corp"
#   - MONEY:  "$5,000,000", "USD 10,000"
#   - DATE:   "December 31, 2026", "30 days"
#   - CLAUSE: "Section 5.2", "Article III"
#
# We won't build a full NER system in Tier 0, but you should understand
# the concept because the Knowledge Graph (Tier 2) will use entity
# extraction to build nodes:
#
#   [Acme Corp] ──(shall pay)──▶ [Google Inc]
#                    │
#                [$5,000,000]
#
# Interview Tip:
#   Q: "How would you extract parties from a legal contract?"
#   A: Three approaches:
#      1. Rule-based: regex for patterns like "hereinafter the 'Client'"
#      2. spaCy NER: Pre-trained model recognises ORG, PERSON, DATE
#      3. Fine-tuned BERT: Train on legal NER datasets for legal-specific
#         entities like PARTY, OBLIGATION, CONDITION.
#      I'd start with spaCy (fast, good enough) and upgrade to BERT
#      if accuracy is insufficient.
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 4: TEXT CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════════
#
# This is the CORE task of your project:
#   Input:  "The Contractor shall indemnify and hold harmless..."
#   Output: INDEMNITY (confidence: 0.94)
#
# The ML pipeline is:
#
#   Raw Text
#      ↓
#   Preprocessing (lowercase, remove punctuation, tokenize)
#      ↓
#   Feature Extraction (TF-IDF vectors)
#      ↓
#   Classifier (Logistic Regression / SVM / BERT)
#      ↓
#   Prediction (clause_type + confidence)
#
# We will build this EXACT pipeline in `app/models/baseline_classifier.py`.
#
# Interview Tip:
#   Q: "Why start with Logistic Regression instead of going straight to BERT?"
#   A: Three reasons:
#      1. BASELINE: You need a simple model to compare against.
#         If BERT only beats LogReg by 1%, the complexity isn't worth it.
#      2. SPEED: LogReg trains in seconds, BERT takes hours on GPU.
#         For rapid iteration and debugging, a fast baseline is essential.
#      3. INTERPRETABILITY: LogReg gives you feature weights — you can
#         see exactly which words drive the prediction.  BERT is a
#         black box (which is why we add SHAP in Tier 2).
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 5: EVALUATION METRICS
# ═══════════════════════════════════════════════════════════════════════════
#
# After building a classifier, how do you know if it's GOOD?
#
# ┌──────────────────────────────────────────────────────────────────────┐
# │ Metric     │ What it measures                │ When to use          │
# ├────────────┼─────────────────────────────────┼──────────────────────┤
# │ Accuracy   │ % of correct predictions        │ Balanced datasets    │
# │ Precision  │ Of predicted INDEMNITY, how     │ When false positives │
# │            │ many are actually INDEMNITY?    │ are expensive        │
# │ Recall     │ Of actual INDEMNITY clauses,    │ When missing a       │
# │            │ how many did we find?           │ clause is dangerous  │
# │ F1-Score   │ Harmonic mean of P and R        │ Imbalanced datasets  │
# │ Confusion  │ Full matrix of predictions      │ Always! Shows where  │
# │ Matrix     │ vs actual labels                │ the model fails      │
# └──────────────────────────────────────────────────────────────────────┘
#
# For LEGAL AI, Recall is more important than Precision.
# Missing a high-risk INDEMNITY clause (false negative) is worse
# than flagging a PAYMENT clause as INDEMNITY (false positive).
#
# Interview Tip:
#   Q: "Your model has 95% accuracy.  Is it good?"
#   A: NOT NECESSARILY.  If 90% of clauses are GENERAL, a model that
#      always predicts GENERAL gets 90% accuracy but is useless.
#      This is the ACCURACY PARADOX.  I always report F1-score
#      (especially macro-F1 for multi-class) and check the confusion
#      matrix for per-class performance.  For legal AI, I weight
#      recall higher because missing a risky clause has real
#      consequences.
#
