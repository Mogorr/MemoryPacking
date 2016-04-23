#!/usr/bin/python

import sys, getopt
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
	return intsplitlist

def createFreeSpaceSegs(memBank):
	freeSegs = []
	for space in memBank.freeSpaces:
		freeSegs.append(memoryClasses.MemorySegment(((space[1]-space[0])+1),1))
	for seg in freeSegs:
		memBank.addSegment(seg,'free')
	
def fillMemory(infile, outfile, memsize):
	print 'Filling Memory'
	formattedInput = formatInput(infile)
	memBank=memoryClasses.MemoryBank(memsize)
	segments=[]
	for pair in formattedInput:
		segments.append(memoryClasses.MemorySegment(pair[0],pair[1]))
	for seg in segments:
		memBank.addSegment(seg)
	createFreeSpaceSegs(memBank)
	outfp=open(outfile,'w')
	outfp.write('Address,Size,Note\n')
	for block in memBank.blocks:
		for item in block:
			outfp.write('%s,' % item)
		outfp.write('\n')
	
def main(argv):
	inputfile = ''
	outputfile = ''
	memsize = 16
	opts, args = getopt.getopt(argv,'hi:o:s:',['ifile=','ofile=','memsize='])
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
	if inputfile=='':
		inputfile='genInp.txt'
		memoryGenerator.createSegments(memsize)
	fillMemory(inputfile, outputfile, memsize)	
   
if __name__ == '__main__':
   main(sys.argv[1:])