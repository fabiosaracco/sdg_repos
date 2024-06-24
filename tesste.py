# texts' semantic similarity test
# 
import os, sys, json, pickle
import datetime as dt
import numpy as np
import inspect
from pypdf import PdfReader

from sentence_transformers import SentenceTransformer, util

from tqdm.autonotebook import tqdm, trange

from scipy.stats._continuous_distns import _distn_names
import scipy.stats as st

from multiprocessing import Pool
from functools import partial

class tesste:
    
    def __init__(self, text_0, text_1, n_sample=10**3, verbose=False, tqdm_loops=True):
        if verbose:
            print('[{:%H:%M:%S}]\t{:}\t starting!'.format(dt.datetime.now(),inspect.currentframe().f_code.co_name))
            
        self.text_0=text_0
        self.text_1=text_1
        self.n_sample=n_sample
        self.verbose=verbose
        self.tqdm_loops=tqdm_loops
        
        self.model_name="all-MiniLM-L6-v2"
        if self.verbose:
            print('[{:%H:%M:%S}]\t{:}\t model={:}'.format(dt.datetime.now(),inspect.currentframe().f_code.co_name, self.model_name))
        
        self.model = SentenceTransformer(self.model_name)
        
        self.se_emb_0 = self.model.encode(text_0)
        self.se_emb_1 = self.model.encode(text_1)
        
        self.cos_sim=util.cos_sim(self.se_emb_0,self.se_emb_1)[0,0].tolist()
        self.va_co_si()
        self.fit_cos_sim_mielke()
        self.pval=self.get_pvalue(self.cos_sim, st.mielke, self.cosi_arg, self.cosi_loc, self.cosi_scale)
        self.sampled_pval=np.sum(self.ra_se_co_si>=self.cos_sim)/self.n_sample
        
    
    @staticmethod
    def semantic_randomizer(text, model):
        shuffled_text=text.split(' ')
        shuffled_text = np.random.permutation(shuffled_text)
        shuffled_text= ' '.join(shuffled_text)
        shuffled_embedding = model.encode(shuffled_text)
        return shuffled_embedding
    
    
    def single_step_randomization(self, fake):
        se_ra_te_0=self.semantic_randomizer(self.text_0, self.model)
        se_ra_te_1=self.semantic_randomizer(self.text_1, self.model)
        return util.cos_sim(se_ra_te_0,se_ra_te_1)[0,0].tolist()
            
    
    def va_co_si(self):
        # validate cosine similarity
        if self.verbose:
            print('[{:%H:%M:%S}]\t{:}'.format(dt.datetime.now(),inspect.currentframe().f_code.co_name))
            print('[{:%H:%M:%S}]\tself.n_sample={:}'.format(dt.datetime.now(),self.n_sample))
        
        self.ra_se_co_si=np.zeros(self.n_sample)
        if self.tqdm_loops:
            for i in trange(self.n_sample, leave=False):
                self.ra_se_co_si[i]=self.single_step_randomization(1)
        else:
            for i in range(self.n_sample):
                self.ra_se_co_si[i]=self.single_step_randomization(1)
            
            
    def fit_cos_sim_mielke(self):
        if self.verbose:
            print('[{:%H:%M:%S}]\t{:}'.format(dt.datetime.now(),inspect.currentframe().f_code.co_name))
        bins=200
        # Get histogram of original data
        y, x = np.histogram(self.ra_se_co_si, bins=bins, density=True)
        x = (x + np.roll(x, -1))[:-1] / 2.0
        
        # mielke function worked well in previous tests. To be checked
        dist=st.mielke
        params = dist.fit(self.ra_se_co_si)

        # Separate parts of parameters
        self.cosi_arg = params[:-2]
        self.cosi_loc = params[-2]
        self.cosi_scale = params[-1]
        
        self.cosi_pdf=(x, dist.pdf(x, loc=self.cosi_loc, scale=self.cosi_scale, *self.cosi_arg))
        sse = np.sum((y - self.cosi_pdf[1])**2)
        if self.verbose:
            print('[{:%H:%M:%S}]\t{:}\t sse={:.3f}'.format(dt.datetime.now(),inspect.currentframe().f_code.co_name, sse))
    
    @staticmethod
    def get_pvalue(x, dist, arg, loc, scale):
        """Generate distributions's Probability Distribution Function """
        #p_val = dist.pdf(x, *arg, loc=loc, scale=scale) if arg else dist.ppf(x, loc=loc, scale=scale)
        p_val= dist.sf(x, *arg, loc=loc, scale=scale) if arg else dist.ppf(x, loc=loc, scale=scale)
        return p_val            
