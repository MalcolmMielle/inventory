#!/usr/bin/python

import pickle
import sys

def main(config):
	file = open(config['inventory'], 'r')
	inventoryarr = pickle.load(file)
	file.close()

	while True:
		linetmp = raw_input("Enter the EAN code of an item you wish to modify : ")
		if not linetmp:
			break
		#line = linetmp.rstrip()[7:]
		line = linetmp.rstrip()
		try:
			tmp = inventoryarr[line]
		except:
			print "This EAN doesn't exist in the database."
			break
		print 
		length = raw_input("Please enter the name for this item : ")
		if length:
			#predate = inventoryarr[line][0][1]
			inventoryarr[line][0][1]=length
			print "Name updated to " + length.rstrip() + "."

	print "this is your inventory"
	print inventoryarr
	file = open(config['inventory'], 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
