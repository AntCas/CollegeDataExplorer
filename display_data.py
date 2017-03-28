import csv
import numpy
import matplotlib.pyplot as plt

def plot_all_bars(ranks, acceptance_rates, exported_figure_filename):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    #prices = list(map(int, ranks))
    X = numpy.arange(len(ranks))
    width = 0.25
    ax.bar(X+width, acceptance_rates, width) 
    ax.set_xlim([0, 250])
    fig.savefig(exported_figure_filename)

fieldNames = ['name', 'rank', 'acceptance']
dataTypes = [('name', 'a200'), ('rank','i'), ('acceptance', 'i')]

# Load data from csv into numpy
college_data = numpy.genfromtxt('college_data.csv', delimiter=',', skip_header=1,
                            names=fieldNames, invalid_raise=False, 
                            dtype=dataTypes) 

plot_all_bars(college_data['rank'], college_data['acceptance'], 'chart_college_data.png')
