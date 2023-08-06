import shutil
import os
import sys
import subprocess
from typing import List

import typer

from piter.env import ENVIRONMENTS
from piter.cli.utils import check_path_is_dir
import piter.cli.output as output
from piter.config import config

app = typer.Typer()


@app.command("config")
def print_config():
    typer.echo(f"{config.to_toml()}")
    for warning in config.get_warnings():
        output.warning(warning.line, warning.env, warning.script)


@app.command()
def env(
    name: str,
    install: bool = typer.Option(False, "--install", "-i"),
    remove: bool = typer.Option(False, "--remove", "-r"),
    remove_lockfile: bool = typer.Option(False, "--remove-lockfile", "-rl"),
    reinstall: bool = typer.Option(False, "--reinstall", "-ri"),
):
    environment = ENVIRONMENTS[name]

    if remove or reinstall:
        try:
            shutil.rmtree(environment.path)
        except FileNotFoundError:
            output.info(f"Environment not found", name)
        else:
            output.info(f"Environment removed", name)

    if remove_lockfile:
        environment.remove_lockfile()
        output.info(f"Lockfile removed", name)

    if install or reinstall:
        environment.create()
        output.info(f"Environment created", name)
        environment.install_dependencies()
        output.info(f"Dependencies installed", name)
        environment.generate_lockfile()
        output.info(f"Lockfile generated", name)
        environment.generate_gitignore()
        output.info(f".gitignore generated", name)


# TODO: if environment does not exists, create it and install dependencies
# TODO: run scripts from file like "./install.sh" is not working
@app.command("run")
def execute_script(
    env_and_script: str
):
    exec_status = 0

    environment_name = None
    script = None
    if ':' in env_and_script:
        environment_name = env_and_script.split(':')[0]
        script = env_and_script.split(':')[1]
    else:
        script = env_and_script

    if not environment_name:
        env_candidates: list[str] = []
        for env_name, env in config.env.items():
            if script in env.scripts.keys():
                env_candidates.append(env_name)

        if len(env_candidates) == 1:
            environment_name = env_candidates[0]
        elif len(env_candidates) == 0:
            output.error(f"No environment has script {output.script(script)}")
            return
        else:
            output.error(
                f"Multiple environments {env_candidates} have script {output.script(script)}. Please specify environment like this: piter run {env_candidates[0]}:{script}"
            )
            return

    environment = ENVIRONMENTS[environment_name]

    for script_line in config.env[environment_name].scripts[script]:
        env_execs = environment.executives
        command = []

        first_command_part = script_line.split(" ")[0]
        if first_command_part in env_execs:
            first_command_part = os.path.join(
                environment.executives_path, first_command_part
            )

        command.append(first_command_part)

        command.extend(script_line.split(" ")[1:])

        output.info(
            f"Command to execute {output.script(command)}", environment_name, script,
        )
        try:
            subprocess.check_call(command)
            output.success(
                f"Script line executed successfully: {output.script(script_line)}",
                environment_name,
                script,
            )
        except subprocess.CalledProcessError:
            output.error(
                f"Script line finished with error: {output.script(script_line)}",
                environment_name,
                script,
            )
            exec_status = 1

    sys.exit(exec_status)


@app.command("install")
def install(
    dependencies: List[str],
    environment_name: str = typer.Option("", "--environment", "-e"),
):
    environment = ENVIRONMENTS[environment_name]
    dependencies = list(dependencies)

    environment.install_dependencies(dependencies)
    output.info(f"Dependencies installed", environment_name)
    environment.generate_lockfile()
    output.info(f"Lockfile generated", environment_name)
