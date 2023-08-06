from xonsh.completers.tools import contextual_command_completer_for
from xonsh.parsers.completion_context import CommandContext

__version__ = '0.1.1'


@contextual_command_completer_for('make')
def makefile_complete(command: CommandContext):
    """Autocomlete for Makefile."""
    import re
    from pathlib import Path, PosixPath

    commands = set()

    def find_makefile(path: PosixPath):
        if path.is_file() and re.search(r'([Mm]akefile|\.ma?k)$', path.name):
            with path.open() as file:
                [parse_line(line) for line in file.readlines()]

    def parse_line(line: str):
        result = re.search(r'^[a-zA-Z0-9_-]+:([^=]|$)', line)
        if result:
            cmd = re.sub(r':\s', '', result.group())
            if not command.prefix:
                commands.add(cmd)
            elif cmd.startswith(command.prefix):
                commands.add(cmd)

    [find_makefile(path) for path in Path().glob(r'*')]

    return commands


completer add 'make' makefile_complete


# CLEAN
# ============================================================================

# Imports third-party
# ----------------------------------------------------------------------------
del contextual_command_completer_for
del CommandContext

# Variables and functions
# ----------------------------------------------------------------------------
del makefile_complete
