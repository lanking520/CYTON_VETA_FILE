import matplotlib.pyplot as plt
import numpy as np

class plotting:
   def __init__(self):
	self.dataset = [[5,0],[0,1],[2,3],[3,2]]
	self.label_x = []
	self.label_y = []
	self.fit_result = [[0],[0],[0]]
	self.file_name = 'Rubber.txt'

   def from_file(self,file_name = 'helper4'):
	self.file_name = file_name
	self.label_x, self.label_y = np.loadtxt(self.file_name, delimiter=',', unpack=True)

   def from_device(self, data):
	self.dataset = data
	self.data_sort()
	self.transform()
   
   def transform(self):
	for i in range(len(dataset)):
		self.label_x.append(self.dataset[i][0])
		self.label_y.append(self.dataset[i][1])

   def data_sort(self):
	data = np.array(self.dataset)
	self.dataset = data[np.argsort(data[:, 0])]

   def plotgraph(self):
	plt.plot(self.label_x, self.label_y, 'ro')
	plt.axis([-1, 1, 0, 12])
	plt.show()

   def plotfitting(self):
	point = np.linspace(-1, 1, 100)
	p1 = np.poly1d(self.fit_result[0])
	p2 = np.poly1d(self.fit_result[1])
	p3 = np.poly1d(self.fit_result[2])
	plt.plot(self.label_x, self.label_y, 'ro', point, p1(point), 'g.', point, p2(point), 'b--', point, p3(point), '-')
	plt.axis([-1, 1, 0, 12])
	plt.show()

   def subplotfitting(self):
	point = np.linspace(-1, 1, 100)
	p1 = np.poly1d(self.fit_result[0])
	p2 = np.poly1d(self.fit_result[1])
	p3 = np.poly1d(self.fit_result[2])
	f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

	ax1.set_title(str("%.3f" % self.fit_result[0][0]) + ' + ' + str("%.3f" % self.fit_result [0][1])+ 'x')
	ax2.set_title(str("%.3f" % self.fit_result[1][0]) + ' + ' + str("%.3f" % self.fit_result [1][1])+ 'x + ' + 			      str("%.3f" % self.fit_result[1][2])+'x^2')
	ax3.set_title(str("%.3f" % self.fit_result[2][0]) + ' + ' + str("%.3f" % self.fit_result [2][1])+ 'x + ' + 			      str("%.3f" % self.fit_result[2][2])+'x^2 + ' +str("%.3f" % self.fit_result [2][3])+ 'x^3')
	ax1.plot(self.label_x, self.label_y, 'o', point, p1(point), 'g.')
	ax2.plot(self.label_x, self.label_y, 'o', point, p2(point), 'b--')
	ax3.plot(self.label_x, self.label_y, 'o', point, p3(point), '-')
	plt.xlabel('Displacement Value')
	plt.ylabel('Force Value')
	plt.axis([-1, 1, 0, 12])
	plt.show()

   def fitting(self):
	x = np.array(self.label_x)
	y = np.array(self.label_y)
	self.fit_result[0] = np.polyfit(x, y, 1)
	self.fit_result[1] = np.polyfit(x, y, 2)
	self.fit_result[2] = np.polyfit(x, y, 3)

test = plotting()
test.from_file()
test.fitting()
test.subplotfitting()
