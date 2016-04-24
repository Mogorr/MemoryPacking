class MemoryBank:

	def __init__(self,inpsize=65536):
		self.blocks = []
		self.size=inpsize
		self.freeSpaces=[[0,inpsize-1]]
		

		
	def addSegment(self,segment,note=''):
		address=self.findAddress(segment)
		if address==-1:
			#print 'couldn\'t find a spot for this segment:'
			#print (segment.size,segment.align)
			return
		if segment.align != 1:
			note='align:{0}'.format(segment.align)
		self.blocks.append([address,segment.size,note])
		self.updateFreeSpace(address,segment.size)
		self.blocks.sort(key=lambda k: k[0])
		
	def findAddress(self,segment):
		newAddress=-1
		# print 'trying to find ', segment.size, 'addressses'
		for space in self.freeSpaces:
			theorStartAddr = ((space[0]-1)+(segment.align - (space[0]-1)%segment.align))
			theorEndAddr = theorStartAddr+segment.size-1
			# print 'theoretical start address = ', theorStartAddr
			# print 'theoretical end address = ', theorEndAddr
			# print 'max end address = ', space[1]
			if (theorEndAddr<=space[1]):
				newAddress = theorStartAddr
				break
			
		return newAddress
		
	def updateFreeSpace(self,newAddress,size):
		for space in self.freeSpaces:
			if ((newAddress >=space[0]) and (newAddress+size-1)<=space[1]):
				oldEnd=space[1]
				space[1]=newAddress-1
				if space[1]<space[0]:
					self.freeSpaces.remove(space)
				if oldEnd>=newAddress+size:
					self.freeSpaces.append([newAddress+size,oldEnd])
		self.freeSpaces.sort(key=lambda k: k[0])
		# print self.freeSpaces
	def createFreeSpaceSegs(self,memBank):
		freeSegs = []
		for space in memBank.freeSpaces:
			freeSegs.append(MemorySegment(((space[1]-space[0])+1),1))
		for seg in freeSegs:
			memBank.addSegment(seg,'free')
		
class MemoryBankOS:

	def __init__(self,inpsize=65536):
		self.blocks = []
		self.size=inpsize
		self.freeSpace=[0,inpsize-1]

	def addSegment(self,segment,note=''):
		address=self.findAddress(segment)
		if address==-1:
			#print 'couldn\'t find a spot for this segment:'
			#print (segment.size,segment.align)
			return
		if segment.align != 1:
			note='align:{0}'.format(segment.align)
		if len(self.blocks)>0:
			firstFreeAddress=(self.blocks[-1][0]+self.blocks[-1][1])
			if (firstFreeAddress<address):
				self.blocks.append([firstFreeAddress,address-firstFreeAddress,'free'])
		self.blocks.append([address,segment.size,note])
		self.freeSpace[0]=address+segment.size
		self.blocks.sort(key=lambda k: k[0])
		
	def findAddress(self,segment):
		newAddress=-1
		# print 'trying to find ', segment.size, 'addressses'
		theorStartAddr = ((self.freeSpace[0]-1)+(segment.align - (self.freeSpace[0]-1)%segment.align))
		theorEndAddr = theorStartAddr+segment.size-1
		# print 'theoretical start address = ', theorStartAddr
		# print 'theoretical end address = ', theorEndAddr
		# print 'max end address = ', space[1]
		if (theorEndAddr<=self.freeSpace[1]):
			newAddress = theorStartAddr
		return newAddress			

class MemorySegment:
	def __init__(self,size,alignment):
		self.size = size
		self.align = alignment
	def __str__(self):
		return str((self.size,self.align))