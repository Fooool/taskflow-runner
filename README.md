# taskflow-runner

> A lightweight, YAML-driven task runner for Python automation, ETL, and data pipelines.

**`taskflow-runner`** lets you define flexible, dependency-aware task workflows using plain YAML and modular Python code. Perfect for running data transformations, CLI workflows, or even lightweight devops pipelines — all in a container-friendly, hackable setup.

---

## Features

- YAML-defined workflows with dependency resolution
- Modular Python actions via `task_lib` plug-ins
- Variable substitution: `${var}` syntax in YAML
- Dry run support (see what would execute)
- CLI filters to run specific tasks
- Docker-friendly and portable
- Minimal dependencies

---

## Installation

```bash
git clone https://github.com/Fooool/taskflow-runner.git
cd taskflow-runner
pip install -r requirements.txt
