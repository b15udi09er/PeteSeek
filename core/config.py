import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config/settings.json"

class Config:
    def __init__(self):
        self.data = self._load_config()
        
    def _load_config(self):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    
    @property
    def status_channel(self):
        return self.data["channels"]["status"]
    
    @property 
    def response_channels(self):
        return self.data["channels"]["response"]
    
    @property
    def admin_roles(self):
        return self.data["permissions"]["admin_roles"]

    @property
    def status_message_id(self):
        return self.data["status_message_id"]

    @property 
    def primary_location(self):
        return self.data["system"]["primary_location"]

config = Config()  # Singleton instance