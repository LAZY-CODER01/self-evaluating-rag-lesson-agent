from src.nodes import route_after_evaluation
from src.schemas import EvaluationCheck, EvaluationResult
from src.nodes import build_feedback



def test_bad_lesson_is_rejected():
    evaluation = EvaluationResult(
        overall_pass=False,
        checks=[
            EvaluationCheck(
                name="accuracy",
                status="FAIL",
                reason=(
                    "The lesson incorrectly claims that "
                    "RAG retrains the model for every question."
                ),
            ),
            EvaluationCheck(
                name="jargon",
                status="PASS",
                reason="Technical terms are explained.",
            ),
        ],
    )

    state = {
        "evaluation": evaluation,
        "attempt": 1,
        "max_retries": 2,
    }

    assert route_after_evaluation(state) == "retry"


def test_bad_lesson_stops_after_retry_limit():
    evaluation = EvaluationResult(
        overall_pass=False,
        checks=[
            EvaluationCheck(
                name="accuracy",
                status="FAIL",
                reason="Incorrect technical claim.",
            ),
        ],
    )

    state = {
        "evaluation": evaluation,
        "attempt": 3,
        "max_retries": 2,
    }

    assert route_after_evaluation(state) == "ship"
def test_failed_evaluation_creates_regeneration_feedback():
    evaluation = EvaluationResult(
        overall_pass=False,
        checks=[
            EvaluationCheck(
                name="accuracy",
                status="FAIL",
                reason="RAG does not retrain the model.",
            ),
            EvaluationCheck(
                name="jargon",
                status="PASS",
                reason="Terms are explained.",
            ),
        ],
    )

    feedback = build_feedback(evaluation)

    assert "previous lesson was rejected" in feedback
    assert "accuracy" in feedback
    assert "RAG does not retrain the model" in feedback


def test_complete_demo_workflow(tmp_path, monkeypatch):
    import src.memory as memory_mod
    from src.schemas import Lesson, LessonSection
    from src.workflow import build_workflow

    monkeypatch.setattr(memory_mod, "MEMORY_FILE", tmp_path / "memory.json")
    monkeypatch.setattr("src.generator.DEMO_MODE", True)

    def fake_generate_lesson(topic, learner_profile, memory=None, previous_feedback="", attempt=1):
        lesson = Lesson(
            title="Introduction to RAG",
            introduction="RAG retrieves external information to answer questions.",
            sections=[
                LessonSection(title="What is RAG?", content="Retrieval-Augmented Generation"),
                LessonSection(title="How it works", content="It finds documents and answers."),
            ],
            examples=["A support chatbot that searches company manuals."],
            key_takeaways=["RAG does not retrain the base model."],
        )
        if attempt == 1:
            from src.generator import inject_demo_error
            lesson = inject_demo_error(lesson)
        return lesson

    def fake_evaluate_lesson(lesson):
        if "retrains the AI model" in lesson.introduction:
            return EvaluationResult(
                overall_pass=False,
                checks=[
                    EvaluationCheck(
                        name="accuracy",
                        status="FAIL",
                        reason="The lesson incorrectly claims RAG retrains the model.",
                    ),
                ],
            )
        return EvaluationResult(
            overall_pass=True,
            checks=[
                EvaluationCheck(
                    name="accuracy",
                    status="PASS",
                    reason="Accurate claims.",
                ),
            ],
        )

    monkeypatch.setattr("src.nodes.generate_lesson", fake_generate_lesson)
    monkeypatch.setattr("src.nodes.evaluate_lesson", fake_evaluate_lesson)

    workflow = build_workflow()
    initial_state = {
        "topic": "Introduction to RAG",
        "learner_profile": "Beginner",
        "attempt": 0,
        "max_retries": 2,
        "previous_feedback": "",
        "rejection_logs": [],
        "memory": [],
    }

    final_state = workflow.invoke(initial_state)

    # Attempt 1 rejected, attempt 2 passed
    assert final_state["attempt"] == 2
    assert final_state["evaluation"].overall_pass is True
    assert len(final_state["rejection_logs"]) == 1
    assert final_state["rejection_logs"][0].attempt == 1

    # Final lesson does NOT contain the deliberate false claim
    final_intro = final_state["lesson"].introduction
    assert "RAG retrains the AI model" not in final_intro