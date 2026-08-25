from pathlib import Path

from src.output import (
    save_evaluation_report,
    save_lesson,
    save_run_report,
)


def test_output_files_are_created(tmp_path, monkeypatch):
    import src.output as output

    monkeypatch.setattr(
        output,
        "OUTPUT_DIR",
        tmp_path,
    )

    state = {
        "topic": "Introduction to RAG",
        "attempt": 1,
        "lesson": None,
        "evaluation": None,
        "rejection_logs": [],
    }

    # This test will be expanded once we add
    # proper fixture objects for Lesson and EvaluationResult.