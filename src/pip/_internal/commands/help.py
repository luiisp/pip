from optparse import Values
from typing import List

from pip._internal.cli.base_command import Command
from pip._internal.cli.status_codes import SUCCESS
from pip._internal.exceptions import CommandError


class HelpCommand(Command):
    """Show help for commands"""

    usage = """
      %prog <command>"""
    ignore_require_venv = True

    def run(self, options: Values, args: List[str]) -> int:
        from pip._internal.commands import (
            commands_abbreviations,
            commands_dict,
            create_command,
            get_similar_commands,
        )

        try:
            # 'pip help' with no args is handled by pip.__init__.parseopt()
            cmd_arg_is_abbreviated = args[0] in commands_abbreviations
            if (
                cmd_arg_is_abbreviated
            ):  # Retrieve full command name if using abbreviation
                cmd_name = commands_abbreviations[args[0]]

            cmd_name = args[0]  # the command we need help for
        except IndexError:
            return SUCCESS

        if cmd_name not in commands_dict:
            guess = get_similar_commands(cmd_name)

            msg = [f'unknown command "{cmd_name}"']
            if guess:
                msg.append(f'maybe you meant "{guess}"')

            raise CommandError(" - ".join(msg))

        command = create_command(cmd_name)
        command.parser.print_help()

        return SUCCESS
