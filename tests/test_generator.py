from src.generator import format_memory
from src.schemas import MemoryEntry


def test_format_memory():
    memory = [
        MemoryEntry(
            failure_type="jargon",
            reason="Embedding was not explained.",
            learned_rule="Explain embeddings before using the term.",
            frequency=2,
        )
    ]

    result = format_memory(memory)

    assert "jargon" in result
    assert "embedding" in result.lower()
    assert "Explain embeddings" in result