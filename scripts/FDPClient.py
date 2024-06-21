import Config
import requests
import json


"""
Interface to interact FDP content
"""

class FDPClient:

    FDP_URL = None
    FDP_ADMIN_USERNAME = "albert.einstein@example.com"
    FDP_ADMIN_PASSWORD = "password"
    FDP_P_URL =None

    def __init__(self, fdp_url, username, password, persistent_url):
        self.FDP_URL = fdp_url
        self.FDP_ADMIN_USERNAME = username
        self.FDP_ADMIN_PASSWORD = password
        self.FDP_P_URL = persistent_url

    def fdp_get_token(self):
        url = self.FDP_URL + "/tokens"
        data = {"email": self.FDP_ADMIN_USERNAME, "password": self.FDP_ADMIN_PASSWORD}
        payload = json.dumps(data)
        headers = {
            'Content-Type': "application/json"
        }
        
        if Config.DEBUG:
            print("Sending authentication request:")
            print("URL:", url)
            print("headers:", headers)
            print("payload:", payload)

        response = requests.request("POST", url, data=payload, headers=headers)
        data = json.loads(response.text)
        if Config.DEBUG:
            print("server response:", response)
            print("response data:", response.text)
        try:
            return data["token"]
        except:
            raise SystemError("Error getting authentication token. Is the configuration of the FDP URL, username and password correct? Make sure the URL's don't end with a '/' character.")
        

    def fdp_create_metadata(self, data, resource_type):

        url = self.FDP_URL + "/" + resource_type
        token = self.fdp_get_token()
        authorization = "Bearer " + token
        headers = {
            'Content-Type': "text/turtle",
            'Authorization': authorization
        }
        if not isinstance(data, str):
            data = data.decode("utf-8")

        if Config.DEBUG:
            print("Sending POST request:")
            print("URL:", url)
            print("authorization:", authorization)
            print("headers:", headers)
            print("payload:", data)

        response = requests.request("POST", url, data=data.encode('utf-8'), headers=headers)
        
        if Config.DEBUG:
            print("server response:", response)
            print("response data:", response.text)

        try:
            resource_url = response.headers["Location"]
        except:
            raise SystemError("Error getting location url after sending RDF. Did the RDF fail validation in the FDP? (Then check the FPD logs)")

        self.fdp_publish_metadata(resource_url.replace(self.FDP_P_URL, self.FDP_URL))

        return resource_url

    def fdp_publish_metadata(self, url):
        token = self.fdp_get_token()
        authorization = "Bearer " + token
        state_url = url + "/meta/state"
        data = {"current": "PUBLISHED"}
        headers = {
            'Content-Type': "application/json",
            'Authorization': authorization
        }
        payload = json.dumps(data)
        response = requests.request("PUT", state_url, data=payload, headers=headers)
        print(response)

    def does_metadata_exists(self, url):
        response = requests.request("GET", url)

        if response.status_code == 200:
            return True
        else:
            return False
