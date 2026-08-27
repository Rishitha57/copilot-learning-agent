from agent.utils.connectors import JiraConfluenceConnector


class DummyResponse:
    status_code = 200
    text = '{"id": "1"}'

    def json(self):
        return {"id": "1"}


class DummyConfluence:
    def __init__(self, url=None, username=None, password=None):
        self.url = url
        self.username = username
        self.password = password

    def request(self, method, path, json=None, data=None, **kwargs):
        self.last_request = {
            "method": method,
            "path": path,
            "json": json,
        }
        return DummyResponse()


def test_sync_to_confluence_falls_back_to_request_api(monkeypatch):
    import agent.utils.connectors as connector_module

    monkeypatch.setattr(connector_module, "Confluence", DummyConfluence)
    connector = JiraConfluenceConnector()

    result = connector.sync_to_confluence("DS", "Title", "<p>Body</p>")

    assert result is not None
    assert result["status"] == "published"
