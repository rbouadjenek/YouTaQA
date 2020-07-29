# YouTaQA
YouTaQA is a powerful Q&A system that provides a complete pipeline. Unlike existing QA systems, our system allows users to have accurate answers to their questions based entirely on our search engine, saving the user from having to provide anything other than the question, and possibly making their task easier.
To achieve the objective of our system, as shown in the general diagram, we designed an architecture composed of three basic modules and an interface to interact with the user:
- A search engine (MRI) that serves to provide the 5 most relevant passages to a given question.
- A module of context classiﬁcation (MC) based on BERT to choose and identiﬁer among the 5 search engine results the best passage likely to contain the correct answer to the question.
- Answer Extraction module (MER) based on BERT that extracts the correct answer from the passage chosen by classiﬁeur in the previous step.
![GitHub Logo](/Paper/Figures/schema global.png)
Format: ![Alt Text](url)
