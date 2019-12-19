import os
import click
import json

from click import echo, style
from evalai.utils.auth import get_user_auth_token_by_login, write_json_auth_token_to_file
from evalai.utils.config import AUTH_TOKEN_PATH, AUTH_TOKEN_DIR


@click.group(invoke_without_command=True)
@click.option('-p', '--password', type=str, hide_input=True, prompt=True)
@click.option('-u', '--username', type=str, hide_input=False, prompt=True)
@click.pass_context
def login(ctx, username, password):
    """
    Login to EvalAI and save token.
    """
    token = get_user_auth_token_by_login(username, password)
    write_json_auth_token_to_file(token)
    echo(style("\nLogged in successfully!", bold=True))
