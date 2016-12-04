from __future__ import print_function
import time 
import requests
import operator



_translatorKey = '420c6ab49ed1449db517207d6aef32d9'
_tokenURL = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
_maxNumRetries = 10


def processRequest(headers, url):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:
        response = requests.request( 'post', url, headers = headers)
        print ("response: %s", response.status_code)
        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:
            if len(response.content) == 0 or response.content == None:
            	result = None
            else:
        		result = response.content

        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break
        
    return result