from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field


class EquationSequencePattern(BaseModel):
    pattern: Literal["equation_sequence"]
    title: str
    equations: list[str]
    captions: list[str] = Field(default_factory=list)


class EquationTransformPattern(BaseModel):
    pattern: Literal["equation_transform"]
    title: str
    start_equation: str
    end_equation: str
    explanation: str = ""


class FunctionGraphPattern(BaseModel):
    pattern: Literal["function_graph"]
    title: str
    function_latex: str
    function_python: str
    x_min: float = -5
    x_max: float = 5
    y_min: float = -3
    y_max: float = 3
    caption: str = ""


class VectorTransformPattern(BaseModel):
    pattern: Literal["vector_transform"]
    title: str
    matrix: list[list[float]]
    vector: list[float]
    before_label: str = r"\mathbf{v}"
    after_label: str = r"A\mathbf{v}"
    equation: str = r"A\mathbf{v} = \lambda \mathbf{v}"


class DefinitionRevealPattern(BaseModel):
    pattern: Literal["definition_reveal"]
    title: str
    term: str
    definition: str
    formula: str | None = None


ScenePattern = Annotated[
    Union[
        EquationSequencePattern,
        EquationTransformPattern,
        FunctionGraphPattern,
        VectorTransformPattern,
        DefinitionRevealPattern,
    ],
    Field(discriminator="pattern"),
]


class AnimationSpec(BaseModel):
    topic: str
    target_level: str
    scenes: list[ScenePattern]