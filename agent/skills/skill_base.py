class BaseSkill:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, context: dict) -> dict:
        raise NotImplementedError("Each skill must implement the execute method.")