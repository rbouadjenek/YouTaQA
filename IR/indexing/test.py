import lucene
import wiki_extractor
from org.apache.lucene.search.similarities import *
from search import Searcher
from similarity import Similarity

import torch
import numpy as np

from transformers import BertForSequenceClassification
from transformers import BertTokenizer
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader, SequentialSampler
from transformers import BertTokenizer, BertForQuestionAnswering
import torch

inputQuery = ""
inputQuery = input("Enter your request, otherwise tape 'exit' to exit\n")
searchObject = Searcher("/Users/younesagabi/Desktop/YouTaQA/IR/index_wiki_v7.0")
result = searchObject.multiFieldsSearch(inputQuery, BM25Similarity())
# print(result)
# print("#" * 100)
# print("#" * 100)
content = ""
tab=['']
tab.append(inputQuery)
tab.pop(0)
j=0
for i in range(len(result)):
    hitDoc = searchObject.searcher.doc(result[i].doc)
    score = result[i].score
    content = hitDoc.get("content_section")
    tab.append(content)
    # print("#"*100)
    id = hitDoc.get("id_section")
        #print(id)
        #print(tab[j])
        #print("#"*100)
        #print("#"*100)  
# print(tab)    
searchObject.reader.close()
searchObject.directory.close()

inputs = [[tab[0],tab[1]],[tab[0],tab[2]],[tab[0],tab[3]],[tab[0],tab[4]],[tab[0],tab[5]]]
x = np.array(inputs)
question = x[0,0]

# print(x)


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

encoded_data = tokenizer.batch_encode_plus(
    zip(x[:,0],x[:,1]), 
    add_special_tokens=True, 
    return_attention_mask=True, 
    pad_to_max_length=True, 
    max_length=256, 
    return_tensors='pt'
)

input_ids = encoded_data['input_ids']
attention_masks = encoded_data['attention_mask']

dataset = TensorDataset(input_ids, attention_masks)

dataloader = DataLoader(dataset,
                        sampler=SequentialSampler(dataset),
                        batch_size=32)
                        
model = BertForSequenceClassification.from_pretrained('bert-base-uncased',
                                                      num_labels=2,
                                                      output_attentions=False,
                                                      output_hidden_states=False)
                                                      
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.load_state_dict(torch.load('/Users/younesagabi/Desktop/YouTaQA/DeepLearning/Classifier/Models/BERT_ft_epoch10.model', map_location=torch.device(device)), strict=False)
def evaluate(dataloader_val):

    model.eval()
    predictions, true_vals = [], []
    
    for batch in dataloader_val:
        
        batch = tuple(b.to(device) for b in batch)
        
        inputs = {'input_ids':      batch[0],
                  'attention_mask': batch[1],
                 }

        outputs = model(**inputs)
            
        logits = outputs[0]

        logits = logits.detach().cpu().numpy()
        predictions.append(logits)
    
    predictions = np.concatenate(predictions, axis=0)
            
    return predictions
  
predictions = evaluate(dataloader)
preds_flat = np.argmax(predictions, axis=1).flatten()                                                      
values = predictions[:,1]
answer = x[np.where(values == max(values)),1]                                                    
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

text = str(answer)
q = question
encoding = tokenizer.encode_plus(q, text, max_length=256)
input_ids, token_type_ids = encoding["input_ids"], encoding["token_type_ids"]

start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
all_tokens = tokenizer.convert_ids_to_tokens(input_ids)

a = ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])
print(a) 
 
  

