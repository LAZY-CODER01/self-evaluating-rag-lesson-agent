from src.config import MAX_RETRIES
from src.generator import generate_lesson
from src.evaluator import evaluate_lesson
from src.schemas import RejectionLog
from src.state import AgentState


def generate_node(state: AgentState) -> AgentState:
    """Generate or regenerate the lesson."""

    lesson = generate_lesson(
        topic=state["topic"],
        learner_profile=state["learner_profile"],
        memory=state.get("memory", []),
        previous_feedback=state.get("previous_feedback", ""),
    )

    return {
        **state,
        "lesson": lesson,
        "attempt": state.get("attempt", 0) + 1,
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
    """Prepare the state for a retry."""
    evaluation = state.get("evaluation")
    if not evaluation:
        raise ValueError("Evaluation is missing in state.")
        
    failures = [
        f"{check.name}: {check.reason}"
        for check in evaluation.checks
        if check.status == "FAIL"
    ]
    
    rejection_log = RejectionLog(
        attempt=state.get("attempt", 1),
        status="REJECTED",
        failures=failures,
    )
    
    previous_feedback = "The previous lesson was rejected due to the following failures:\n" + "\n".join(f"- {f}" for f in failures)
    
    rejection_logs = state.get("rejection_logs", [])
    rejection_logs.append(rejection_log)
    
    return {
        **state,
        "rejection_logs": rejection_logs,
        "previous_feedback": previous_feedback,
    }