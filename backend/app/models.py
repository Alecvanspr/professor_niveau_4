from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Framework(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    version: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    skills: list["Skill"] = Relationship(back_populates="framework")


class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    framework_id: int = Field(foreign_key="framework.id")
    name: str
    description: str

    framework: Optional[Framework] = Relationship(back_populates="skills")
    levels: list["SkillLevel"] = Relationship(back_populates="skill")


class SkillLevel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    skill_id: int = Field(foreign_key="skill.id")
    level_index: int
    title: str
    descriptor: str

    skill: Optional[Skill] = Relationship(back_populates="levels")


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class AssessmentResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(foreign_key="document.id")
    framework_id: int = Field(foreign_key="framework.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    model_name: str = "hybrid-rubric-v1"


class SkillAssessment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    assessment_id: int = Field(foreign_key="assessmentresult.id")
    skill_id: int = Field(foreign_key="skill.id")
    current_level: int
    rationale: str
    next_level_guidance: str
    gaps: str
    evidence: str
    improvement_actions: str
