# taskflow-runner

> A lightweight, YAML-driven task runner for Python automation.

**`taskflow-runner`** lets you define flexible, dependency-aware task workflows using plain YAML and modular Python code. Perfect for running data transformations, CLI workflows or even lightweight devops pipelines all in a hackable setup.

---

## Features

- YAML-defined workflows with dependency resolution
- Modular Python actions via `task_lib` plug-ins
- Variable substitution: `${var}` syntax in YAML
- Dry run support (see what would execute)
- CLI filters to run specific tasks
- Minimal dependencies

---

## Installation

```bash
git clone https://github.com/Fooool/taskflow-runner.git
cd taskflow-runner
pip install -r requirements.txt
```

---

## Usage Examples

### Run an entire workflow from a YAML file

```bash
python runner.py --file my_pipeline.yml
```

This will execute all tasks defined in `my_pipeline.yml`, resolving dependencies automatically.

---

### Run a specific task only

```bash
python runner.py --file my_pipeline.yml --task prepare_data
```

This will execute the task `prepare_data` and all of its dependencies, if any.

You can also use the `--dry-run` and `--verbose` flags to inspect what would be executed and see detailed output:

```bash
python runner.py --file my_pipeline.yml --task prepare_data --dry-run --verbose
```

---
