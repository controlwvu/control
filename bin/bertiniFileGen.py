
import copy, sys, numpy, sympy
from numpy.random import rand

def getPadding():
	return 4

def getRandomVector(size, upperBound = 10000000, lowerBound = 0):
	tmp = (rand(size) * (upperBound - lowerBound)) + lowerBound
	return (tmp);

def getRandomSample(numReac, numSpec):
	s = ''
	# Random sampling of constants
	k_values = getRandomVector(numReac+1);
	for i in range(1,numReac+1):
		s += ("k%d = %f;\n" %(i, k_values[i]))
	#Random sampling of initial conditions
	y_values = getRandomVector(numSpec+1);
	for i in range(1,numSpec+1):
		s += ("y%d = %f;\n" %(i, y_values[i]))
	return s


# pass into this method the file open('real_finite_solutions', 'r')
def printPositiveSolutions(file1):
	isPositive = 1
	x = []
	for line in file1:
		# print line
		if (((line == '') | (line == '\n')) & (isPositive == 1) &  (len(x) > 0)):
			print x
			x = []
			isPositive = 1
		elif ((line == '') | (line == '\n')):
			x = []
			isPositive = 1
		elif (line != ''):
			nums = line.split(' ', 4)
			if (len(nums) == 2): # & (len([c for c in nums[1] if c==' ']) > 1)
				x.append(float(nums[0]))
				if (float(nums[0]) < 1e-10):
					isPositive = 0
			else:
				x = []



def bertiniFileGenWithFile(inputfile, constantsfile, outputfile):
	def sampleFromFile(s):
		file = open(constantsfile)
		k = ''
		for line in file:
			k += line
		return k
	return bertiniFileGen(inputfile, outputfile, 1, sampleFromFile)

def bertiniFileGen(inputfile, outputfile, samples, samplingFunction):
	#inputfilename = str(sys.argv[1])
	inputfilename = inputfile
	file = open(inputfilename, 'r')

	# Create two variables to store first half and last half of the file
	first = ''
	last = ''

	writeLeft=False
	writeRight=False
	SMat=[]
	TMat=[]

	for line in file:
	    if line.rstrip('\n')=='S MATRIX':
		writeLeft=True
	    elif line.rstrip('\n')=='T MATRIX':
		writeLeft=False
		writeRight=True
	    elif line.rstrip('\n')!='':
		TT=map(int, line.rstrip('\n').split(' '))
		if writeLeft:
		    SMat.append(TT)
		elif writeRight:
		    TMat.append(TT)

	file.close()

	numSpec=len(SMat)
	numReac=len(SMat[0])
	
	stoich=numpy.matrix(TMat)-numpy.matrix(SMat)


	"""
	symSMat=sympy.Matrix(SMat)
	symTMat=sympy.Matrix(TMat)
	symStoich=symTMat-symSMat
	symStoich=sympy.Matrix(sympy.Transpose(symStoich))

	symStoich=[]
	for j in range (0, numReac):
	    symStoich.append([])

	for i in range(0,numSpec):
	    for j in range(0, numReac):
		symStoich[i].append(TMat[i][j]-SMat[i][j])
	"""

	rates=[]

	for j in range(0,numReac):
	    rate="k%d" % (j+1)
	    for i in range(0,numSpec):
		if SMat[i][j]>0:
		    rate=rate+"*x%d" % (i+1)
		    if SMat[i][j]>1:
			rate=rate+"^%d" % SMat[i][j]
	    rates.append(rate)

	#outputfilename = str(outputfile)
	#file = open(outputfilename, 'w')

	#Uncomment this for parameters from another file
	#file.write('CONFIG\n ParameterHomotopy:2;\nEND;\n\n')

	#conservation laws
	symStoich=sympy.Matrix(numpy.transpose(stoich))
	consLaws=symStoich.nullspace()
	#print(consLaws)

	noConsLaws=len(consLaws)
	numEqns=numSpec-noConsLaws #numEqns=numSpec

	#file.write('INPUT\n')
	#file.write('variable_group x1');
	first += 'INPUT\nvariable_group x1'
	variables=sympy.symbols('x1:%d'%(numSpec+1))
	initConds=sympy.Matrix(sympy.symbols('y1:%d'%(numSpec+1)))
	variables=sympy.Matrix(variables)
	if numSpec>1:
	    for i in range(2,numSpec+1):
		#file.write("," + " x%d" %i)
		first += ", x%d" %i
	first += ';\nconstant y1'	
	if numSpec>1:
	    for i in range(2,numSpec+1):
		#file.write("," + " x%d" %i)
		first += ", y%d" %i
	#file.write(';\n')
	first += ';\nconstant k1'

	#file.write('constant k1');
	if numReac>1:
	    for i in range(2,numReac+1):
		#file.write("," + " k%d" %i)
		first += ", k%d" %i
	#file.write(';\n')
	first += ';\n'
	
	if (noConsLaws>0):
		consTotals=sympy.symbols('Tot1:%d'%(noConsLaws+1))
		consTotals=sympy.Matrix(consTotals)
	freeVars=range(0,len(variables))
	if (noConsLaws>0):
	    augMatrix=consLaws[0]
	    #file.write('constant Tot1')
	    first += 'constant Tot1'
	    if (noConsLaws>1):
		for i in range (1, noConsLaws):
		    #file.write(","+ " Tot%d" %(i+1))
		    first += ", Tot%d" %(i+1)
		    augMatrix=augMatrix.row_join(consLaws[i])
		#file.write(';\n')
		first += ';\n'
	    first += ';\n'
	    augMatrix=augMatrix.col_join(sympy.Transpose(consTotals))
	    for j in range(0, noConsLaws):
		#first += '%'
		last += "Tot%d" %(j+1)+"=%s;\n" %(sympy.Matrix.transpose(initConds)*consLaws[j])[0]  # first += ...
		#file.write('%')
		#file.write("Tot%d" %(j+1)+"=%s" %(sympy.Matrix.transpose(variables)*consLaws[j])[0])
		#file.write('\n')
	    #file.write('\n')
	    first += '\n'
	

	
	    augMatrix=augMatrix.transpose()
	    augMatrix=augMatrix.rref()
	    pivots=augMatrix[1]
	    augMatrix=augMatrix[0]
	    freeVars=list(set(range(1,numSpec))-set(pivots))

	    replacedVariables=copy.deepcopy(variables)

	    for j in pivots:
	        cc=list(augMatrix[j,:])
	        i=cc.index(1)
	        variab=copy.deepcopy(variables)
	        variab[i]=0
	        variab=variab.col_join(sympy.Matrix([-1]))
	        variab=list(variab)
	        replacedVariables[j]=-augMatrix[j,:].dot(variab)

	    replacedVariables=list(replacedVariables)

	last += ('\nfunction f1')
	if numEqns>1:
	    for i in range(2,numEqns+1):
		last += (", f%d" %i)
	last += (';\n')

	last += ('\n')

	rates=[]

	for j in range(0,numReac):
	    rate="k%d" % (j+1)
	    for i in range(0,numSpec):
		    if SMat[i][j]>0:
			rate=rate+"*"+str(variables[i])
			if SMat[i][j]>1:
			    rate=rate+"^%d" % SMat[i][j]
	    rates.append(rate)

	freeRates=[]
	if (noConsLaws>0):
		for j in range(0,numReac):
		    rate="k%d" % (j+1)
		    for i in range(0,numSpec):
			    if SMat[i][j]>0:
				par1=""
				par2=""
				if i in pivots:
				    par1="("
				    par2=")"
				rate=rate+"*"+par1+str(replacedVariables[i])+par2
			    if SMat[i][j]>1:
				rate=rate+"^%d" % SMat[i][j]
		    freeRates.append(rate)
	else:
		freeRates = rates

	eqns=[]

	for i in range(0,len(freeVars)):
	    eq=''
	    for j in range(0, numReac):
		if stoich[freeVars[i],j]>0:
		    eq=eq+"+"
		elif stoich[freeVars[i],j]<0:
		    eq=eq+"-"
		if abs(stoich[freeVars[i],j])==1:
		    eq=eq + freeRates[j]
		elif stoich[freeVars[i],j]!=0:
		    eq=eq + "%d*" % abs(stoich[freeVars[i],j]) + freeRates[j]
	    if eq=='':
		eq="f%d=" % (i+1)+"0"
	    elif eq[0]=='+':
		eq="f%d=" % (i+1) + eq[1:]
	    else:
		 eq="f%d=" % (i+1)+eq
	    eqns.append(eq)
	    #file.write(eq+';\n')
	    last += eq + ';\n'

	last += 'END;\n'
	#file.write('END;\n')
	#file.close()
	filenames = []

	for i in range(0, samples):
		with open(outputfile + '-' + str(i).zfill(getPadding()), 'w+') as f:
			filenames.append(outputfile + '-' + str(i).zfill(getPadding()))
			f.write(first)
			f.write(samplingFunction(numReac, numSpec))#getRandomSample(numReac))
			f.write(last)
			f.close()
	return filenames



