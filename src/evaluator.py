from src.llm import get_llm
from src.rubric import get_rubric_text
from src.schemas import (
    EvaluationCheck,
    EvaluationResult,
    Lesson,
)


EVALUATOR_SYSTEM_PROMPT = """
You are a strict quality evaluator for beginner educational content.

Your job is to evaluate a lesson against explicit pass/fail criteria.

You MUST:
- Judge every criterion independently.
- Use only PASS or FAIL.
- Give a specific reason for every decision.
- Be strict.
- Do not give partial credit.
- Do not assume information that is not present in the lesson.
- Do not rewrite the lesson.
- Do not reward a lesson merely because it sounds polished.

A criterion passes only when its pass condition is clearly satisfied.
If there is meaningful doubt, mark it FAIL.
"""


def lesson_to_text(lesson: Lesson) -> str:
    """Convert a structured lesson into readable text for evaluation."""

    sections = [
        f"# {lesson.title}",
        "",
        "## Introduction",
        lesson.introduction,
    ]

    for section in lesson.sections:
        sections.extend(
            [
                "",
                f"## {section.title}",
                section.content,
            ]
        )

    sections.extend(
        [
            "",
            "## Examples",
        ]
    )

    for example in lesson.examples:
        sections.append(f"- {example}")

    sections.extend(
        [
            "",
            "## Key Takeaways",
        ]
    )

    for takeaway in lesson.key_takeaways:
        sections.append(f"- {takeaway}")

    return "\n".join(sections)


def build_evaluator_prompt(lesson: Lesson) -> str:
    rubric = get_rubric_text()
    lesson_text = lesson_to_text(lesson)

    return f"""
Evaluate the following lesson.

RUBRIC:

{rubric}

LESSON:

{lesson_text}

Evaluation rules:

1. Evaluate every rubric criterion.
2. Return exactly one PASS or FAIL for every criterion.
3. A single failed criterion makes the overall evaluation FAIL.
4. Explain the concrete evidence behind each decision.
5. Do not infer missing explanations.
6. Do not give partial credit.
7. Be especially strict about technical accuracy.
"""


def run_deterministic_checks(lesson: Lesson) -> list[str]:
    """
    Return structural failures that can be detected without an LLM.
    """

    failures = []

    if not lesson.title.strip():
        failures.append("Lesson title is missing.")

    if not lesson.introduction.strip():
        failures.append("Lesson introduction is missing.")

    if len(lesson.sections) < 2:
        failures.append(
            "Lesson must contain at least two sections."
        )

    if not lesson.examples:
        failures.append(
            "Lesson must contain at least one example."
        )

    if not lesson.key_takeaways:
        failures.append(
            "Lesson must contain key takeaways."
        )

    return failures

def evaluate_lesson(lesson: Lesson) -> EvaluationResult:
    """Evaluate a lesson using deterministic checks and an LLM judge."""

    deterministic_failures = run_deterministic_checks(lesson)

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        EvaluationResult
    )

    prompt = build_evaluator_prompt(lesson)

    result = structured_llm.invoke(
        [
            ("system", EVALUATOR_SYSTEM_PROMPT),
            ("human", prompt),
        ]
    )

    if deterministic_failures:
        result.checks.append(
            EvaluationCheck(
                name="deterministic_structure",
                status="FAIL",
                reason="; ".join(deterministic_failures),
            )
        )

    # The workflow decision is derived from the individual checks.
    # This prevents an inconsistent LLM-generated overall_pass value.
    result.overall_pass = all(
        check.status == "PASS"
        for check in result.checks
    )

    return result