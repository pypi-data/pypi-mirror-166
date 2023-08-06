import json
import os
import base64
from PIL import Image
import requests
from io import BytesIO
from pymongo import MongoClient
from pymongo import MongoClient
import pymongo
connection = "mongodb+srv://vienamongo1:Ncet123@cluster0.qqqyj.mongodb.net/viena_baikal"
myclient = pymongo.MongoClient("mongodb+srv://vienamongo1:Ncet123@cluster0.qqqyj.mongodb.net/")
mydb = myclient["viena_baikal"]
mycol = mydb["apikey"]
from pathlib import Path
def generate_access_token_from_config_file():
    pass

def get_api_key_from_credentials():
    API_KEY=""
    if (not os.path.isfile(os.path.expanduser('~/.viena/credentials'))):
        return "Not Found"
    f = open(os.path.expanduser('~/.viena/credentials'), "r")
    token = f.read()
    if (token == ""):
        return "Not Found"
    token = token.split(":")
    API_KEY = token[1]
    return API_KEY

def configuredetails(jsonpath):
    apikey=get_api_key_from_credentials()
    #print(apikey)
    if(apikey=='' or apikey=="Not Found"):
        return "API key not found, Please run 'viena --configure' to configure"
    mycol = mydb["apikey"]
    if mycol.count({'apikey': apikey}, limit=1) != 0:
        for itm in mycol.find({"apikey": apikey}):
            accountId=(itm.get('accountId'))
    else:
        return "Invaild API Key or API key Not Exists"
    with open(jsonpath) as f:
        data = json.load(f)
    meta=data["actions"]["meta"]
    ai=data["actions"]["ai"]
    displayType=data["container"]["name"]
    providerType=data["container"]["type"]
    bucketType=data["container"]['bucket_name']
    containerType=data["container"]['config_json']
    results_endpoint=data["results_endpoint"]

    mydict = {"apikey": apikey,
              "accountId": accountId,
              "bucketName": bucketType,
              "displayName": displayType,
              "provider": providerType,
              "meta":meta,
              "ai":ai,
              "results_endpoint":results_endpoint,
              "container":json.dumps(containerType)
              }
    mycol2=mydb["account"]
    x = mycol2.insert_one(mydict)
    if(x.inserted_id):
        return "Successfully configured the details"
    else:
        return "Update failed"

def updatedetails(jsonpath):
    apikey = get_api_key_from_credentials()
    # print(apikey)
    if (apikey == '' or apikey == "Not Found"):
        return "API key not found, Please run 'viena --configure' to configure"
    mycol = mydb["apikey"]
    if mycol.count({'apikey': apikey}, limit=1) != 0:
        for itm in mycol.find({"apikey": apikey}):
            accountId=(itm.get('accountId'))
    else:
        return "Invaild API Key or API key Not Exists"
    with open(jsonpath) as f:
        data = json.load(f)
    meta = data["actions"]["meta"]
    ai = data["actions"]["ai"]
    displayType = data["container"]["name"]
    providerType = data["container"]["type"]
    bucketType = data["container"]['bucket_name']
    containerType = data["container"]['config_json']
    results_endpoint = data["results_endpoint"]
    mycol = mydb["account"]
    if mycol.count({'bucketName': bucketType}, limit=1) != 0:
        myquery = {"bucketName": bucketType}
        newvalues = {"$set": {"apikey": apikey ,
                              "accountId":accountId,
                              "displayName": displayType,
                              "provider": providerType,
                               "meta": meta,
                                "ai": ai,
                                "results_endpoint": results_endpoint,
                                "container": json.dumps(containerType)
                      }}
        mycol.update_many(myquery, newvalues)
        return "Successfully updated the details"
    else:
        return "Details not found to update"

def getlogs():
    apikey = get_api_key_from_credentials()
    # print(apikey)
    if (apikey == '' or apikey == "Not Found"):
        return "API key not found, Please run 'viena --configure' to configure"
    mycol = mydb["apikey"]
    if mycol.count({'apikey': apikey}, limit=1) != 0:
        for itm in mycol.find({"apikey": apikey}):
            accountId=(itm.get('accountId'))
    else:
        return "Invaild API Key or API key Not Exists"
    Url="http://3.210.100.166:5000/getlogs/"+str(accountId)
    r = requests.get(url=Url)
    if(r.status_code==200):
        return r.text
    else:
        return "NO logs Found"

def getsummarydetails(videoid,videopath):
    apikey = get_api_key_from_credentials()
    # print(apikey)
    if (apikey == '' or apikey == "Not Found"):
        return "API key not found, Please run 'viena --configure' to configure"
    mycol = mydb["apikey"]
    if mycol.count({'apikey': apikey}, limit=1) != 0:
        for itm in mycol.find({"apikey": apikey}):
            accountId=(itm.get('accountId'))
    else:
        return "Invaild API Key or API key Not Exists"
    if(videoid !="None"):
        Url="http://3.210.100.166:5000/getsummary/"+str(accountId)+ "/"+str(videoid)
        print("Getting the data please wait ...")
        r = requests.get(url=Url,timeout = 6000)
        if(r.text=="No data Found" ):
            return "No data available for video Id"
        elif(r.text=="Invaild API Key or API key Not Exists"):
            return r.text
        else:
            data = r.content
            print("Downloading please wait ...")
            zipFile=str(Path.home() / "Downloads")+"/"+str(videoid)+"_summary.zip"
            with open(zipFile, 'wb') as f:
                f.write(data)
            return "Successfully downloaded the file to "+str(zipFile)
    elif(videopath !="None"):
        Url = "http://3.210.100.166:5000/getsummarybypath/" + str(accountId)
        data = {'videopath': videopath}
        print("Getting the data please wait ...")
        r = requests.get(url=Url, params=data,timeout=6000)
        if (r.text == "No data Found"):
            return "No data available for video Id"
        else:
            data = r.content
            print("Downloading please wait ...")
            zipFile = str(Path.home() / "Downloads") + "/summary.zip"
            with open(zipFile, 'wb') as f:
                f.write(data)
            return "Successfully downloaded the file to " + str(zipFile)


def getframedetails(path):
    apikey = get_api_key_from_credentials()
    # print(apikey)
    if (apikey == '' or apikey == "Not Found"):
        return "API key not found, Please run 'viena --configure' to configure"
    mycol = mydb["apikey"]
    if mycol.count({'apikey': apikey}, limit=1) != 0:
        for itm in mycol.find({"apikey": apikey}):
            accountId=(itm.get('accountId'))
    else:
        return "Invaild API Key or API key Not Exists"
    if(path !="None"):
        Url = "http://3.210.100.166:5000/getframedetails"
        data = {'path': path}
        print("Getting the data please wait ...")
        r = requests.get(url=Url, params=data, timeout=6000)
        return  r.text


def getframeimage(path):
    apikey = get_api_key_from_credentials()
    # print(apikey)
    if (apikey == '' or apikey == "Not Found"):
        return "API key not found, Please run 'viena --configure' to configure"
    mycol = mydb["apikey"]
    if mycol.count({'apikey': apikey}, limit=1) != 0:
        for itm in mycol.find({"apikey": apikey}):
            accountId=(itm.get('accountId'))
    else:
        return "Invaild API Key or API key Not Exists"
    if(path !="None"):
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


def getvideoid():
    apikey = get_api_key_from_credentials()
    # print(apikey)
    if (apikey == '' or apikey == "Not Found"):
        return "API key not found, Please run 'viena --configure' to configure"
    mycol = mydb["apikey"]
    if mycol.count({'apikey': apikey}, limit=1) != 0:
        for itm in mycol.find({"apikey": apikey}):
            accountId=(itm.get('accountId'))
    else:
        return "Invaild API Key or API key Not Exists"
    Url="http://3.210.100.166:5000/getvideoid/"+str(accountId)
    r = requests.get(url=Url)
    print(r.text)

def getframespathfromDB(videoid,videopath):
    apikey = get_api_key_from_credentials()
    # print(apikey)
    if (apikey == '' or apikey == "Not Found"):
        return "API key not found, Please run 'viena --configure' to configure"
    mycol = mydb["apikey"]
    if mycol.count({'apikey': apikey}, limit=1) != 0:
        for itm in mycol.find({"apikey": apikey}):
            accountId=(itm.get('accountId'))
    else:
        return "Invaild API Key or API key Not Exists"
    if(videoid !="None"):
        Url="http://3.210.100.166:5000/getframespathbyId/"+str(accountId)+ "/"+str(videoid)
        print("Getting the data please wait ...")
        r = requests.get(url=Url,timeout = 6000)
        if(r.text=="No data Found"):
            return "No data available for video Id"
        else:
            return (r.text)
    elif(videopath !="None"):
        Url = "http://3.210.100.166:5000/getframespath/" + str(accountId)
        data = {'videopath': videopath}
        print("Getting the data please wait ...")
        r = requests.get(url=Url, params=data,timeout=6000)
        if (r.text == "No data Found"):
            return "No data available for video "
        else:
            return r.text

