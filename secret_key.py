#This is how all the personal data will be accessed so we dont have to hard code the data user can edit the settings.json to make any changes 

import json
import base64

def getCW_ClientID():
    try:
        with open("backend/api_holder.json" , "r") as read: 
            data = json.load(read)

        return data.get("Cw client ID")
    except: 
        print("cant find client id " + data.get("Cw client ID"))
        return "" 
        
def generateToken(): 
    #The reason why I dont call once and pass around the data is because functions wont be called in any order 
    try:
        with open("backend/api_holder.json" , "r") as read: 
            data = json.load(read)
            
            #Encode the data to transfer it to byte type

            key = (data.get("CW company identifier") + "+" + data.get("CW public key") + ":" + data.get("CW private key"))
        #Decode the data later to transfer it back into str type
        encode = base64.b64encode(key.encode())
        
    except: 
        print("CANT FIND SETTINGS")
        return ""
    

    # encode = encode.replace("b" , "")
    
    return encode.decode()

#Returns the stuff needed to gain the syncro msp data 

def getSyncroSubDomain(): 
    try:
        with open("backend/api_holder.json" , "r") as read: 
            data = json.load(read)
            
        subDomain = data.get("SyncroMSP subdomain")
        return subDomain
    except: 
        return ""

def getSyncro_APIKey(): 
    print("here")
    try:
        with open("backend/api_holder.json" , "r") as read: 
            data = json.load(read)

        key = data.get("SyncroMsp Api key")
        return key
    except Exception as e:
        print("Cant open api holder")
        print(e)
        return ""