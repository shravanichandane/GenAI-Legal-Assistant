"""
=============================================================================
Module 1.2: Understanding Legal-BERT & NLP Fundamentals
=============================================================================

Welcome to Module 1.2! In this guide, we will explore the foundational concepts 
behind Legal-BERT, a specialized AI model used for processing legal text. By the 
end of this module, you will understand how modern Natural Language Processing (NLP) 
models read, understand, and classify text.

-----------------------------------------------------------------------------
1. What is BERT? What is a Transformer?
-----------------------------------------------------------------------------
BERT (Bidirectional Encoder Representations from Transformers) is a groundbreaking 
language model developed by Google. Unlike older models that read text sequentially 
(left-to-right), BERT reads the entire sequence of words at once (bidirectionally). 
This allows it to understand the deep context and meaning of words based on their 
surroundings.

Transformers: BERT is built on an architecture called the "Transformer." The 
Transformer uses a mechanism called "Self-Attention," which allows the model to 
weigh the importance of different words in a sentence relative to each other, no 
matter how far apart they are. Think of it like reading a complex legal sentence 
and instantly knowing which clauses modify which subjects.

-----------------------------------------------------------------------------
2. What is Tokenization?
-----------------------------------------------------------------------------
Computers don't understand text; they only understand numbers. Tokenization is the 
process of breaking down text into smaller pieces called "tokens" (which can be 
words, subwords, or characters) and converting them into numerical IDs.

Example:
Sentence: "The contract is void."
Tokens: ["The", "contract", "is", "void", "."]
IDs: [101, 2034, 3056, 1023, 4087, 102]

BERT uses a specific type of tokenization called WordPiece, which can break 
unknown words into smaller subwords (e.g., "unbreakable" -> "un", "##break", "##able"). 
This ensures the model can handle almost any word it encounters.

-----------------------------------------------------------------------------
3. Why use Legal-BERT instead of standard BERT?
-----------------------------------------------------------------------------
Standard BERT was trained on general text like Wikipedia and BookCorpus. While it 
is great for everyday language, it struggles with the dense, specialized vocabulary 
and complex syntax of legal documents (legalese).

Legal-BERT, on the other hand, was pre-trained specifically on large amounts of 
legal text (contracts, court cases, legislation). As a result, it understands legal 
jargon and context much better, making it highly accurate for tasks like contract 
analysis, legal classification, and risk assessment.

-----------------------------------------------------------------------------
4. What is the CLS Token and why is it used for classification?
-----------------------------------------------------------------------------
When we feed text into BERT, we always add a special token at the very beginning 
called the `[CLS]` (Classification) token. 

As the text passes through the Transformer layers, the `[CLS]` token acts as an 
aggregator. Because of the Self-Attention mechanism, the `[CLS]` token looks at 
every other word in the sentence and gathers a summary of the entire sequence's 
meaning. By the time it reaches the final layer, the representation (vector) of the 
`[CLS]` token contains the "global context" of the input text, making it the perfect 
starting point for classification tasks (e.g., deciding if a clause is "Fair" or "Unfair").

-----------------------------------------------------------------------------
5. Embeddings vs. Logits
-----------------------------------------------------------------------------
- Embeddings: These are high-dimensional vectors (arrays of numbers) that 
  represent the meaning of a token. For example, the embedding for "contract" will 
  be mathematically closer to the embedding for "agreement" than to "apple." They 
  are the internal representations the model uses to understand text.

- Logits: These are the raw, unnormalized scores output by the final layer of our 
  classification model. For instance, if we are classifying text into 3 categories, 
  the model will output 3 logits (e.g., [2.5, -1.2, 0.8]). They represent the 
  model's raw confidence for each category, but they are not probabilities.

-----------------------------------------------------------------------------
6. Why do we apply Softmax?
-----------------------------------------------------------------------------
Logits are raw numbers that can be any value (positive or negative) and don't sum 
to 1. To make sense of them, we apply a mathematical function called "Softmax."

Softmax converts the raw logits into a probability distribution. It forces all the 
numbers to be between 0 and 1, and ensures they all add up to 1 (100%).

Example:
Logits: [2.5, -1.2, 0.8]
Softmax Probabilities: [0.82, 0.02, 0.16] -> 82% confidence for Category A.

=============================================================================
Study Notes & Takeaways
=============================================================================
- BERT = Bidirectional Context + Transformer Architecture.
- Tokenization bridges the gap between human text and machine numbers.
- Domain-specific models (like Legal-BERT) outperform general models on specialized tasks.
- `[CLS]` token holds the summary of the entire sentence for classification.
- Embeddings = Meaning; Logits = Raw Scores; Softmax = Probabilities.

=============================================================================
Interview Questions to Practice
=============================================================================
1. How does the Self-Attention mechanism in a Transformer differ from how older 
   models processed text?
2. Why is subword tokenization (like WordPiece) useful for handling rare or 
   misspelled words in legal documents?
3. In a text classification pipeline, describe the journey of the `[CLS]` token 
   from the input layer to the final output prediction.
4. If a model outputs logits of [10, 2], what does the Softmax function do to these 
   values conceptually?

=============================================================================
Mini-Exercises
=============================================================================
Exercise 1: Mental Tokenization
Take the phrase: "The lessee shall indemnify the lessor."
How might a standard tokenizer break this down? Identify which words might be 
split into subwords if the model isn't specialized for law.

Exercise 2: Logits to Probabilities
Imagine a model outputs the following logits for three classes (Fair, Unfair, Neutral): 
[1.0, 3.0, 0.5]. Without calculating exactly, which class will have the highest 
probability after applying Softmax? Why?

Exercise 3: The CLS conceptualization
Write a 2-sentence explanation of the `[CLS]` token as if you were explaining it to 
a junior lawyer with no technical background.
"""

def print_guide():
    print(__doc__)

if __name__ == "__main__":
    print_guide()
