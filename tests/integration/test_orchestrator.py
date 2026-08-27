from agent.core.orchestrator import Orchestrator


def test_orchestrator_runs_prompt_and_context():
    orchestrator = Orchestrator()
    result = orchestrator.execute("test prompt", {"source": "unit-test"})

    assert result["status"] == "ok"
    assert result["prompt"] == "test prompt"
    assert result["context"]["source"] == "unit-test"
    assert result["phase"] == "execute"
