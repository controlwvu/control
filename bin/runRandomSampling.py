# Run this file by providing a single command line argument
# Ex:
# python runRandomSampling.py test4.txt


import sys, subprocess, os
import bertiniFileGen as bertini
from numpy.random import *
from numpy import *
from subprocess import call

samples = 100;
inputfilename = str(sys.argv[1])
outputfilename = str(sys.argv[2])
# Generate a unique filename
outputhash = str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + str(randint(1000000,9999999))

print 'Bertini files will be generated in filename=bertini'+outputhash

tmpoutputfile = 'bertini' + outputhash 



bufferfile = open('buffer_file', 'w')
bufferfile.close()
bufferfile = open('buffer_file', 'a')

out = open(outputfilename, 'w')

bistability = False
total = 0

x = []

while (bistability == False):
	total = 0
	# Generate the file to run bertini with.
	filenames = bertini.bertiniFileGen(inputfilename, tmpoutputfile, samples, bertini.getRandomSample)

	# Run bertini
	for filename in filenames:
	#	print filename
	#	subprocess.call(['bertini', filename])
		subprocess.call(['bertini', filename], stdout=bufferfile)
		z=bertini.printPositiveSolutions(open('real_finite_solutions', 'r'))
		x.append(z)
		print('Iteration ' + str(total) + ', found = ' + str(len(z)))
		bistability = len(z) > 1
		total = total + 1
		if (bistability):
			break
	#	print(z.shape(1))
	



	for i in range(0, total):
		# filename, x[i] - solution sets, 
		solutions=bertini.getFullSolutions(filenames[i], x[i])
		out.write('File'+str(i+1)+'\n')
		for solution in solutions:
		    out.write(str(solution)+'\n')
		out.write('\n\n')


	bertini.deleteFiles(filenames)
#filename2 = bertini.bertiniFileGenWithFile(inputfilename, 'constants', tmpoutputfile)
#print filename2
