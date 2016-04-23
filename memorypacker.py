#!/usr/bin/python

import sys, getopt
import memoryClasses

def formatInput(inputfile):
	infile = open(inputfile,'r')
	linelist = infile.readlines()
	splitlist=[]
	for line in linelist:
		splitlist.append(line.split())
	intsplitlist = [map(int,x) for x in splitlist]
	sortedlist = intsplitlist.sort(key = lambda k: (k[0], k[1]), reverse=True)
	return intsplitlist
	
def fillMemory(infile, outfile, memsize):
	print "Filling Memory"
	formattedInput = formatInput(infile)
	memBank=memoryClasses.MemoryBank(memsize)
	segments=[]
	for pair in formattedInput:
		segments.append(memoryClasses.MemorySegment(pair[0],pair[1]))
	for seg in segments:
		memBank.addSegment(seg)
	for block in memBank.blocks:
		print block
	print memBank.freeSpaces
	
def main(argv):
	inputfile = ''
	outputfile = ''
	memsize = 16
	try:
		opts, args = getopt.getopt(argv,"hi:o:s:",["ifile=","ofile=","memsize="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile> -s <memsize>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile> -s <memsize>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-s", "--memsize"):
			memsize = int(arg)
	fillMemory(inputfile, outputfile, memsize)	
   
if __name__ == "__main__":
   main(sys.argv[1:])