"""
Runs analysis according to specific demands
"""

from DataHandler import *
from Graph import *
from CurveFit import *
from Equations import *
from PIL import Image
from ImageHandler import *
import numpy as np
from scipy.stats import linregress
import os
import matplotlib.pyplot as plt


def calculate_lumen(csv_path):
    """
    Calculates the average value of lumen from the given data file
    :param csv_path: path of csv file
    :return: the average lumen
    """
    try:
        data_handler = DataHandler(csv_path)
        a = data_handler._df[data_handler._df.columns[-1:data_handler._df.columns.size]].to_numpy()
        a = a.reshape(1, a.size)[0][5:]
        return a.mean()
    except:
        return "An error occurred during processing of file: {}".format(csv_path)


def graph_results_2(a, b):
    """
    Plots the
    :param results_dict: holds voltages and magnetization percentages
    :return: None
    """
    g = Graph(a - a[0], b)
    g.set_labels("Light Lumen vs. Relative Angle between 2 Polarizers, With fit.", "Relative Angle", "Lumen")
    g.plot_with_fit(cos_squared)


def graph_results_3(a, b):
    """
    Plots the
    :param results_dict: holds voltages and magnetization percentages
    :return: None
    """
    a = a - a[0]
    g = Graph(a, b)
    g.set_labels("Light Lumen vs. Relative Angle between 3 Polarizers, With fit.", "Relative Angle", "Lumen")
    g.set_errors(a/50, b/50)
    g.plot_with_fit_and_errors(cos_squared)


if __name__ == '__main__':
    for i, num_polarizers in enumerate([2, 3]):
        angles = []
        lumens = []
        directory = "data\\{0}".format(num_polarizers)
        dir_name = "experiment {0}: {1} polarizers".format(i, num_polarizers)
        for filename in os.listdir(directory):
            angles.append(os.path.splitext(filename)[0])
            lumen = calculate_lumen(os.path.join(directory, filename))
            if type(lumen) != str:
                lumens.append(lumen)
            else:
                print("An error occurred during processing of file: {}".format(filename))
        angles = np.array(angles).astype(float) * np.pi / 180
        lumens = np.array(lumens).astype(float)
        if i == 0:
            # pass
            graph_results_3(angles, lumens)
        # elif i == 1:
        #     plt.plot(lumens)
        #     plt.show()
        #     graph_results_3(angles, lumens)
