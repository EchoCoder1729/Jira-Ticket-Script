# Jira Threat Converter

A tool to convert security threats from a JSON file into Jira tickets.

## Features
- Reads threats from `input.json`
- Creates Jira tickets using the REST API
- Maps "High" severity to "Highest" priority
- Includes CVSS, Category, and Mitigations in the description
- Prevents duplicate ticket creation for the same Threat ID

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   Create a `.env` file in the root directory (copy `.env.example`) and fill in your Jira details:
   ```properties
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_USER_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token
   JIRA_PROJECT_KEY=PROJ
   ```
   
   To get an API Token, go to: https://id.atlassian.com/manage-profile/security/api-tokens

3. **Input Data**
   Ensure `input.json` exists in the root directory. See `input.json` for the expected format.

## Usage

Run the script:
```bash
python main.py
```

## Testing

Run unit tests:
```bash
python -m unittest discover tests
```
