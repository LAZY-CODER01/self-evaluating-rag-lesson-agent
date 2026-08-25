from pathlib import Path

from src.output import save_final_outputs
from src.schemas import (
    EvaluationCheck,
    EvaluationResult,
    Lesson,
    LessonSection,
    RejectionLog,
)


def test_output_files_are_created(tmp_path, monkeypatch):
    import src.output as output

    monkeypatch.setattr(
        output,
        "OUTPUT_DIR",
        tmp_path,
    )

    lesson = Lesson(
        title="Introduction to RAG",
        introduction="RAG helps AI retrieve external knowledge.",
        sections=[
            LessonSection(title="What is RAG?", content="Retrieval-Augmented Generation"),
            LessonSection(title="How it works", content="Searches and generates."),
        ],
        examples=["A medical QA system."],
        key_takeaways=["RAG enhances accuracy."],
    )

    evaluation = EvaluationResult(
        overall_pass=True,
        checks=[
            EvaluationCheck(name="accuracy", status="PASS", reason="Accurate."),
        ],
    )

    rejection_log = RejectionLog(
        attempt=1,
        status="REJECTED",
        failures=["accuracy: False claim."],
        reasons=["False claim."],
        corrections=["Fix accuracy."],
    )

    state = {
        "topic": "Introduction to RAG",
        "attempt": 2,
        "lesson": lesson,
        "evaluation": evaluation,
        "rejection_logs": [rejection_log],
    }

    save_final_outputs(state)

    lesson_path = tmp_path / "lesson.md"
    eval_path = tmp_path / "evaluation_report.json"
    run_path = tmp_path / "run_report.md"

    assert lesson_path.exists()
    assert eval_path.exists()
    assert run_path.exists()

    run_report_content = run_path.read_text()
    assert "# Lesson Generation Report" in run_report_content
    assert "## Final Evaluation" in run_report_content
    assert "## Rejection Log" in run_report_content
    assert "### Attempt 1 — REJECTED" in run_report_content
    assert "#### Failures" in run_report_content
    assert "#### Corrections" in run_report_content
    assert "## Final Lesson" in run_report_content
    assert "### Introduction to RAG" in run_report_content