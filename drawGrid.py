# def drawGrid(n):

from __future__ import division
from psychopy import visual, event, core
backgroundColor = [-1, -1, -1]
win = visual.Window([600,600], monitor='testMonitor', color=backgroundColor, units='pix')

outerBorder=200
innerLines = (1/3)*outerBorder
lineWidth = 1.0
outerVertices = [ [outerBorder,-outerBorder], [-outerBorder,-outerBorder], 
                [-outerBorder,outerBorder], [outerBorder,outerBorder],
                [outerBorder,-outerBorder]]

outerGrid = visual.ShapeStim(win, 
                 lineColor='green',
                 lineWidth=lineWidth, #in pixels
                 fillColor=backgroundColor, #beware, with convex shapes this won't work
                 fillColorSpace='rgb',
                 vertices=outerVertices,#choose something from the above or make your own
                 closeShape=False,#do you want the final vertex to complete a loop with 1st?
                 pos= [0.5,0.5], #the anchor (rotaion and vertices are position with respect to this)
                 interpolate=True,
                 opacity=1,
                 autoLog=False)

innerVertices1 = [[ outerBorder,-innerLines], [-outerBorder,-innerLines],
                  [-outerBorder, innerLines], [outerBorder, innerLines]]
innerGrid1 = visual.ShapeStim(win,
                             lineColor='green',
                 lineWidth=lineWidth, #in pixels
                 fillColor=None, #beware, with convex shapes this won't work
                 fillColorSpace='rgb',
                 vertices=innerVertices1,#choose something from the above or make your own
                 closeShape=True,#do you want the final vertex to complete a loop with 1st?
                 pos= [0.5,0.5], #the anchor (rotaion and vertices are position with respect to this)
                 interpolate=True,
                 opacity=1,
                 autoLog=False)

innerVertices2 = [[ innerLines,-outerBorder], [-innerLines,-outerBorder],
                  [-innerLines, outerBorder], [innerLines, outerBorder]]
innerGrid2 = visual.ShapeStim(win,
                             lineColor='green',
                 lineWidth=lineWidth, #in pixels
                 fillColor=None, #beware, with convex shapes this won't work
                 fillColorSpace='rgb',
                 vertices=innerVertices2,#choose something from the above or make your own
                 closeShape=True,#do you want the final vertex to complete a loop with 1st?
                 pos= [0.5,0.5], #the anchor (rotaion and vertices are position with respect to this)
                 interpolate=True,
                 opacity=1,
                 autoLog=False)


target = visual.Rect(win = win, pos=positions['A'], width=40, height=40,
                     lineColor = targetColor, fillColor = targetColor,
                    opacity = 1)


outerGrid.draw()
innerGrid1.draw()
innerGrid2.draw()
win.flip()
core.wait(2)

win.close()
core.quit()
