from functools import partial
from typing import Iterable
from pathlib import Path

from xonsh.built_ins import XSH
from xonsh.completers.tools import contextual_command_completer_for
from xonsh.parsers.completion_context import CommandContext

__version__ = '0.1.4'


def helper_completer(paths: Iterable[str], context: CommandContext):
    from xonsh import platform  # noqa
    from xonsh import tools  # noqa
    from xonsh.built_ins import XSH  # noqa
    from xonsh.completers.bash_completion import bash_completions  # noqa
    from xonsh.completers.tools import RichCompletion  # noqa

    env = XSH.env.detype()
    command = platform.bash_command()
    args = [arg.value for arg in context.args]
    prefix = context.prefix
    args.insert(context.arg_index, prefix)
    line = " ".join(args)

    # lengths of all args + joining spaces
    begidx = sum(len(a) for a in args[: context.arg_index]) + context.arg_index
    endidx = begidx + len(prefix)

    opening_quote = context.opening_quote
    closing_quote = context.closing_quote
    if closing_quote and not context.is_after_closing_quote:
        # there already are closing quotes after our cursor, don't complete
        # new ones (i.e. `ls "/pro<TAB>"`)
        closing_quote = ""
    elif opening_quote and not closing_quote:
        # get the proper closing quote
        closing_quote = tools.RE_STRING_START.sub("", opening_quote)

    comps, lprefix = bash_completions(
        prefix,
        line,
        begidx,
        endidx,
        env=env,
        paths=paths,
        command=command,
        line_args=args,
        opening_quote=opening_quote,
        closing_quote=closing_quote,
        arg_index=context.arg_index,
    )

    def enrich_comps(comp: str):
        append_space = False
        if comp.endswith(" "):
            append_space = True
            comp = comp.rstrip()

        # ``bash_completions`` may have added closing quotes:
        return RichCompletion(
            comp, append_closing_quote=False, append_space=append_space
        )

    comps = set(map(enrich_comps, comps))

    if lprefix == len(prefix):
        lprefix += len(context.opening_quote)
    if context.is_after_closing_quote:
        # since bash doesn't see the closing quote, we need to add its
        # length to lprefix
        lprefix += len(context.closing_quote)

    return comps, lprefix


def add_completers(diretory: str):
    for path in Path(diretory).glob('*'):
        name = path.name
        _completer = contextual_command_completer_for(name)(
            partial(helper_completer, [path.as_posix()])
        )

        completer add f'{name}' _completer


[add_completers(_dir) for _dir in XSH.env.get('BASH_COMPLETIONS_DIRS', [])]


# CLEAN
# ============================================================================

# Imports buit-ins
# ----------------------------------------------------------------------------
del partial
del Iterable
del Path

# Imports third-party
# ----------------------------------------------------------------------------
del XSH
del contextual_command_completer_for
del CommandContext

# Variables and functions
# ----------------------------------------------------------------------------
del helper_completer
del add_completers
