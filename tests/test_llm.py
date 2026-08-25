from src.llm import get_llm


def test_llm_can_be_created():
    llm = get_llm()

    assert llm is not None
    assert llm.model == "qwen3:14b"