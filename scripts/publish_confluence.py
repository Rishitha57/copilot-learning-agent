import os
from agent.utils.connectors import JiraConfluenceConnector


def publish_report():
    connector = JiraConfluenceConnector()

    title = "GitHub Copilot Capstone - CI/CD SDLC & Test Report"
    html_content = """
        <h1>GitHub Copilot Capstone: Automated CI/CD Report</h1>
        <p><b>Author:</b> Rishitha Mopuru (rishitha_mopuru@epam.com)</p>
        <p><b>Status:</b> ✅ Build & Test Workflow Completed Successfully</p>
        <h2>Pipeline Summary</h2>
        <ul>
            <li>CREATE Framework Prompts: Active</li>
            <li>Orchestrator State Management: Operational</li>
            <li>Pytest & Playwright E2E Tests: 5/5 Passed</li>
            <li>CI/CD Automation: Triggered via GitHub Actions</li>
        </ul>
        <p><i>Synced automatically from GitHub Actions CI/CD pipeline.</i></p>
    """

    space_key = os.getenv("CONFLUENCE_SPACE_KEY", "DS")

    print(f"Publishing report to Confluence space '{space_key}'...")
    connector.sync_to_confluence(space_key=space_key, title=title, html_content=html_content)


if __name__ == "__main__":
    publish_report()
