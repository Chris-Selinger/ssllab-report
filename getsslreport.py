#SSLlab scanner designed to scan the URL of westjet and then return an ssl grade
#to the terminal when it has finished scanning
#Developed by Chris Selinger with infomation on SSL provided by https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v3.md
#requires python library "requests"

import requests
import time

#Constant section, these will always be the same when using the same API

API = "https://api.ssllabs.com/api/v3/"
Domain = "www.westjet.com"

#Makes sure to launch a new scan of the current domain, through checking on startNew and checking off fromCache
analyzeCommand = API + "analyze?host=" + Domain + "&startNew=on&fromCache=off&all=done"
endpointShell = API + "getEndpointData?host=" + Domain + "&s="
waitCommand = API + "analyze?host=" + Domain + "&fromCache=off&all=done"

#Function requestWeb : is called whenever the script needs to access ssllabs
#PARAM : command = the command in which ssl labs will prvoke
def requestWeb(command):
    responce = requests.get(command)
    responceData = responce.json()
    return responceData

#Access ssllabs in order to get initial data of the domain requested
data = requestWeb(analyzeCommand)

#Waits for the analysis of the data to happen, once ready assuming there is no error, it goes on
while data["status"] != "READY" and data["status"] != "ERROR":
    print("Scan is still in progress")
    time.sleep(10)
    #Uses wait command to not start a new instance of scan, defeating the purpose of scanning in the first place
    data = requestWeb(waitCommand)

#checks list length to see amount of endpoints at current domain so it can check them all
listLength = len(data["endpoints"])
i = 0

#Loop cycles through endpoints, displaying the current IP address being looked at as well as the grade given the address
while i < listLength:
    tempEndpoint = data["endpoints"]
    currentEndpoint = tempEndpoint[i]
    currentIp = currentEndpoint["ipAddress"]
    endpointCommand = endpointShell + currentEndpoint["ipAddress"]
    endpointData = requestWeb(endpointCommand)
    grade = endpointData["grade"]
    print("Currently testing IP: " + currentIp)
    print(Domain + "'s SSL grade is: " + grade)
    i =+ 1
