from oss import OSS
from ost import OST
from mds import RandomMDS, RoundRobinMDS, DivideMDS
import math
import random

class LustreSimulator:
	def __init__(self, numOSS, numOSTPerOSS, diskSpacePerOST):
		self.ossList = []
		self.ostList = []
		for i in range(numOSS):
			oss = OSS(numOSTPerOSS)
			for j in range(numOSTPerOSS):
				ost = OST(diskSpacePerOST, oss)
				self.ostList.append(ost)
				oss.addOST(ost)
			self.ossList.append(oss)
		#self.mds = RandomMDS(numOSS*numOSTPerOSS, self)
		#self.mds = RoundRobinMDS(numOSS*numOSTPerOSS, self)
		self.mds = DivideMDS(numOSS*numOSTPerOSS, self)

	def simulateTimeUnits(self, numUnits):
		for i in range(numUnits):
			for oss in self.ossList:
				for ost in oss.ostList:
					ost.simulateTimeUnit()
				oss.simulateTimeUnit()
			self.mds.simulateTimeUnit()
			ostStats = [ost.stats() for ost in self.ostList]
			capacityStats = [stats[0] for stats in ostStats]
			capacityLine = ",".join(map(str, capacityStats)) + "\n"
			self.capacityPtr.write(capacityLine)
			bytesToWriteStats = [stats[1] for stats in ostStats]
			bytesToWriteLine = ",".join(map(str, bytesToWriteStats)) + "\n"
			self.bytesToWritePtr.write(bytesToWriteLine)
			bandwidthStats = [stats[2] for stats in ostStats]
			bandwidthLine = ",".join(map(str, bandwidthStats)) + "\n"
			self.bandwidthPtr.write(bandwidthLine)

	def accommodateWriteRequest(self, bytes, numOST, timeUnitsTillNextRequest):
		selectedOSTIndices = self.mds.getOSTsForWrite(bytes, numOST)
		bytesPerOST = int(math.ceil(float(bytes)/numOST))
		for ostIndex in selectedOSTIndices:
			ost = self.ostList[ostIndex]
			ost.addBytesToStore(bytesPerOST)
		self.simulateTimeUnits(timeUnitsTillNextRequest)

	def readAppLog(self, filename):
		fptr = open(filename, 'r')
		text = fptr.read()
		lines = text.split("\n")
		lines.remove('')
		fptr.close()
		numReq = len(lines)
		self.capacityPtr = open(capacityCSV, 'w')
		self.bytesToWritePtr = open(bytesToWriteCSV, 'w')
		self.bandwidthPtr = open(bandwidthCSV, 'w')
		for i in range(numReq):
			line = lines[i]
			print "Request: {0}".format(line)
			currTimestamp, reqSize, numOSTs = map(int, line.split(" ")) 
			if i != (numReq - 1):
				nextLine = lines[i+1]
				nextTimeStamp, _, _ = map(int, nextLine.split(" "))
				timeUnits = nextTimeStamp - currTimestamp
			else:
				timeUnits = 5
			self.accommodateWriteRequest(reqSize, numOSTs, timeUnits)
		self.capacityPtr.close()
		self.bytesToWritePtr.close()
		self.bandwidthPtr.close()

##########################################################
random.seed(1)
numOSS = 8
numOSTPerOSS = 4
diskSpacePerOST = 8796093022208		# 8 TB
sim = LustreSimulator(numOSS, numOSTPerOSS, diskSpacePerOST)
capacityCSV = 'capacityLog1-Divide.csv'
bytesToWriteCSV = 'writeLoadLog1-Divide.csv'
bandwidthCSV = 'bandwidthLog1-Divide.csv'
sim.readAppLog("AppLog1.txt")