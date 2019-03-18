#SSLlab scanner designed to scan the URL of westjet and then return an ssl grade
#to the terminal when it has finished scanning
#Developed by Chris Selinger with infomation on SSL provided by https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v3.md
#requires python library "requests"

import requests
import time
import sys
import logging

API = "https://api.ssllabs.com/api/v3/"
Domain = "www.westjet.com"
analyzeCommand = API + "analyze?host=" + Domain + "&startNew=on&fromCache=off&all=done"
endpointShell = API + "getEndpointData?host=" + Domain + "&s="
waitCommand = API + "analyze?host=" + Domain + "&fromCache=off&all=done"


def requestWeb(command):
    responce = requests.get(command)
    responceData = responce.json()
    return responceData

data = requestWeb(analyzeCommand)
while data['status'] != 'READY' and data['status'] != 'ERROR':
    print("Scan is still in progress")
    time.sleep(10)
    data = requestWeb(waitCommand)
listLength = len(data['endpoints'])
i = 0
while i < listLength:
    tempEndpoint = data['endpoints']
    currentEndpoint = tempEndpoint[i]
    currentIp = currentEndpoint['ipAddress']
    endpointCommand = endpointShell + currentEndpoint['ipAddress']
    endpointData = requestWeb(endpointCommand)
    grade = endpointData['grade']
    print("Currently testing IP: " + currentIp)
    print(Domain + "'s SSL grade is: " + grade)
    i =+ 1
