import torch
import numpy as np

from transformers import BertForSequenceClassification
from transformers import BertTokenizer
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader, SequentialSampler
from transformers import BertTokenizer, BertForQuestionAnswering
import torch

inputs = [["What famous snowbaorder lives in southern California?", "Southern California is also home to a large home grown surf and skateboard culture. Companies such as Volcom, Quiksilver, No Fear, RVCA, and Body Glove are all headquartered here. Professional skateboarder Tony Hawk, professional surfers Rob Machado, Tim Curran, Bobby Martinez, Pat O'Connell, Dane Reynolds, and Chris Ward, and professional snowboarder Shaun White live in southern California. Some of the world's legendary surf spots are in southern California as well, including Trestles, Rincon, The Wedge, Huntington Beach, and Malibu, and it is second only to the island of Oahu in terms of famous surf breaks. Some of the world's biggest extreme sports events, including the X Games, Boost Mobile Pro, and the U.S. Open of Surfing are all in southern California. Southern California is also important to the world of yachting. The annual Transpacific Yacht Race, or Transpac, from Los Angeles to Hawaii, is one of yachting's premier events. The San Diego Yacht Club held the America's Cup, the most prestigious prize in yachting, from 1988 to 1995 and hosted three America's Cup races during that time."] ]   

x = np.array(inputs)
question = x[0,0]


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
model.load_state_dict(torch.load('Models/BERT_ft_epoch10.model', map_location=torch.device(device)), strict=False)
predictions = evaluate(dataloader)
preds_flat = np.argmax(predictions, axis=1).flatten()                                                      
values = predictions[:,1]
answer = x[np.where(values == max(values)),1]                                                    
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

text = str(answer)
q = question

encoding = tokenizer.encode_plus(q, text)
input_ids, token_type_ids = encoding["input_ids"], encoding["token_type_ids"]

start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
all_tokens = tokenizer.convert_ids_to_tokens(input_ids)

a = ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])
print(a)                                                
                                                                              
                        
                        
                        