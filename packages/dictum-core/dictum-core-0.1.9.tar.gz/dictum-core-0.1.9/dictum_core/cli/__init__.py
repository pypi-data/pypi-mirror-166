import shutil
from pathlib import Path
from typing import Optional

import typer
import yaml
from jinja2 import Template
from rich.console import Console
from rich.prompt import IntPrompt, Prompt

from dictum_core import Project
from dictum_core.backends.base import Backend
from dictum_core.schema.catalog import Catalog, CatalogMetric

app = typer.Typer()
console = Console()

backends = list(Backend.registry)

template_path = Path(__file__).parent / "project_template"


@app.command()
def new(
    project_dir: str = typer.Argument(None, help="Project directory"),
    project_name: str = typer.Option(None, help="Project name"),
    backend: str = typer.Option(None, help="Project backend"),
    default_profile: str = typer.Option(None, help="Default profile name"),
):
    if project_dir is None:
        project_dir = Prompt.ask("[bold blue]Project directory")
    project_dir = Path(project_dir)
    if project_dir.is_file():
        console.print("[red]Project path is a file")
        exit()
    if project_dir.is_dir() and not next(project_dir.iterdir(), None) is None:
        console.print("[red]Project directory must be empty")
        exit()
    if project_name is None:
        project_name = Prompt.ask("[bold blue]Project name", default=project_dir.name)
    if backend is None:
        backend_options = "\n".join(f"{i+1}. {name}" for i, name in enumerate(backends))
        backend_prompt = (
            f"[bold blue]Select a backend for your project:[/]\n\n{backend_options}\n"
            f"\nEnter a number [1-{len(backends)}]"
        )
        n = IntPrompt.ask(backend_prompt)
        backend = backends[n - 1]
    if default_profile is None:
        default_profile = Prompt.ask(
            "Enter a profile name for this backend", default=backend
        )

    if not project_dir.exists():
        project_dir.mkdir()

    backend_parameters = yaml.safe_dump(
        Backend.registry[backend].parameters(), sort_keys=False
    )
    template_vars = {
        "project_name": project_name,
        "backend": backend,
        "profile": default_profile,
        "backend_parameters": backend_parameters,
    }

    for path in template_path.iterdir():
        if path.name in {"__init__.py", ".gitkeep"}:
            continue
        new_path = project_dir / path.relative_to(template_path)
        if path.is_file():
            template = Template(path.read_text())
            rendered = template.render(**template_vars)
            new_path.write_text(rendered)
        elif path.is_dir():
            shutil.copytree(str(path), str(new_path))
    console.print(f"[bold green]Project {project_name} created")


@app.command()
def version():
    from dictum_core import __version__

    typer.echo(f"Dictum {__version__}")


@app.command()
def catalog(
    path: Optional[Path] = typer.Argument(default=None), output: Optional[Path] = None
):
    project = Project(path=path)
    metrics = [CatalogMetric.from_orm(m) for m in project.model.metrics.values()]
    catalog = Catalog(
        name=project.model.name, description=project.model.description, metrics=metrics
    )
    json = catalog.json()
    if output is None:
        import sys

        sys.stdout.write(json)
        return

    output.write_text(json)
