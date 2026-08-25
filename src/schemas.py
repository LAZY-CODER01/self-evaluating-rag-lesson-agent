from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class LessonSection(BaseModel):
    title: str
    content: str


class Lesson(BaseModel):
    title: str
    introduction: str
    sections: List[LessonSection]
    examples: List[str]
    key_takeaways: List[str]


class EvaluationCheck(BaseModel):
    name: str
    status: Literal["PASS", "FAIL"]
    reason: str


class EvaluationResult(BaseModel):
    overall_pass: bool
    checks: List[EvaluationCheck]


class RejectionLog(BaseModel):
    attempt: int
    status: Literal["REJECTED", "PASSED"]
    failures: List[str] = Field(default_factory=list)
    corrections: List[str] = Field(default_factory=list)


class MemoryEntry(BaseModel):
    failure_type: str
    reason: str
    learned_rule: str
    frequency: int = 1


class WorkflowState(BaseModel):
    topic: str
    learner_profile: str

    lesson: Optional[Lesson] = None
    evaluation: Optional[EvaluationResult] = None

    attempt: int = 0
    rejection_logs: List[RejectionLog] = Field(default_factory=list)

    memory: List[MemoryEntry] = Field(default_factory=list)