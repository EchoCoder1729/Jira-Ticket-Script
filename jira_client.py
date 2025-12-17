import requests
import base64
from typing import Dict, Any, Optional

class JiraClient:
    def __init__(self, base_url: str, email: str, api_token: str, project_key: str):
        self.base_url = base_url.rstrip('/')
        self.email = email
        self.api_token = api_token
        self.project_key = project_key
        
        # Determine authentication header
        auth_str = f"{self.email}:{self.api_token}"
        self.auth_header = {
            "Authorization": f"Basic {base64.b64encode(auth_str.encode()).decode()}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def issue_exists(self, threat_id: str) -> bool:
        """
        Checks if an issue with the given Threat ID already exists in the project.
        Uses JQL to search for the Threat ID in the summary.
        """
        jql = f'project = "{self.project_key}" AND summary ~ "{threat_id}"'
        search_url = f"{self.base_url}/rest/api/3/search/jql"
        
        params = {
            "jql": jql,
            "maxResults": 1,
            "fields": "id,key,summary"
        }
        
        try:
            response = requests.get(search_url, headers=self.auth_header, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("total", 0) > 0
        except requests.exceptions.RequestException as e:
            print(f"Error checking for existing issue: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False

    def create_issue(self, issue_fields: Dict[str, Any]) -> Optional[str]:
        """
        Creates a new issue in Jira.
        Returns the Key of the created issue, or None if failed.
        """
        create_url = f"{self.base_url}/rest/api/3/issue"
        
        # Ensure project key is set in fields
        if "project" not in issue_fields:
            issue_fields["project"] = {"key": self.project_key}
            
        payload = {"fields": issue_fields}
        
        try:
            response = requests.post(create_url, headers=self.auth_header, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("key")
        except requests.exceptions.RequestException as e:
            print(f"Error creating issue: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
