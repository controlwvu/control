# Run this file by providing a single command line argument
# Ex:
# python runFromFile.py test4.txt constants 3


import sys, subprocess, os
import bertiniFileGen as bertini
from numpy.random import *
from numpy import *
from subprocess import call

samples = int(float(sys.argv[3]))
inputfilename = str(sys.argv[1])
constants = str(sys.argv[2])

# Generate a unique filename
outputhash = str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999))

print 'Bertini files will be generated in filename=bertini'+outputhash

tmpoutputfile = 'bertini' + outputhash 

# Generate the file to run bertini with.
#filenames = bertini.bertiniFileGen(inputfilename, tmpoutputfile, samples, bertini.getRandomSample)

#Wipe the buffer file
bufferfile = open('buffer_file', 'w')
bufferfile.close()
bufferfile = open('buffer_file', 'a')

filenames = bertini.bertiniFileGenWithFile(inputfilename, constants, samples, tmpoutputfile)
print 'Generated Files.'
#print filenames

x = []

# Run bertini
for filename in filenames:
	subprocess.call(['bertini', filename], stdout=bufferfile)
	z=bertini.printPositiveSolutions(open('real_finite_solutions', 'r'))
	#print z
	#print filename
	x.append(z)

bufferfile.close()

for i in range(0, len(filenames)):
	# filename, x[i] - solution sets, 
	solutions=bertini.getFullSolutions(filenames[i], x[i])
	print solutions
	

bertini.deleteFiles(filenames)


