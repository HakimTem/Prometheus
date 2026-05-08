from stemanim.schemas import AnimationSpec


def mock_generate_spec(notes: str) -> AnimationSpec:
    return AnimationSpec(
        topic="Eigenvectors",
        target_level="first-year linear algebra",
        scenes=[
            {
                "pattern": "definition_reveal",
                "title": "Eigenvectors",
                "term": "Eigenvector",
                "definition": (
                    "An eigenvector is a nonzero vector whose direction is "
                    "preserved by a linear transformation."
                ),
                "formula": r"A\mathbf{v} = \lambda \mathbf{v}",
            },
            {
                "pattern": "equation_sequence",
                "title": "The eigenvalue equation",
                "equations": [
                    r"A\mathbf{v} = \lambda \mathbf{v}",
                    r"A\mathbf{v} \text{ is parallel to } \mathbf{v}",
                ],
                "captions": [
                    "The matrix A transforms v into a scalar multiple of itself.",
                    "So the direction is unchanged.",
                ],
            },
        ],
    )
