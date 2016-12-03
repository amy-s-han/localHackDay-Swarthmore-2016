#!/usr/bin/env python
import sys
sys.path.append('../cvk2')
import cvk2
import cv2
import httplib
import microsoftCVHelpers as msCV
import numpy as np
import requests
import socket
import urllib
import utils

NUM_CAMS = 1
webpageIP = 'http://192.168.43.31:5000'

if __name__ == "__main__":

	streamURLS = ['http://192.168.43.100:8080/video']

	for i in range(NUM_CAMS):
		worker = threading.Thread(target = runStream, args = (i, streamURLS[i]))
		worker.daemon = False
		worker.start()

	if cv2.waitKey(1) == 27:
		exit(0)