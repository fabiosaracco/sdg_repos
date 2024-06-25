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
    for key in sdgs_dict.keys():
        which=int(key.split(':')[0].split(' ')[1])-1
        sdgs_vec[which]=1
    return sdgs_vec


def text2dict(text):
    # the information contained here is the same of the entire text, but organised per SDG...
    sdgs_dict={}
    counter=0
    # the issue is that there are plenty of entries that do not meet any rigorous pattern, 
    # therefore the only way out is to consider as a description of the activities over an SDGs
    # everything that is between the names of two different SDGs
    aux=text.split('\n')
    if all([sdg in aux for sdg in sdgs]):
        # well-behaving text
        w_sdgs=[np.where(np.array(aux)==sdg)[0][0] for sdg in sdgs]

        for i_sdg, sdg in enumerate(sdgs):
            if i_sdg<len(sdgs)-1:
                my_text=aux[w_sdgs[i_sdg]+1:w_sdgs[i_sdg+1]]
            else:
                my_text=aux[w_sdgs[i_sdg]+1:]
            if type(my_text)==list:
                my_text=' '.join(my_text)
            if 'Not explicitly mentioned' not in my_text:
                sdgs_dict[sdg]=my_text.replace('\u200b', '').strip()
    
        return sdgs_dict, 0
    else:
        # not well behaving text: the sdg is not divided from the rest of the text by a colon (:)
        for i_sdg, sdg in enumerate(sdgs):
            if i_sdg<len(sdgs)-1:
                my_text=text.split(sdgs[i_sdg])[1].split(sdgs[i_sdg+1])[0].replace('\n', '').strip()
            else:
                my_text=text.split(sdgs[-1])[1].strip()
            if 'Not explicitly mentioned' not in my_text:
                sdgs_dict[sdg]=my_text.replace('\u200b', '').strip()
        return sdgs_dict, 1
