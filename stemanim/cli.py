from pathlib import Path
import json
import subprocess

import typer
from rich import print

from stemanim.ai import mock_generate_spec
from stemanim.render import generate_manim_file

app = typer.Typer()


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
    cmd = ["manim", f"-q{quality}", str(scene_file), "GeneratedScene"]
    print(f"[cyan]Running:[/cyan] {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


@app.command()
def all(notes_file: Path, out_dir: Path = Path("outputs/demo"), quality: str = "l"):
    notes = notes_file.read_text(encoding="utf-8")
    spec = mock_generate_spec(notes)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "spec.json").write_text(spec.model_dump_json(indent=2), encoding="utf-8")

    scene_path = generate_manim_file(spec, out_dir)

    cmd = ["manim", f"-q{quality}", str(scene_path), "GeneratedScene"]
    print(f"[cyan]Running:[/cyan] {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    app()