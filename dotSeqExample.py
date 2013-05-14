#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.77.00), Mon May 13 22:17:42 2013
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions

# Store info about the experiment session
expName = u'dotSeqExample'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'ae'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

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
    monitor=u'testMonitor', color=[0,0,0], colorSpace=u'rgb', units=u'pix')

# Initialize components for Routine "trial"
trialClock = core.Clock()

pos1 = visual.GratingStim(win=win, name='pos1',
    tex=None, mask='circle',
    ori=0, pos=[0, 0], size=[200, 200], sf=None, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    texRes=128, interpolate=True, depth=-1.0)
pos2 = visual.GratingStim(win=win, name='pos2',
    tex=None, mask=None,
    ori=0, pos=[0, 0], size=[200, 200], sf=None, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    texRes=128, interpolate=True, depth=-2.0)
pos3 = visual.GratingStim(win=win, name='pos3',
    tex='sin', mask=None,
    ori=0, pos=[0, 0], size=[0.5, 0.5], sf=None, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    texRes=128, interpolate=True, depth=-3.0)
pos4 = visual.GratingStim(win=win, name='pos4',
    tex='sin', mask=None,
    ori=0, pos=[0, 0], size=[0.5, 0.5], sf=None, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    texRes=128, interpolate=True, depth=-4.0)
target = visual.GratingStim(win=win, name='target',
    tex='sin', mask=None,
    ori=0, pos=[0,0], size=[0.5, 0.5], sf=None, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    texRes=128, interpolate=True, depth=-5.0)
fixCross = visual.TextStim(win=win, ori=0, name='fixCross',
    text='+',    font='Arial',
    pos=[0, 0], height=30, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=0.3,
    depth=-6.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
blockLoop = data.TrialHandler(nReps=5, method=u'sequential', 
    extraInfo=expInfo, originPath=None,
    trialList=[None],
    seed=None, name='blockLoop')
thisExp.addLoop(blockLoop)  # add the loop to the experiment
thisBlockLoop = blockLoop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisBlockLoop.rgb)
if thisBlockLoop != None:
    for paramName in thisBlockLoop.keys():
        exec(paramName + '= thisBlockLoop.' + paramName)

for thisBlockLoop in blockLoop:
    currentLoop = blockLoop
    # abbreviate parameter names if possible (e.g. rgb = thisBlockLoop.rgb)
    if thisBlockLoop != None:
        for paramName in thisBlockLoop.keys():
            exec(paramName + '= thisBlockLoop.' + paramName)
    
    # set up handler to look after randomisation of conditions etc
    trialLoop = data.TrialHandler(nReps=10, method=u'sequential', 
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
        # update component parameters for each repeat
        circleOpacity = 0.3
        circleRadius = 100
        markerSize = 20
        targetFillColor = [1, 1, -1] # yellow
        targetDuration = 30
        targetSize = [40, 40]
        #
        
        positions = {'pos1': [circleRadius*sin(pi/4), circleRadius*cos(pi/4)], 
                     'pos2': [circleRadius*sin(3*pi/4), circleRadius*cos(3*pi/4)],
                     'pos3': [circleRadius*sin(5*pi/4), circleRadius*cos(5*pi/4)],
                     'pos4': [circleRadius*sin(7*pi/4), circleRadius*cos(7*pi/4)]}
        
        fixCross = visual.TextStim(win=win, ori=0, name='fixCross',
            text='+',    font='Arial',
            units='pix', pos=[0, 0], height=20, wrapWidth=None,
            color='white', colorSpace='rgb', opacity=1,
            depth=-4.0)
        
        circle = visual.Circle(win = win, radius = circleRadius, edges=512, lineColor =
                               (1, 1, 1), fillColor = 'black', fillColorSpace = 'rgb',
                               interpolate = True, opacity = 0)
        
        pos1 = visual.Circle(win = win, pos=positions['pos1'], radius = markerSize,
                             edges=256, lineColor = (1, 1, 1), fillColor = 'black',
                             fillColorSpace = 'rgb', interpolate = True, opacity =
                             circleOpacity)
        
        pos2 = visual.Circle(win = win, pos=positions['pos2'], radius = markerSize,
                             edges=256, lineColor = (1, 1, 1), fillColor = 'black',
                             fillColorSpace = 'rgb', interpolate = True, opacity =
                             circleOpacity)
        
        pos3 = visual.Circle(win = win, pos=positions['pos3'], radius = markerSize,
                             edges=256, lineColor = (1, 1, 1), fillColor = 'black',
                             fillColorSpace = 'rgb', interpolate = True, opacity =
                             circleOpacity)
        
        pos4 = visual.Circle(win = win, pos=positions['pos4'], radius = markerSize,
                             edges=256, lineColor = (1, 1, 1), fillColor = 'black',
                             fillColorSpace = 'rgb', interpolate = True, opacity =
                             circleOpacity)
        
        target = visual.Circle(win = win, pos=positions['pos4'], radius = markerSize,
                             edges=256, lineColor = (1, 1, 1), fillColor = targetFillColor,
                             fillColorSpace = 'rgb', interpolate = True, opacity = 1)
        target.setPos(thisPosition)
        keyResponse = event.BuilderKeyResponse()  # create an object of type KeyResponse
        keyResponse.status = NOT_STARTED
        # keep track of which components have finished
        trialComponents = []
        trialComponents.append(pos1)
        trialComponents.append(pos2)
        trialComponents.append(pos3)
        trialComponents.append(pos4)
        trialComponents.append(target)
        trialComponents.append(fixCross)
        trialComponents.append(keyResponse)
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "trial"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *pos1* updates
            if frameN >= 0 and pos1.status == NOT_STARTED:
                # keep track of start time/frame for later
                pos1.tStart = t  # underestimates by a little under one frame
                pos1.frameNStart = frameN  # exact frame index
                pos1.setAutoDraw(True)
            elif pos1.status == STARTED and frameN >= (pos1.frameNStart + 30):
                pos1.setAutoDraw(False)
            
            # *pos2* updates
            if frameN >= 0 and pos2.status == NOT_STARTED:
                # keep track of start time/frame for later
                pos2.tStart = t  # underestimates by a little under one frame
                pos2.frameNStart = frameN  # exact frame index
                pos2.setAutoDraw(True)
            elif pos2.status == STARTED and frameN >= (pos2.frameNStart + 30):
                pos2.setAutoDraw(False)
            
            # *pos3* updates
            if frameN >= 0 and pos3.status == NOT_STARTED:
                # keep track of start time/frame for later
                pos3.tStart = t  # underestimates by a little under one frame
                pos3.frameNStart = frameN  # exact frame index
                pos3.setAutoDraw(True)
            elif pos3.status == STARTED and frameN >= (pos3.frameNStart + 30):
                pos3.setAutoDraw(False)
            
            # *pos4* updates
            if frameN >= 0 and pos4.status == NOT_STARTED:
                # keep track of start time/frame for later
                pos4.tStart = t  # underestimates by a little under one frame
                pos4.frameNStart = frameN  # exact frame index
                pos4.setAutoDraw(True)
            elif pos4.status == STARTED and frameN >= (pos4.frameNStart + 30):
                pos4.setAutoDraw(False)
            
            # *target* updates
            if frameN >= 0 and target.status == NOT_STARTED:
                # keep track of start time/frame for later
                target.tStart = t  # underestimates by a little under one frame
                target.frameNStart = frameN  # exact frame index
                target.setAutoDraw(True)
            elif target.status == STARTED and frameN >= (target.frameNStart + 30):
                target.setAutoDraw(False)
            
            # *fixCross* updates
            if frameN >= 0 and fixCross.status == NOT_STARTED:
                # keep track of start time/frame for later
                fixCross.tStart = t  # underestimates by a little under one frame
                fixCross.frameNStart = frameN  # exact frame index
                fixCross.setAutoDraw(True)
            elif fixCross.status == STARTED and frameN >= (fixCross.frameNStart + 30):
                fixCross.setAutoDraw(False)
            
            # *keyResponse* updates
            if frameN >= 0 and keyResponse.status == NOT_STARTED:
                # keep track of start time/frame for later
                keyResponse.tStart = t  # underestimates by a little under one frame
                keyResponse.frameNStart = frameN  # exact frame index
                keyResponse.status = STARTED
                # keyboard checking is just starting
                keyResponse.clock.reset()  # now t=0
                event.clearEvents()
            elif keyResponse.status == STARTED and t >= (keyResponse.tStart + trialDuration):
                keyResponse.status = STOPPED
            if keyResponse.status == STARTED:
                theseKeys = event.getKeys(keyList=['space'])
                if len(theseKeys) > 0:  # at least one key was pressed
                    if keyResponse.keys == []:  # then this was the first keypress
                        keyResponse.keys = theseKeys[0]  # just the first key pressed
                        keyResponse.rt = keyResponse.clock.getTime()
                        # was this 'correct'?
                        if (keyResponse.keys == str(isCatchTrial)): keyResponse.corr = 1
                        else: keyResponse.corr=0
            
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
        
        # check responses
        if len(keyResponse.keys) == 0:  # No response was made
           keyResponse.keys=None
           # was no response the correct answer?!
           if str(isCatchTrial).lower() == 'none': keyResponse.corr = 1  # correct non-response
           else: keyResponse.corr = 0  # failed to respond (incorrectly)
        # store data for trialLoop (TrialHandler)
        trialLoop.addData('keyResponse.keys',keyResponse.keys)
        trialLoop.addData('keyResponse.corr', keyResponse.corr)
        if keyResponse.keys != None:  # we had a response
            trialLoop.addData('keyResponse.rt', keyResponse.rt)
        thisExp.nextEntry()
        
    # completed 10 repeats of 'trialLoop'
    
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
    
# completed 5 repeats of 'blockLoop'

# get names of stimulus parameters
if blockLoop.trialList in ([], [None], None):  params = []
else:  params = blockLoop.trialList[0].keys()
# save data for this loop
blockLoop.saveAsExcel(filename + '.xlsx', sheetName='blockLoop',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])
blockLoop.saveAsText(filename + 'blockLoop.csv', delim=',',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

win.close()
core.quit()
