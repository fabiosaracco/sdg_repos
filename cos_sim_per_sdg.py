import os, sys, pickle
import numpy as np
from tqdm import trange, tqdm
from tesste import tesste

import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', '-t', dest='test', default=False)
    return parser    


def main():
    # getting data
    parser = get_parser()
    args = parser.parse_args()
    test=bool(args.test)
    
    print('Ready!')
    
    
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
            #csps_dict[key][sector]['cos_sim']=np.zeros((len(firms), len(firms)))
            #csps_dict[key][sector]['theo_pvals']=np.zeros((len(firms), len(firms)))
            #csps_dict[key][sector]['sam_pvals']=np.zeros((len(firms), len(firms)))
                                                        
            # the third key is the firm
            if len(firms)>1:
                for i in trange(len(firms), desc=str(key), leave=False):
                    firm_i=firms[i]
                    dict_i=sdgs_dict[key][sector][firm_i]
                    for j in range(i+1, len(firms)):
                        firm_j=firms[j]
                        
                        csps_dict[key][sector]['firms']=[]
                        csps_dict[key][sector]['firms'].append((firm_i, firm_j))
                        
                        dict_j=sdgs_dict[key][sector][firm_j]
                        csps=cos_sim_per_sdg(dict_i, dict_j, n_sample=n_sample,tqdm_loops=True)
                        
                        for s_key in csps.keys():
                            if s_key not in csps_dict[key][sector].keys():
                                    csps_dict[key][sector][s_key]={}
                                    csps_dict[key][sector][s_key]['cos_sim']=[]
                                    csps_dict[key][sector][s_key]['sam_pvals']=[]
                                    csps_dict[key][sector][s_key]['theo_pvals']=[]
                                    csps_dict[key][sector][s_key]['firms']=[]
                            
                        
                                    
                            csps_dict[key][sector][s_key]['cos_sim'].append(csps[s_key].cos_sim)
                            csps_dict[key][sector][s_key]['theo_pvals'].append(csps[s_key].pval)
                            csps_dict[key][sector][s_key]['sam_pvals'].append(csps[s_key].sampled_pval)
                            csps_dict[key][sector][s_key]['firms'].append((firm_i, firm_j))
                            
   
                    
        with open('./data/csps_dict.pickle', 'wb') as f:
            pickle.dump(csps_dict, f)
                    
                    
                    
                    
        
def cos_sim_per_sdg(dict_0, dict_1, tqdm_loops=False, verbose=False, n_sample=10**3):
    common_sdgs=[key for key in dict_0.keys() if key in dict_1.keys()]
    aux={}
    for sdg in common_sdgs:
        aux[sdg]=tesste(dict_0[sdg], dict_1[sdg], tqdm_loops=tqdm_loops, n_sample=n_sample, verbose=False)
        
    return aux

if __name__ == "__main__":
    main()   