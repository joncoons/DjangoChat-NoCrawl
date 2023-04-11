import openai
from openai.embeddings_utils import cosine_similarity
import pandas as pd
import numpy as np
import time
import re

LOADED_CSV = None

class LoadEmbeddingDF():
    def __init__(self, f_name, e_model) -> None:
        self.f_name = f_name
        self.e_model = e_model
        self.load_csv(self.f_name)

    def load_csv(self, csv_file):
        self.df=pd.read_csv(f'{csv_file}', index_col=0)
        self.df['embeddings'] = self.df['embeddings'].apply(eval).apply(np.array)

    def vector_distance(self, query):
        q_vector = self.new_embedding(query, self.e_model)
        self.df['similarity'] = self.df['embeddings'].apply(lambda x: cosine_similarity(x, q_vector))
        top_df = self.df.sort_values("similarity", ascending=False).nlargest(3, "similarity")
        returns = []
        for row in top_df.iterrows():
            if row[1]['text'] is None:
                continue
            if row[1]['text'] is not None:
                row_sentences = row[1]['text'].split(".")
                url = "https://www.openai.com/" + row_sentences[0].replace('_',"/").replace('.',"")
                returns.append('Source: \n' + row[1]['text'] + f'\n\n <a href>{url} target="_blank"<a>\n')
        return_str = ''.join(str(x) for x in returns)
        # print(return_str)
        return return_str

    def new_embedding(self, input_str, model):
        input_str = normalize_text(input_str)
        txt2embedding = openai.Embedding.create(
            input=input_str,
            engine=model,
            )["data"][0]['embedding']
        time.sleep(60/300)
        return txt2embedding

def normalize_text(input_str=str):
    input_str = re.sub(r'\s+',  ' ', input_str).strip()
    input_str = re.sub(r". ,","",input_str)
    # remove all instances of multiple spaces
    input_str = input_str.replace("..",".")
    input_str = input_str.replace(". .",".")
    input_str = input_str.replace("\n", " ")
    input_str = input_str.replace("\n\n", " ")
    input_str = input_str.replace("\\n", " ")
    input_str = input_str.replace("  ", " ")
    # input_str = input_str.strip()
    return input_str

def init_csv(f_name, e_model):
    global LOADED_CSV
    LOADED_CSV = LoadEmbeddingDF(f_name, e_model)

def new_query(query):
    response = LOADED_CSV.vector_distance(query)
    return response
