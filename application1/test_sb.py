# import libraries
import csv

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# For getting the column names of the data.
file = open('KGSizeTrendWithDates_v2.csv', mode='r')
csvreader = csv.reader(file)
column_names = next(csvreader)

# For adding all rows to a dictionary where the keys are the id(order) of the row.
rows = []
data_dict = {}
for row in csvreader:
    rows.append(row)
    data_dict[str(row[0])] = row

# For taking the names of the knowledge graphs (to use them on plot labels if needed).
kg_names = []
for values in data_dict.values():
    kg_names.append(values[1])

# For creating data for x- and y-axes and adding them to respective lists.
x_dates = []
x_date_int_list = []
y_entities = []
citation_counts = []
z_relations = []
with open('KGSizeTrendWithDates_v2.csv', mode='r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    titles = next(lines)
    for column in lines:
        citation_counts.append(int(column[5]))
        temp_date_str = str(column[4])
        temp_datetime_obj = datetime.strptime(temp_date_str, '%d/%m/%Y %H:%M:%S')
        temp_date_obj = temp_datetime_obj.date()
        x_dates.append(temp_date_obj)
        str_date = (str(temp_date_obj.year) + f"{temp_datetime_obj.month:02d}" + f"{temp_datetime_obj.day:02d}")
        x_date_int_list.append(int(str_date))
        y_entities.append(int(column[6]))

# For scaling the data points proportional to citation count of the original study
citation_sum = sum(citation_counts)
scaler = 3000
relative_cc_list = []
for i in range(len(citation_counts)):
    temp_ratio = (citation_counts[i] / citation_sum) * scaler
    relative_cc_list.append(temp_ratio)

# For adding the Usage Count legend
plt.rc('legend', title_fontsize=8, fontsize=7, labelspacing=0.75, handlelength=2)

# For creating scatter plot for data points.
fig, ax = plt.subplots()
scatter = ax.scatter(x_date_int_list, y_entities, s=relative_cc_list, facecolors='none', color='g', marker='o', label=kg_names)
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))

# For creating 90% confidence interval in visual graph.
sns.regplot(x=x_date_int_list, y=y_entities, ci=90, color=None)

# For writing x-,y-axis and data point labels.
plt.xlabel('Date')
plt.ylabel('Number of Entities')
plt.title('Knowledge Graph Sizes', fontsize=15)
for index in range(len(x_dates)):
    ax.text(x_dates[index], y_entities[index], kg_names[index], size=7)
plt.grid()

plt.show()
