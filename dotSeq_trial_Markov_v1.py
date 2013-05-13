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


# Store info about the experiment session
expName = u'dotSeq_trial'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'Optimal Learner', 'sequenceLength':25}


dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

sequenceLength = expInfo['sequenceLength']

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

# Setup the Window
win = visual.Window(size=[800, 800], fullscr=False, screen=0, allowGUI=True, allowStencil=False,
    monitor=u'testMonitor', color=[-1,-1,-1], colorSpace=u'rgb')

# Initialize components for Routine "trial"
trialClock = core.Clock()


circleOpacity = 0.3
circleRadius = 100
markerSize = 20
targetColor = [1, 1, -1] # yellow
targetDuration = 30
targetSize = [40, 40]
isi = 30
trialDuration = targetDuration + isi


# generate Markov chain
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
N = len(stateSpace)

start_probs = np.array([0.6, 0.3, 0.1, 0.0])

## generate transition matrix
"""
solution from:
http://stackoverflow.com/questions/8904694/how-to-normalize-a-2-dimensional-numpy-array-in-python-less-verbose
"""
trans_mat = np.random.randint(0,100.0,N*N).reshape(N,N).astype(float) 
# row sums:
# row_sums = trans_mat.sum(axis=1)
# trans_mat = trans_mat / row_sums[:, np.newaxis]

# with the following (/=) we can eliminate intermediate temp variables:
trans_mat /= trans_mat.sum(axis=1)[:, np.newaxis]

# trans_mat = np.array([[0.6, 0.2, 0.1, 0.1],
#                       [0.3, 0.5, 0.2, 0.0],
#                       [0.0, 0.3, 0.5, 0.2],
#                       [0.2, 0.0, 0.2, 0.6]])

# check if trans_mat is a stochastic matrix
isStochastic = trans_mat.sum(axis=1)
print isStochastic

trans = pd.DataFrame(trans_mat, index=stateSpace, columns=stateSpace)

##
def markovChain(stateSpace, trans, start_probs, chain_length=10):
    seq = []
    seq.append(stateSpace[weighted_choice(start_probs)])
    
    for k in range(chain_length):
        # .loc introduced in 0.11 - not available in psychopy version of pandas
        # seq.append(stateSpace[weighted_choice(trans.loc[seq[k]])])
        # use .ix instead
         seq.append(stateSpace[weighted_choice(trans.ix[seq[k]])])
    return seq
    #
thisMarkovChain = markovChain(stateSpace, trans, start_probs, chain_length=100)
print thisMarkovChain
    
# TODO: position names would make more sense if A were top left, instead of top right
positions = {'A': [circleRadius*sin(pi/4), circleRadius*cos(pi/4)], 
             'B': [circleRadius*sin(3*pi/4), circleRadius*cos(3*pi/4)],
             'C': [circleRadius*sin(5*pi/4), circleRadius*cos(5*pi/4)],
             'D': [circleRadius*sin(7*pi/4), circleRadius*cos(7*pi/4)]}

fixCross = visual.TextStim(win=win, ori=0, name='fixCross',
                           text='+',    font='Arial',
                           units='pix', pos=[0, 0], height=20, wrapWidth=None,
                           color='white', colorSpace='rgb', opacity=circleOpacity,
                           depth=-4.0)

# circle = visual.Circle(win = win, radius = circleRadius, edges=512, lineColor =
#                        (1, 1, 1), fillColor = 'black', fillColorSpace = 'rgb',
#                        interpolate = True, opacity = 0)

# pos1 = visual.Circle(win = win, pos=positions['A'], radius = markerSize,
#                      edges=256, lineColor = (1, 1, 1), fillColor = 'black',
#                      fillColorSpace = 'rgb', interpolate = True, opacity =
#                      circleOpacity)

pos1 = visual.Rect(win = win, pos=positions['A'], width=40, height=40,
                     lineColor = (1, 1, 1), fillColor = 'black',
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)

# pos2 = visual.Circle(win = win, pos=positions['B'], radius = markerSize,
#                      edges=256, lineColor = (1, 1, 1), fillColor = 'black',
#                      fillColorSpace = 'rgb', interpolate = True, opacity =
#                      circleOpacity)

pos2 = visual.Rect(win = win, pos=positions['B'], width=40, height=40,
                     lineColor = (1, 1, 1), fillColor = 'black',
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)

# pos3 = visual.Circle(win = win, pos=positions['C'], radius = markerSize,
#                      edges=256, lineColor = (1, 1, 1), fillColor = 'black',
#                      fillColorSpace = 'rgb', interpolate = True, opacity =
#                      circleOpacity)
pos3 = visual.Rect(win = win, pos=positions['C'], width=40, height=40,
                     lineColor = (1, 1, 1), fillColor = 'black',
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)

# pos4 = visual.Circle(win = win, pos=positions['D'], radius = markerSize,
#                      edges=256, lineColor = (1, 1, 1), fillColor = 'black',
#                      fillColorSpace = 'rgb', interpolate = True, opacity =
#                      circleOpacity)
pos4 = visual.Rect(win = win, pos=positions['D'], width=40, height=40,
                     lineColor = (1, 1, 1), fillColor = 'black',
                     fillColorSpace = 'rgb', interpolate = True, opacity =
                     circleOpacity)

# target = visual.Circle(win = win, pos=positions['D'], radius = markerSize,
#                        edges=256, lineColor = targetColor, fillColor = targetColor,
#                        fillColorSpace = 'rgb', interpolate = True, opacity = 1)

target = visual.Rect(win = win, pos=positions['A'], width=40, height=40,
                     lineColor = targetColor, fillColor = targetColor,
                    opacity = 1)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
outer_loop = data.TrialHandler(nReps=2, method=u'sequential', 
    extraInfo=expInfo, originPath=None,
    trialList=[None],
    seed=None, name='outer_loop')
thisExp.addLoop(outer_loop)  # add the loop to the experiment
thisOuter_loop = outer_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisOuter_loop.rgb)
if thisOuter_loop != None:
    for paramName in thisOuter_loop.keys():
        exec(paramName + '= thisOuter_loop.' + paramName)

for thisOuter_loop in outer_loop:
    currentLoop = outer_loop
    # abbreviate parameter names if possible (e.g. rgb = thisOuter_loop.rgb)
    if thisOuter_loop != None:
        for paramName in thisOuter_loop.keys():
            exec(paramName + '= thisOuter_loop.' + paramName)
            
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=sequenceLength, method=u'sequential', 
        extraInfo=expInfo, originPath=None,
        trialList=[None],
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)
        
        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1

        history = []
        # update component parameters for each repeat

        #
        


        # positionKeys=positions.keys()
        # positionKeys.sort()
        
        # set random target position
        # thisPosition = rand.choice(positionKeys)

        target.setPos(positions[thisMarkovChain[trials.thisN]])
        history.append(thisMarkovChain[trials.thisN])
        currentLoop.addData('History', history[-1])
        currentLoop.addData('Position', positions[thisMarkovChain[trials.thisN]])

        # keep track of which components have finished
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
        
    # completed n repeats of 'trials'

    thisExp.nextEntry()
    
# completed 5 repeats of 'outer_loop'


win.close()
core.quit()
