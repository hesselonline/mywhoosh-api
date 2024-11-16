"""

MyWhoosh class

"""

from datetime import datetime
from requests.auth import HTTPBasicAuth
import requests

class MyWhoosh:
    """
    MyWhoosh class
    """
    def __init__(self, user, password):
        """ Constructor for MyWhoosh class """
        self.user = user
        self.password = password
        self.auth_url = 'https://event.mywhoosh.com/api/auth/login'
        self.profile_url = 'https://event.mywhoosh.com/api/auth/profile'
        self.base_url = 'https://service14.mywhoosh.com/v2/'
        self.token = self.get_token()
        self.auth_header = {'Authorization': 'Bearer ' + self.token}

    def get_token(self):
        """ Get token for authentication """	
        data = {
            'email': self.user,
            'password': self.password,
            'remember': 'true'
        }
        response = requests.post(self.auth_url, data=data)
        return response.json()['data']['token']
    

    def get_activities(self):
        """ Get activities """	
        activities_url = self.base_url + 'rider/profile/activities'
        current_page = 1
        activities = []
        while True:
            
            body = {'sortDate': "DESC", 'page': current_page}
            response = requests.post(activities_url, headers=self.auth_header, json=body)
            activities.extend(response.json()['data']['results'])
            if response.json()['data']['totalPages'] == current_page:
                break
            
            current_page += 1
        return activities
    
    def get_activity_file(self, activity_id, file_name):
        """ Get activity file """	
        get_file_url = self.base_url + 'rider/profile/download-activity-file'
        response = requests.post(get_file_url, headers=self.auth_header, json={'fileId': activity_id})
        file_url = response.json()['data']
        with requests.get(file_url, stream=True) as r:
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def get_profile(self):
        """ Get profile """	
        profile_url = self.profile_url
        response = requests.get(profile_url, headers=self.auth_header)
        return response.json()['data']

