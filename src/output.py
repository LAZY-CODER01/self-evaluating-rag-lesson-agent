import json
from pathlib import Path

from src.state import AgentState


OUTPUT_DIR = Path("outputs")


def save_final_outputs(state: AgentState) -> None:
    """Save the final lesson and evaluation artifacts."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_lesson(state)
    save_evaluation_report(state)
    save_run_report(state)


def save_lesson(state: AgentState) -> None:
    """Save the final lesson as Markdown."""

    lesson = state["lesson"]

    content = [
        f"# {lesson.title}",
        "",
        lesson.introduction,
        "",
    ]

    for section in lesson.sections:
        content.extend(
            [
                f"## {section.title}",
                "",
                section.content,
                "",
            ]
        )

    content.extend(
        [
            "## Example",
            "",
            lesson.examples[0],
            "",
            "## Key Takeaways",
            "",
        ]
    )

    for takeaway in lesson.key_takeaways:
        content.append(f"- {takeaway}")

    lesson_path = OUTPUT_DIR / "lesson.md"

    lesson_path.write_text(
        "\n".join(content),
        encoding="utf-8",
    )


def save_evaluation_report(state: AgentState) -> None:
    """Save the final evaluation in JSON format."""

    evaluation = state["evaluation"]

    report = {
        "topic": state["topic"],
        "attempts": state["attempt"],
        "overall_pass": evaluation.overall_pass,
        "checks": [
            check.model_dump()
            for check in evaluation.checks
        ],
    }

    report_path = (
        OUTPUT_DIR / "evaluation_report.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def save_run_report(state: AgentState) -> None:
    """Save a human-readable generation and rejection report."""

    lesson = state["lesson"]
    evaluation = state["evaluation"]

    lines = [
        "# Lesson Generation Report",
        "",
        f"**Topic:** {state['topic']}",
        f"**Final Status:** {'PASSED' if evaluation.overall_pass else 'REJECTED'}",
        f"**Attempts:** {state['attempt']}",
        "",
        "## Final Evaluation",
        "",
    ]

    for check in evaluation.checks:
        lines.extend(
            [
                f"### {check.name}",
                "",
                f"**Status:** {check.status}",
                "",
                f"**Reason:** {check.reason}",
                "",
            ]
        )

    lines.extend(
        [
            "## Rejection Log",
            "",
        ]
    )

    rejection_logs = state.get("rejection_logs", [])

    if not rejection_logs:
        lines.extend(
            [
                "No rejected attempts.",
                "",
            ]
        )
    else:
        for log in rejection_logs:
            lines.extend(
                [
                    f"### Attempt {log.attempt} — {log.status}",
                    "",
                    "#### Failures",
                    "",
                ]
            )

            for failure in log.failures:
                lines.append(f"- {failure}")

            if log.corrections:
                lines.extend(
                    [
                        "",
                        "#### Corrections",
                        "",
                    ]
                )
                for correction in log.corrections:
                    lines.append(f"- {correction}")

            lines.append("")

    lines.extend(
        [
            "## Final Lesson",
            "",
            f"### {lesson.title}",
            "",
            lesson.introduction,
            "",
        ]
    )

    for section in lesson.sections:
        lines.extend(
            [
                f"#### {section.title}",
                "",
                section.content,
                "",
            ]
        )

    if lesson.examples:
        lines.extend(
            [
                "#### Examples",
                "",
            ]
        )
        for example in lesson.examples:
            lines.append(f"- {example}")
        lines.append("")

    if lesson.key_takeaways:
        lines.extend(
            [
                "#### Key Takeaways",
                "",
            ]
        )
        for takeaway in lesson.key_takeaways:
            lines.append(f"- {takeaway}")
        lines.append("")

    report_path = OUTPUT_DIR / "run_report.md"

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )