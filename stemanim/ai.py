from stemanim.schemas import AnimationSpec


def mock_generate_spec(notes: str) -> AnimationSpec:
    return AnimationSpec(
        topic="Eigenvectors",
        target_level="first-year linear algebra",
        scenes=[
            {
                "title": "The eigenvalue equation",
                "kind": "equation_sequence",
                "narration": (
                    "An eigenvector is a nonzero vector whose direction is "
                    "preserved by a linear transformation."
                ),
                "equations": [
                    {
                        "latex": r"A\mathbf{v} = \lambda \mathbf{v}",
                        "narration": "The matrix A transforms v into a scalar multiple of itself.",
                    }
                ],
            }
        ],
    )