from src.config import DEFAULT_LEARNER_PROFILE
from src.generator import generate_lesson


def main():
    topic = "Introduction to RAG"

    print(f"\nGenerating lesson for: {topic}\n")

    lesson = generate_lesson(
        topic=topic,
        learner_profile=DEFAULT_LEARNER_PROFILE,
    )

    print("=" * 60)
    print(lesson.title)
    print("=" * 60)

    print("\nIntroduction:")
    print(lesson.introduction)

    print("\nSections:")

    for section in lesson.sections:
        print(f"\n### {section.title}")
        print(section.content)

    print("\nExamples:")

    for example in lesson.examples:
        print(f"- {example}")

    print("\nKey Takeaways:")

    for takeaway in lesson.key_takeaways:
        print(f"- {takeaway}")


if __name__ == "__main__":
    main()