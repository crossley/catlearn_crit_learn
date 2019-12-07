library(data.table)
library(ggplot2)

rm( list = ls())

d = fread('../data/data_sub_2.csv')

d[, t2c := max(current_trial_prob),
  .(sub_num, condition_timing, condition_stim, prob_num)]

d[order(condition_stim, condition_timing),
  unique(t2c),
  .(sub_num, condition_stim, condition_timing)]

d[order(condition_stim, condition_timing),
  mean(t2c),
  .(sub_num, condition_stim, condition_timing)]

d[, .(min(x), max(x), unique(xc)), .(condition_timing, condition_stim)]
