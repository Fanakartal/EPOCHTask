import numpy
from matplotlib import pyplot as plt

x = [x for x in range(0, 10)]
y = numpy.random.rand(10)

# Plot the Data itself.
plt.plot(x, y)

# Calculate the Trendline
z = numpy.polyfit(x, y, 1)
p = numpy.poly1d(z)

# Display the Trendline
plt.plot(x, p(x))
plt.show()
