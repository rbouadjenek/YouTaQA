# Description of the datasets

## 1- SQuAD2.0: The Stanford Question Answering Dataset

### What is SQuAD?
Stanford Question Answering Dataset (SQuAD) is a reading comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.

SQuAD2.0 combines the 100,000 questions in SQuAD1.1 with over 50,000 unanswerable questions written adversarially by crowdworkers to look similar to answerable ones. To do well on SQuAD2.0, systems must not only answer questions when possible, but also determine when no answer is supported by the paragraph and abstain from answering.

**Website:** https://rajpurkar.github.io/SQuAD-explorer/

## 2- HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering
### What is HotpotQA?
HotpotQA is a question answering dataset featuring natural, multi-hop questions, with strong supervision for supporting facts to enable more explainable question answering systems. It is collected by a team of NLP researchers at Carnegie Mellon University, Stanford University, and Université de Montréal.

**Website:** https://hotpotqa.github.io/

## 3- QuAC: Question Answering in Context

### What is QuAC?
Question Answering in Context is a dataset for modeling, understanding, and participating in information seeking dialog. Data instances consist of an interactive dialog between two crowd workers: (1) a student who poses a sequence of freeform questions to learn as much as possible about a hidden Wikipedia text, and (2) a teacher who answers the questions by providing short excerpts (spans) from the text. QuAC introduces challenges not found in existing machine comprehension datasets: its questions are often more open-ended, unanswerable, or only meaningful within the dialog context.

### Is QuAC exactly like SQuAD 2.0?
No, QuAC shares many principles with SQuAD 2.0 such as span based evaluation and unanswerable questions (including website design principles! Big thanks for sharing the code!) but incorporates a new dialog component. We expect models can be easily evaluated on both resources and have tried to make our evaluation protocol as similar as possible to their own.


**Website:** https://quac.ai/

## 4- CoQA: A Conversational Question Answering Challenge 

### What is CoQA?
CoQA is a large-scale dataset for building Conversational Question Answering systems. The goal of the CoQA challenge is to measure the ability of machines to understand a text passage and answer a series of interconnected questions that appear in a conversation. CoQA is pronounced as coca .

CoQA contains 127,000+ questions with answers collected from 8000+ conversations. Each conversation is collected by pairing two crowdworkers to chat about a passage in the form of questions and answers. The unique features of CoQA include 1) the questions are conversational; 2) the answers can be free-form text; 3) each answer also comes with an evidence subsequence highlighted in the passage; and 4) the passages are collected from seven diverse domains. CoQA has a lot of challenging phenomena not present in existing reading comprehension datasets, e.g., coreference and pragmatic reasoning.

**Website:** https://stanfordnlp.github.io/coqa/
