BPS = 268435456		# 256 MB/s

class OST:
	def __init__(self, diskSpace, oss):
		self.totalDiskSpace = diskSpace
		self.usedDiskSpace = 0
		self.oss = oss
		self.maxBPS = BPS
		self.bytesToStore = 0
		self.writeSpeed = 0

	def simulateTimeUnit(self):
		if self.bytesToStore < self.maxBPS:
			self.usedDiskSpace += self.bytesToStore
			self.bytesToStore = 0
			self.writeSpeed = self.bytesToStore
		else:
			self.usedDiskSpace += self.maxBPS
			self.bytesToStore -= self.maxBPS
			self.writeSpeed = self.maxBPS

	def freeDiskSpace(self):
		return self.totalDiskSpace - self.usedDiskSpace

	def addBytesToStore(self, bytes):
		self.bytesToStore += bytes

	def stats(self):
		return (self.freeDiskSpace(), self.bytesToStore, self.writeSpeed)