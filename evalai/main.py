import click

from click import echo

from .challenges import challenge, challenges
from .set_host import host
from .set_token import token
from .submissions import submission
from .teams import teams


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """
    Welcome to the EvalAI CLI.
    """
    if ctx.invoked_subcommand is None:
        welcome_text = ("""#######                  ###      ###    #######
##      ##   ##   #####  ###     #####     ###
#####    ## ##   ##  ##  ###    ##   ##    ###
##        ###   ###  ##  #####  #######    ###
#######    #     ### ### #####  ##   ##  #######\n\n"""

                        "Welcome to the EvalAI CLI. Use evalai --help for viewing all the options\n"
                        "CHALLENGE and PHASE placeholders used throughout the CLI are"
                        " for challenge_id\nand phase_id of the challenges and phases.")
        echo(welcome_text)


main.add_command(challenges) #ignore: cover
main.add_command(challenge) #ignore: cover
main.add_command(host) #ignore: cover
main.add_command(token) #ignore: cover
main.add_command(submission) #ignore: cover
main.add_command(teams) #ignore: cover
