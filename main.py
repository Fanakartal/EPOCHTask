import matplotlib.pyplot as plt
import csv

import numpy

file = open('KGSizeTrend.csv', mode='r')
csvreader = csv.reader(file)
column_names = next(csvreader)
print(len(column_names))
rows = []
data_dict = {}
for row in csvreader:
    rows.append(row)
    data_dict[str(row[0])] = row

kg_names = []
for values in data_dict.values():
    kg_names.append(values[1])

x_dates = []
y_entities = []
z_relations = []

with open('KGSizeTrend.csv', mode='r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    titles = next(lines)
    for column in lines:
        x_dates.append(int(column[2]))
        y_entities.append(int(column[4]))

plt.scatter(x_dates, y_entities, color='g', marker='x', label=kg_names)  # , color='g', linestyle='dashed', marker='o', label="Knowledge Graph Sizes")

# Calculate the Trendline
z = numpy.polyfit(x_dates, y_entities, 1)
p = numpy.poly1d(z)

plt.plot(x_dates, p(x_dates))

# plt.xticks(rotation=25)
plt.xlabel('Year')
plt.ylabel('Number of Entities')
plt.title('Knowledge Graph Sizes', fontsize=15)
# plt.grid()
# plt.legend()
plt.show()
