import urllib
import time

url = 'http://192.168.0.102:5000'
startTime = time.time()
response = urllib.urlopen(url).read()
endTime = time.time()
print "GET request time:",endTime-startTime,"s"
