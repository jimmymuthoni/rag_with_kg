import re
import sys, os
from loguru import logger
import pandas as pd
from utils.pdf_splitter import PDFSplitter
from exllamav2 import (
    ExLlamaV2,
    ExLlamaV2Config,
    ExLlamaV2Cache,
    ExLlamaV2Tokenizer
)

from exlallamv2.generator import (
    ExLlamaV2BaseGenerator,
    ExLlamaV2Sampler
)

def lowercase_dict(d):
    return {key: value.lower() for key, value in d.items()}

def process_results(object):
    filtered_list = [item for item in object if len(item) > 1]
    elements_to_remove = {
        'node_1': 'A concept from extracted ontology',
        'node_2': 'A related concept from extracted ontology',
        'edge': 'Relationship between the two concepts, node_1 and node_2 in one or two sentences'
    }

    filtered_list = [lowercase_dict(item) for item in filtered_list if item != elements_to_remove]
    return filtered_list

system_prompt = """
You are a network graph maker who extracts terms and their relations from a given context. 
You are provided with a context chunk (delimited by ```) Your task is to extract the ontology
of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n
Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n
\tTerms may include object, entity, location, organization, person, \n
\tcondition, acronym, documents, service, concept, etc.\n
\tTerms should be as atomistic as possible\n\n
Thought 2: Think about how these terms can have one on one relation with other terms.\n
\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n
\tTerms can be related to many other terms\n\n
Thought 3: Find out the relation between each such related pair of terms. \n\n
Format your output as a list of json. Each element of the list contains a pair of terms
and the relation between them, like the following: \n
[\n
    {\n
        "node_1": "A concept from extracted ontology",\n
        "node_2": "A related concept from extracted ontology",\n
        "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"\n
    }, {...}\n"
]"
DO NOT RETURN ANY EXPLANATION, ONLY RETURN THE LIST OF JSON.

"""

qna_prompt = """You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'.
You only respond once as Assistant. You are allowed to use only the given context below to answer the user's queries, 
and if the answer is not present in the context, say you don't know the answer.
CONTEXT: {context}
"""


class RAGLLM:
    def __init__(self,model_directory:str, temprature:float, top_k:float, top_p: float,top_a:float, token_repetition_penalty:float):
        self.model_directory = model_directory
        self.temperature = temprature
        self.top_k = top_k
        self.top_p = top_p
        self.top_a = top_a
        self.token_repetition_penalty = token_repetition_penalty
    
    