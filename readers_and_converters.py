import pickle

from docx import Document
import numpy as np

with open('./data/sdgs.pickle', 'rb') as f:
    sdgs=pickle.load(f)

def file2text(file):
    doc=Document(file)
    full_text=''
    for par in doc.paragraphs:
        full_text+='\n'+par.text
    return full_text
    

def text2vec(sdgs_dict):
    # Here I brutally binarized by presence/absence of mention in the report of the given SDG
    # there are 17 sdgs, starting from the entries from text2dict
    sdgs_vec=np.zeros(17, dtype=int)
    for key in sdg_dict.keys():
        which=int(key.split(':')[0].split(' ')[1])-1
        sdgs_vec[which]=1
    return sdgs_vec


def text2dict(text):
    # the information contained here is the same of the entire text, but organised per SDG...
    sdgs_dict={}
    counter=0
    aux=text.split('\n')
    while counter<len(aux):
        _a=aux[counter]

        if len(_a)>0:
            if 'SDG' in _a:
                sdg=[sdg for sdg in sdgs if sdg in _a]
                if len(sdg)==1:
                    sdg=sdg[0]
                    # well-behaving text
                    if _a==sdg and 'Not explicitly mentioned' not in aux[counter+1]:
                        sdgs_dict[_a]=aux[counter+1]
                        counter+=2
                    elif _a==sdg and 'Not explicitly mentioned' in aux[counter+1]:
                        counter+=2
                    else:
                        # not well-behaving text
                        _text=_a.split(sdg)[1]
                        if 'Not explicitly mentioned' not in _text:
                            sdgs_dict[sdg]=_text.strip().replace('\u200b', '')
                        counter+=1
                else:
                    counter+=1
            else:
                counter+=1
        else:
            counter+=1
    return sdgs_dict