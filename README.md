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

3. **Configuration**
   Create a `.env` file in the root directory (copy `.env.example`) and fill in your Jira details:
   ```properties
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_USER_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token
   JIRA_PROJECT_KEY=SCRUM
   INPUT_FILE=input.json
   ```
   
   **How to get these values:**
   - **JIRA_URL**: Your Jira Cloud instance URL (e.g., `https://mycompany.atlassian.net`).
   - **JIRA_USER_EMAIL**: The email address you use to log in to Jira.
   - **JIRA_API_TOKEN**: Create one at [Atlassian ID - API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
   - **JIRA_PROJECT_KEY**: The key of the project where tickets should be created (e.g., `SCRUM`, `PROJ`). You can find this in your project settings.
   - **INPUT_FILE**: Path to the JSON file containing threats (defaults to `input.json`).

3. **Input Data**
   Ensure `input.json` exists in the root directory. See `input.json` for the expected format. This is the sample input expected.

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

## Output Example

The script creates Jira tickets with the appropriate priority and description:

![Jira Output](assets/output_example.png)
