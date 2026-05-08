from pathlib import Path
from textwrap import indent

from stemanim.schemas import AnimationSpec
from stemanim.pattern_renderer import render_scene_pattern


def generate_manim_file(spec: AnimationSpec, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    scene_path = out_dir / "scene.py"

    pattern_code = "\n\n".join(
        render_scene_pattern(scene) for scene in spec.scenes
    )
    indented_pattern_code = indent(pattern_code, "        ")

    code = f"""
from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        opening = Text({spec.topic!r}).scale(0.8)
        self.play(Write(opening))
        self.wait(0.8)
        self.play(FadeOut(opening))

{indented_pattern_code}

        closing = Text("Done").scale(0.7)
        self.play(FadeIn(closing))
        self.wait(0.8)
        self.play(FadeOut(closing))
""".strip()

    scene_path.write_text(code, encoding="utf-8")
    return scene_path
