from src.config import MAX_RETRIES
from src.generator import generate_lesson
from src.evaluator import evaluate_lesson
from src.memory import update_memory
from src.schemas import RejectionLog, EvaluationResult
from src.state import AgentState


def generate_node(state: AgentState) -> AgentState:
    """Generate or regenerate the lesson."""

    attempt = state.get("attempt", 0) + 1

    lesson = generate_lesson(
        topic=state["topic"],
        learner_profile=state["learner_profile"],
        memory=state.get("memory", []),
        previous_feedback=state.get("previous_feedback", ""),
        attempt=attempt,
    )

    return {
        **state,
        "lesson": lesson,
        "attempt": attempt,
        "max_retries": state.get("max_retries", MAX_RETRIES),
    }


def evaluate_node(state: AgentState) -> AgentState:
    """Evaluate the generated lesson."""
    lesson = state.get("lesson")
    if not lesson:
        raise ValueError("Lesson is missing in state.")
    
    evaluation = evaluate_lesson(lesson)
    return {
        **state,
        "evaluation": evaluation,
    }


def route_after_evaluation(state: AgentState) -> str:
    """Route to END if passed or max retries reached, else retry."""
    evaluation = state.get("evaluation")
    attempt = state.get("attempt", 0)
    max_retries = state.get("max_retries", MAX_RETRIES)
    
    if evaluation and evaluation.overall_pass:
        return "ship"
    
    if attempt >= max_retries:
        return "ship"
        
    return "retry"


def retry_node(state: AgentState) -> AgentState:
    """Prepare evaluator feedback and update persistent memory."""

    evaluation = state["evaluation"]

    rejection_log = create_rejection_log(state)

    rejection_logs = [
        *state.get("rejection_logs", []),
        rejection_log,
    ]

    current_memory = state.get("memory", [])

    updated_memory = update_memory(
        memory=current_memory,
        rejection_log=rejection_log,
    )

    return {
        **state,
        "previous_feedback": build_feedback(evaluation),
        "rejection_logs": rejection_logs,
        "memory": updated_memory,
    }


def build_feedback(evaluation: EvaluationResult) -> str:
    failures = [
        f"{check.name}: {check.reason}"
        for check in evaluation.checks
        if check.status == "FAIL"
    ]
    return "The previous lesson was rejected due to the following failures:\n" + "\n".join(f"- {f}" for f in failures)


def create_rejection_log(
    state: AgentState,
) -> RejectionLog:
    """Create a structured record for a rejected attempt."""

    evaluation = state["evaluation"]

    failed_checks = [
        check
        for check in evaluation.checks
        if check.status == "FAIL"
    ]

    failures = [
        f"{check.name}: {check.reason}"
        for check in failed_checks
    ]

    reasons = [
        check.reason
        for check in failed_checks
    ]

    corrections = [
        (
            f"Fix {check.name} based on evaluator feedback: "
            f"{check.reason}"
        )
        for check in failed_checks
    ]

    return RejectionLog(
        attempt=state["attempt"],
        status="REJECTED",
        failures=failures,
        reasons=reasons,
        corrections=corrections,
    )