#AUTHOR : Riley Hall 
#Date : Feb 19 2025   
#Description : Finds user inputed company and then changes the assets associated with that company from type "Laptop" , "Desktop" to "Managed Workstation"

#Hey Leo!!!
#I have built a little error handling into this program, not too much yet, but I think it gets most of the errors. 
#If you manage to break the program or notice any errors in the return configurations or anything you want changed let me know. 

#If you want to test the multiple company return path I would type in "Pacific" and you should get a list of a couple companies. When prompted is this your company hit "n"
#Then it should ask is the company in the list hit "y" and then it should print out the indexes for the companies select the correct index and it should find the assets
#associated with that company

#As of right now it should error out at the end since there is no Prison Mike PC anymore 


import re 
import requests as req
import secret_key as keys


HEADER_DATA = req.get(url = "https://na.myconnectwise.net/login/companyinfo/nexthop" )
CW_HEADER = {"Authorization" : "Basic " + keys.generateToken(), "clientID":"3040b6af-ac90-42e6-932d-9178fc76f128"  ,\
                    "Content-Type":"application/json; charset=utf-8"\
                    , "Accept" : f"application/vnd.connectwise.com+json; {HEADER_DATA.json().get("VersionCode")}"}
CODE_BASE = HEADER_DATA.json().get("Codebase")
CW_URL = "https://api-na.myconnectwise.net/"+CODE_BASE+"//apis/3.0/"

#Get User input. Wait for correct company name and then return it
def get_user_input() -> str:

    company_name : str = ""
    valid = False
    while True:
        company_name : str = input("Input Company Name... ==>> ")
        #Regular expression, just checking if a number exists inside the company name or a special character. Most likley that wasn't meant to be inputed. 
        if(re.search("[0-9]" , company_name) or re.search("[%^&*$!#.,;]" , company_name)):
            print("Company Name invalid! Please try again")
        else:
            valid = True
        if(valid):
            #Striping away any leading or trailing white space 
            company_name = company_name.lstrip()
            company_name = company_name.rstrip()

            #Check if the company name is the correct company name
            right_input = input(f"Is this the right company name {company_name}? y/n ==>> ")

            if(right_input == 'y' or right_input == 'Y'):
                return company_name
        

#Find the company in connectwise
def find_company_connectwise(company_name : str)->dict:

    try: 
        results = req.get(url=f'{CW_URL}company/companies?conditions=name like "%{company_name}%"&fields=name,id,identifier' , headers=CW_HEADER)
        #INFO if company is found and the results are greater than 0 meaning if there are results
        if(results.status_code == 200 and len(results.json()) == 1):
            print(f"Company Found! Here are the details \n *******************************************\n{results.json()}\n*******************************************")
            #Check with user if the company found is the correct company 
            valid = input("Is this the right company y/n ==>> ")
            if(valid == "y" or valid == "Y"):
                return results.json()[0]
            else:
                return -1
        elif(results.status_code == 200 and len(results.json()) > 1):
            #Else there might be multiple returned values meaning multiple companies with similar names 
            counter = 0
                #Layout the companies with list position, allowing the user to identify the correct position of company within the list  
            for item in results.json():
                print(f"Company name ==>> {item.get("name")} Position ==>> {counter}")
                counter += 1
            index_value = input("What is the position of the company in the list. Input n if company is noth there ==>> ")
            #Check with user if the company selected is the right company 
            if(index_value != "n" or index_value != "N"):
                right_choice = input(f"You have chosen {results.json()[int(index_value)]}. Is this right y/n ==>> ")
                if(right_choice == "y" or right_choice == 'y'):
                    return results.json()[int(index_value)]

            else:
                #Company was not in the list provided 
                print("Company was not in the list provided")
                return -1
        else:
            print("Couldn't find company. Check spelling of company name. Make sure it is the NAME of comapny and not identifier")
            return -1
    except Exception as e:
        print(e)
        return -1

#Getting company configurations 
def get_company_assets(company_details : dict)-> list: 
    #INFO This will hold all assets that contain Laptop / Desktop as their Type
    config_list = []
    try:
        results = req.get(url=f'{CW_URL}company/configurations?conditions=company/id={company_details.get("id")}&pageSize=1000' , headers=CW_HEADER)

        if(results.status_code == 200 and len(results.json()) > 0):
            print(f"Company Assets Found! Are these the assets you want to change \n*******************************************\n")
            for item in results.json():
                #Only gathering the assets if they are equal to a desktop or laptop.... Can add server to it as well later.
                    if(item.get("type").get("name") == "Desktop" or item.get("type").get("name") == "Laptop"):
                        #Printing out the names of the assets for the user to view. Make sure the assets are correct
                        print(f"Name ==> {item.get("name")} Type ==>> {item.get("type").get("name")}")
                        config_list.append(item)
            
            print("\n*******************************************")
            valid = input("Are those assets correct? Review them carefully! y/n ==>> ")
            if(valid == 'y' or valid == "Y"):
                return config_list
            else:
                print("These aren't the assets you're looking for....")
                return -2
    except Exception as e:
        print("Error in get company assets")
        print(e)
#This is where the change of the assets occurs 
def change_type_name(config_list : list):
    try:
        print("Changing type")
        patch_data = [{
                        "op" : "replace",
                        "path" : "type",
                        "value" : {
                            "name" : "Managed Workstation"
                        }
                    }]
        
        #id of managed workstation == >> 17
        for item in config_list:
            #Remove If statement before deploying
            
                
            results = req.patch(url=f'{CW_URL}company/configurations/{item.get("id")}/changeType', json=patch_data , headers=CW_HEADER)
            print(f"URL of Asset ==>> {results.url}")
            #Checking if the patch request was done correctly. If not then stop the code and tell user to restart program.
            if(results.status_code == 200):
                print("Change Successful")
            else:
                print("Change Unsuccessful. Shutting Program down")
                print(results.json())
                return -3
    except UnboundLocalError:
        print("PC Prison Mike is not found")
        return -3
    except Exception as e:
        return -3

        
#Gets the error code from the functions and prints out the translation
def error_handler(error_code : int) -> None:
    
    match(error_code):
        case -1:
            print("Can't find company. ")
        case -2:
            print("Can't find any configurations for the company. ")
        case -3:
            print("Couldn't change the type of the configuration. ")
        case _:
            print("An error occured while searching. Please try again")




if __name__ == "__main__":

    running = True 
    while running:
        #Prompt User to get Company name. Do a little data cleaning. 
        company_name = get_user_input()
        print(company_name)
        #Find the company in Connecwise 
        company_details = find_company_connectwise(company_name=company_name)

        if(type(company_details) != int):
            #Finding the configurations for the company 
            config_list = get_company_assets(company_details=company_details)
            if(type(config_list) != int):
            #Change the Configuration data type for the company 
                change_type_name(config_list=config_list)
            else:
                error_handler(config_list)
        else:
            print("There seems to have been an error within the search....")
            error_handler(company_details)
        con = input("Would you like to continue? y/n ==>> ")
        con = con.lower()

        if(con == "n"):
            print("Goodbye")
            running = False
        







