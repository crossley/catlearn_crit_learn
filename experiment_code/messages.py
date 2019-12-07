from __future__ import division
from psychopy import visual, core, data, event, sound
from psychopy.constants import *
from psychopy.tools.monitorunittools import pix2cm, pix2deg
from psychopy.monitors import Monitor
import datetime
import numpy as np
import pandas as pd
import os
import sys

# allocate window and graphics
win = visual.Window(
    size=(1920, 1080),
    fullscr=True,
    # fullscr=False,
    screen=0,
    allowGUI=False,
    allowStencil=False,
    monitor='testMonitor',
    color=[0, 0, 0],
    colorSpace='rgb',
    blendMode='avg',
    useFBO=False,
)

h = 0.1
text_correct = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='Correct!',
    font='Arial',
    pos=(0, 0),
    height=h,
    wrapWidth=None,
    color='Lime',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

text_incorrect = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='Incorrect',
    font='Arial',
    pos=(0.0),
    height=h,
    wrapWidth=None,
    color='red',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

text_between_blocks = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='Nice work! Press any key to continue.',
    font='Arial',
    pos=(0.0),
    height=h,
    wrapWidth=None,
    color='white',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

text_faster = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='Please respond faster.',
    font='Arial',
    pos=(0.0),
    height=h,
    wrapWidth=None,
    color='white',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

text_outro = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text='You\'re finished! Thanks for being awesome.',
    font='Arial',
    pos=(0.0),
    height=h,
    wrapWidth=None,
    color='white',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

text_problem_solved = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text=
    'You solved the problem! Press any key to proceed to the next problem.',
    font='Arial',
    pos=(0.0),
    height=h,
    wrapWidth=None,
    color='white',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

text_problem_failed = visual.TextStim(
    win=win,
    ori=0,
    name='text',
    text=
    'This problem seems tough. Lets try a different one. Press any key to proceed to the next problem.',
    font='Arial',
    pos=(0.0),
    height=h,
    wrapWidth=None,
    color='white',
    colorSpace='rgb',
    opacity=1,
    bold=False,
    alignHoriz='center',
    alignVert='center')

def TransformStim(xin, yin):

    #initialize variable, transfer labels
    trans_y = np.zeros(np.shape(xin)[0])

    # Convert x values; as long as input's x-values are in 0-100 space, this
    # line linearly transforms those values to -1:2 space; to choose
    # a different range, simply change the linear scaling, but be sure to
    # change the scaling for the y transformation as well so the ratio of the
    # axes remains the same.
    trans_x = (xin / 100) * 3 - 0.5
    # trans_x = (xin / 100) * 3 - 1

    # Nonlinear conversion of x values: trans_x exponentiated, resulting in a
    # range of .5-4 for CPD. DO NOT CHANGE.
    trans_x = 2**trans_x

    # Y values should also be in 0-100; negative values in particular cause
    # problems.
    if np.any(xin < 0) or np.any(yin < 0):
        print('Negative value for input!')

    # Linear conversion of y values to pi/11:(3*pi/8+pi/11) space. Again,
    # different ranges and bounds can be chosen at this step.
    # y = (yin / 100) * ((3 * np.pi / 8) + (np.pi / 11))
    y = (yin / 100) * ((3 * np.pi / 8) + (np.pi / 9))

    # # The remainder of the code performs the nonlinear transformation on the y
    # # values, which remain in the same space, but warped. DO NOT CHANGE.
    # ind = np.argsort(y)
    # sort_y = y[ind]
    # z = 4.7 * np.sin(sort_y)**2

    # trans_y[0] = np.sqrt(sort_y[0]**2 + z[0]**2)

    # for i in range(1, np.shape(sort_y)[0]):
    #     trans_y[i] = trans_y[i - 1] + np.sqrt(
    #         np.power(sort_y[i] - sort_y[i - 1], 2) +
    #         np.power(z[i] - z[i - 1], 2))

    # range_trans_y = np.amax(trans_y) - np.amin(trans_y)
    # range_sort_y = np.amax(sort_y) - np.amin(sort_y)

    # trans_y = trans_y / range_trans_y * range_sort_y
    # trans_y = trans_y - np.min(trans_y) + np.min(sort_y)

    # # NOTE: Convert radians to degrees
    # trans_y = trans_y * 180 / np.pi

    # xout = trans_x
    # yout = np.zeros(np.shape(xin)[0])
    # for i in range(0, len(ind)):
    #     yout[ind[i]] = trans_y[i]

    xout = trans_x
    yout = y * 180 / np.pi

    # NOTE: Convert Cycles per degree to cycles per cm
    mon = Monitor('testMonitor')
    mon.distance = 20.0  # viewing distance in cm
    xout = xout * (pix2deg(1, mon) / pix2cm(1, mon))

    return ([xout, yout])
