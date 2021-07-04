#!/usr/bin/env python3

import click
import os


from click import echo, style
from evalai.utils.config import AUTH_TOKEN_DIR


@click.group(invoke_without_command=True)
def show_stdout():
    """
    Shows output data from stdout.txt file.
    """
    file_path = os.path.join(AUTH_TOKEN_DIR, "stdout.txt")
    if not os.path.exists(file_path):
        echo(
            style(
                "The stdout.txt file does not exist.",
                bold=True,
                fg="red",
            )
        )
    else:
        with open(file_path, "r") as fr:
            try:
                stdout = fr.read()
                echo(stdout)
            except (OSError, IOError) as e:
                echo(str(e))
