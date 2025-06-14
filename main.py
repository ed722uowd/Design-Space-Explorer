import pandas as pd
import os
import subprocess

from extract_attributes import get_attributes, attribute_combination

import matplotlib.pyplot as plt
import numpy as np

import numpy as np

def read_plot_points(filename):

    plot_points = []

    with open(filename, 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split(','))
            plot_points.append([x, y])

    return plot_points



def pareto_plotting(plot_points):
    # Sort plot_points by latency (x-axis) for easier Pareto search
    plot_points = np.array(plot_points)

    sorted_points = plot_points[plot_points[:, 1].argsort()]

    optimal_aluts = []
    optimal_latency =[]

    # Identify Pareto-optimal points
    pareto_points = []
    current_min_aluts = float('inf')
    for aluts, latency in sorted_points:
        if aluts < current_min_aluts:
            pareto_points.append([aluts, latency])
            current_min_aluts = aluts

    pareto_points = np.array(pareto_points)

    # Plotting all points
    plt.scatter(plot_points[:, 1], plot_points[:, 0], label="All Designs", color="blue")

    # Plotting Pareto-optimal points
    plt.scatter(pareto_points[:, 1], pareto_points[:, 0], label="Pareto-optimal", color="red")

    plt.xlabel("Latency")
    plt.ylabel("ALUTs")
    plt.title("ALUTs vs. Latency of Designs")
    plt.legend()
    plt.show()

    # Print Pareto-optimal points
    for aluts, latency in pareto_points:
        optimal_aluts.append(aluts)
        optimal_latency.append(latency)
        print(f"Pareto-optimal design: ALUTs={aluts}, Latency={latency}")
    
    return optimal_aluts, optimal_latency


def change_extension(file_path, new_extension):
    base_name, _ = os.path.splitext(file_path)
    new_file_path = base_name + "." + new_extension
    os.rename(file_path, new_file_path)

def extract_points (file_path):

    find_ALUTs = 0
    find_Latency = 0
    found_both = 0
    with open(file_path,'r+') as file:
            for line in file:
                if (found_both == 2):
                        break
                extracted_words = line.split()
                if (not extracted_words):
                        continue
                else:
                        if (extracted_words[0] == "ALUTs" and find_ALUTs == 0):
                            ALUTs = int(extracted_words[-1])
                            find_ALUTs = 1
                            found_both += 1
                            #print(ALUTs)
                        elif (extracted_words[0] == "Latency" and find_Latency == 0):                            
                            find_Latency = 1
                            found_both += 1
                            Latency = int(extracted_words[-1])
                            #print(Latency)
    
    return ALUTs, Latency


file_path = "lib_sobel.info"
attributes = get_attributes(file_path)


for x in attributes:
     print(x)

combination_matrix, combination = attribute_combination(attributes)

df_comb_matrix = pd.DataFrame(combination_matrix)
print(df_comb_matrix)

rows, cols = combination, 2
plot_points = [[0 for _ in range(cols)] for _ in range(rows)]

file_path = "attrs.txt"
c_file = "attrs.h"
qor_file = "sobel.QOR"
file = open(file_path,"w")

for i in range(combination):
    if os.path.exists(file_path):
            file.close()
            os.remove(file_path) 
    file = open(file_path,"w")
    for j in range(len(attributes)):
        line = combination_matrix[j][i]
        file.write(line+"\n")
    
    file.close()

    if os.path.exists(c_file):
            os.remove(c_file)
    change_extension(file_path,"h")

    """
    If you have cyber workbench 
        uncomment the following lines
        Comment the line: plot_points = read_plot_points ("plot_points.txt")

    if you don't have cyber workbench
     remove comment from the line: plot_points = read_plot_points ("plot_points.txt")
     and comment the lines below

    """

    """
    If you have cyberworkbench remove the comment for the following lines of code
    """
    """
    if os.path.exists(qor_file):
          os.remove(qor_file)
    subprocess.run('cpars sobel.c', shell=True)
    subprocess.run('bdltran -c2000 -s sobel.IFF -lfl cycloneV.FLIB -lb cycloneV.BLIB', shell=True)

    ALUTs, Latency = extract_points (qor_file)

    plot_points [i][0] = ALUTs
    plot_points [i][1] = Latency

    print(plot_points)
    subprocess.run('clear', shell=True)
    print(i)

    """

"""
If you do not have cyberworkbench remove the comment for the following lines of code
"""
plot_points = read_plot_points ("plot_points.txt")
#print(plot_points)
optimal_aluts, optimal_latency = pareto_plotting(plot_points)

optimal_aluts = [175,176]
optimal_latency = [1,1]

df_plot_points = pd.read_csv("plot_points.txt", sep=",", header=None, names=["ALUTs", "Latency"])
pragma_pos = []

#Get pragma pos from combination matrix
for i in range(len(optimal_aluts)):
    tmp_pragma_pos = []
    for j in range(combination):
        if (df_plot_points.iloc[j, 0] == optimal_aluts[i] and df_plot_points.iloc[j, 1] == optimal_latency[i]):
            tmp_pragma_pos.append(j)
    
    pragma_pos.append(tmp_pragma_pos)

print(pragma_pos)
extracted_optimal_pragmas ={}
for i in range (len(pragma_pos)):
     extracted_optimal_pragmas[i]= df_comb_matrix[pragma_pos[i]].T
     print("Pragma combinations for ALUTs ", optimal_aluts[i], " and latency ", optimal_latency[i])
     print(extracted_optimal_pragmas[i])
     file_name = f"pragmas_Latency_{optimal_latency[i]}_ALUTs_{optimal_aluts[i]}_{i}.csv"
     extracted_optimal_pragmas[i].to_csv(file_name)
     print(f"File saved: {file_name}")
