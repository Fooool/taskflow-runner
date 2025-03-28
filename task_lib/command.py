import subprocess


def run(command, set_var=None, **kwargs):
    """Execute a shell command"""
    console_log = subprocess.run(command, shell=True, check=True)
    print(f"Executed: {command}")

    if set_var:
        return {set_var: console_log.stdout.decode("utf-8").strip()}

    return True
