#!/usr/bin/env python

import pickle
import sys
from xmlrpclib import ServerProxy, Error
import datetime
import urllib2
import simplejson
import inventory_grabcronometer
import requests
import webbrowser

def main(config):
	try:
		with open(config['inventory'], 'r') as filename:
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
				arr2 = [config["DEFAULT_EXPIRY_TIME"],arr[0],arr[1]]
				inventoryarr[upc] = [arr2]
				inventoryarr[upc].append(itemdata)
				continue

			params = {'upc' : upc }
			url="http://api.upcdatabase.org/json/"+config["API_KEY"]+"/"+upc
			bcodeinfo = requests.get(url).json()
			print bcodeinfo
			
			try:
				if bcodeinfo['reason']: 
					print "Error in accessing upc : "+ bcodeinfo['reason']
					print 'Item not added to inventory'
					continue
			except:
				pass
			
			if bcodeinfo['valid'] == "false":
				print "This item wasn't in the online database. Please submit it at upcdatabase.org! It was not entered in your inventory."
				#webbrowser.open("http://upcdatabase.org/code/"+upc,new=2)
				print "in the meantime, you should add it manually"
				print "the UPC code is : "+upc

			
			elif bcodeinfo['itemname'] == '':
				print "This item as no name. You should update it on upcdatabase ! It was not added in the inventory."
				#webbrowser.open("http://upcdatabase.org/code/"+upc,new=2)
				print "in the meantime, you shoud modify the name :"
				print "the UPC code is : "+upc
				
			#I don't want the description but just the name
			#if bcodeinfo['description']:
			#bcodeinfo['itemname'] += bcodeinfo['description']
				
			inventoryarr[upc] = [[config["DEFAULT_EXPIRY_TIME"],bcodeinfo['itemname']]]
			inventoryarr[upc].append(itemdata)

		print "Successfully entered upc " + upc

	print "Your current inventory contains:"
	print inventoryarr

	file = open(config['inventory'], 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
