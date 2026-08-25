from unittest.mock import MagicMock

from src.generator import format_memory, generate_lesson
from src.schemas import Lesson, LessonSection, MemoryEntry


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


def _sample_lesson():
    return Lesson(
        title="Introduction to RAG",
        introduction="RAG helps AI retrieve facts.",
        sections=[
            LessonSection(title="What is RAG?", content="Retrieval-Augmented Generation"),
            LessonSection(title="How it works", content="It finds documents and answers."),
        ],
        examples=["A search bot."],
        key_takeaways=["RAG retrieves knowledge."],
    )


def test_demo_mode_injects_error_on_attempt_1(monkeypatch):
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = _sample_lesson()
    mock_llm.with_structured_output.return_value = mock_structured

    monkeypatch.setattr("src.generator.get_llm", lambda: mock_llm)
    monkeypatch.setattr("src.generator.DEMO_MODE", True)

    lesson = generate_lesson(
        topic="Introduction to RAG",
        learner_profile="Beginner",
        attempt=1,
    )

    assert "RAG retrains the AI model" in lesson.introduction


def test_demo_mode_does_not_inject_error_on_retry(monkeypatch):
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_structured.invoke.return_value = _sample_lesson()
    mock_llm.with_structured_output.return_value = mock_structured

    monkeypatch.setattr("src.generator.get_llm", lambda: mock_llm)
    monkeypatch.setattr("src.generator.DEMO_MODE", True)

    lesson = generate_lesson(
        topic="Introduction to RAG",
        learner_profile="Beginner",
        attempt=2,
    )

    assert "RAG retrains the AI model" not in lesson.introduction