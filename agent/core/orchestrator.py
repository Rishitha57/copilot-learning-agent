import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional


class Orchestrator:
    """Coordinates agent execution lifecycle."""

    def __init__(self, skills: Optional[List[Any]] = None, output_dir: str = "output_artifacts"):
        self.skills = skills or []
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        return {
            "status": "ok",
            "prompt": prompt,
            "context": context,
            "skills_used": [skill.__class__.__name__ for skill in self.skills],
            "phase": "execute",
        }


class SDLCOrchestrator:
    def __init__(self, output_dir="output_artifacts"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_artifact(self, phase_name: str, content: str, extension: str = "md") -> str:
        """State Management: Automatically stores output files for each SDLC phase."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{phase_name}_{timestamp}.{extension}"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        latest_path = os.path.join(self.output_dir, f"latest_{phase_name}.{extension}")
        with open(latest_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[State Management] Saved artifact for phase '{phase_name}' at: {filepath}")
        return filepath

    def run_phase(self, phase_name: str, input_data: dict) -> str:
        print(f"\n--- Starting Phase: {phase_name.upper()} ---")

        simulated_output = f"# SDLC Report: {phase_name.upper()}\n\n"
        simulated_output += f"**Execution Timestamp:** {datetime.now().isoformat()}\n\n"
        simulated_output += f"## Processed Input Data\n```json\n{json.dumps(input_data, indent=2)}\n```\n\n"
        simulated_output += f"## Phase Results\n- Successfully analyzed requirements.\n- Generated compliance and verification checks.\n"

        artifact_path = self.save_artifact(phase_name, simulated_output)
        return artifact_path


if __name__ == "__main__":
    orchestrator = SDLCOrchestrator()
    sample_story = {"id": "PROJ-101", "title": "Automated Documentation Sync", "acceptance_criteria": ["Fetch from Jira", "Sync to Confluence"]}
    orchestrator.run_phase("requirements", sample_story)
    orchestrator.run_phase("architecture", {"design": "Microservices with Agentic workflow"})
