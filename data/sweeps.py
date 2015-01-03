#!/usr/bin/python

import sys
sys.path.extend(['../..'])
import tsg_plot
import numpy

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
  f = open("sweeps.csv", 'r')
  for line in f:
    # Skip empty lines and comments
    if not line.strip() or line[0] == '#':
      continue
    ls = line.strip().split(',')
    # Find monitor names
    if len(ls) == 1:
      if ls[0] != '':
        monitor = ls[0]
        data[monitor] = {}
        data[monitor]['overheads'] = []
        data[monitor]['data'] = []
    else:
      # Benchmarks
      if ls[0] == '':
        data[monitor]['benchmarks'] = ls[1:] + ["geomean"]
      # Data line
      else:
        overhead = float(ls[0].split('=')[1])
        if overhead != 0 and overhead != 30:
          if overhead < 0.1:
            data[monitor]['overheads'].append("%.2fx" % (overhead + 1))
          else:
            data[monitor]['overheads'].append("%.1fx" % (overhead + 1))
          d = [float(x)*100 for x in ls[1:]]
          d.append(geomean(d))
          data[monitor]['data'].append(d)
  f.close()
  for mon in data.keys():
    print mon
    print data[mon]

  # Reformat data
  for monitor in data.keys():
    d = data[monitor]['data']
    # Get differences for stacked graph
    diffs = [d[0]]
    for i in range(1, len(d)):
      diffs.append([x - y for (x, y) in zip(d[i], d[i-1])])
    # Transpose
    diffs = numpy.array(diffs).transpose()
    data[monitor]['data'] = diffs

  return data


def plot(data, filename):
  # Set up plotting options
  opts = tsg_plot.PlotOptions()
  # Benchmarks
  cat = data['benchmarks']
  # Overheads
  subcat = data['overheads']
  opts.data = data['data']
  opts.labels = [cat, subcat]

  attribute_dict = \
      {
          'plot_type' : 'stacked_bar',
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
  for mon in data.keys():
    if mon != "insttype":
      plot(data[mon], "../figs/data_%s_sweep.pdf" % (mon))
