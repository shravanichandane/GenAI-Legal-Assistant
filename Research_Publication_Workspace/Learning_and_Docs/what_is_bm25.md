# What is BM25?

Before the era of AI and dense embeddings, search engines still needed a way to rank documents based on a user's query. The gold standard for this—and a technique that is still widely used today—is **BM25** (Best Matching 25).

To understand BM25, we first need to understand the building blocks of traditional Information Retrieval.

## Traditional Information Retrieval (IR)
Traditional IR relies on **lexical matching**—finding exact word overlaps between a search query and a document. 

Imagine you search for "breach of contract." A simple search engine might just count how many times those words appear in each document. The document with the highest count wins. However, this naive approach has a huge flaw: common words like "of" will heavily skew the results.

## The Foundation: TF-IDF
To fix this, scientists created **TF-IDF (Term Frequency - Inverse Document Frequency)**. It balances two key metrics:

1. **Term Frequency (TF):** How often does the word appear in *this specific document*? 
   * *More appearances = more relevant.*
2. **Inverse Document Frequency (IDF):** How common is this word across the *entire database of all documents*?
   * *If a word is everywhere (like "the" or "law"), it is less informative. If it's rare (like "habeas"), it is highly informative.*

TF-IDF multiplies these two scores together. A word gets a high score if it appears frequently in the target document, but rarely in the rest of the database.

## Enter BM25
**BM25** is an advanced, modernized version of TF-IDF. It improves upon the classic formula in two critical ways to make search results much more human-like and accurate:

### 1. Term Frequency Saturation
In standard TF-IDF, if a document mentions "contract" 100 times, it gets a massively higher score than a document mentioning it 10 times. 
BM25 recognizes that after a certain point, mentioning a word over and over again doesn't make the document infinitely more relevant. BM25 puts a "cap" (saturation curve) on the Term Frequency score. Going from 1 mention to 3 mentions is a huge jump in relevance; going from 100 to 102 mentions barely moves the needle.

### 2. Document Length Normalization
Imagine a 10-page document that mentions "fraud" 5 times, and a 1,000-page book that mentions "fraud" 5 times. The 10-page document is likely far more focused on fraud than the massive book.
BM25 adjusts scores based on the length of the document compared to the average length of all documents in the database. Shorter documents are rewarded for keyword hits, while incredibly long documents are penalized slightly to level the playing field.

## Why Does This Matter?
BM25 remains incredibly powerful because it is fast, highly interpretable, and doesn't require expensive GPUs to run. In modern systems like LegalSight AI, BM25 is often combined with Vector Search in a process called **Hybrid Search**—using BM25 to catch exact keyword matches (like specific case numbers or statutes) and Vector Search to catch conceptual meaning.
