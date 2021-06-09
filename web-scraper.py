import sys
import requests
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import distutils.util
import time

#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))

_debug_ = False
_timeDelaySeconds_ = 60
_senderEmail_ = ""
_password_ = ""
_reciverEmail = ""

argsLen = range(1,len(sys.argv)-1)

foundGpus = []

"""
Parsing argumentsfrom command line
"""
for i in argsLen:
    if sys.argv[i] == "--debug":
        _debug_ = bool(distutils.util.strtobool(sys.argv[i+1]))
    if sys.argv[i] == "--seconds":
        _timeDelaySeconds_ = int(sys.argv[i+1])

"""
Parsing data from settings.json
"""
with open("settings.json","r") as settings:
    jsonData = json.load(settings)
    for setting in jsonData:
        if setting == "senderEmail":
            _senderEmail_ = jsonData[setting]
        if setting == "password":
            _password_ = jsonData[setting]
        if setting == "receiverEmail":
            _reciverEmail = jsonData[setting]



def send_email(gpuName, gpuUrl):
    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = _senderEmail_
    message["To"] = _reciverEmail

    text = gpuName + ", " + gpuUrl

    message.attach(MIMEText(text, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(_senderEmail_, _password_)
        
        
        server.sendmail(_senderEmail_, _reciverEmail, message.as_string())

def logData(data):
    with open(str(datetime.datetime.now().date())+".log","a") as file:
        file.write("[" + str(datetime.datetime.now()) + "] ")
        file.write(data)
        file.write("\n")
        file.close()

def search_webhallen():
    startTime = datetime.datetime.now()
    gpuCount = 0
    webhallen_url1 = "https://www.webhallen.com/api/search?query%5BsortBy%5D=sales&query%5Bfilters%5D%5B0%5D%5Btype%5D=category&query%5Bfilters%5D%5B0%5D%5Bvalue%5D=4684&query%5Bfilters%5D%5B1%5D%5Btype%5D=attributes&query%5Bfilters%5D%5B1%5D%5Bvalue%5D=110-1-NVIDIA%2BGeForce%2BRTX%2B3070%7ENVIDIA%2BGeForce%2BRTX%2B3080%7ENVIDIA%2BGeForce%2BRTX%2B3060%2BTi%7ENVIDIA%2BGeForce%2BRTX%2B3060&query%5BminPrice%5D=0&query%5BmaxPrice%5D=999999&page="
    webhallen_url2 = "&noCount=true"

    pages = range(1,10000)

    for page in pages:
        url = webhallen_url1+str(page)+webhallen_url2
        res = requests.get(url)
        jsonRes = json.loads(res.content)
        if len(jsonRes['products']) <= 0:
            break

        for product in jsonRes['products']:
            gpuName = product['name']
            gpuId = product['id']

            if _debug_:
                print("checking: " + gpuName + " : "+ str(gpuId))

            gpuCount += 1
            for stockLocation in product['stock']:
                if product['stock'][stockLocation] > 0:

                    #if _debug_:
                    print(gpuName + " : "+ str(gpuId) + " in stock")

                    #foundGpus.append((datetime.datetime.now, gpuId))

                    logData("Found GPU: " + str(gpuId) + " : " + gpuName)

                    send_email(gpuName,
                    "https://www.webhallen.com/se/product/"+str(gpuId))
                    break

    endTime = datetime.datetime.now() -  startTime
    perGpuTime = endTime / gpuCount
    perGpuTime = perGpuTime.seconds*1000 + perGpuTime.microseconds/1000

    return str(endTime.seconds)+"."+str(endTime.microseconds) + " s total, " + str(perGpuTime) + " ms per gpu"
        
#inetUrl = "https://www.inet.se/kategori/167/geforce-gtx-rtx?filters=%7B%2229%22%3A%7B%22type%22%3A%22PropAny%22%2C%22any%22%3A%5B15734%2C14294%2C14297%2C14700%2C14764%5D%7D%7D"

"""
main

"""

while  True:

    run = search_webhallen()

    #if _debug_:
    print(run)
    
    logData(run)

    time.sleep(_timeDelaySeconds_)