from agent.core.agent import Agent, AgentInput


def test_agent_run_returns_response_envelope():
    agent = Agent(name="test-agent")
    output = agent.run(AgentInput(prompt="Hello"))
    assert output["agent"] == "test-agent"
    assert output["input"] == "Hello"
    assert "response" in output
