#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import random as rand
import pandas as pd
################################################################################


# Store info about the experiment session
expName = u'genRandSeq'  # from the Builder filename that created this script
expInfo = {u'session': u'001', 
           u'participant': u'ae', 
           u'sequenceLength':25,
           u'fullScreen': False,
            u'stimType': 'Circle'}
# stimType should be either 'Rect' or 'Circle'

# open dialogue window
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# get sequence length from info dlg
sequenceLength = expInfo['sequenceLength']
fullScreen = expInfo['fullScreen']

# Setup files for saving
if not os.path.isdir('Data'):
    os.makedirs('Data')  # if this fails (e.g. permissions) we will get error
filename = 'Data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)



################################################################################
# Setup the Window
################################################################################
backgroundColor = [-1, -1, -1]
win = visual.Window(size=[800, 800], 
                    fullscr=fullScreen, screen=0, allowGUI=True, 
                    allowStencil=False,
                    monitor=u'testMonitor', 
                    color=backgroundColor, 
                    colorSpace=u'rgb')

trialClock = core.Clock()

################################################################################
# define parameters
################################################################################
fontSize = 30
circleOpacity = 0.3
circleRadius = 200
markerSize = 30
rectSize = 50
lineWidth = 2 # pixels
targetColor = [1, 0.75, -1] # [1, 1, -1] # yellow
targetDuration = 30
targetSize = [40, 40]
isi = 60
trialDuration = targetDuration + isi




def weighted_choice(weights, n_picks):
    """
    Weighted random selection
    returns n_picks random indexes.
    the chance to pick the index i 
    is give by the weight weights[i].
    Weights don't have to sum to 1.
    """
    t = np.cumsum(weights)
    s = np.sum(weights)
    return np.searchsorted(t, np.random.rand(n_picks)*s)

################################################################################
# define sequences
################################################################################
stateSpace = ['A','B','C','D']
nStates = len(stateSpace)

# define starting probability (uniform)
# start_probs = np.array([1/4, 1/4, 1/4, 1/4])
# tile is equivalent of Matlab's repmat
start_probs = np.tile(1/nStates, (1, nStates))

## generate transition matrix
"""
solution from:
http://stackoverflow.com/questions/8904694/how-to-normalize-a-2-dimensional-numpy-array-in-python-less-verbose
"""

trans_mat = np.random.randint(0,100.0,nStates*nStates).reshape(nStates,nStates).astype(float) 
# row sums:
# row_sums = trans_mat.sum(axis=1)
# trans_mat = trans_mat / row_sums[:, np.newaxis]

# with the following (/=) we can eliminate intermediate temp variables:
trans_mat /= trans_mat.sum(axis=1)[:, np.newaxis]

# define an almost determistic path, i.e. A->B->C->D
trans_mat = np.array([[0.1, 0.7, 0.1, 0.1],
                      [0.1, 0.1, 0.7, 0.1], 
                      [0.1, 0.1, 0.1, 0.7],
                      [0.7, 0.1, 0.1, 0.1]])

# check if trans_mat is a stochastic matrix
isStochastic = trans_mat.sum(axis=1)
print isStochastic

trans = pd.DataFrame(trans_mat, index=stateSpace, columns=stateSpace)



def markovChainGenerator(stateSpace, trans, history, start_probs):
    """
    Starts with empty list, and then adds starting position, according to
    start_probs. Then adds further positions, according to transition matrix.
    """
    k=0
    seq=[]
    while True:
        if k==0:
            yield stateSpace[weighted_choice(start_probs, 1)]
            # seq.append(stateSpace[weighted_choice(start_probs, 1)])
            # yield seq
            k+=1
        elif k>=1:
            # yield stateSpace[weighted_choice(trans.ix[seq[k-1]], 1)]
            yield stateSpace[weighted_choice(trans.ix[history[-1]], 1)]
            # seq.append(stateSpace[weighted_choice(trans.ix[seq[k-1]], 1)])
            # yield seq
            # k+=1
"""
usage:
observedHistory = []
thisSequence = markovChainGenerator(stateSpace, trans, observedHistory, start_probs)
observedHistory.append(thisSequence.next())
"""


################################################################################
# draw positions on screen:
# TODO: position names would make more sense if A were top left, instead of top right
positions = {'A': [circleRadius*sin(pi/4), circleRadius*cos(pi/4)], 
             'B': [circleRadius*sin(3*pi/4), circleRadius*cos(3*pi/4)],
             'C': [circleRadius*sin(5*pi/4), circleRadius*cos(5*pi/4)],
             'D': [circleRadius*sin(7*pi/4), circleRadius*cos(7*pi/4)]}

# create all stimuli
fixCross = visual.TextStim(win=win, ori=0, name='fixCross',
                           text='+',    font='Arial',
                           units='pix', pos=[0, 0], height=fontSize, wrapWidth=None,
                           color='white', colorSpace='rgb', opacity=circleOpacity,
                           depth=-4.0)

if expInfo['stimType'] == 'Rect':
    pos1 = visual.Rect(win = win, pos=positions['A'], width=rectSize, height=rectSize,
                     lineColor = (1, 1, 1), fillColor = 'black',
                     lineWidth=lineWidth,
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)
    pos2 = visual.Rect(win = win, pos=positions['B'], width=rectSize, height=rectSize,
                     lineColor = (1, 1, 1), fillColor = 'black',
                     lineWidth=lineWidth,
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)
    pos3 = visual.Rect(win = win, pos=positions['C'], width=rectSize, height=rectSize,
                     lineColor = (1, 1, 1), fillColor = 'black',
                     lineWidth=lineWidth,
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)
    pos4 = visual.Rect(win = win, pos=positions['D'], width=rectSize, height=rectSize,
                     lineColor = (1, 1, 1), fillColor = 'black',
                     lineWidth=lineWidth,
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)
    target = visual.Rect(win = win, pos=positions['A'], width=rectSize, height=rectSize,
                     lineColor = targetColor, fillColor = targetColor,
                    opacity = 1)
elif expInfo['stimType'] == 'Circle':
    circle = visual.Circle(win = win, radius = circleRadius, edges=512, lineColor =
                           (1, 1, 1), fillColor = 'black', fillColorSpace = 'rgb',
                           interpolate = True, opacity = 0)
    pos1 = visual.Circle(win = win, pos=positions['A'], radius = markerSize,
                     edges=256, lineColor = (1, 1, 1), fillColor = 'black',
                     lineWidth=lineWidth,
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)
    pos2 = visual.Circle(win = win, pos=positions['B'], radius = markerSize,
                     edges=256, lineColor = (1, 1, 1), fillColor = 'black',
                     lineWidth=lineWidth,
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)
    pos3 = visual.Circle(win = win, pos=positions['C'], radius = markerSize,
                     edges=256, lineColor = (1, 1, 1), fillColor = 'black',
                     lineWidth=lineWidth,
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)
    pos4 = visual.Circle(win = win, pos=positions['D'], radius = markerSize,
                     edges=256, lineColor = (1, 1, 1), fillColor = 'black',
                     lineWidth=lineWidth,
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)
    target = visual.Circle(win = win, pos=positions['A'], radius = markerSize,
                       edges=256, lineColor = targetColor, fillColor = targetColor,
                       fillColorSpace = 'rgb', interpolate = True, opacity = 1)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine



# set up handler to look after randomisation of conditions etc
blockLoop = data.TrialHandler(nReps=2, method=u'sequential', 
    extraInfo=expInfo, originPath=None,
    trialList=[None],
    seed=None, name='blockLoop')
thisExp.addLoop(blockLoop)  # add the loop to the experiment
thisBlockLoop = blockLoop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisOuter_loop.rgb)
if thisBlockLoop != None:
    for paramName in thisBlockLoop.keys():
        exec(paramName + '= thisBlockLoop.' + paramName)

for thisBlockLoop in blockLoop:
    currentLoop = blockLoop
    # abbreviate parameter names if possible (e.g. rgb = thisOuter_loop.rgb)
    if thisBlockLoop != None:
        for paramName in thisBlockLoop.keys():
            exec(paramName + '= thisBlockLoop.' + paramName)
            

    # set up handler to look after randomisation of conditions etc
    trialLoop = data.TrialHandler(nReps=sequenceLength, method=u'sequential', 
                                  extraInfo=expInfo, originPath=None,
                                  trialList=[None],
                                  seed=None, name='trialLoop')
    thisExp.addLoop(trialLoop)  # add the loop to the experiment
    thisTrialLoop = trialLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisTrialLoop.rgb)
    if thisTrialLoop != None:
        for paramName in thisTrialLoop.keys():
            exec(paramName + '= thisTrialLoop.' + paramName)

    for thisTrialLoop in trialLoop:
        currentLoop = trialLoop
        # abbreviate parameter names if possible (e.g. rgb = thisTrialLoop.rgb)
        if thisTrialLoop != None:
            for paramName in thisTrialLoop.keys():
                exec(paramName + '= thisTrialLoop.' + paramName)

        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1

        observedHistory = []
        thisSequence = markovChainGenerator(stateSpace, trans, observedHistory, start_probs)
        observedHistory.append(thisSequence.next())



################################################################################
### demo
        trialComponents = []
        trialComponents.append(pos1)
        trialComponents.append(pos2)
        trialComponents.append(pos3)
        trialComponents.append(pos4)
        trialComponents.append(target)
        trialComponents.append(fixCross)
        
        [item.draw() for item in trialComponents]
        win.flip()
        core.wait(5)

        ### end demo
        ################################################################################

    # end'trialLoop'
        
    # get names of stimulus parameters
    if trialLoop.trialList in ([], [None], None):  params = []
    else:  params = trialLoop.trialList[0].keys()
    # save data for this loop
    trialLoop.saveAsExcel(filename + '.xlsx', sheetName='trialLoop',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    trialLoop.saveAsText(filename + 'trialLoop.csv', delim=',',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    thisExp.nextEntry()

    # end 'blockLoop'
    
# get names of stimulus parameters
if blockLoop.trialList in ([], [None], None):  params = []
else:  params = blockL.trialList[0].keys()
# save data for this loop
blockLoop.saveAsExcel(filename + '.xlsx', sheetName='blockLoop',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])
blockLoop.saveAsText(filename + 'blockLoop.csv', delim=',',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])



win.close()
core.quit()
