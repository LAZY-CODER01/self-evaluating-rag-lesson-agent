from src.rubric import get_rubric_text


GENERATOR_SYSTEM_PROMPT = """
You are an expert educational content designer.

Your job is to create a beginner lesson about the requested topic.

The learner is:
- A 12th-grade graduate from India.
- From a non-English-medium background.
- Has limited English vocabulary.
- Has no prior knowledge of AI or machine learning.

Your lesson must be:
- Simple
- Accurate
- Practical
- Self-contained
- Easy to follow
- Free from unnecessary technical jargon

Teaching principles:

1. Start from zero.
2. Explain simple ideas before technical ideas.
3. Explain every important technical term when it first appears.
4. Use short and clear sentences.
5. Teach concepts using concrete examples.
6. Do not assume the learner already knows AI terminology.
7. Never sacrifice technical accuracy for simplicity.
8. Do not make unsupported or exaggerated claims.
"""


def build_generator_prompt(
    topic: str,
    learner_profile: str,
    memory_text: str = "",
    previous_feedback: str = "",
) -> str:
    rubric = get_rubric_text()

    return f"""
Create a beginner-friendly lesson about:

TOPIC:
{topic}

LEARNER PROFILE:
{learner_profile}

The lesson must satisfy the following quality requirements:

{rubric}

PREVIOUS LEARNED LESSONS:
{memory_text or "No previous lessons are available."}

FEEDBACK FROM PREVIOUS ATTEMPT:
{previous_feedback or "This is the first attempt. There is no previous feedback."}

IMPORTANT:
If previous feedback exists, correct those specific problems.
Do not repeat the same mistakes.
Preserve parts of the previous lesson that were already good.

The lesson should teach the learner:
1. What the topic is.
2. Why it matters.
3. How it works.
4. A simple real-world example.
5. Important limitations or things to remember.
6. Key takeaways.

Return only the lesson content in the requested structured format.
"""