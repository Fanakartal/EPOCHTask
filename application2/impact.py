import math

import matplotlib.pyplot as plt
import csv

# UNCOMMENT BELOW if you want auto-scaled graph
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm


# plt.figure(figsize=(32, 18), dpi=480)

# For getting the column names of the data.
file = open('..\\application2\\dataset.csv', mode='r', encoding='UTF-8', errors='ignore')
csvreader = csv.reader(file, delimiter=';')
column_names = next(csvreader)

print(column_names)

# For adding all rows to a dictionary where the keys are the id(order) of the row.
rows = []
data_dict = {}
games_dict = {}
vision_dict = {}
language_dict = {}
games_index, vision_index, language_index = 0, 0, 0
for index, row in enumerate(csvreader):
    rows.append(row)
    data_dict[index] = row
    if row[2] == 'Games':
        games_dict[games_index] = row
        games_index += 1
    if row[2] == 'Vision':
        vision_dict[vision_index] = row
        vision_index += 1
    if row[2] == 'Language':
        language_dict[language_index] = row
        language_index += 1

print(data_dict)
print(games_dict)
print(vision_dict)
print(language_dict)

all_years = []

game_years_x_axis = []
game_citation_counts_y_axis = []
game_research_label = []

vision_years_x_axis = []
vision_citation_counts_y_axis = []
vision_research_label = []

language_years_x_axis = []
language_citation_counts_y_axis = []
language_research_label = []

with open('..\\application2\\dataset.csv', mode='r', encoding='UTF-8', errors='ignore') as file:
    lines = csv.reader(file, delimiter=';')
    titles = next(lines)
    for column in lines:
        all_years.append(int(column[3]))
        if column[5] == '':
            continue
        if column[2] == 'Games':
            game_years_x_axis.append(int(column[3]))
            game_citation_counts_y_axis.append(int(column[5]))
            game_research_label.append(int(column[0]))
        if column[2] == 'Vision':
            vision_years_x_axis.append(int(column[3]))
            vision_citation_counts_y_axis.append(int(column[5]))
            vision_research_label.append(int(column[0]))
        if column[2] == 'Language':
            language_years_x_axis.append(int(column[3]))
            language_citation_counts_y_axis.append(int(column[5]))
            language_research_label.append(int(column[0]))

fig, axs = plt.subplots()  # (1, 3)
fig.set_figwidth(16)
fig.set_figheight(9)
fig.set_dpi(120)

scatter1 = axs.scatter(game_years_x_axis, game_citation_counts_y_axis,
                          facecolors='none', color='g', marker='o', label=game_research_label)
scatter2 = axs.scatter(vision_years_x_axis, vision_citation_counts_y_axis,
                          facecolors='none', color='r', marker='s', label=vision_research_label)
scatter3 = axs.scatter(language_years_x_axis, language_citation_counts_y_axis,
                          facecolors='none', color='b', marker='v', label=language_research_label)
axs.set_xticks(np.arange(min(all_years), max(all_years), 5))
axs.legend(['Games', 'Vision', 'Language'])

# log_y_games = [math.log10(num) for num in game_citation_counts_y_axis]
game_regression = np.polyfit(game_years_x_axis, game_citation_counts_y_axis, deg=1)
game_xseq = np.linspace(min(game_years_x_axis), max(game_years_x_axis), num=len(game_years_x_axis))
axs.plot(game_xseq, game_regression[0] * game_xseq + game_regression[1], color="g", linestyle='dashed')

# test1 = sm.het_goldfeldquandt(results.resid, results.model.exog)

X = sm.add_constant(game_years_x_axis)
np_x = np.array(game_years_x_axis).reshape((-1, 1))
np_y = np.array(game_citation_counts_y_axis)
model = sm.OLS(np_y, np_x).fit()
print(model.summary())

res1, res2, order = sm.stats.diagnostic.het_goldfeldquandt(np_y, np_x, drop=0.2)
print(res1, res2, order)

# test2 = sm.het_breuschpagan(fit.resid, fit.model.exog)

# log_y_vision = [math.log2(num) for num in vision_citation_counts_y_axis]
vision_regression = np.polyfit(vision_years_x_axis, vision_citation_counts_y_axis, deg=1)
vision_xseq = np.linspace(min(vision_years_x_axis), max(vision_years_x_axis), num=len(all_years))
axs.plot(vision_xseq, vision_regression[0] * vision_xseq + vision_regression[1], color="r", linestyle='dashed')
# axs.plot(vision_xseq, vision_regression[0] * (vision_xseq ** 2) + vision_regression[1] * vision_xseq +
# vision_regression[2], color="r", linestyle='dashed')

language_regression = np.polyfit(language_years_x_axis, language_citation_counts_y_axis, deg=1)
language_xseq = np.linspace(min(language_years_x_axis), max(language_years_x_axis), num=len(language_years_x_axis))
axs.plot(language_xseq, language_regression[0] * language_xseq + language_regression[1], color="b", linestyle='dashed')

plt.grid()
# plt.tight_layout()
plt.xticks(rotation=45)
plt.xlabel('Year')
plt.ylabel('Citations')

# UNCOMMENT BELOW if you want to show the figure in PyCharm
plt.show()
