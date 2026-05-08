from stemanim.schemas import (
    EquationSequencePattern,
    EquationTransformPattern,
    FunctionGraphPattern,
    VectorTransformPattern,
    DefinitionRevealPattern,
    ScenePattern,
)


def py_string(s: str) -> str:
    return repr(s)


def render_scene_pattern(scene: ScenePattern) -> str:
    if isinstance(scene, EquationSequencePattern):
        return render_equation_sequence(scene)

    if isinstance(scene, EquationTransformPattern):
        return render_equation_transform(scene)

    if isinstance(scene, FunctionGraphPattern):
        return render_function_graph(scene)

    if isinstance(scene, VectorTransformPattern):
        return render_vector_transform(scene)

    if isinstance(scene, DefinitionRevealPattern):
        return render_definition_reveal(scene)

    raise TypeError(f"Unknown scene pattern: {type(scene)}")


def render_equation_sequence(scene: EquationSequencePattern) -> str:
    lines = []
    lines.append(f'title = Text({py_string(scene.title)}).scale(0.65).to_edge(UP)')
    lines.append("self.play(Write(title))")
    lines.append("self.wait(0.5)")

    for i, eq in enumerate(scene.equations):
        caption = scene.captions[i] if i < len(scene.captions) else ""

        lines.append(f'eq_obj = MathTex({py_string(eq)}).scale(1.1)')
        lines.append("self.play(Write(eq_obj))")
        if caption:
            lines.append(f'caption = Text({py_string(caption)}).scale(0.42).next_to(eq_obj, DOWN)')
            lines.append("self.play(FadeIn(caption))")
            lines.append("self.wait(1.5)")
            lines.append("self.play(FadeOut(caption), FadeOut(eq_obj))")
        else:
            lines.append("self.wait(1.5)")
            lines.append("self.play(FadeOut(eq_obj))")

    lines.append("self.play(FadeOut(title))")
    return "\n".join(lines)


def render_equation_transform(scene: EquationTransformPattern) -> str:
    return f"""
title = Text({py_string(scene.title)}).scale(0.65).to_edge(UP)
self.play(Write(title))

eq1 = MathTex({py_string(scene.start_equation)}).scale(1.1)
eq2 = MathTex({py_string(scene.end_equation)}).scale(1.1)

self.play(Write(eq1))
self.wait(1)
self.play(TransformMatchingTex(eq1, eq2))
self.wait(1)

caption = Text({py_string(scene.explanation)}).scale(0.42).next_to(eq2, DOWN)
self.play(FadeIn(caption))
self.wait(1.5)

self.play(FadeOut(title), FadeOut(eq2), FadeOut(caption))
""".strip()


def render_function_graph(scene: FunctionGraphPattern) -> str:
    return f"""
title = Text({py_string(scene.title)}).scale(0.65).to_edge(UP)
self.play(Write(title))

axes = Axes(
    x_range=[{scene.x_min}, {scene.x_max}, 1],
    y_range=[{scene.y_min}, {scene.y_max}, 1],
    axis_config={{"include_numbers": True}},
).scale(0.75)

graph = axes.plot(lambda x: {scene.function_python}, x_range=[{scene.x_min}, {scene.x_max}])
label = MathTex({py_string(scene.function_latex)}).scale(0.8).to_corner(UR)

self.play(Create(axes))
self.play(Create(graph), Write(label))

caption = Text({py_string(scene.caption)}).scale(0.42).to_edge(DOWN)
self.play(FadeIn(caption))
self.wait(2)

self.play(FadeOut(title), FadeOut(axes), FadeOut(graph), FadeOut(label), FadeOut(caption))
""".strip()


def render_vector_transform(scene: VectorTransformPattern) -> str:
    m = scene.matrix
    v = scene.vector
    return f"""
title = Text({py_string(scene.title)}).scale(0.65).to_edge(UP)
self.play(Write(title))

plane = NumberPlane(
    x_range=[-4, 4, 1],
    y_range=[-3, 3, 1],
    background_line_style={{"stroke_opacity": 0.35}},
)
self.play(Create(plane))

v = np.array([{v[0]}, {v[1]}, 0.0])
matrix = np.array([[{m[0][0]}, {m[0][1]}], [{m[1][0]}, {m[1][1]}]])
Av2 = matrix @ np.array([{v[0]}, {v[1]}])
Av = np.array([Av2[0], Av2[1], 0.0])

arrow_v = Vector(v, buff=0)
label_v = MathTex({py_string(scene.before_label)}).next_to(arrow_v.get_end(), UP)

self.play(GrowArrow(arrow_v), Write(label_v))
self.wait(0.8)

arrow_Av = Vector(Av, buff=0)
label_Av = MathTex({py_string(scene.after_label)}).next_to(arrow_Av.get_end(), UP)

self.play(Transform(arrow_v, arrow_Av), Transform(label_v, label_Av))
self.wait(0.8)

equation = MathTex({py_string(scene.equation)}).scale(0.85).to_edge(DOWN)
self.play(Write(equation))
self.wait(2)

self.play(FadeOut(title), FadeOut(plane), FadeOut(arrow_v), FadeOut(label_v), FadeOut(equation))
""".strip()


def render_definition_reveal(scene: DefinitionRevealPattern) -> str:
    formula_code = ""
    if scene.formula:
        formula_code = f"""
formula = MathTex({py_string(scene.formula)}).scale(0.9).next_to(definition, DOWN)
self.play(Write(formula))
self.wait(1.5)
self.play(FadeOut(formula))
"""

    return f"""
title = Text({py_string(scene.title)}).scale(0.65).to_edge(UP)
term = Text({py_string(scene.term)}).scale(0.9)

self.play(Write(title))
self.play(Write(term))
self.wait(0.7)

definition = Text({py_string(scene.definition)}).scale(0.42)
definition.next_to(term, DOWN, buff=0.5)

self.play(FadeIn(definition))
self.wait(1.5)

{formula_code}

self.play(FadeOut(title), FadeOut(term), FadeOut(definition))
""".strip()
