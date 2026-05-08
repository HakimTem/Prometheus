from typing import Literal
from pydantic import BaseModel, Field


class EquationStep(BaseModel):
    latex: str
    narration: str


class SceneSpec(BaseModel):
    title: str
    kind: Literal["equation_sequence", "concept_intro"]
    narration: str
    equations: list[EquationStep] = Field(default_factory=list)


class AnimationSpec(BaseModel):
    topic: str
    target_level: str
    scenes: list[SceneSpec]