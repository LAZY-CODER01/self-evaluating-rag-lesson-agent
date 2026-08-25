from typing import List

from src.config import DEMO_MODE
from src.llm import get_llm
from src.prompts import (
    GENERATOR_SYSTEM_PROMPT,
    build_generator_prompt,
)
from src.schemas import Lesson, MemoryEntry


def inject_demo_error(lesson: Lesson) -> Lesson:
    """Inject a deliberate factual error for evaluator demonstration."""

    lesson.introduction = (
        lesson.introduction
        + "\n\n"
        + "Incorrect demo claim: RAG retrains the AI model "
          "every time a user asks a question."
    )

    return lesson


def format_memory(memory: List[MemoryEntry]) -> str:
    if not memory:
        return ""

    lines = []

    for entry in memory:
        lines.append(
            f"- Failure type: {entry.failure_type}\n"
            f"  Previous issue: {entry.reason}\n"
            f"  Learned rule: {entry.learned_rule}\n"
            f"  Frequency: {entry.frequency}"
        )

    return "\n".join(lines)


def generate_lesson(
    topic: str,
    learner_profile: str,
    memory: List[MemoryEntry] | None = None,
    previous_feedback: str = "",
) -> Lesson:
    """
    Generate a structured beginner lesson using the configured LLM.
    """

    memory = memory or []

    prompt = build_generator_prompt(
        topic=topic,
        learner_profile=learner_profile,
        memory_text=format_memory(memory),
        previous_feedback=previous_feedback,
    )

    llm = get_llm()

    structured_llm = llm.with_structured_output(Lesson)

    response = structured_llm.invoke(
        [
            ("system", GENERATOR_SYSTEM_PROMPT),
            ("human", prompt),
        ]
    )

    lesson = response

    # Demo-only behavior.
    # Normal runs keep DEMO_MODE=False.
    if DEMO_MODE:
        lesson = inject_demo_error(lesson)

    return lesson