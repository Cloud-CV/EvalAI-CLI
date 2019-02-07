import click
import os

from click import echo, style

from evalai.utils.config import AUTH_TOKEN_PATH


@click.group(invoke_without_command=True)
@click.pass_context
def gettoken(gettoken):
    """
    Get the EvalAI token.
    """
    if not os.path.exists(AUTH_TOKEN_PATH):
        echo(style("\nThe authentication token json file doesn't exist at the required path. "
                   "Please download the file from the Profile section of the EvalAI webapp and "
                   "place it at ~/.evalai/token.json or use evalai -t <token> to add it.\n\n", bold=True))
    else:
        with open(AUTH_TOKEN_PATH, 'r') as fr:
            try:
                data = fr.read()
                echo(style("Current token: {}".format(data), bold=True))
            except (OSError, IOError) as e:
                echo(e)
