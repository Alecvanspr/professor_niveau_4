from typing import Optional

from pydantic import BaseModel


class SkillLevelCreate(BaseModel):
    level_index: int
    title: str
    descriptor: str


class SkillCreate(BaseModel):
    name: str
    description: str
    levels: list[SkillLevelCreate]


class FrameworkCreate(BaseModel):
    name: str
    version: str
    description: str
    skills: list[SkillCreate]


class FrameworkRead(BaseModel):
    id: int
    name: str
    version: str
    description: str


class DocumentRead(BaseModel):
    id: int
    filename: str
    content: str


class AnalyzeRequest(BaseModel):
    document_id: int
    framework_id: int


class SkillAssessmentRead(BaseModel):
    skill_name: str
    current_level: int
    rationale: str
    evidence: str
    gaps: str
    next_level_guidance: str
    improvement_actions: str


class AssessmentRead(BaseModel):
    id: int
    document_id: int
    framework_id: int
    model_name: str
    skills: list[SkillAssessmentRead]


class Message(BaseModel):
    message: str
    id: Optional[int] = None
