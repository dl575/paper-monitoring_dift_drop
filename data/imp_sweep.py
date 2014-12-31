#!/usr/bin/python

import sys
sys.path.extend(['../..'])
import tsg_plot
import math

# Parse data
f = open("imp_sweep.csv", 'r')
"""
f.readline()
subcat = f.readline().strip().split(',')[1:]

cat = []
average_errors = []
for i in range(4):
  ls = f.readline().split(',')
  cat.append(ls[0])
  average_errors.append([float(x) for x in ls[1:]])
for i in range(5):
  f.readline()
max_errors = []
for i in range(4):
  ls = f.readline().split(',')
  max_errors.append([float(x) for x in ls[1:]])
for i in range(5):
  f.readline()
min_errors = []
for i in range(4):
  ls = f.readline().split(',')
  min_errors.append([float(x) for x in ls[1:]])
"""

average_errors = []
min_errors = []
max_errors = []
overheads = []
mode = None
line = f.readline()
while line:
  ls = line.strip()
  # Skip empty lines
  if not ls:
    pass
  # Switch to new data type
  elif ls == "Average" or ls == "Min" or ls == "Max":
    mode = ls
    benchmarks = f.readline().strip().split(',')[1:]
  elif mode == "Average":
    ls = ls.split(',')
    overheads.append(ls[0])
    average_errors.append([float(x) for x in ls[1:]])
  elif mode == "Min":
    ls = ls.split(',')
    min_errors.append([float(x) for x in ls[1:]])
  elif mode == "Max":
    ls = ls.split(',')
    overheads.append(ls[0])
    max_errors.append([float(x) for x in ls[1:]])
  else:
    pass

  line = f.readline()

f.close()

import numpy
average_errors = numpy.array(average_errors).transpose()
min_errors = numpy.array(min_errors).transpose()
max_errors = numpy.array(max_errors).transpose()
subcat = benchmarks
cat = overheads

# Set up plotting options
opts = tsg_plot.PlotOptions()
opts.data = average_errors
opts.labels = [subcat, cat]

attribute_dict = \
    {
        'show' : False,
        'file_name' : '../figs/data_imp_sweep.pdf',
        'paper_mode' : True,
        'figsize' : (7.0, 2.0),
        'ylabel' : 'Error [%]',
        'legend_ncol' : 6,
        'rotate_labels' : False,
        'rotate_labels_angle' : -45,
        'fontsize' : 8,
        'errorbars' : [min_errors, max_errors],
        #'colors' : ['#eff3ff', '#bdd7e7', '#6baed6', '#2171b5']
        'colors' : ['#deebf7', '#9acae1', '#3182bd', '#deebf7', '#9ecae1', '#3182bd'],
        'hatch' : ['']*3 + ['//']*3
    }
for name, value in attribute_dict.iteritems():
  setattr( opts, name, value )

# Plot
tsg_plot.add_plot( opts )
