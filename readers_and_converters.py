from docx import Document
import numpy as np

def file2text(file):
    doc=Document(file)
    full_text=''
    for par in doc.paragraphs:
        full_text+='\n'+par.text
    return 
    

def text2vec(text):
    # Here I brutally binarized by presence/absence of mention in the report of the given SDG
    # there are 17 sdgs
    sdgs_vec=np.zeros(17, dtype=int)
    aux=text.split('\n')
    counter=0
    sdgs_vec_i=0
    while counter<len(aux):
        _a=aux[counter]
        if len(_a)>0:
            if _a[:3]=='SDG' and aux[counter+1]!='Not explicitly mentioned.':
                sdgs_vec[sdgs_vec_i]=1
                counter+=2
                sdgs_vec_i+=1
            elif _a[:3]=='SDG' and aux[counter+1]=='Not explicitly mentioned.':
                counter+=2
                sdgs_vec_i+=1
        else:
            counter+=1
    return sdgs_vec


def text2dict(text):
    # the information contained here is the same of the entire text, but organised per SDG...
    sdgs_dict={}
    counter=0
    aux=text.split('\n')
    while counter<len(aux):
        _a=aux[counter]
        if len(_a)>0:
            if _a[:3]=='SDG' and aux[counter+1]!='Not explicitly mentioned.':
                sdgs_dict[_a]=aux[counter+1]
                counter+=2
            elif _a[:3]=='SDG' and aux[counter+1]=='Not explicitly mentioned.':
                counter+=2
        else:
            counter+=1
    return sdgs_dict