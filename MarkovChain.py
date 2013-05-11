import random as rand
import numpy as np
import pandas as pd

def weighted_choice(weights):
    """
    Given a list of weights, this function returns an index randomly, according to these weights
    """
    rnd = rand.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

stateSpace = ['A','B','C','D']
start_probs = np.array([0.6, 0.3, 0.1, 0.0])
# trans = arange(16).reshape(4,4)
trans_mat = np.array([[0.7, 0.2, 0.0, 0.1],
                      [0.3, 0.5, 0.2, 0.0],
                      [0.0, 0.3, 0.5, 0.2],
                      [0.2, 0.0, 0.2, 0.6]])

trans = pd.DataFrame(trans_mat, index=stateSpace, columns=stateSpace)

def markovChain(stateSpace, trans, start_probs, sequenceLength=10):
    seq = []
    seq.append(stateSpace[weighted_choice(start_probs)])
    
    for k in range(sequenceLength):
        # .loc introduced in 0.11 - not available in psychopy version of pandas
        # seq.append(stateSpace[weighted_choice(trans.loc[seq[k]])])
        # use .ix instead
         seq.append(stateSpace[weighted_choice(trans.ix[seq[k]])])
    return seq
        
thisMarkovChain = markovChain(stateSpace, trans, start_probs, sequenceLength=100)
