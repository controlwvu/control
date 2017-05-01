# Run this file by providing a single command line argument
# Ex:
# python runFromFile.py test4.txt constants 3


import sys, subprocess, os
import bertiniFileGen as bertini
from numpy.random import *
from numpy import *
from subprocess import call

outputfilename = str(sys.argv[3])
inputfilename = str(sys.argv[1])
constants = str(sys.argv[2])

# Generate a unique filename
outputhash = str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999))

#print 'Bertini files will be generated in filename=bertini'+outputhash

tmpoutputfile = 'bertini' + outputhash 

# Generate the file to run bertini with.
#filenames = bertini.bertiniFileGen(inputfilename, tmpoutputfile, samples, bertini.getRandomSample)

#Wipe the buffer file
bufferfile = open('buffer_file', 'w')
bufferfile.close()
bufferfile = open('buffer_file', 'a')

out = open(outputfilename, 'w')

filenames = bertini.bertiniFileGenWithFile(inputfilename, constants, tmpoutputfile)
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
	out.write('File'+str(i+1)+'\n')
	for solution in solutions:
	    out.write(str(solution)+'\n')
	out.write('\n\n')

out.close()
#bertini.deleteFiles(filenames)


