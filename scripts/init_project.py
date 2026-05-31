#!/usr/bin/env python3
"""Scaffold a new project from the template."""

import argparse
import shutil
from pathlib import Path


TEMPLATE_DIR = Path(__file__).parent.parent / "projects" / "_template"
PROJECTS_DIR = Path(__file__).parent.parent / "projects"


def init_project(name: str) -> None:
    target = PROJECTS_DIR / name
    if target.exists():
        print(f"Error: project '{name}' already exists at {target}")
        return

    if not TEMPLATE_DIR.exists():
        print(f"Error: template not found at {TEMPLATE_DIR}")
        print("Creating from scratch...")
        target.mkdir(parents=True)
        (target / "config.yaml").write_text(f"# TODO: configure project '{name}'\n")
        (target / "brand-voice.md").write_text(f"# Brand Voice: {name}\n")
        (target / "content-plan.yaml").write_text("plan:\n  - topic: 'Hello world'\n")
        templates = target / "templates"
        templates.mkdir()
        (templates / "default.yaml").write_text("template: default\n")
        print(f"Created bare project at {target}")
        return

    shutil.copytree(TEMPLATE_DIR, target)
    print(f"Created project '{name}' at {target}")
    print("Next steps:")
    print(f"  1. Edit {target / 'config.yaml'}")
    print(f"  2. Edit {target / 'brand-voice.md'}")
    print(f"  3. Fill {target / 'content-plan.yaml'}")
    print(f"  4. Add secrets to .env")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new Social AI Engine project")
    parser.add_argument("--name", required=True, help="Project name (alphanumeric + underscore)")
    args = parser.parse_args()
    init_project(args.name)
