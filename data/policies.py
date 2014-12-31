#!/usr/bin/python

import sys
sys.path.extend(['../..'])
import tsg_plot
import numpy

monitors = ["BC", "UMC"]
metrics = ["Coverage", "Overhead difference"]

def geomean(l):
  """
  Return the geometric mean of the passed list.
  """
  prod = 1.0
  n = 0
  for ll in l:
    prod *= ll
    n += 1
  return prod**(1.0/n)


def parse():
  # Parse data
  data = {}
  f = open("policies.csv", 'r')
  for line in f:
    ls = line.strip().split(',')
    if ls == ['']:
      continue
    elif ls[0] in monitors:
      monitor = ls[0]
      data[monitor] = {}
    else:
      if ls[0] in metrics:
        metric = ls[0]
        data[monitor][metric] = {}
        data[monitor][metric]['data'] = []
        data[monitor][metric]['categories'] = []
        data[monitor][metric]['benchmarks'] = ls[1:]
      elif len(ls) > 0:
        data[monitor][metric]['categories'].append(ls[0])
        ls2 = [float(d[:-1]) for d in ls[1:]]
        data[monitor][metric]['data'].append(ls2)
  f.close()

  # Transpose
  for x in monitors:
    for y in metrics:
      d = data[x][y]['data']
      d = numpy.array(d).transpose()
      data[x][y]['data'] = d

  return data

def plot(data, filename):
  # Set up plotting options
  opts = tsg_plot.PlotOptions()
  # Benchmarks
  cat = data['benchmarks']
  # Overheads
  subcat = data['categories']
  opts.data = data['data']
  opts.labels = [cat, subcat]

  attribute_dict = \
      {
          'plot_type' : 'bar',
          'show' : False,
          'file_name' : filename,
          'paper_mode' : True,
          'figsize' : (3.5, 2.0),
          'ylabel' : 'Coverage [%]',
          'legend_ncol' : 6,
          'legend_handlelength' : 1.0,
          'legend_columnspacing' : 0.8,
          'legend_handletextpad' : 0.5,
          'legend_bbox' : [-0.05, 1.05, 1, 0.1],
          'rotate_labels' : True,
          'rotate_labels_angle' : -45,
          'fontsize' : 8,
          'bar_width' : 0.5,

          'colors' : ['#deebf7', '#9acae1', '#3182bd', '#deebf7', '#9ecae1', '#3182bd'],
          'hatch' : ['']*3 + ['//']*3

      }
  for name, value in attribute_dict.iteritems():
    setattr( opts, name, value )

  # Plot
  tsg_plot.add_plot( opts )

if __name__ == "__main__":
  data = parse()
  plot(data["UMC"]["Coverage"], "temp.pdf")
  for x in monitors:
    for y in metrics:
      plot(data[x][y], "../figs/data_%s_%s.pdf" % (x.lower(), y.split(' ')[0].lower()))
  #for mon in data.keys():
  #  if mon != "insttype":
  #    plot(data[mon], "../figs/data_%s_sweep.pdf" % (mon))
