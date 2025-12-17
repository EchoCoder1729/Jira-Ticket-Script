from models import Threat
from typing import Dict, Any

class ThreatConverter:
    @staticmethod
    def get_priority(severity: str) -> str:
        """
        Maps High/Medium/Low severity to Jira Priority.
        Note: Exact priority names depend on the Jira project configuration.
        Standard Cloud priorities are often: Highest, High, Medium, Low, Lowest.
        """
        s = severity.lower()
        if s == "high":
            return "Highest" # Or Urgent
        elif s == "medium":
            return "High"
        elif s == "low":
            return "Medium"
        return "Medium" # Default

    @staticmethod
    def to_jira_fields(threat: Threat, project_key: str) -> Dict[str, Any]:
        """
        Converts a Threat object into a dictionary of Jira issue fields.
        """
        
        # Construct a rich description
        description_text = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": threat.description}]
                },
                {
                    "type": "heading",
                    "attrs": {"level": 3},
                    "content": [{"type": "text", "text": "Details"}]
                },
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [{
                                "type": "paragraph",
                                "content": [{"type": "text", "text": f"ID: {threat.id}"}]
                            }]
                        },
                        {
                            "type": "listItem",
                            "content": [{
                                "type": "paragraph",
                                "content": [{"type": "text", "text": f"Category: {threat.category}"}]
                            }]
                        },
                        {
                            "type": "listItem",
                            "content": [{
                                "type": "paragraph",
                                "content": [{"type": "text", "text": f"CVSS Rating: {threat.cvss_rating}"}]
                            }]
                        },
                        {
                            "type": "listItem",
                            "content": [{
                                "type": "paragraph",
                                "content": [{"type": "text", "text": f"Severity: {threat.severity}"}]
                            }]
                        }
                    ]
                },
                {
                    "type": "heading",
                    "attrs": {"level": 3},
                    "content": [{"type": "text", "text": "Mitigations"}]
                }
            ]
        }
        
        # Add mitigations to the description
        mitigation_list = {
            "type": "bulletList",
            "content": []
        }
        for mitigation in threat.mitigations:
            mitigation_list["content"].append({
                "type": "listItem",
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": mitigation}]
                }]
            })
        
        description_text["content"].append(mitigation_list)

        priority_name = ThreatConverter.get_priority(threat.severity)

        return {
            "project": {"key": project_key},
            "summary": f"{threat.id}: {threat.title}",
            "description": description_text,
            "issuetype": {"name": "Bug"}, # Using Bug as requested/default
            "priority": {"name": priority_name},
            # Labels can be useful for filtering
            "labels": ["security_threat", threat.category.replace(" ", "_")]
        }
