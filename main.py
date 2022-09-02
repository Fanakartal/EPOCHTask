import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import numpy
from datetime import datetime

plt.figure(figsize=(35, 15), layout='tight')  # dpi=600) # , figsize=(15, 5))  # 1200
# plt.rcParams["figure.figsize"] = [25, 15]
# plt.rcParams["figure.autolayout"] = True

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

plt.rc('legend', title_fontsize=8, fontsize=7, labelspacing=0.75, handlelength=2)

# For creating scatter plot for data points.
fig, ax = plt.subplots()
# ax.tick_params(axis='x', length=12, width=25, grid_linewidth=15)
scatter = ax.scatter(x_dates, y_entities, s=relative_cc_list, facecolors='none', color='g', marker='o', label=kg_names)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))

# For calculating and plotting the trend line.
z = numpy.polyfit(x_date_int_list, y_entities, 1)
p = numpy.poly1d(z)
plt.plot(x_dates, p(x_date_int_list), linestyle='dashed')

# For writing x-,y-axis and data point labels.
plt.xticks(rotation=45)
plt.xlabel('Year')
plt.ylabel('Number of Entities')
plt.title('Knowledge Graph Sizes', fontsize=15)
for index in range(len(x_dates)):
    ax.text(x_dates[index], y_entities[index], kg_names[index], size=7)
plt.grid()
# plt.legend(fontsize=10)

# For creating a legend for every data point study with their citation counts
handles, labels = scatter.legend_elements(prop="sizes", alpha=0.2)
citation_count_labels = []
for element in labels:
    int_element = int(''.join(i for i in element if i.isdigit()))
    temp_element = int((int_element / scaler) * citation_sum)
    str_label = '$\\mathdefault{' + str(temp_element) + '}$'
    citation_count_labels.append(str_label)
plt_size_legend = ax.legend(handles, citation_count_labels, loc="upper left", title="Usage Count")

# spacing = 1
# fig.subplots_adjust(right=spacing)
plt.tight_layout()
plt.show()
