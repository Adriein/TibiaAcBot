class CommandExecutionError(Exception):
    def __init__(self, args: list[str], output: str):
        super(CommandExecutionError, self).__init__(f'Error executing {args} - {output}')
