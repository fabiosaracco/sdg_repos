import os, sys, pickle
import numpy as np
from tqdm import trange, tqdm

import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', '-t', dest='test',
                    default=False)
    return parser    


def main():
    
    parser = get_parser()
    args = parser.parse_args()
    test=bool(args.test)
    
    
    
    # load data
    with open ('./data/sdgs_dict.pickle', 'rb') as f:
        sdgs_dict=pickle.load(f)
    
    keys=list(sdgs_dict.keys())
    
    if test:
        keys=keys[:2]
        n_sample=20
    else:
        n_sample=200
        
    csps_dict={}
    for key in tqdm(keys):
        # the first key is the year
        csps_dict[key]={}
        for sector in ['Energy', 'Utilities']:
            firms=list(sdgs_dict[key][sector].keys())
            csps_dict[key][sector]={}
            csps_dict[key][sector]['cos_sim']=np.zeros((len(firms), len(firms)))
            csps_dict[key][sector]['theo_pvals']=np.zeros((len(firms), len(firms)))
            csps_dict[key][sector]['sam_pvals']=np.zeros((len(firms), len(firms)))
                                                        
            # the third key is the firm
            if len(firms)>1:
                for i in range(len(firms)):
                    firm_i=firms[i]
                    dict_i=sdgs_dict[key][sector][firm_i]
                    for j in range(i+1, len(firms)):
                        firm_j=firms[j]
                        dict_j=sdgs_dict[key][sector][firm_j]
                        csps=cos_sim_per_sdg(dict_i, dict_j, n_sample=n_sample,tqdm_loops=True)
                        csps_dict[key][sector]['cos_sim'][i, j]=csps.cos_sim
                        csps_dict[key][sector]['theo_pvals'][i, j]=csps.pval
                        csps_dict[key][sector]['sam_pvals'][i, j]=csps.sampled_pval
   
                    
    with open('./data/csps_dict.pickle', 'wb') as f:
        pickle.dump(csps_dict, f)
                    
                    
                    
                    
        
def cos_sim_per_sdg(dict_0, dict_1, tqdm_loops=False, verbose=False, n_sample=10**3):
    common_sdgs=[key for key in dict_0.keys() if key in dict_1.keys()]
    for sdg in common_sdgs:
        aux=tesste(dict_0[sdg], dict_1[sdg], tqdm_loops=tqdm_loops, n_sample=n_sample, verbose=False)
        
    return aux