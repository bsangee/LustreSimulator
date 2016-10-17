import random

appLogFile = "AppLog1.txt"
rseed = 1
writeSizeMu = 4294967296	# 4 GB
writeSizeSigma = 536870912	# 512 MB
totalSecs = 86400			# 24 hours

random.seed(rseed)
t = 0
fptr = open(appLogFile, 'w')
while t < totalSecs:
	writeSize = abs(int(random.gauss(writeSizeMu, writeSizeSigma)))
	numOSTs = random.randint(1, 4)
	line = "{0} {1} {2}\n".format(t, writeSize, numOSTs)
	fptr.write(line)
	t += random.randint(1, 5)

fptr.close()