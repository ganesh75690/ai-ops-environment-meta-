"""
OpenEnv Client for AI Operations Environment
"""

import requests
from typing import Dict, Any, List
from ai_ops_env.models import Action, Observation


class OpenEnvClient:
    """Client for interacting with the AI Operations Environment"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def reset(self) -> Dict[str, Any]:
        """Reset the environment"""
        response = requests.get(f"{self.base_url}/reset")
        return response.json()
    
    def step(self, action: Action) -> Dict[str, Any]:
        """Take a step in the environment"""
        response = requests.post(f"{self.base_url}/step", json=action.dict())
        return response.json()
    
    def get_state(self) -> Dict[str, Any]:
        """Get current environment state"""
        response = requests.get(f"{self.base_url}/state")
        return response.json()
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        """Get available tasks"""
        response = requests.get(f"{self.base_url}/tasks")
        return response.json()


# Default client instance
client = OpenEnvClient()
