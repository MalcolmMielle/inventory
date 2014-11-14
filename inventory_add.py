#!/usr/bin/env python

import pickle
import sys
from xmlrpclib import ServerProxy, Error
import datetime
import urllib2
import simplejson
import inventory_grabcronometer
import requests

def main():
	try:
		with open('inventory.inv', 'r') as filename:
			inventoryarr = pickle.load(filename)
			filename.close()
	except IOError:
		inventoryarr = {}


	while True:
		linetmp = sys.stdin.readline()
		if not linetmp:
			break
		line = linetmp.rstrip()
		upc = line[7:]
		itemdata = datetime.date.today()
		if inventoryarr.has_key(upc):
			inventoryarr[upc].append(itemdata)
		else:
			print "This is a brand new item. Searching Cronometer..."
			arr = inventory_grabcronometer.cronometer(upc)
			if arr != 0:
				print "Found in Cronometer! Item successfully entered."
				#inventoryarr[upc] = [arr] 
				arr2 = [DEFAULT_EXPIRY_TIME,arr[0],arr[1]]
				inventoryarr[upc] = [arr2]
				inventoryarr[upc].append(itemdata)
				continue

			params = {'upc' : upc }
			url="http://api.upcdatabase.org/json/"+config["API_KEY"]+"/"+upc
			bcodeinfo = requests.get(url).json()
			print bcodeinfo

			if bcodeinfo['valid'] == "false":
				print "This item wasn't in the online database. Please submit it at upcdatabase.org! It was not entered in your inventory."
				continue

			if bcodeinfo['description']:
				bcodeinfo['itemname'] += bcodeinfo['description']
				
			inventoryarr[upc] = [[config["DEFAULT_EXPIRY_TIME"],bcodeinfo['itemname']]]
			inventoryarr[upc].append(itemdata)

		print "Successfully entered upc " + upc

	print "Your current inventory contains:"
	print inventoryarr

	file = open('inventory.inv', 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
