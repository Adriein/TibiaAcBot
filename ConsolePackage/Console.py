import subprocess
import shlex
from ConsolePackage.CommandExecutionError import CommandExecutionError


class Console:
    @staticmethod
    def execute(command: str, text=True, check_return_code=True) -> str | None | bytes:
        args = shlex.split(command)

        process = subprocess.run(args, stdout=subprocess.PIPE, text=text)

        try:
            if check_return_code:
                process.check_returncode()

            return process.stdout
        except subprocess.CalledProcessError:
            raise CommandExecutionError(process.args, process.stderr)
