import uuid

import requests

import src.config as config

SAPLING_URL = 'https://api.sapling.ai/api/v1/edits'

class Editor:    
    def edit(self, text):
        try:
            response = requests.post(
                "https://api.sapling.ai/api/v1/edits",
                json={
                    "key": str(uuid.uuid4()),
                    "text": text,
                    "session_id": self.session_id
                }
            )
            response_json = response.json()
            if response.ok:
                return response_json
            else:
                raise Exception(f"{response_json}")
        except Exception as e:
            print(f'An error occurred: {e}')
        
        return None # error :(
        
        
