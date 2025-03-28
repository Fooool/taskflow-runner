import yaml
import importlib
import re
import argparse
import logging
import traceback
from typing import Any


# Setup logging

logger = logging.getLogger("TaskRunner")
logging.basicConfig(level=logging.INFO, format="%(message)s")


# Load Workflow

with open("tasks.yml", "r") as f:
    workflow = yaml.safe_load(f)

tasks = workflow.get("tasks", {})
variables = workflow.get("variables", {})
executed_tasks = set()



# Variable Resolution

def resolve_variables(value: Any) -> Any:
    """Resolve ${var} placeholders recursively"""
    if isinstance(value, str):
        return re.sub(r"\$\{(.*?)\}", lambda m: str(variables.get(m.group(1), m.group(0))), value)
    if isinstance(value, list):
        return [resolve_variables(v) for v in value]
    if isinstance(value, dict):
        return {k: resolve_variables(v) for k, v in value.items()}
    return value



# Load Action Module

def load_action(action_name: str):
    try:
        module = importlib.import_module(f"task_lib.{action_name}")
        return module.run
    except ModuleNotFoundError:
        logger.error(f"⚠️  Action module not found: task_lib/{action_name}.py")
    except Exception as e:
        logger.error(f"❌ Error loading module '{action_name}': {e}")
        traceback.print_exc()
    return None



# Execute a Task

def run_task(task_name: str, dry_run=False):
    if task_name in executed_tasks:
        return

    task = tasks.get(task_name)
    if not task:
        logger.error(f"❌ Task '{task_name}' not found!")
        raise ValueError(f"Task '{task_name}' not defined")

    if task.get("disabled", False):
        logger.info(f"⏭️  Skipping Task: {task_name}")
        return

    display_name = task.get("name", task_name)

    # Run dependencies first
    for dep in task.get("dependencies", []):
        run_task(dep, dry_run=dry_run)

    action_name = task.get("action")
    if not action_name:
        logger.error(f"❌ Task '{task_name}' missing required 'action' key")
        raise ValueError(f"Task '{task_name}' missing action")

    resolved_task = resolve_variables(task)
    action_func = load_action(action_name)

    kwargs = {k: v for k, v in resolved_task.items() if k not in ["action", "dependencies", "name"]}

    if dry_run:
        logger.info(f"🧪 [Dry Run] Would run: {display_name} ({task_name}) [{action_name}]")
        executed_tasks.add(task_name)
        return

    if action_func:
        try:
            logger.info(f"▶️ Running Task: {display_name} ({task_name}) [{action_name}]...")
            result = action_func(**kwargs)

            if isinstance(result, dict):
                variables.update(result)
                logger.info(f"✅ Returned variables: {result}")

            if not result:
                raise RuntimeError("Task returned failure or empty result")

            logger.info(f"✅ Completed: {display_name} ({task_name})")
            executed_tasks.add(task_name)

        except Exception as e:
            logger.error(f"❌ Exception while running task '{task_name}': {e}")
            traceback.print_exc()
            raise e



# CLI Entry Point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Task Flow Runner")
    parser.add_argument("--task", help="Run only a specific task (and its dependencies)")
    parser.add_argument("--dry-run", action="store_true", help="Only print what would run")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("\n🚀 Starting Task Execution...\n")

    try:
        if args.task:
            run_task(args.task, dry_run=args.dry_run)
        else:
            for task_name in tasks:
                run_task(task_name, dry_run=args.dry_run)

        logger.info("\n🎉 All Tasks Completed!\n")
    except Exception:
        logger.error("💥 Pipeline failed due to an error.")
        exit(1)
