#!/usr/bin/env python
import sys
sys.path.append('../cvk2')
import cv2
import httplib
import microsoftCVHelpers as msCV
import numpy as np
import requests
import time


_key = 'e80f8ece393f4eebb3d98b0bb36f04d0'

if __name__ == "__main__":


	# Load raw image file into memory
	pathToFileInDisk = 'bathroom.jpg'
	with open( pathToFileInDisk, 'rb' ) as f:
	    data = f.read()

	# Computer Vision parameters
	params = { 'visualFeatures' : 'Categories, Tags, Description, Faces'} 

	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/octet-stream'

	json = None


	start = time.time()
	

	result = msCV.processRequest(json, data, headers, params )

	if result is not None:

		# Load the original image, fetched from the URL
		data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
		img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )

		# in reverse order: lowest confidence -> highest confidence
		tags = sorted(result['tags'], key=lambda x: x['confidence'])

		description = result['description']
		caption = description['captions'][0]['text']

		print "here and:"
		print tags
		print description

	end = time.time()
	print(end - start)