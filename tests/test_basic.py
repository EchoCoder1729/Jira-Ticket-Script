import unittest
from unittest.mock import MagicMock, patch
from models import Threat
from converter import ThreatConverter
from jira_client import JiraClient

class TestThreatConverter(unittest.TestCase):
    def test_priority_mapping(self):
        self.assertEqual(ThreatConverter.get_priority("High"), "Highest")
        self.assertEqual(ThreatConverter.get_priority("Medium"), "High")
        self.assertEqual(ThreatConverter.get_priority("Low"), "Medium")
        self.assertEqual(ThreatConverter.get_priority("Unknown"), "Medium")

    def test_jira_fields(self):
        threat = Threat(
            id="T-100",
            title="Test Threat",
            category="Test Cat",
            description="Test Desc",
            mitigations=["Fix it"],
            cvss_rating=5.0,
            severity="Medium"
        )
        fields = ThreatConverter.to_jira_fields(threat, "TEST")
        self.assertEqual(fields["project"]["key"], "TEST")
        self.assertEqual(fields["summary"], "T-100: Test Threat")
        self.assertEqual(fields["priority"]["name"], "High")
        self.assertIn("Fix it", str(fields["description"]))

class TestJiraClient(unittest.TestCase):
    @patch('requests.get')
    def test_issue_exists_true(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"total": 1, "issues": [{"key": "TEST-1"}]}
        mock_get.return_value = mock_response
        
        client = JiraClient("http://jira.com", "u", "p", "TEST")
        self.assertTrue(client.issue_exists("T-100"))

    @patch('requests.get')
    def test_issue_exists_false(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"total": 0, "issues": []}
        mock_get.return_value = mock_response
        
        client = JiraClient("http://jira.com", "u", "p", "TEST")
        self.assertFalse(client.issue_exists("T-100"))

if __name__ == '__main__':
    unittest.main()
