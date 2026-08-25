from src.config import DEFAULT_LEARNER_PROFILE, MAX_RETRIES
from src.memory import load_memory
from src.workflow import build_workflow
from src.output import save_final_outputs


def main():
    topic = "Introduction to RAG"

    workflow = build_workflow()

    initial_state = {
        "topic": topic,
        "learner_profile": DEFAULT_LEARNER_PROFILE,
        "attempt": 0,
        "max_retries": MAX_RETRIES,
        "previous_feedback": "",
        "rejection_logs": [],
        "memory": load_memory(),
    }

    final_state = workflow.invoke(initial_state)
    save_final_outputs(final_state)

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    lesson = final_state["lesson"]
    evaluation = final_state["evaluation"]

    print(f"\nTitle: {lesson.title}")
    print(f"\nOverall evaluation: {evaluation.overall_pass}")
    print(f"Attempts: {final_state['attempt']}")

    print("\nEvaluation checks:")

    for check in evaluation.checks:
        print(
            f"- {check.name}: "
            f"{check.status} — {check.reason}"
        )

    print("\nRejection logs:")

    for log in final_state["rejection_logs"]:
        print(f"\nAttempt {log.attempt}")

        for failure in log.failures:
            print(f"- {failure}")


if __name__ == "__main__":
    main()