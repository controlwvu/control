# Run this file by providing a single command line argument
# Ex:
# python runRandomSampling.py test4.txt


import sys, subprocess, os
import bertiniFileGenRandom as bertiniRand
from numpy.random import *
from numpy import *
from subprocess import call

samples = 3;
inputfilename = str(sys.argv[1])
# Generate a unique filename
outputhash = str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999))

print 'Bertini files will be generated in filename=bertini'+outputhash

tmpoutputfile = 'bertini' + outputhash 

# Generate the file to run bertini with.
filenames = bertiniRand.bertiniFileGenRandom(inputfilename, tmpoutputfile, samples)

# bufferfile = open('buffer_file', 'w')

# Run bertini
for filename in filenames:
	#subprocess.call(['./bertini', filename], stdout=bufferfile)
	print filename
