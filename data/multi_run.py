#!/usr/bin/python

import sys
sys.path.extend(['../..'])
import tsg_plot
import math

# Parse data
f = open("multi_run.csv", 'r')
#subcat = f.readline().strip().split(',')[1:]
cat = []
data = []
for line in f:
  if line.strip():
    ls = line.strip().split(',')
    cat.append(ls[0])
    data.append([float(x)*100 for x in ls[1:]])
f.close()

subcat = ["%d" % (x + 1) for x in range(len(data[0]))]
subcat[-1] += " runs"

# Set up plotting options
opts = tsg_plot.PlotOptions()
opts.data = data
opts.labels = [cat, subcat]

attribute_dict = \
    {
        'show' : False,
        'file_name' : '../figs/data_multirun_coverage.pdf',
        'paper_mode' : True,
        'figsize' : (3.5, 2.0),
        'ylabel' : 'Coverage [%]',
        'legend_ncol' : 8,
        'legend_handlelength' : 1.0,
        'legend_columnspacing' : 0.8,
        'legend_handletextpad' : 0.5,
        'legend_bbox' : [-0.05, 1.05, 1, 0.1],
        'rotate_labels' : False,
        'rotate_labels_angle' : -30,
        'fontsize' : 8,
        'yrange' : [80, 100],

        #'colors' : ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd"]

        # 'colors' : ["#d7191c", "#fdae61", "#ffffbf", "#abdda4", "#2b83ba", "#d7191c", "#fdae61", "#ffffbf", "#abdda4", "#2b83ba"],
        # 'hatch' : [' ']*5 + ['///']*5

        #'colors' : ['#8dd3c7', '#ffffb3', '#bebada', '#8dd3c7', '#ffffb3', '#bebada', '#8dd3c7', '#ffffb3', '#bebada', '#8dd3c6'],
        #'hatch' : ['']*3 + ['/']*3 + ['xx']*3 + ['//']

        'colors' : ['#eff3ff', '#bdd7e7', '#6baed6', '#2171b5', '#eff3ff', '#bdd7e7', '#6baed6', '#2171b5'],
        'hatch' : ['']*4 + ['//']*4

    }
for name, value in attribute_dict.iteritems():
  setattr( opts, name, value )

# Plot
tsg_plot.add_plot( opts )
