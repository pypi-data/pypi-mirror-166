"""
MIT License
Copyright (c) 2022 Stefan Güttel, Xinye Chen
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import time
import numpy as np
from scipy.linalg import get_blas_funcs, eigh
    

class build_snn_model:
    def __init__( self, data):
        self.mu = data.mean(axis=0)
        data = data - self.mu
        if data.shape[1]>1:
            gemm = get_blas_funcs("gemm", [data.T, data])
            dTd = gemm(1, data.T, data)
            _, v = eigh(dTd, subset_by_index=[data.shape[1]-1, data.shape[1]-1])
            sort_vals = data@v.reshape(-1)
        else:
            sort_vals = data[:,0].reshape(-1)
        
        self.sort_id = np.argsort(sort_vals)
        self.sort_vals = sort_vals[self.sort_id]
        self.data = data[self.sort_id]
        self.v = v.reshape(-1)
        self.xxt = np.einsum('ij,ij->i', self.data, self.data) # np.linalg.norm(X, axis=1)**2
    

def query_radius(query, model, radius):
    query = np.subtract(query, model.mu)
    sv_q = np.inner(query, model.v) # *np.sign(-sort_vals[0]) # ensure the same sign
    left = np.searchsorted(model.sort_vals, sv_q-radius)
    right = np.searchsorted(model.sort_vals, sv_q+radius)
    dist_set =  euclid(model.xxt[left:right], model.data[left:right], query)
    
    filter_radius = dist_set <= radius**2
    knn_ind = model.sort_id[np.arange(left, right, dtype=int)[filter_radius]]
    knn_dist = np.sqrt(dist_set[filter_radius])
    return knn_ind, knn_dist


    

def euclid(xxt, X, v):
    return (xxt + np.inner(v,v).ravel() -2*X.dot(v)).astype(float)

