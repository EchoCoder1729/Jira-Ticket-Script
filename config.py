import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
INPUT_FILE = os.getenv("INPUT_FILE", "input.json")

def validate_config():
    missing = []
    if not JIRA_URL: missing.append("JIRA_URL")
    if not JIRA_USER_EMAIL: missing.append("JIRA_USER_EMAIL")
    if not JIRA_API_TOKEN: missing.append("JIRA_API_TOKEN")
    if not JIRA_PROJECT_KEY: missing.append("JIRA_PROJECT_KEY")
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
