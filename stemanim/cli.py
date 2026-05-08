from pathlib import Path
import shutil
import subprocess
import sys

import typer
from rich import print

from stemanim.ai import mock_generate_spec
from stemanim.render import generate_manim_file

app = typer.Typer()


def manim_command(scene_file: Path, quality: str) -> list[str]:
    manim_exe = shutil.which("manim")
    if manim_exe is None:
        venv_manim = Path(sys.executable).with_name("manim")
        if venv_manim.exists():
            manim_exe = str(venv_manim)

    if manim_exe is None:
        raise typer.BadParameter(
            "Could not find the 'manim' executable. Activate the virtualenv or "
            "install Manim in the environment used to run this CLI."
        )

    return [manim_exe, f"-q{quality}", str(scene_file), "GeneratedScene"]


def run_manim(scene_file: Path, quality: str) -> None:
    cmd = manim_command(scene_file, quality)
    print(f"[cyan]Running:[/cyan] {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


@app.command()
def plan(notes_file: Path):
    notes = notes_file.read_text(encoding="utf-8")
    spec = mock_generate_spec(notes)
    print(spec.model_dump_json(indent=2))


@app.command()
def generate(notes_file: Path, out_dir: Path = Path("outputs/demo")):
    notes = notes_file.read_text(encoding="utf-8")
    spec = mock_generate_spec(notes)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "spec.json").write_text(spec.model_dump_json(indent=2), encoding="utf-8")

    scene_path = generate_manim_file(spec, out_dir)
    print(f"[green]Generated Manim scene:[/green] {scene_path}")


@app.command()
def render(scene_file: Path, quality: str = "l"):
    run_manim(scene_file, quality)


@app.command()
def all(notes_file: Path, out_dir: Path = Path("outputs/demo"), quality: str = "l"):
    notes = notes_file.read_text(encoding="utf-8")
    spec = mock_generate_spec(notes)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "spec.json").write_text(spec.model_dump_json(indent=2), encoding="utf-8")

    scene_path = generate_manim_file(spec, out_dir)

    run_manim(scene_path, quality)


@app.command()
def from_spec(spec_file: Path, out_dir: Path = Path("outputs/from_spec"), quality: str = "l"):
    from stemanim.schemas import AnimationSpec

    data = spec_file.read_text(encoding="utf-8")
    spec = AnimationSpec.model_validate_json(data)

    scene_path = generate_manim_file(spec, out_dir)

    run_manim(scene_path, quality)


if __name__ == "__main__":
    app()
