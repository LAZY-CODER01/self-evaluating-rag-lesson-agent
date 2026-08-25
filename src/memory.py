import json
from pathlib import Path

from src.schemas import MemoryEntry, RejectionLog


MEMORY_FILE = Path("data/memory.json")


def load_memory() -> list[MemoryEntry]:
    """Load persistent memory from disk."""

    if not MEMORY_FILE.exists():
        return []

    with MEMORY_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        MemoryEntry(**entry)
        for entry in data
    ]


def save_memory(memory: list[MemoryEntry]) -> None:
    """Persist memory to disk."""

    MEMORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with MEMORY_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            [
                entry.model_dump()
                for entry in memory
            ],
            file,
            indent=2,
            ensure_ascii=False,
        )



def normalize_failure_type(failure_type: str) -> str:
    """Normalize evaluator check names into stable categories."""

    normalized = failure_type.lower().strip()

    if "(" in normalized:
        normalized = normalized.split("(", 1)[0].strip()

    return normalized


def update_memory(
    memory: list[MemoryEntry],
    rejection_log: RejectionLog,
) -> list[MemoryEntry]:
    """
    Learn reusable rules from a rejected lesson
    and persist them for future runs.
    """

    updated_memory = list(memory)

    for failure in rejection_log.failures:
        failure_type, _, reason = failure.partition(":")

        failure_type = normalize_failure_type(failure_type)
        reason = reason.strip()

        learned_rule = build_learned_rule(
            failure_type=failure_type,
            reason=reason,
        )

        existing = next(
            (
                entry
                for entry in updated_memory
                if entry.failure_type == failure_type
                and entry.learned_rule == learned_rule
            ),
            None,
        )

        if existing:
            existing.frequency += 1
            existing.reason = reason
        else:
            updated_memory.append(
                MemoryEntry(
                    failure_type=failure_type,
                    reason=reason,
                    learned_rule=learned_rule,
                    frequency=1,
                )
            )

    save_memory(updated_memory)

    return updated_memory


def build_learned_rule(
    failure_type: str,
    reason: str,
) -> str:
    """
    Convert evaluator feedback into a reusable rule.

    The goal is to generalize a failure instead of simply
    memorizing the exact wording of one rejected lesson.
    """

    normalized = failure_type.lower().strip()

    if normalized in {
        "accuracy",
        "technical accuracy",
    }:
        return (
            "Verify technical claims carefully. "
            "Never describe RAG as retraining the model "
            "during a user query."
        )

    if normalized in {
        "jargon",
        "jargon handling",
    }:
        return (
            "Explain technical terms in simple language "
            "before using them."
        )

    if normalized in {
        "beginner_friendly",
        "beginner friendly",
    }:
        return (
            "Use short sentences and explain concepts "
            "from the learner's starting level."
        )

    if normalized in {
        "example",
        "concrete example",
    }:
        return (
            "Include a concrete example that directly "
            "shows how the concept works."
        )

    if normalized in {
        "rag_fundamentals",
        "rag fundamentals",
    }:
        return (
            "Clearly explain retrieval, augmentation, "
            "and generation as the core RAG pipeline."
        )

    if normalized in {
        "why_rag",
        "why rag",
    }:
        return (
            "Explain why RAG is useful, especially for "
            "providing external or updated information."
        )

    if normalized in {
        "coherence",
        "teaching flow",
    }:
        return (
            "Keep the lesson organized in a logical "
            "teaching sequence without conceptual jumps."
        )

    if normalized in {
        "standalone",
        "standalone completeness",
    }:
        return (
            "Make the lesson self-contained and define "
            "all required concepts within the lesson."
        )

    return (
        "Review the evaluator feedback carefully and "
        "avoid repeating the identified issue."
    )