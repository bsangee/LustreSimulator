
class OSS:
	def __init__(self, numOST):
		self.numOST = numOST
		self.cpuUsage = 0.0
		self.memoryUsage = 0.0
		self.ioUsage = 0.0
		self.ostList = []

	def addOST(self, ost):
		self.ostList.append(ost)

	def simulateTimeUnit(self):
		totalDiskPercent = 0.0
		for ost in self.ostList:
			totalDiskPercent += float(ost.usedDiskSpace)/ost.totalDiskSpace
		self.cpuUsage = totalDiskPercent/len(self.ostList)
		

