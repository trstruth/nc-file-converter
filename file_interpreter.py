import os
import shutil

def translate(ncFileName):
	"""translate method"""
	
	# inputDirectory variables dictates where the source files are located, opens the desired file which is passed as a method argument in r+ mode, creates buffer lists
	# TODO: add functionality to editing inputDirectory
	inputDirectory = getInputDir()
	targetFilepath = ncFileName
	ncFile = open(targetFilepath, "r+")
	buff = []
	outBuff = []

	# moves the lines from the source file into the buff list and stores the length of this list into numLines
	for line in ncFile:
		formattedLine = line.rstrip('\n')
		buff.append(formattedLine)
	numLines = len(buff)

	outBuff.append("N0000 G00 X0 Y0 Z1.3 A0")
	outBuff.append("N0001 G01 X0 Y0 Z1.3 A0")
	outPointer = 1

	# for loop that cycles through every value in the file
	for i in range(2, numLines-4):

		# skips line if "T1 M" is present
		if "T1 M" in buff[i]: continue

		# increments the outPointer and determines the indexes of B and G90
		outPointer = outPointer + 1
		idxB = buff[i].find("B")
		idxG90 = buff[i].find("G90")

		# performs the necessary transformations dictated by the boolean in expressions
		if "B" in buff[i]:
			pointer = str(outPointer)
			outBuff.append("N" + pointer + " Z 1.3")
			outPointer = outPointer + 1
			idx0 = 0
			idxRot = idxB + 1
			idxF = buff[i].find("F")
			idxEnd = len(buff[i])
			sub = buff[i][idx0:idxB]
			subRot = buff[i][idxRot:idxF]
			subF = buff[i][idxF:idxEnd]
			f = float(subRot)
			f = f/360
			subRot = str(f)
			outBuff.append((sub + " A " + subRot + " " + subF))

		elif "G90" in buff[i]:
			idxX = buff[i].find("X")
			idxS = buff[i].find("S")
			G00 = buff[i][idxX:idxS]
			outBuff.append("N0005 " + G00)

		else:
			outBuff.append(buff[i])

	outBuff.append(("G01 Z 2.000"))
	outBuff.append(("A 0.0"))
	outBuff.append(("M5"))
	outBuff.append(("M30"))
	print ncFileName
	newNcFileName = getOutputDir() + ncFileName[len(getInputDir()):-3] + "OUT" + ncFileName[-3:]
	print newNcFileName

	# calls the outputFile method on the file
	outputFile(outBuff, newNcFileName)
	ncFile.close()

def outputFile(outputList, fileName):
	"""writes to the output file, takes the outputlist and filename as args"""

	outputDir = getOutputDir()

	with open(fileName, 'w') as f:
		for line in outputList:
			f.write(line + '\n')

def getInputDir():
	config = open('config.txt', 'r')
	for line in config:
		line = line.rstrip('\n')
		if line.split('=')[0] == "inputDir":
			return str(line.split('=')[1])

def getOutputDir():
	config = open('config.txt', 'r')
	for line in config:
		line = line.rstrip('\n')
		if line.split('=')[0] == "outputDir":
			return str(line.split('=')[1])

def recreateFileStructure():
	inputRootDir = getInputDir()
	outputRootDir = getOutputDir()
	try:
		if os.path.exists(outputRootDir):
			shutil.rmtree(outputRootDir)
		shutil.copytree(inputRootDir, outputRootDir)
	except shutil.Error as e:
		print('Directory not copied. Error: %s' % e)

def crawl(rootFile):
	"""recursively navigates a directory tree and calls translate if it is a .nc file"""
	for dirpath, dirnames, filenames in os.walk(rootFile):
		for aFile in filenames:
			if aFile[-3:] == ".nc":
				pathToFile = os.path.join(dirpath, aFile)
				translate(pathToFile)

def initialize():
	f = open("config.txt", 'r+')
	cwd = os.getcwd()[:-6]
	if os.stat("config.txt").st_size == 0:
		f.write("inputDir="+cwd+"input_files\n")
		f.write("outputDir="+cwd+"output_files\n")

def executeInterpreter():
	"""main method"""

	inputDirectory = getInputDir()

	# Determines if the input directory is empty
	if len(os.listdir(inputDirectory)) == 0:
		print "The files directory is empty, please move the files you wish to alter into the files directory."
		exit()
	recreateFileStructure()

	# Calls crawl on the input Directory, which in turn calls translate on each file therein
	#crawl(inputDirectory) 