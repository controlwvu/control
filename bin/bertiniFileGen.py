import copy, sys, numpy, sympy

inputfilename = str(sys.argv[1])
file = open(inputfilename, 'r')

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

file.close

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


outputfilename = str(sys.argv[2])
file = open(outputfilename, 'w')

#conservation laws
symStoich=sympy.Matrix(numpy.transpose(stoich))
consLaws=symStoich.nullspace()
#print(consLaws)

noConsLaws=len(consLaws)
numEqns=numSpec-noConsLaws

file.write('INPUT\n')
file.write('variable_group x1');
variables=sympy.symbols('x1:%d'%(numSpec+1))
variables=sympy.Matrix(variables)
#if numSpec>1:
if numSpec>1:
    for i in range(2,numSpec+1):
        file.write("," + " x%d" %i)
file.write(';\n')

file.write('constant k1');
if numReac>1:
    for i in range(2,numReac+1):
        file.write("," + " k%d" %i)
file.write(';\n')

consTotals=sympy.symbols('Tot1:%d'%(noConsLaws+1))
consTotals=sympy.Matrix(consTotals)

if (noConsLaws>0):
    augMatrix=consLaws[0]
    file.write('constant Tot1')
    if (noConsLaws>1):
        for i in range (1, noConsLaws):
            file.write(","+ " Tot%d" %(i+1))
            augMatrix=augMatrix.row_join(consLaws[i])
        file.write(';\n')
    augMatrix=augMatrix.col_join(sympy.Transpose(consTotals))
    for j in range(0, noConsLaws):
        file.write('%')
        file.write("Tot%d" %(j+1)+"=%s" %(sympy.Matrix.transpose(variables)*consLaws[j])[0])
        file.write('\n')
    file.write('\n')

augMatrix=augMatrix.transpose()
augMatrix=augMatrix.rref()
pivots=augMatrix[1]
augMatrix=augMatrix[0]
freeVars=list(set(range(1,numSpec))-set(pivots))

#print(augMatrix)
#print(pivots)

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

file.write('function f1')
if numEqns>1:
    for i in range(2,len(freeVars)+1):
        file.write("," + " f%d" %i)
file.write(';\n')

file.write('\n')

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
    file.write(eq+';\n')

file.close()
