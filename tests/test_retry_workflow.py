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