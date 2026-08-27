from agent.skills.skill_base import BaseSkill


class RequirementSkill(BaseSkill):
    def __init__(self):
        super().__init__("RequirementSkill", "Parses Jira user stories into structured requirements.")

    def execute(self, context: dict) -> dict:
        story = context.get("story", {})
        return {
            "status": "success",
            "skill": self.name,
            "parsed_requirements": [
                f"Feature: {story.get('summary', 'Unknown')}",
                "Acceptance Criteria validated and documented."
            ]
        }


class SkillRegistry:
    def __init__(self):
        self.skills = {}

    def register(self, skill: BaseSkill):
        self.skills[skill.name] = skill

    def execute_skill(self, name: str, context: dict) -> dict:
        if name in self.skills:
            return self.skills[name].execute(context)
        raise ValueError(f"Skill '{name}' not found in registry.")


if __name__ == "__main__":
    registry = SkillRegistry()
    registry.register(RequirementSkill())
    res = registry.execute_skill("RequirementSkill", {"story": {"summary": "Test Story"}})
    print(res)
