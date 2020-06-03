
from click import echo, style


def print_message(message, error=False):

    style_message = ""

    index = 0

    for i in list(message.split("`")):

        if index % 2:
            style_message += style(i, fg="cyan")

        elif error:
            style_message += style(i, fg="red", bold=True)

        else:
            style_message += style(i, fg="green")

        index += 1

    echo(
        style_message,
        color=True
    )
