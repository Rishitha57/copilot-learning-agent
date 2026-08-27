import os
from jira import JIRA
from atlassian import Confluence


class JiraConfluenceConnector:
    def __init__(self):
        # Pre-configured with your Atlassian credentials
        self.jira_url = os.getenv("JIRA_URL", "https://testingwithelitea.atlassian.net")
        self.jira_user = os.getenv("JIRA_USER", "rishitha_mopuru@epam.com")
        self.jira_token = os.getenv("JIRA_API_TOKEN", "ATATT3xFfGF01GA-Cp7fFw6AHXRvtcB3Ty0nAfnG3eCvEd5PhZLQkqFpfO6qL5FLjzyEsYlv6gN4xgznLHWVkIE8xfkwTtqmOdatJR4a47ceF9YCw_QkmYE-cMddN6zAJpUKqgdZnLDFTEItEIaln0hpeL5zIYxcHHzgM-fTDHmmGV6I-MoCCGY=3C1BFECA")

        self.confluence_url = os.getenv("CONFLUENCE_URL", "https://testingwithelitea.atlassian.net/wiki")
        self.confluence_user = os.getenv("CONFLUENCE_USER", "rishitha_mopuru@epam.com")
        self.confluence_token = os.getenv("CONFLUENCE_API_TOKEN", "ATATT3xFfGF01GA-Cp7fFw6AHXRvtcB3Ty0nAfnG3eCvEd5PhZLQkqFpfO6qL5FLjzyEsYlv6gN4xgznLHWVkIE8xfkwTtqmOdatJR4a47ceF9YCw_QkmYE-cMddN6zAJpUKqgdZnLDFTEItEIaln0hpeL5zIYxcHHzgM-fTDHmmGV6I-MoCCGY=3C1BFECA")

    def create_jira_story(self, project_key: str, summary: str, description: str) -> dict:
        """Creates a new User Story in your Jira project."""
        try:
            jira_client = JIRA(server=self.jira_url, basic_auth=(self.jira_user, self.jira_token))
            issue_dict = {
                'project': {'key': project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': 'Story'},
            }
            new_issue = jira_client.create_issue(fields=issue_dict)
            print(f"[Jira] Successfully created user story: {new_issue.key}")
            return {"key": new_issue.key, "summary": summary, "status": "Created"}
        except Exception as e:
            print(f"[Jira Error] Could not create story: {e}")
            return {"error": str(e)}

    def fetch_jira_story(self, issue_key: str) -> dict:
        """Fetches user story details and acceptance criteria from Jira."""
        try:
            jira_client = JIRA(server=self.jira_url, basic_auth=(self.jira_user, self.jira_token))
            issue = jira_client.issue(issue_key)
            return {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "status": issue.fields.status.name,
            }
        except Exception as e:
            print(f"[Jira Warning] Live fetch failed ({e}). Returning fallback mock story.")
            return {
                "key": issue_key,
                "summary": "Mock User Story: Agentic Documentation Sync",
                "description": "As a developer, I want automated artifact syncing.",
                "status": "In Progress",
            }

    def sync_to_confluence(self, space_key: str, title: str, html_content: str):
        """Pushes generated documentation / reports to your Confluence space.

        Uses the preferred Atlassian high-level method when available and falls back
        to the installed low-level request API shown by the workspace dependency.
        """
        try:
            confluence = Confluence(
                url=self.confluence_url,
                username=self.confluence_user,
                password=self.confluence_token,
            )

            # Preferred API shape when installed library provides it.
            if hasattr(confluence, "update_or_create"):
                confluence.update_or_create(
                    parent_id=None,
                    title=title,
                    body=html_content,
                    space=space_key,
                    type="page",
                )
                print(f"[Confluence] Successfully published page: '{title}' to space '{space_key}' at {self.confluence_url}")
                return {"status": "published", "title": title, "space": space_key}

            # Fallback for installed version that exposes generic request/REST API.
            # This avoids crashing when the underlying 'atlassian' package does not
            # implement the requested helper methods.
            response = confluence.request(
                method="POST",
                path=f"/rest/api/content",
                json={
                    "type": "page",
                    "title": title,
                    "space": {"key": space_key},
                    "body": {"storage": {"value": html_content, "representation": "storage"}},
                },
                params={"expand": "body.storage"},
            )
            if response.status_code == 200 or response.status_code == 201:
                print(f"[Confluence] Successfully published page: '{title}' to space '{space_key}' at {self.confluence_url}")
                return {"status": "published", "title": title, "space": space_key}

            print(f"[Confluence Error] Received response code {response.status_code}")
            return {"status": "error", "code": response.status_code}
        except Exception as e:
            print(f"[Confluence Error] Could not sync to Confluence: {e}")
            return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    connector = JiraConfluenceConnector()
    print("Connector initialized for user:", connector.jira_user)

