import os
import pytest
from playwright.sync_api import sync_playwright
from agent.skills.skill_registry import SkillRegistry, RequirementSkill


def test_requirement_skill_execution():
    """Verify skill execution returns expected structured output."""
    registry = SkillRegistry()
    registry.register(RequirementSkill())

    context = {"story": {"summary": "Capstone Workflow Test"}}
    result = registry.execute_skill("RequirementSkill", context)

    assert result["status"] == "success"
    assert len(result["parsed_requirements"]) > 0


def test_playwright_workflow_simulation():
    """Simulate checking a documentation portal using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://github.com")
        assert "GitHub" in page.title()
        browser.close()
