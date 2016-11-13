left=[[1, 2, 2], [3, 4, 1]]
right=[[0,2,1], [2,1,3]]
numSpec=len(left)
numReac=len(left[0])

stoich=[]

stoich.append([])
stoich.append([])

for i in range(0,numSpec):
    for j in range(0, numReac):
        stoich[i].append(right[i][j]-left[i][j])

print stoich

rates=[]

for j in range(0,numReac):
    rate="k%d" % (j+1)
    for i in range(0,numSpec):
        if left[i][j]>0:
            rate=rate+"*x%d" % (i+1)
            if left[i][j]>1:
                rate=rate+"^%d" % left[i][j]
    rates.append(rate)

for i in range (0,numSpec):
    eq="f%d=" % (i+1)
    for j in range(0, numReac):
        if stoich[i][j]>0:
            eq=eq+"+"
        elif stoich[i][j]<0:
            eq=eq+"-"
        if abs(stoich[i][j])==1:
            eq=eq + rates[j]
        elif stoich[i][j]!=0:
            eq=eq + "%d*" % abs(stoich[i][j]) + rates[j]
    print eq
