import os
import re
import numpy as np
import pandas as pd
import nltk
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
import multiprocessing



doc2vec_model = Doc2Vec.load('./models/listingdoc2vec13.model')
nymerge = pd.read_csv('./Datasets/finalmergedlisting.csv')
nymerge.id = nymerge.id.astype(str)

def doc2vec(inputstring):

    userinputstr = inputstring
    userinput = userinputstr.lower().split()
    userinfervec = doc2vec_model.infer_vector(userinput, alpha = 0.025, steps = 20)
    simresult = doc2vec_model.docvecs.most_similar([userinfervec], topn=200)

    result = pd.DataFrame()

    for i in simresult:
        result = result.append(nymerge[nymerge.id == i[0]])

    return result
