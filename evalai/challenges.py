import click
from click import echo

from evalai.utils.challenges import (
                                    get_challenge_list,
                                    get_ongoing_challenge_list,
                                    get_past_challenge_list,
                                    get_future_challenge_list,
                                    get_challenge_count,
                                    get_phase_list,
                                    get_phase_details,)


@click.group(invoke_without_command=True)
@click.pass_context
def challenges(ctx):
    """
    Challenges and related options.
    """
    if ctx.invoked_subcommand is None:
        welcome_text = ("Welcome to the EvalAI CLI. Use evalai"
                        "challenges --help for viewing all the options.")
        echo(welcome_text)


@click.group(invoke_without_command=True, name='list')
@click.pass_context
@click.option('--participant', is_flag=True,
              help="Show the challenges that you've participated")
@click.option('--host', is_flag=True,
              help="Show the challenges that you've hosted")
def list_challenges(ctx, participant, host):
    """
    Used to list challenges.
    Invoked by running `evalai challenges list`
    """
    if participant:
        get_challenge_count(host, participant)
    elif host:
        get_challenge_count(host, participant)
    elif ctx.invoked_subcommand is None:
        get_challenge_list()


@click.command(name='ongoing')
def list_ongoing_challenges():
    """
    Used to list all the challenges which are active.
    Invoked by running `evalai challenges list ongoing`
    """
    get_ongoing_challenge_list()


@click.command(name='past')
def list_past_challenges():
    """
    Used to list all the past challenges.
    Invoked by running `evalai challenges list past`
    """
    get_past_challenge_list()


@click.command(name='future')
def list_future_challenges():
    """
    Used to list all the challenges which are coming up.
    Invoked by running `evalai challenges list future`
    """
    get_future_challenge_list()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-c', '--challenge-id', type=int,
              help="Challenge ID for viewing its phases.")
@click.option('-p', '--phase-id', type=int,
              help="Phase ID for showing the phase details")
def phases(ctx, challenge_id, phase_id):
    """
    Displays phase and phase related details.
    Invoked by running `evalai challenges phases`
    """
    if ctx.invoked_subcommand != "list":
        if challenge_id is None or phase_id is None:
            echo("Please pass in both parameters.")
        else:
            get_phase_details(challenge_id, phase_id)


@click.command(name='list')
@click.option('-c', '--challenge-id', type=int,
              help="Challenge ID for viewing its phases.")
def list_phases(challenge_id):
    """
    Displays phases as a list.
    Invoked by running `evalai challenges phases list`
    """

    if challenge_id is None:
        echo("Please pass in parameters.")
    else:
        challenge_id = int(challenge_id)
        get_phase_list(challenge_id)


# Command -> evalai challenges list
challenges.add_command(list_challenges)

# Command -> evalai challenges list ongoing/past/future
list_challenges.add_command(list_ongoing_challenges)
list_challenges.add_command(list_past_challenges)
list_challenges.add_command(list_future_challenges)

# Command -> evalai challenges phases
challenges.add_command(phases)

# Command -> evalai challenges phases list
phases.add_command(list_phases)
