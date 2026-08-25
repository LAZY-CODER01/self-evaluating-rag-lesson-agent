from src.evaluator import run_deterministic_checks
from src.schemas import Lesson


def test_empty_lesson_fails_structure():
    lesson = Lesson(
        title="",
        introduction="",
        sections=[],
        examples=[],
        key_takeaways=[],
    )

    failures = run_deterministic_checks(lesson)

    assert len(failures) == 5


def test_valid_structure_passes():
    lesson = Lesson(
        title="Introduction to RAG",
        introduction="RAG helps an AI use outside information.",
        sections=[
            {
                "title": "What is RAG?",
                "content": "RAG retrieves useful information before generating an answer.",
            },
            {
                "title": "Why use RAG?",
                "content": "It can help an AI answer using relevant external information.",
            },
        ],
        examples=[
            "A company can use RAG to answer questions from its internal documents."
        ],
        key_takeaways=[
            "RAG retrieves information.",
            "The retrieved information helps the model answer."
        ],
    )

    failures = run_deterministic_checks(lesson)

    assert failures == []