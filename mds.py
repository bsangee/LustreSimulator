import random

class RandomMDS:
	def __init__(self, totalNumOST, parentSimulator):
		self.totalNumOST = totalNumOST
		self.parentSimulator = parentSimulator

	def simulateTimeUnit(self):
		pass

	def getOSTsForWrite(self, bytes, numOST):
		# Logic to select OSTs
		selectedOST = random.sample(range(self.totalNumOST), numOST)
		return selectedOST

class RoundRobinMDS:
	def __init__(self, totalNumOST, parentSimulator):
		self.totalNumOST = totalNumOST
		self.parentSimulator = parentSimulator
		self.currOST = 0

	def simulateTimeUnit(self):
		pass

	def getOSTsForWrite(self, bytes, numOST):
		# Logic to select OSTs
		selectedOST = [(self.currOST+i)%self.totalNumOST for i in range(numOST)]
		self.currOST = (self.currOST+numOST)%self.totalNumOST
		return selectedOST

class DivideMDS:
	def __init__(self, totalNumOST, parentSimulator):
		self.totalNumOST = totalNumOST
		self.parentSimulator = parentSimulator

	def simulateTimeUnit(self):
		pass

	def getOSTsForWrite(self, bytes, numOST):
		# Logic to select OSTs
		wbByKaList = [(float(ost.bytesToStore)/ost.freeDiskSpace(), -ost.freeDiskSpace()) for ost in self.parentSimulator.ostList]
		wbByKaIndex = sorted(range(len(wbByKaList)), key=lambda k: wbByKaList[k])
		selectedOST = wbByKaIndex[:numOST]
		return selectedOST