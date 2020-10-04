import sys
import os
import json
import getopt
import lucene
import string
import numpy as np
import tensorflow as tf

from tqdm import tqdm
from search import Searcher
from tensorflow import keras
from tensorflow.keras import layers
from tokenizers import BertWordPieceTokenizer
from transformers import BertTokenizer, TFBertModel
from org.apache.lucene.search.similarities import *
from transformers import BertConfig


max_len = 500
# Save the slow pretrained tokenizer
slow_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
save_path = "bert_base_uncased/"
if not os.path.exists(save_path):
    os.makedirs(save_path)
slow_tokenizer.save_pretrained(save_path)

# Load the fast tokenizer from saved file
tokenizer = BertWordPieceTokenizer("bert_base_uncased/vocab.txt", lowercase=True)

def create_model():
    ## BERT encoder
    encoder = TFBertModel.from_pretrained("bert-base-uncased")
    
    # QA Model
    input_ids = layers.Input(shape=(max_len,), dtype=tf.int32)
    token_type_ids = layers.Input(shape=(max_len,), dtype=tf.int32)
    attention_mask = layers.Input(shape=(max_len,), dtype=tf.int32)
    output = encoder(
        input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask
    )[1]
    
    output = layers.Dense(1, use_bias=True)(output)
    output = layers.Activation(keras.activations.sigmoid)(output)


    model = keras.Model(
        inputs=[input_ids, token_type_ids, attention_mask],
        outputs=output,
    )

    model.compile()
    return model

class Example:
    def __init__(self, question, context):
        self.question = question
        self.context = context
        self.skip = False

    def preprocess(self):
        context = self.context
        question = self.question

        # Clean context, answer and question
        context = " ".join(str(context).split())
        question = " ".join(str(question).split())

        # Tokenize context
        tokenized_context = tokenizer.encode(context)

        # Tokenize question
        tokenized_question = tokenizer.encode(question)

        # Create inputs
        input_ids = tokenized_context.ids + tokenized_question.ids[1:]
        token_type_ids = [0] * len(tokenized_context.ids) + [1] * len(tokenized_question.ids[1:])
        attention_mask = [1] * len(input_ids)

        # Pad and create attention masks.
        # Skip if truncation is needed
        padding_length = max_len - len(input_ids)
        if padding_length > 0:  # pad
            input_ids = input_ids + ([0] * padding_length)
            attention_mask = attention_mask + ([0] * padding_length)
            token_type_ids = token_type_ids + ([0] * padding_length)
        elif padding_length < 0:  # skip
            tokenized_context_ = []
            m = len(tokenized_context.ids) + padding_length - 1
            
            i = 0
            for item in tokenized_context.ids:
              if i > m:
                break
              else:
                tokenized_context_.append(item)
                i += 1
            
            input_ids = tokenized_context_ + tokenized_question.ids[1:]
            token_type_ids = [0] * len(tokenized_context_) + [1] * len(tokenized_question.ids[1:])
            attention_mask = [1] * len(input_ids)

        self.input_ids = input_ids
        self.token_type_ids = token_type_ids
        self.attention_mask = attention_mask
        self.context_token_to_char = tokenized_context.offsets
        self.context = context

class ResultsGenerator:
    def __init__(self, index_dir):
        self.searcher = Searcher(index_dir)

    def get_id_section(self, request):
        idList = list()
        for i in range(len(request)):
            hitDoc = self.searcher.searcher.doc(request[i].doc)
            idList.append(hitDoc.get("id_section"))
        return idList

    def process(self, input_file, index_dir, output_dir):
        output_file_1 = open(
            output_dir + "/results.txt", 'a+', encoding="utf-8")

        num_lines = 0
        with open(input_file, encoding="utf-8") as json_file:
            data = json.load(json_file)
            for p in data['data']:
                for par in p['paragraphs']:
                    for q in par["qas"]:
                        num_lines += 1

        model = create_model()
        model.load_weights("Model-2e-5-0.2.h5")

        with tqdm(total=num_lines) as pbar:
            with open(input_file, encoding="utf-8") as json_file:
                data = json.load(json_file)
                for p in data['data']:
                    for par in p['paragraphs']:
                        for q in par["qas"]:
                            pbar.update(1)
                            if q["is_impossible"] is False:
                                result = self.searcher.simpleSearch(q["question"], BM25Similarity())
                                ids = []
                                if(result == []):
                                    output_file_1.write('"'+str(q['id'])+'": "",\n')
                                    continue

                                content = ""
                                tab = ['']
                                tab.append(q["question"])
                                tab.pop(0)

                                for i in range(len(result)):
                                    hitDoc = self.searcher.searcher.doc(result[i].doc)
                                    content = hitDoc.get("content_section")
                                    tab.append(str(content))
                                    ids.append(hitDoc.get("id_section"))

                                inputs = []
                                for i in range(1, len(tab)):
                                    inputs.append([tab[0],tab[i]])
                            
                                # tokenization
                                squad_examples = []

                                for i in inputs:
                                    question = i[0]
                                    context = i[1]
                                    squad_eg = Example(q["question"], context)
                                    squad_eg.preprocess()
                                    squad_examples.append(squad_eg)

                                dataset_dict = {"input_ids": [],
                                                "token_type_ids": [],
                                                "attention_mask": [],}
                                for item in squad_examples:
                                    if item.skip == False:
                                        for key in dataset_dict:
                                            dataset_dict[key].append(getattr(item, key))
                                for key in dataset_dict:
                                    dataset_dict[key] = np.array(dataset_dict[key])

                                x = [dataset_dict["input_ids"],
                                    dataset_dict["token_type_ids"],
                                    dataset_dict["attention_mask"]]

                                y_pred = model.predict(x)
                                
                                sorted_indexes = sorted(range(len(y_pred)), key=lambda k: y_pred[k], reverse=True)
                                
                                r = 1
                                for i in sorted_indexes:
                                    output_file_1.write(
                                        q["id"] + " Q0 " + str(ids[i]) + " " + str(r) + " " + str(y_pred[i][0]) + " STANDARD\n")
                                    r += 1
        print("==> Results successfully created.\n")

def main(argv):
    """
    Main function that read input arguments to lunch the script.
    :param argv:
    :return:
    """

    input_file = ''
    output_dir = ''
    index_dir = ''
    try:
        opts, args = getopt.getopt(
            argv, "hi:d:o:", ["ifile=", "dfile=", "ofile="])
    except getopt.GetoptError:
        print('generate_classifier_results.py -i <input_file> -d <index_dir> -o <output_folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'generate_classifier_results.py -i <input_file> -d <index_dir> -o <output_folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
            if not os.path.isfile(input_file):
                print(input_file + ' does not exist.')
                print("\n")
                sys.exit(2)
        elif opt in ("-o", "--ofile"):
            output_dir = arg
            if not os.path.isdir(output_dir):
                print(output_dir + ' does not exist.')
                print("\n")
                sys.exit(2)
        elif opt in ("-d"):
            index_dir = arg
            if not os.path.isdir(index_dir):
                print(index_dir + ' does not exist.')
                print("\n")
                sys.exit(2)

    if input_file != '' and output_dir != '' and index_dir != '':
        rg = ResultsGenerator(index_dir)
        rg.process(input_file, index_dir, output_dir)
    else:
        print('generate_classifier_results.py -i <input_file> -d <index_dir> -o <output_folder>')
        sys.exit(2)


if __name__ == "__main__":
    """
    The main function.
    """
    main(sys.argv[1:])
