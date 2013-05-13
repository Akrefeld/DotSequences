# http://glowingpython.blogspot.ch/2012/09/weighted-random-choice.html

from numpy import cumsum, sort, sum, searchsorted
from numpy.random import rand
from pylab import hist,show,xticks

def weighted_pick(weights,n_picks):
 """
  Weighted random selection
  returns n_picks random indexes.
  the chance to pick the index i 
  is give by the weight weights[i].
 """
 t = cumsum(weights)
 s = sum(weights)
 return searchsorted(t,rand(n_picks)*s)

# weights, don't have to sum up to one
w = [0.1, 0.2, 0.5, 0.5, 1.0, 1.1, 2.0]

# picking 10000 times
picked_list = weighted_pick(w,10000)

# plotting the histogram
hist(picked_list,bins=len(w),normed=1,alpha=.8,color='red')
show()
