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


def update_memory(
    memory: list[MemoryEntry],
    rejection_log: RejectionLog,
) -> list[MemoryEntry]:
    """
    Learn reusable rules from a rejected lesson.
    """

    updated_memory = list(memory)

    for failure in rejection_log.failures:
        failure_type, _, reason = failure.partition(":")

        failure_type = failure_type.strip()
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
    """Convert evaluator feedback into a reusable rule."""

    if failure_type == "accuracy":
        return (
            "Prioritize technical accuracy and never make "
            "unsupported claims."
        )

    if failure_type == "jargon":
        return (
            "Explain technical terms in simple language "
            "before using them."
        )

    if failure_type == "beginner_friendly":
        return (
            "Use short sentences and explain concepts "
            "from the learner's starting level."
        )

    if failure_type == "example":
        return (
            "Include a concrete example that directly "
            "shows how the concept works."
        )

    return (
        f"Avoid repeating this issue: {reason}"
    )