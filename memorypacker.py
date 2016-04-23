#!/usr/bin/python

import sys, getopt

def formatInput(inputfile):
	infile = open(inputfile,'r')
	linelist = infile.readlines()
	splitlist=[]
	for line in linelist:
		splitlist.append(line.split())
    intsplitlist = [map(int,x) for x in splitlist]
	sortedlist = intsplitlist.sort(key = lambda k: (k[0], k[1]), reverse=True)
	return intsplitlist

def 	
def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	formattedInput = formatInput(inputfile)
	
   
if __name__ == "__main__":
   main(sys.argv[1:])