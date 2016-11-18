import sys

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

stoich=[]
for j in range (0, numReac):
    stoich.append([])

for i in range(0,numSpec):
    for j in range(0, numReac):
	stoich[i].append(TMat[i][j]-SMat[i][j])

rates=[]

for j in range(0,numReac):
    rate="k%d" % (j+1)
    for i in range(0,numSpec):
	if SMat[i][j]>0:
	    rate=rate+"*x%d" % (i+1)
	    if SMat[i][j]>1:
	        rate=rate+"^%d" % SMat[i][j]
    rates.append(rate)

outputfilename = str(sys.argv[2])
file = open(outputfilename, 'w')

#change this with conservation laws
numEqns=numSpec

file.write('INPUT\n')
file.write('variable_group x1');
if numSpec>1:
    for i in range(2,numSpec+1):
        file.write("," + " x%d" %i)
file.write(';\n')

file.write('constant k1');
if numReac>1:
    for i in range(2,numReac+1):
        file.write("," + " k%d" %i)
file.write(';\n')

file.write('function f1')
if numEqns>1:
    for i in range(2,numEqns+1):
        file.write("," + " f%d" %i)
file.write(';\n')

file.write('\n')

eqns=[]

for i in range (0,numSpec):
    eq=''
    for j in range(0, numReac):
	if stoich[i][j]>0:
	    eq=eq+"+"
	elif stoich[i][j]<0:
	    eq=eq+"-"
	if abs(stoich[i][j])==1:
	    eq=eq + rates[j]
	elif stoich[i][j]!=0:
	    eq=eq + "%d*" % abs(stoich[i][j]) + rates[j]
    if eq=='':
        eq="f%d=" % (i+1)+"0"
    elif eq[0]=='+':
        eq="f%d=" % (i+1) + eq[1:]
    else:
         eq="f%d=" % (i+1)+eq
    eqns.append(eq)
    file.write(eq+';\n')

file.close()
