from src.memory import build_learned_rule


def test_accuracy_memory_rule():
    rule = build_learned_rule(
        failure_type="accuracy",
        reason="The lesson contained an incorrect technical claim.",
    )

    assert "technical accuracy" in rule


def test_jargon_memory_rule():
    rule = build_learned_rule(
        failure_type="jargon",
        reason="Embedding was not explained.",
    )

    assert "technical terms" in rule