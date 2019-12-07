from __future__ import division
from psychopy import visual, core, data, event, sound
from psychopy.constants import *
import datetime
import numpy as np
import pandas as pd
from copy import deepcopy
import os
import sys
import csv
from itertools import product
from consent import *
from instructions import *
from messages import *

# NOTE: SET THIS BEFORE RUNNING THE EXPERIMENT
sub_num = 2

data_dir = '../data'
stimuli_dir = '../stimuli'

# response key information
resp_key = {'f': 1, 'j': 2}

resp = -1
rt = -1

# open data file
f_data = open(data_dir + '/data_sub_' + str(sub_num) + '.csv', 'w')
f_okaydata = open(data_dir + '/ok_data' + '.csv', 'a')

data = csv.writer(f_data, quoting=csv.QUOTE_MINIMAL)
okaydata = csv.writer(f_okaydata, quoting=csv.QUOTE_MINIMAL)

okaydata.writerow([ok_data[0], ok_data[1]])

# set up for t2c --- iterate through many problems
max_trials_exp = 1200
max_trials_prob = 300
criterion = 0.9
recent_acc = np.empty(10)
recent_acc[:] = np.nan
consecutive_correct = 0
num_problems_solved = 0
prob_num = 0
prob_num_grating = 0
prob_num_binary = 0
relevant_dim = np.array([0, 1, 2, 3, 4, 5])
np.random.shuffle(relevant_dim)

current_trial_exp = 0
current_trial_prob = 0
current_trial_stim = 0

# load binary-dimension stimuli
stim_df = pd.read_csv(stimuli_dir + '/stimuli.txt',
                      sep=" ",
                      header=None,
                      dtype=int).values
num_stim = len(stim_df)

stim_bmp_arr = [
    visual.ImageStim(win,
                     image='../stimuli/bmp/' + str(i) + '.bmp',
                     pos=(0.0, 0.0)) for i in (range(1, num_stim + 1))
]

stim_ind_current_prob = np.arange(0, num_stim, 1)
np.random.shuffle(stim_ind_current_prob)

# setup grating stimuli
num_bins = 6
bin_width = 100 // num_bins
bin_bounds = np.arange(0, 100, bin_width)
bins = np.zeros((num_bins, 2))
for i in range(bin_bounds.shape[0] - 1):
    bins[i, 0] = bin_bounds[i]
    bins[i, 1] = bin_bounds[i + 1]

bin_dim = np.arange(0, num_bins, 1)
np.random.shuffle(bin_dim)

x_range = bins[bin_dim[prob_num_grating]]
xc = np.random.uniform(x_range[0], x_range[1])
lb1 = x_range[0]
ub1 = xc - 0.05 * bin_width
lb2 = xc + 0.05 * bin_width
ub2 = x_range[1]

if np.random.uniform() > 0.5:
    cat_map = 1
else:
    cat_map = 2

# setup fixation
fixation = visual.Rect(win, size=(1920, 1080))

# create and start timers
experiment_clock = core.Clock()
state_clock = core.Clock()

# display welcome message and wait for key press
give_instructions(win)

condition_timing = np.array(['delay', 'long_iti'])
condition_stimuli = np.array(['grating', 'binary'])
condition_1 = np.array(list(product(*[condition_timing, condition_stimuli])))
condition_2 = np.array(list(product(*[condition_timing, condition_stimuli])))
condition_3 = np.array(list(product(*[condition_timing, condition_stimuli])))
np.random.shuffle(condition_1)
np.random.shuffle(condition_2)
np.random.shuffle(condition_3)
condition = np.vstack((condition_1, condition_2, condition_3))

experiment_clock.reset()
while current_trial_exp < max_trials_exp:

    # determine problem type
    if condition[prob_num, 0] == 'delay':
        t_iti = 0.5
        t_fb_delay = 3.5
        t_fb_dur = 1.0

    elif condition[prob_num, 0] == 'long_iti':
        t_iti = 3.5
        t_fb_delay = 0.5
        t_fb_dur = 1.0

    # iti
    fixation.draw()
    win.flip()
    core.wait(t_iti)

    # stimulus
    if condition[prob_num, 1] == 'binary':
        x = -1
        y = -1

        if current_trial_stim == num_stim:
            np.random.shuffle(stim_ind_current_prob)
            current_trial_stim = 0
        current_stim = stim_bmp_arr[stim_ind_current_prob[current_trial_stim]]

        current_stim.draw()
        win.flip()
        state_clock.reset()

    elif condition[prob_num, 1] == 'grating':
        x1 = np.random.uniform(lb1, ub1)
        x2 = np.random.uniform(lb2, ub2)
        x = np.random.choice([x1, x2])
        y = np.mean(x_range)
        [xt, yt] = TransformStim(np.array([x]), np.array([y]))

        current_stim = visual.GratingStim(win,
                                          units='cm',
                                          mask='circle',
                                          sf=xt,
                                          ori=yt,
                                          pos=(0.0, 0.0),
                                          size=(5, 5))

        current_stim.draw()
        win.flip()
        state_clock.reset()

    # response
    resp = event.waitKeys(keyList=['f', 'j', 'escape'])[0]
    rt = state_clock.getTime()

    fixation.draw()

    if resp == 'escape':
        win.close()
        core.quit()

    # mask
    mask = visual.ImageStim(win,
                            units='cm',
                            image=np.random.uniform(0, 1, (100, 100, 3)),
                            pos=(0.0, 0.0),
                            size=(8, 8))
    mask.draw()
    win.flip()
    # win.getMovieFrame()
    # win.saveMovieFrames('mask.png')

    # feedback delay
    core.wait(t_fb_delay)

    # feedback
    if condition[prob_num, 1] == 'binary':
        if stim_df[stim_ind_current_prob[current_trial_stim],
                   relevant_dim[prob_num_binary] + 1] == 1:
            cat = 1
        else:
            cat = 2

    if condition[prob_num, 1] == 'grating':
        if cat_map == 1:
            if x < xc:
                cat = 1
            else:
                cat = 2
        else:
            if x >= xc:
                cat = 1
            else:
                cat = 2

    if rt > 5.0:
        consecutive_correct = 0
        recent_acc[:-1] = recent_acc[1:]
        recent_acc[-1] = 0
        text_faster.draw()
        win.flip()
        core.wait(2 * t_fb_dur)
    elif resp_key[resp] == cat:
        consecutive_correct += 1
        recent_acc[:-1] = recent_acc[1:]
        recent_acc[-1] = 1
        text_correct.draw()
        win.flip()
        core.wait(t_fb_dur)
    else:
        consecutive_correct = 0
        recent_acc[:-1] = recent_acc[1:]
        recent_acc[-1] = 0
        text_incorrect.draw()
        win.flip()
        core.wait(t_fb_dur)

    # write trial to file
    col_names = [
        'sub_num', 'condition_timing', 'condition_stim', 'stim_id', 'cat',
        'resp', 'rt', 'age', 'gender', 'date', 'prob_num', 'prob_num_grating',
        'prob_num_binary', 'num_problems_solved', 'current_trial_prob',
        'current_trial_stim', 'current_trial_exp', 'relevant_dim', 'x', 'y',
        'xc'
    ]

    if current_trial_exp == 0:
        data.writerow(col_names)

    data.writerow([
        sub_num, condition[prob_num, 0], condition[prob_num, 1],
        stim_ind_current_prob[current_trial_stim], cat, resp_key[resp], rt,
        ok_data[2], ok_data[3], datetime.datetime.today().strftime('%Y-%m-%d'),
        prob_num, prob_num_grating, prob_num_grating, num_problems_solved,
        current_trial_prob, current_trial_stim, current_trial_exp,
        relevant_dim[prob_num_binary] + 1, x, y, xc
    ])

    # reset trial
    resp = -1
    rt = -1
    current_trial_exp += 1
    current_trial_prob += 1
    current_trial_stim += 1

    # if they've reached criterion, then advance to the next problem
    # if consecutive_correct == criterion:
    if (np.nanmean(recent_acc) >= criterion) and (current_trial_prob >= 10):
        recent_acc[:] = np.nan
        consecutive_correct = 0
        num_problems_solved += 1

        prob_num += 1
        if (condition[prob_num, 1] == 'grating'):
            prob_num_grating += 1
        elif (condition[prob_num, 1] == 'binary'):
            prob_num_binary += 1

        current_trial_prob = 0
        current_trial_stim = 0
        np.random.shuffle(stim_ind_current_prob)

        if (condition[prob_num, 1] == 'grating') and (prob_num <
                                                      condition.shape[0]):
            x_range = bins[bin_dim[prob_num_grating]]
            xc = np.random.uniform(x_range[0], x_range[1])
            lb1 = x_range[0]
            ub1 = xc - 0.1 * bin_width
            lb2 = xc + 0.1 * bin_width
            ub2 = x_range[1]

            if np.random.uniform() > 0.5:
                cat_map = 1
            else:
                cat_map = 2

        text_problem_solved.draw()
        win.flip()
        event.waitKeys()

    # if reached max trials per problem, then advance to the next problem
    if current_trial_prob == max_trials_prob:
        prob_num += 1
        if (condition[prob_num, 1] == 'grating'):
            prob_num_grating += 1
        elif (condition[prob_num, 1] == 'binary'):
            prob_num_binary += 1
        current_trial_prob = 0
        current_trial_stim = 0
        np.random.shuffle(stim_ind_current_prob)

        if condition[prob_num, 1] == 'grating':
            x_range = bins[bin_dim[prob_num]]
            xc = np.random.uniform(x_range[0], x_range[1])
            lb1 = x_range[0]
            ub1 = xc - 0.1 * bin_width
            lb2 = xc + 0.1 * bin_width
            ub2 = x_range[1]

            if np.random.uniform() > 0.5:
                cat_map = 1
            else:
                cat_map = 2

        text_problem_failed.draw()
        win.flip()
        event.waitKeys()

    if prob_num_binary == 6:
        prob_num_binary = 0

    if prob_num == condition.shape[0]:
        break

# stop global timer
t_exp = experiment_clock.getTime()

# display welcome message and wait for key press
text_outro.draw()
win.flip()
event.waitKeys()

# close files
f_data.close()
f_okaydata.close()

# exit experiment
win.close()
core.quit()
