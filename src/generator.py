from typing import List

from src.llm import get_llm
from src.prompts import (
    GENERATOR_SYSTEM_PROMPT,
    build_generator_prompt,
)
from src.schemas import Lesson, MemoryEntry


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

    return response