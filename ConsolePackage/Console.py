import subprocess
import shlex
from ConsolePackage.CommandExecutionError import CommandExecutionError


class Console:
    @staticmethod
    def execute(command: str) -> str | None:
        args = shlex.split(command)

        process = subprocess.run(args, stdout=subprocess.PIPE, text=True)

        try:
            process.check_returncode()
            return process.stdout
        except subprocess.CalledProcessError:
            raise CommandExecutionError(process.args, process.stderr)
