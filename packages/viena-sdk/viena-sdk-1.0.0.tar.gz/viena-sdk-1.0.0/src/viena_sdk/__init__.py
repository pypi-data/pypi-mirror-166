# viena-sdk/__init__.py

__app_name__ = "viena-sdk"
__version__ = "0.1.0"
import json
import os
import base64
from PIL import Image
import requests
from io import BytesIO
from pathlib import Path

def getlogs(apikey):
    Url = "http://3.210.100.166:5000/getaccountId"
    data = {'apikey': apikey}
    print("Getting the data please wait ...")
    accId = requests.get(url=Url, params=data, timeout=6000)
    if(accId.text !="Invaild API Key or API key Not Exists"):
        accountId=accId.text
        Url = "http://3.210.100.166:5000/getlogs/" + str(accountId)
        r = requests.get(url=Url)
        if (r.status_code == 200):
            return r.text
        else:
            return "NO logs Found"
    else:
        return accId.text

def getsummarydetailsById(apikey,videoId):
    Url = "http://3.210.100.166:5000/getaccountId"
    data = {'apikey': apikey}
    accId = requests.get(url=Url, params=data, timeout=6000)
    if(accId.text !="Invaild API Key or API key Not Exists"):
        accountId=accId.text
        if (videoId != "None"):
            Url = "http://3.210.100.166:5000/getsummary/" + str(accountId) + "/" + str(videoId)
            print("Getting the data please wait ...")
            r = requests.get(url=Url, timeout=6000)
            if (r.text == "No data Found"):
                return "No data available for video Id"
            else:
                data = r.content
                print("Downloading please wait ...")
                zipFile = str(Path.home() / "Downloads") + "/" + str(videoId) + "_summary.zip"
                with open(zipFile, 'wb') as f:
                    f.write(data)
                return "Successfully downloaded the file to " + str(zipFile)
    else:
        return accId.text

def getsummarydetailsByPath(apikey,videopath):
    Url = "http://3.210.100.166:5000/getaccountId"
    data = {'apikey': apikey}
    accId = requests.get(url=Url, params=data, timeout=6000)
    if(accId.text !="Invaild API Key or API key Not Exists"):
        accountId=accId.text
        Url = "http://3.210.100.166:5000/getsummarybypath/" + str(accountId)
        data = {'videopath': videopath}
        print("Getting the data please wait ...")
        r = requests.get(url=Url, params=data, timeout=6000)
        if (r.text == "No data Found"):
            return "No data available for video Id"
        else:
            data = r.content
            print("Downloading please wait ...")
            zipFile = str(Path.home() / "Downloads") + "/summary.zip"
            with open(zipFile, 'wb') as f:
                f.write(data)
            return "Successfully downloaded the file to " + str(zipFile)
    else:
        return accId.text

def getframedetails(apikey,path):
    Url = "http://3.210.100.166:5000/getaccountId"
    data = {'apikey': apikey}
    accId = requests.get(url=Url, params=data, timeout=6000)
    if (accId.text != "Invaild API Key or API key Not Exists"):
        Url = "http://3.210.100.166:5000/getframedetails"
        data = {'path': path}
        print("Getting the data please wait ...")
        r = requests.get(url=Url, params=data, timeout=6000)
        return  r.text
    else:
        return accId.text


def getframeimage(apikey,path):
    Url = "http://3.210.100.166:5000/getaccountId"
    data = {'apikey': apikey}
    accId = requests.get(url=Url, params=data, timeout=6000)
    if (accId.text != "Invaild API Key or API key Not Exists"):
        accountId = accId.text
        Url = "http://3.210.100.166:5000/getframeimage"
        data = {'path': path}
        print("Getting the data please wait ...")
        r = requests.get(url=Url, params=data, timeout=6000)
        if(r.text !="File not Exists"):
            data = r.content
            print("Downloading please wait ...")
            zipFile = str(Path.home() / "Downloads") + "/frame.png"
            im = Image.open(BytesIO(base64.b64decode(data)))
            im.save(zipFile, 'PNG')
            return  "Successfully downloaded the file to " + str(zipFile)
        else:
            return "File not Exists"
    else:
        return accId.text


def getvideoid(apikey):
    Url = "http://3.210.100.166:5000/getaccountId"
    data = {'apikey': apikey}
    accId = requests.get(url=Url, params=data, timeout=6000)
    if (accId.text != "Invaild API Key or API key Not Exists"):
        accountId = accId.text
        Url="http://3.210.100.166:5000/getvideoid/"+str(accountId)
        r = requests.get(url=Url)
        print(r.text)
    else:
        return accId.text

def addCloudContainer(apikey,filePath):
    Url = "http://3.210.100.166:5000/getaccountId"
    data = {'apikey': apikey}
    accId = requests.get(url=Url, params=data, timeout=6000)
    if (accId.text != "Invaild API Key or API key Not Exists"):
        accountId = accId.text
        with open(filePath) as f:
            data = json.load(f)
        meta = data["actions"]["meta"]
        ai = data["actions"]["ai"]
        displayType = data["container"]["name"]
        providerType = data["container"]["type"]
        bucketType = data["container"]['bucket_name']
        containerType = data["container"]['config_json']
        results_endpoint = data["results_endpoint"]

        mydict = {"apikey": apikey,
                  "accountId": accountId,
                  "bucketName": bucketType,
                  "displayName": displayType,
                  "provider": providerType,
                  "meta": meta,
                  "ai": ai,
                  "results_endpoint": results_endpoint,
                  "container": json.dumps(containerType)
                  }
        Url = "http://3.210.100.166:5000/addcontainer"
        r = requests.post(url=Url, headers={"content-type": "application/json"}, data=json.dumps(mydict))
        return  r.text
    else:
        return accId.text

def getframe(filePath):
    Url = "http://3.210.100.166:5000/getframe"
    data = {'path': filePath}
    r = requests.get(url=Url, params=data, timeout=6000)
    if(r.text != "No image found"):
        return r.json()
    else:
        return "No image found"

def getframePathDetailsById(apikey,videoid):
    Url = "http://3.210.100.166:5000/getaccountId"
    data = {'apikey': apikey}
    accId = requests.get(url=Url, params=data, timeout=6000)
    if(accId.text !="Invaild API Key or API key Not Exists"):
        accountId=accId.text
        if (videoid != "None"):
            Url = "http://3.210.100.166:5000/getframespathbyId/" + str(accountId) + "/" + str(videoid)
            print("Getting the data please wait ...")
            r = requests.get(url=Url, timeout=6000)
            if (r.text == "No data Found"):
                return "No data available for video Id"
            else:
                return (r.text)
    else:
        return accId.text

def getframePathDetailsByVideoPath(apikey,videopath):
    Url = "http://3.210.100.166:5000/getaccountId"
    data = {'apikey': apikey}
    accId = requests.get(url=Url, params=data, timeout=6000)
    if (accId.text != "Invaild API Key or API key Not Exists"):
        accountId = accId.text
        Url = "http://3.210.100.166:5000/getframespath/" + str(accountId)
        data = {'videopath': videopath}
        print("Getting the data please wait ...")
        r = requests.get(url=Url, params=data, timeout=6000)
        if (r.text == "No data Found"):
            return "No data available for video "
        else:
            return r.text
    else:
        return accId.text
















