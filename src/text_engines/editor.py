import requests
import uuid
import src.config as config

SAPLING_URL = 'https://api.sapling.ai/api/v1/edits'

class Editor:
    def __init__(self):
        self.api_key = config.SAPLING_API_KEY
        self.session_id = uuid.uuid4()
    
    def edit(self, text):
        try:
            response = requests.post(
                SAPLING_URL, 
                json={
                    'key': self.api_key,
                    'text': text,
                    'session_id': self.session_id
                }
            )
            response_json = response.json()

            if response.status_code == 200:
                return response_json['result']
        except Exception as e:
            print(f'An error occurred: {e}')
        
        return None # error :(
        
        
