RUBRIC = [
    {
        "id": "accuracy",
        "name": "Technical Accuracy",
        "description": (
            "All important technical claims about RAG must be correct. "
            "The lesson must not contain misleading or false statements."
        ),
        "pass_condition": (
            "No significant technical inaccuracies are present."
        ),
    },
    {
        "id": "beginner_friendly",
        "name": "Beginner Friendly",
        "description": (
            "The lesson must be understandable to a learner who has "
            "completed 12th grade and has no prior AI knowledge."
        ),
        "pass_condition": (
            "The language is simple, direct, and does not assume prior "
            "AI or machine-learning knowledge."
        ),
    },
    {
        "id": "jargon",
        "name": "Jargon Handling",
        "description": (
            "Technical terms must be explained in simple language "
            "before or when they are first used."
        ),
        "pass_condition": (
            "Important technical terms are explained clearly before "
            "being used as if already known."
        ),
    },
    {
        "id": "rag_fundamentals",
        "name": "RAG Fundamentals",
        "description": (
            "The lesson must explain what RAG is and the basic flow "
            "of retrieval, augmentation, and generation."
        ),
        "pass_condition": (
            "The learner can explain the basic RAG pipeline after "
            "reading the lesson."
        ),
    },
    {
        "id": "why_rag",
        "name": "Why RAG Matters",
        "description": (
            "The lesson must explain why RAG is useful and what "
            "problem it helps solve."
        ),
        "pass_condition": (
            "The lesson gives a clear reason for using RAG instead "
            "of relying only on the model's existing knowledge."
        ),
    },
    {
        "id": "example",
        "name": "Concrete Example",
        "description": (
            "The lesson must teach the concept using at least one "
            "clear real-world or practical example."
        ),
        "pass_condition": (
            "At least one example shows how RAG works step by step."
        ),
    },
    {
        "id": "coherence",
        "name": "Teaching Flow",
        "description": (
            "The lesson should teach the topic in a logical order "
            "from simple concepts to more detailed concepts."
        ),
        "pass_condition": (
            "The lesson has a clear progression and does not jump "
            "randomly between concepts."
        ),
    },
    {
        "id": "standalone",
        "name": "Standalone Completeness",
        "description": (
            "The learner should be able to understand the basic "
            "concept without needing another resource."
        ),
        "pass_condition": (
            "The lesson provides enough context and explanation "
            "to understand introductory RAG concepts independently."
        ),
    },
]

def get_rubric_text() -> str:
    """Convert the rubric into text suitable for an LLM prompt."""

    lines = []

    for criterion in RUBRIC:
        lines.append(
            f"### {criterion['name']} ({criterion['id']})"
        )
        lines.append(
            f"Description: {criterion['description']}"
        )
        lines.append(
            f"Pass condition: {criterion['pass_condition']}"
        )
        lines.append("")

    return "\n".join(lines)