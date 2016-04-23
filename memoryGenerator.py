import random, bisect

def createSegments(size):
	remainingSize=size
	genInp=open('genInp.txt','w')
	pow2list=map(lambda k: 2**k, [4,5,6,7,8,9,10])
	maxpow=bisect.bisect_left(pow2list,size)
	
	while remainingSize>(size*3/4):
		segSize=pow2list[random.randint(0,maxpow-1)]
		line='{0} {1}\n'.format(segSize,segSize)
		genInp.write(line)
		remainingSize-=segSize
		maxpow=bisect.bisect_left(pow2list,remainingSize)
	while remainingSize>0:
		if remainingSize>1:
			segSize=random.randint(1,remainingSize/2)
		else:
			segSize=1
		line='{0} {1}\n'.format(segSize,1)
		genInp.write(line)
		remainingSize-=segSize
