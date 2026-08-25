from src.rubric import RUBRIC, get_rubric_text


def test_rubric_has_required_checks():
    expected_ids = {
        "accuracy",
        "beginner_friendly",
        "jargon",
        "rag_fundamentals",
        "why_rag",
        "example",
        "coherence",
        "standalone",
    }

    actual_ids = {criterion["id"] for criterion in RUBRIC}

    assert actual_ids == expected_ids


def test_rubric_text_contains_all_checks():
    rubric_text = get_rubric_text()

    for criterion in RUBRIC:
        assert criterion["name"] in rubric_text
        assert criterion["id"] in rubric_text