import subprocess
import shlex
from ConsolePackage.CommandExecutionError import CommandExecutionError


class Console:
    @staticmethod
    def execute(command: str, check_return_code=True) -> str | None:
        args = shlex.split(command)

        process = subprocess.run(args, stdout=subprocess.PIPE, text=True)

        try:
            if check_return_code:
                process.check_returncode()

            return process.stdout
        except subprocess.CalledProcessError:
            raise CommandExecutionError(process.args, process.stderr)
