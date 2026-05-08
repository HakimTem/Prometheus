from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from stemanim.schemas import AnimationSpec


def generate_manim_file(spec: AnimationSpec, out_dir: Path) -> Path:
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("basic_scene.py.j2")

    out_dir.mkdir(parents=True, exist_ok=True)
    scene_path = out_dir / "scene.py"

    code = template.render(spec=spec)
    scene_path.write_text(code, encoding="utf-8")

    return scene_path