from typing import List, Optional, TypedDict

from src.schemas import EvaluationResult, Lesson, MemoryEntry, RejectionLog


class AgentState(TypedDict, total=False):
    topic: str
    learner_profile: str
    lesson: Optional[Lesson]
    evaluation: Optional[EvaluationResult]
    attempt: int
    max_retries: int
    rejection_logs: List[RejectionLog]
    memory: List[MemoryEntry]
    previous_feedback: str
