#!/usr/bin/python

import sys, getopt, time
import memoryClasses
import memoryGenerator

def formatInput(inputfile):
	infile = open(inputfile,'r')
	linelist = infile.readlines()
	splitlist=[]
	for line in linelist:
		splitlist.append(line.split())
	intsplitlist = [map(int,x) for x in splitlist]
	sortedlist = intsplitlist.sort(key = lambda k: (k[0], k[1]), reverse=True)
	infile.close()
	return intsplitlist
	
def fillMemory(infile, outfile, memsize):
	#print 'Filling Memory'
	
	formattedInput = formatInput(infile)
	memBank=memoryClasses.MemoryBank(memsize)
	segments=[]
	for pair in formattedInput:
		segments.append(memoryClasses.MemorySegment(pair[0],pair[1]))
	#totaltimesegs=0
	# SLOWING DOWN
	#sys.stdout.write('before loop: {0}\n'.format(time.clock()))
	for seg in segments:
		#timestart=time.clock()
		memBank.addSegment(seg)
		#totaltimesegs+=time.clock()-timestart
	# SLOWING DOWN
	#timeperseg=totaltimesegs/len(segments)
	# sys.stdout.write('after loop: {0}\n'.format(time.clock()))
	# sys.stdout.write('time per segment: {0}\n'.format(timeperseg))
	# sys.stdout.flush()
	memBank.createFreeSpaceSegs(memBank)
	if outfile != '':
		outfp=open(outfile,'w')
		outfp.write('Address,Size,Note\n')
		for block in memBank.blocks:
			for item in block:
				outfp.write('%s,' % item)
			outfp.write('\n')
		outfp.close()
	freespace = sum([block[1] for block in memBank.blocks if block[2]=='free'])
	return freespace
	
def fillMemoryOS(infile, outfile, memsize):
	#print 'Filling Memory (OS Algorithm)'
	formattedInput = formatInput(infile)
	memBank=memoryClasses.MemoryBankOS(memsize)
	segments=[]
	for pair in formattedInput:
		segments.append(memoryClasses.MemorySegment(pair[0],pair[1]))	
	for seg in segments:
		memBank.addSegment(seg)
	if outfile != '':
		outfp=open(outfile,'w')
		outfp.write('Address,Size,Note\n')
		for block in memBank.blocks:
			for item in block:
				outfp.write('%s,' % item)
			outfp.write('\n')
		outfp.close()
	freespace = sum([block[1] for block in memBank.blocks if block[2]=='free'])
	return freespace	
	
def main(argv):
	inputfile = ''
	outputfile = ''
	memsize = 16
	testmode=0
	opts, args = getopt.getopt(argv,'hi:o:s:t:',['ifile=','ofile=','memsize=','test='])
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile> -s <memsize>'
			sys.exit()
		elif opt in ('-i', '--ifile'):
			inputfile = arg
		elif opt in ('-o', '--ofile'):
			outputfile = arg
		elif opt in ('-s', '--memsize'):
			memsize = int(arg)
		elif opt in ('-t', '--test'):
			testmode = int(arg)
	if testmode==0:
		if inputfile=='':
			inputfile='genInp.txt'
			memoryGenerator.createSegments(memsize)
		fillMemory(inputfile, outputfile, memsize)
	else:
		inputfile='genInp.txt'
		outputfile=''
		totalUnused=0
		unusedSpacePercent=0
		totalUnusedOS=0
		unusedSpaceOSPercent=0
		for i in range(testmode):
			sys.stdout.write('test {0:5}/{1:5}, {2:3f}%\r'.format(i,testmode,(i/float(testmode)*100)))
			sys.stdout.flush()
			#sys.stdout.write('before input generation: {0}\n'.format(time.clock()))
			#sys.stdout.flush()
			memoryGenerator.createSegments(memsize)
			#sys.stdout.write('before my algorithm: {0}\n'.format(time.clock()))
			#sys.stdout.flush()
			unusedSpace=fillMemory(inputfile,outputfile,memsize)
			#sys.stdout.write('before my percentage calc: {0}\n'.format(time.clock()))
			#sys.stdout.flush()
			totalUnused+=unusedSpace
			unusedSpacePercent=(unusedSpacePercent*(i)+unusedSpace/float(memsize)*100)/(i+1)
			#sys.stdout.write('before OS\'s algorithm: {0}\n'.format(time.clock()))
			#sys.stdout.flush()
			unusedSpaceOS=fillMemoryOS(inputfile,outputfile,memsize)
			#sys.stdout.write('before OS percentage calc: {0}\n'.format(time.clock()))
			#sys.stdout.flush()
			totalUnusedOS+=unusedSpaceOS
			unusedSpaceOSPercent=(unusedSpaceOSPercent*(i)+unusedSpaceOS/float(memsize)*100)/(i+1)

		print 'Unused Space (my Algorithm): {0}, {1:3f}%'.format(totalUnused,unusedSpacePercent)
		print 'Unused Space (OS Algorithm): {0}, {1:3f}%'.format(totalUnusedOS, unusedSpaceOSPercent)
		with open('unusedSpace.csv','a') as totalfile:
			totalfile.write('{0},{1},{2}\n'.format(totalUnused,totalUnusedOS,memsize*testmode))
   
if __name__ == '__main__':
   main(sys.argv[1:])
