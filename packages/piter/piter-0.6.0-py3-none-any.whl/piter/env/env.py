import os
import platform
import subprocess
import venv
from typing import List

from piter.config import config


class Env:
    def __init__(self, name: str) -> None:
        self.name: str = name

    @property
    def path(self):
        return os.path.join(config.env_root, self.name, "venv")

    @property
    def lockfile_path(self):
        return os.path.join(config.env_root, self.name, "requirements.txt")

    @property
    def gitignore_path(self):
        return os.path.join(config.env_root, self.name, ".gitignore")

    @property
    def executives_path(self):
        return os.path.join(
            self.path, "Scripts" if platform.system() == "Windows" else "bin"
        )

    @property
    def executives(self) -> List[str]:
        return [
            file
            for file in os.listdir(self.executives_path)
            if os.path.isfile(os.path.join(self.executives_path, file))
        ]

    def generate_lockfile(self):
        dependencies: bytes = subprocess.check_output(
            [os.path.join(self.executives_path, "python"), "-m", "pip", "freeze"]
        )
        lock_file = open(self.lockfile_path, "w")
        lock_file.write(dependencies.decode("utf-8"))
        lock_file.close()

    def generate_gitignore(self):
        gitignore_file = open(self.gitignore_path, "w")
        gitignore_file.write("venv/\n")
        gitignore_file.close()

    def remove_lockfile(self):
        try:
            os.remove(self.lockfile_path)
        except FileNotFoundError:
            pass

    def install_dependencies(self, dependencies: List[str] = None):
        if not dependencies:
            dependencies: list[str] = []

            try:
                lockfile = open(self.lockfile_path)
                dependencies = lockfile.readlines()
            except FileNotFoundError:
                dependencies = config.env[self.name].dependencies
                if config.dependencies:
                    dependencies.extend(config.dependencies)

        if dependencies and len(dependencies) > 0:
            subprocess.check_call(
                [os.path.join(self.executives_path, "python"), "-m", "pip", "install",]
                + dependencies
            )

    def create(self):
        new_venv = venv.EnvBuilder(
            system_site_packages=config.env[self.name].system_site_packages,
            clear=config.env[self.name].clear,
            symlinks=config.env[self.name].symlinks,
            upgrade=config.env[self.name].upgrade,
            with_pip=config.env[self.name].with_pip,
            prompt=config.env[self.name].prompt,
        )
        new_venv.create(self.path)
