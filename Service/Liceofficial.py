from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)
from helper import write_to_excel_sheet
from time import strftime, localtime
import requests
import helper
import json


elk = helper.elk
api = helper.api
headers = helper.headers
odata_lic = helper.odata_lic
odata_machines = helper.odata_machines
orchURL = helper.orchURL
auth = helper.auth

# def authenticate_user(self, orchURL, auth):
def get_licence():
    print("Writing to file please wait ... ")
    try:
        url = orchURL + api
        response = requests.post(
            url, data=json.dumps(auth), headers=headers, verify=False
        )
        getToken = response.json()
        if response.status_code == 200:
            bearer_token = str(getToken["result"])
            print("Successful Authentication")
            # return self.bearer_token
        else:
            print("Authentication Unsuccessful", response.status_code)
        # return False
    except requests.exceptions.RequestException as error:
        print(error)
    except Exception as e:
        print(
            f"An error occurred while authenticating the user on Orchestrator. {e}"
        )
        
    # connecting to server 
    bearer_token = {"Authorization": "Bearer {}".format(bearer_token)}
    headers.update(bearer_token)
    url = orchURL + odata_lic

    # print("Making API call to check the connection.")
    Getlic = requests.get(url, headers=headers, verify=False).json()

    # if response is success get licence
    if response.status_code == 200: 
        data = Getlic['ExpireDate']
        datef = strftime('%Y-%m-%d', localtime(data))
        write_to_excel_sheet('Server Licence', [orchURL, datef], ["Instance Name / Host", "Expire Date"])
        write_to_excel_sheet('Server Licence', [elk, "2024-4-1"], ["Instance Name / Host", "Expire Date"])
        # print("Finished =)")

    else:
        print("Server is not Reachable")
        
    helper.style_cells('Server Licence')
    helper.column_width('Server Licence')