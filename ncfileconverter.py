from Tkinter import *
from tkFileDialog import *
from file_interpreter import *

def changeInputDirectory():
	newInputDir = askdirectory()
	settings = {}
	f = open('config.txt', 'r')
	for line in f:
		settings[line.split('=')[0].rstrip()] = line.split('=')[1].rstrip()
	f.close()

	settings['inputDir'] = newInputDir

	with open('config.txt', 'w') as f:
		for key in settings:
			f.write(key + '=' + settings[key] + '\n')

	a.inputDir.set(newInputDir)

def changeOutputDirectory():
	newOutputDir = askdirectory()
	settings = {}
	f = open('config.txt', 'r')
	for line in f:
		settings[line.split('=')[0].rstrip()] = line.split('=')[1].rstrip()
	f.close()

	settings['outputDir'] = newOutputDir

	with open('config.txt', 'w') as f:
		for key in settings:
			f.write(key + '=' + settings[key] + '\n')

	a.outputDir.set(newOutputDir)


class Window:
	def __init__(self, master):

		initialize()

		Label(master, text="Input Directory: ").grid(row=0)
		Label(master, text="Output Directory: ").grid(row=1)

		self.inputDir = StringVar()
		self.inputDir.set(getInputDir())
		self.outputDir = StringVar()
		self.outputDir.set(getOutputDir())

		Label(master, textvariable=self.inputDir).grid(row=0, column=1)
		Label(master, textvariable=self.outputDir).grid(row=1, column=1)

		Button(master, text="Browse", command=changeInputDirectory).grid(row=0, column=2)
		Button(master, text="Browse", command=changeOutputDirectory).grid(row=1, column=2)

		Button(master, text="Convert Files", command=executeInterpreter).grid(row=2, columnspan=3)


root = Tk()
root.wm_title(".nc file converter")
a = Window(root)
root.mainloop()