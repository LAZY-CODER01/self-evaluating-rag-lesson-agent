from src.nodes import route_after_evaluation
from src.schemas import EvaluationCheck, EvaluationResult


def test_passed_evaluation_ships():
    state = {
        "evaluation": EvaluationResult(
            overall_pass=True,
            checks=[
                EvaluationCheck(
                    name="accuracy",
                    status="PASS",
                    reason="Correct.",
                )
            ],
        ),
        "attempt": 1,
        "max_retries": 2,
    }

    assert route_after_evaluation(state) == "ship"


def test_failed_evaluation_retries():
    state = {
        "evaluation": EvaluationResult(
            overall_pass=False,
            checks=[
                EvaluationCheck(
                    name="accuracy",
                    status="FAIL",
                    reason="Incorrect.",
                )
            ],
        ),
        "attempt": 1,
        "max_retries": 2,
    }

    assert route_after_evaluation(state) == "retry"


def test_retry_limit_terminates():
    state = {
        "evaluation": EvaluationResult(
            overall_pass=False,
            checks=[
                EvaluationCheck(
                    name="accuracy",
                    status="FAIL",
                    reason="Incorrect.",
                )
            ],
        ),
        "attempt": 3,
        "max_retries": 2,
    }

    assert route_after_evaluation(state) == "ship"