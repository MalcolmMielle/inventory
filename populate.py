# -*- coding: utf-8-*-
#!/usr/bin/env python

import sys
import os
import yaml
from getpass import getpass

def run():
	profile = {}
	print("Welcome to the profile populator of the inventory")
	
	

	def simple_request(var, cleanVar, cleanInput=None):
		input = raw_input(cleanVar + ": ")
		if input:
			if cleanInput:
				input = cleanInput(input)
			profile[var] = input
			
	simple_request("DEFAULT_EXPIRY_TIME", "Default expiry time", int)
	simple_request("API_KEY", "Api Key for upcdatabase")
	profile['inventory'] = os.path.expanduser('~/.inventory/inventory.inv')

	# write to profile
	print("Writing to profile...")	
    
	thefile = open(os.path.join(os.path.dirname(__file__),'profile.txt'), 'w')
	try:
		yaml.dump(profile,thefile,default_flow_style=False)
	finally:
		thefile.close()
		
	print("Writing to profile...")
	if not os.path.isdir(os.path.expanduser('.inventory')):
		print os.path.isdir(os.path.expanduser('.inventory'))
		os.makedirs(os.path.expanduser('.inventory'))
	else:
		print 'all good, an inventory already exists'
    
	
if __name__ == "__main__":
    run()