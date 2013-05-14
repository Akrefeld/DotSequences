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
           u'transitionType': u'det',
           u'stimType': 'Circle'}
# transitionType should be either 'rand' or 'det'
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
logFile = logging.LogFile(filename+'.log', level=logging.DEBUG)
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
markerSize = 40
rectSize = 50
lineWidth = 2 # pixels
targetColor = [1, 0.75, -1] # [1, 1, -1] # yellow
targetDuration = 30
targetSize = [40, 40]
isi = 30
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

trans_mat_random = np.random.randint(0,100.0,nStates*nStates).reshape(nStates,nStates).astype(float) 
# row sums:
# row_sums = trans_mat.sum(axis=1)
# trans_mat = trans_mat / row_sums[:, np.newaxis]

# with the following (/=) we can eliminate intermediate temp variables:
trans_mat_random /= trans_mat_random.sum(axis=1)[:, np.newaxis]

"""
 define an almost determistic random, i.e. A->B->C->D
with the option: stay, go left, go right (jumps across are not possible
D -- A
|    |
C -- B
"""
trans_mat_deterministic = np.array([[0.15, 0.7, 0, 0.15],
                                   [0.15, 0.15, 0.7, 0], 
                                   [0, 0.15, 0.15, 0.7],
                                   [0.7, 0, 0.15, 0.15]])


# check if trans_mat is a stochastic matrix
print trans_mat_random.sum(axis=1)
print trans_mat_deterministic.sum(axis=1)
# print isStochastic

trans_deterministic = pd.DataFrame(trans_mat_deterministic, index=stateSpace, columns=stateSpace)
trans_random = pd.DataFrame(trans_mat_random, index=stateSpace, columns=stateSpace)

transitionMatrices = {'det':trans_deterministic,
                      'rand': trans_random}

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

    
positionMarkers = ['pos1', 'pos2', 'pos3', 'pos4']

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

"""
TrialHandler usage:
either use list of dictionaries or import csv:
trialList = myDict
trialList=data.importConditions('mainTrials.csv')
"""

# set up handler to look after randomisation of conditions etc
blockLoop = data.TrialHandler(nReps=1, method=u'sequential', 
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
    

    thisTransitionType = expInfo['transitionType']
    observedHistory = []
    thisSequence = markovChainGenerator(stateSpace, transitionMatrices[thisTransitionType], 
                                        observedHistory, start_probs)

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


        observedHistory.append(thisSequence.next())
        
        # target.setPos(positions[thisMarkovChain[trials.thisN]])
        target.setPos(positions[observedHistory[-1]])
    

        currentLoop.addData('observedHistory', observedHistory[-1])
        

        ### demo
        trialComponents = []
        trialComponents.append(pos1)
        trialComponents.append(pos2)
        trialComponents.append(pos3)
        trialComponents.append(pos4)
        trialComponents.append(target)
        trialComponents.append(fixCross)

        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        #-------Start Routine "trial"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # target.setPos(positions[thisMarkovChain[trials.thisN]])
            # history.append(positions[thisMarkovChain[trials.thisN]])
            # update/draw components on each frame
            
            
            # *pos1* updates
            if frameN >= 0 and pos1.status == NOT_STARTED:
                # keep track of start time/frame for later
                pos1.tStart = t  # underestimates by a little under one frame
                pos1.frameNStart = frameN  # exact frame index
                pos1.setAutoDraw(True)
            elif pos1.status == STARTED and frameN >= (pos1.frameNStart + trialDuration):
                pos1.setAutoDraw(False)
            
            # *pos2* updates
            if frameN >= 0 and pos2.status == NOT_STARTED:
                # keep track of start time/frame for later
                pos2.tStart = t  # underestimates by a little under one frame
                pos2.frameNStart = frameN  # exact frame index
                pos2.setAutoDraw(True)
            elif pos2.status == STARTED and frameN >= (pos2.frameNStart + trialDuration):
                pos2.setAutoDraw(False)
            
            # *pos3* updates
            if frameN >= 0 and pos3.status == NOT_STARTED:
                # keep track of start time/frame for later
                pos3.tStart = t  # underestimates by a little under one frame
                pos3.frameNStart = frameN  # exact frame index
                pos3.setAutoDraw(True)
            elif pos3.status == STARTED and frameN >= (pos3.frameNStart + trialDuration):
                pos3.setAutoDraw(False)
            
            # *pos4* updates
            if frameN >= 0 and pos4.status == NOT_STARTED:
                # keep track of start time/frame for later
                pos4.tStart = t  # underestimates by a little under one frame
                pos4.frameNStart = frameN  # exact frame index
                pos4.setAutoDraw(True)
            elif pos4.status == STARTED and frameN >= (pos4.frameNStart + trialDuration):
                pos4.setAutoDraw(False)
            
            # *target* updates
            if frameN >= 0 and target.status == NOT_STARTED:
                # keep track of start time/frame for later
                target.tStart = t  # underestimates by a little under one frame
                target.frameNStart = frameN  # exact frame index
                target.setAutoDraw(True)
            elif target.status == STARTED and frameN >= (target.frameNStart + targetDuration):
                target.setAutoDraw(False)
            
            # *fixCross* updates
            if frameN >= 0 and fixCross.status == NOT_STARTED:
                # keep track of start time/frame for later
                fixCross.tStart = t  # underestimates by a little under one frame
                fixCross.frameNStart = frameN  # exact frame index
                fixCross.setAutoDraw(True)
            elif fixCross.status == STARTED and frameN >= (fixCross.frameNStart + trialDuration):
                fixCross.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
            else:  # this Routine was not non-slip safe so reset non-slip timer
                routineTimer.reset()
        
        #-------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        thisExp.nextEntry()

        ### start demo
        # [item.draw() for item in trialComponents]
        # win.flip()
        # core.wait(2)

        ### end demo
        #####################################################################

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
    
    # TODO: save full history
    print observedHistory
    
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
