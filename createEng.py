#!/usr/bin/python

import requests as rq
import json
from datetime import datetime

pToken = "Bearer jMG-AyprRK6IOJMBtzsqY5xTHcz_kE-H399qA8GXwqTANwSjMnr1HVef_mTy3GQi"
talendWorkspaces = "https://api.eu.cloud.talend.com/orchestration/workspaces"
headers = {'Authorization': pToken}

def getWorkSpaceAndEnvIds(env="default", personalToken = pToken):
    """
    Function to get workspace and environment id`s
    @env environment name same as it in a cloud
    @personaToken - personal or service Token as a string
    witn Bearer in the begining
    returns workspaceId, environmentId and information of 
    """
    wrkSpcId = ""
    envId = ""
    envData = ""
    talendWorkspaces = "https://api.eu.cloud.talend.com/orchestration/workspaces"
    headers = {'Authorization': personalToken}
    response = rq.get(talendWorkspaces, headers=headers)
    txtResp = response.text
    jsonResp = json.loads(txtResp)
    for i in jsonResp:
        if i["environment"]["name"] == env and i["owner"] == "sergei.raikov":
            wrkSpcId = i["id"]
            envId = i["environment"]["id"]
            envData = i
            break
    print("Information about environment remote engine will be on \n")
    print(envData)
    return wrkSpcId, envId


def createRemoteEngine(name="testName ", env = "default", personalToken = pToken):
    """
    Function creates remote engine at Talend Cloud
    @name - name of remoteEngine
    @env - environment for remote engine
    @personalToken - personal Token or service acc Token
    in Talend Cloud current datetime added to RE name
    returns pre-authorized key and data about created engine
    """
    urlRemoteEng = "https://api.eu.cloud.talend.com/tmc/v1.3/runtimes/remote-engines"
    name = name + str(datetime.now())
    ids = getWorkSpaceAndEnvIds(env, pToken)
    payload = {
    "name": name,
        "environmentId": ids[1],  
    "workspaceId":  ids[0]}
    headers = {'Authorization': personalToken, "Content-Type": "application/json", "Accept": "application/json"}
    response = rq.post(url = urlRemoteEng, headers=headers, json=payload)
    txtResp = response.text
    jsonResp = json.loads(txtResp)
    print(" \nInformation about newly created Remote Engine \n")
    print(jsonResp)
    return jsonResp["preAuthorizedKey"], jsonResp["name"]


key, engineName = createRemoteEngine()
with open('/home/preAuthoKey.txt', 'w') as f:
    f.write(key)