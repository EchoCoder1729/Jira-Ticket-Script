import json
import logging
import sys
from typing import List

import config
from models import Threat
from jira_client import JiraClient
from converter import ThreatConverter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_threats(filepath: str) -> List[Threat]:
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            threats_data = data.get("threats", [])
            return [Threat(**t) for t in threats_data]
    except FileNotFoundError:
        logger.error(f"Input file not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {filepath}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading threats: {e}")
        sys.exit(1)

def main():
    try:
        config.validate_config()
    except ValueError as e:
        logger.error(str(e))
        logger.info("Please create a .env file with the required variables. See README.md.")
        sys.exit(1)

    logger.info("Starting Jira Threat Converter...")
    
    # Initialize Jira Client
    jira = JiraClient(
        base_url=config.JIRA_URL,
        email=config.JIRA_USER_EMAIL,
        api_token=config.JIRA_API_TOKEN,
        project_key=config.JIRA_PROJECT_KEY
    )

    # Load Threats
    logger.info(f"Loading threats from {config.INPUT_FILE}...")
    threats = load_threats(config.INPUT_FILE)
    logger.info(f"Found {len(threats)} threats.")

    # Process Threats
    for threat in threats:
        logger.info(f"Processing threat {threat.id}: {threat.title}")
        
        if jira.issue_exists(threat.id):
            logger.info(f"Issue for threat {threat.id} already exists. Skipping.")
            continue
            
        fields = ThreatConverter.to_jira_fields(threat, config.JIRA_PROJECT_KEY)
        key = jira.create_issue(fields)
        
        if key:
            logger.info(f"Created issue {key} for threat {threat.id}")
        else:
            logger.error(f"Failed to create issue for threat {threat.id}")

    logger.info("Processing complete.")

if __name__ == "__main__":
    main()
