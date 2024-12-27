import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from numpy.linalg import norm

phobert = AutoModel.from_pretrained("vinai/phobert-base-v2")
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")


def get_embed(sentence):
    input_ids = torch.tensor([tokenizer.encode(sentence)])

    with torch.no_grad():
        features = phobert(input_ids)
        return np.array(list(features['pooler_output'][0]))


def get_all_embed(data):
    result = []
    for dt in data:
        result.append(get_embed(dt))
    return np.array(result)


def get_num_text(sentence, text_data, amr_data, num):
    embed_sentence = get_embed(sentence)
    embed_all = get_all_embed(text_data)
    cosin_similar = np.dot(embed_all, embed_sentence) / ((norm(embed_all, axis=1)) * norm(embed_sentence))
    sorted_indices = np.argsort(cosin_similar)[::-1][:num]
    result_text = []
    result_amr = []
    for i in sorted_indices:
        result_text.append(text_data[i])
        result_amr.append(amr_data[i])
    return result_text, result_amr
