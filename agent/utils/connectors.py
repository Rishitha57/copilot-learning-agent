import os
from typing import Any, Dict, Optional

import requests


class JiraConfluenceConnector:
    """Thin Jira + Confluence client backed by the Atlassian REST APIs."""

    def __init__(
        self,
        confluence_url: Optional[str] = None,
        username: Optional[str] = None,
        api_token: Optional[str] = None,
        jira_url: Optional[str] = None,
        jira_username: Optional[str] = None,
        jira_api_token: Optional[str] = None,
    ) -> None:
        self.confluence_url = (confluence_url or os.getenv("CONFLUENCE_URL") or "").rstrip("/")
        self.username = username or os.getenv("CONFLUENCE_USER") or ""
        self.api_token = api_token or os.getenv("CONFLUENCE_API_TOKEN") or ""

        self.jira_url = (jira_url or os.getenv("JIRA_URL") or "").rstrip("/")
        self.jira_username = jira_username or os.getenv("JIRA_USER") or ""
        self.jira_api_token = jira_api_token or os.getenv("JIRA_API_TOKEN") or ""

        self.confluence_session = requests.Session()
        if self.username and self.api_token:
            self.confluence_session.auth = (self.username, self.api_token)
        self.confluence_session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

        self.jira_session = requests.Session()
        if self.jira_username and self.jira_api_token:
            self.jira_session.auth = (self.jira_username, self.jira_api_token)
        self.jira_session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def _validate_confluence(self) -> None:
        if not self.confluence_url:
            raise ValueError("Missing CONFLUENCE_URL environment variable.")
        if not self.username:
            raise ValueError("Missing CONFLUENCE_USER environment variable.")
        if not self.api_token:
            raise ValueError("Missing CONFLUENCE_API_TOKEN environment variable.")

    def _build_url(self, base_url: str, path: str) -> str:
        normalized_base = base_url.rstrip("/")
        if not path.startswith("/"):
            path = "/" + path
        return normalized_base + path

    def _request(self, session: requests.Session, method: str, url: str, payload: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        response = session.request(method=method.upper(), url=url, json=payload, params=params, timeout=30)
        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise RuntimeError(f"HTTP {response.status_code}: {detail}")
        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError:
            return response.text

    def _get_space_id(self, space_key: str) -> str:
        url = self._build_url(self.confluence_url, "/wiki/api/v2/spaces")
        result = self._request(
            self.confluence_session,
            "GET",
            url,
            params={"keys": space_key},
        )
        if not isinstance(result, dict):
            raise RuntimeError(f"Unexpected response while resolving Confluence space {space_key!r}: {result!r}")
        results = result.get("results") or []
        if not results:
            raise ValueError(f"Confluence space {space_key!r} not found or not accessible.")
        return str(results[0]["id"])

    def _get_page_by_title(self, space_key: str, title: str) -> Optional[Dict[str, Any]]:
        url = self._build_url(self.confluence_url, "/wiki/api/v2/pages")
        result = self._request(
            self.confluence_session,
            "GET",
            url,
            params={"spaceKey": space_key, "title": title, "limit": 1},
        )
        if not isinstance(result, dict):
            return None
        results = result.get("results") or []
        return results[0] if results else None

    def sync_to_confluence(self, space_key: str, title: str, html_content: str) -> Dict[str, Any]:
        """Create or update a Confluence page containing the provided HTML."""
        self._validate_confluence()
        space_key = space_key or os.getenv("CONFLUENCE_SPACE_KEY", "GithubCopi")

        space_id = self._get_space_id(space_key)
        existing = self._get_page_by_title(space_key, title)

        payload = {
            "spaceId": space_id,
            "status": "current",
            "title": title,
            "body": {
                "representation": "storage",
                "value": html_content,
            },
        }

        if existing:
            page_id = existing["id"]
            current_version = int((existing.get("version") or {}).get("number", 1))
            
            payload["id"] = page_id
            payload["version"] = {"number": current_version + 1}
            
            if "spaceId" in payload:
                del payload["spaceId"]
            
            self._request(
                self.confluence_session,
                "PUT",
                self._build_url(self.confluence_url, f"/wiki/api/v2/pages/{page_id}"),
                payload=payload,
            )
            return {"id": page_id, "action": "updated", "space_key": space_key}

        response = self._request(
            self.confluence_session,
            "POST",
            self._build_url(self.confluence_url, "/wiki/api/v2/pages"),
            payload=payload,
        )
        return {"id": response.get("id"), "action": "created", "space_key": space_key}

    def create_jira_story(self, project_key: str, summary: str, description: str) -> Dict[str, Any]:
        if not self.jira_url:
            raise ValueError("Missing JIRA_URL environment variable.")
        if not self.jira_username:
            raise ValueError("Missing JIRA_USER environment variable.")
        if not self.jira_api_token:
            raise ValueError("Missing JIRA_API_TOKEN environment variable.")

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Story"},
            }
        }

        url = self._build_url(self.jira_url, "/rest/api/2/issue")
        return self._request(self.jira_session, "POST", url, payload=payload)

    def fetch_jira_story(self, issue_id: str) -> Dict[str, Any]:
        if not self.jira_url:
            raise ValueError("Missing JIRA_URL environment variable.")
        url = self._build_url(self.jira_url, f"/rest/api/2/issue/{issue_id}")
        return self._request(self.jira_session, "GET", url)
