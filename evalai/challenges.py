import click
import json

from click import style
from click.utils import echo

from evalai.utils.auth import get_host_url
from evalai.utils.common import (
    Date,
    notify_user,
    upload_file_using_presigned_url,
)
from evalai.utils.challenges import (
    create_challenge,
    display_all_challenge_list,
    display_future_challenge_list,
    display_ongoing_challenge_list,
    display_past_challenge_list,
    display_participated_or_hosted_challenges,
    display_challenge_details,
    display_challenge_phase_list,
    display_challenge_phase_detail,
    display_challenge_phase_split_list,
    display_leaderboard,
)
from evalai.utils.submissions import (
    display_my_submission_details,
    get_submission_meta_attributes,
)
from evalai.utils.teams import participate_in_a_challenge
from evalai.utils.submissions import make_submission
from evalai.utils.urls import URLS


class Challenge(object):
    """
    Stores user input ID's.
    """

    def __init__(self, challenge=None, phase=None, subcommand=None):
        self.challenge_id = challenge
        self.phase_id = phase
        self.subcommand = subcommand


class PhaseGroup(click.Group):
    """
    Fetch the submcommand data in the phase group.
    """

    def invoke(self, ctx):
        if "--json" in tuple(ctx.protected_args):
            ctx.protected_args = []
            ctx.params["json"] = True
        subcommand = tuple(ctx.protected_args)
        ctx.obj.subcommand = subcommand
        super(PhaseGroup, self).invoke(ctx)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--participant",
    is_flag=True,
    help="List the challenges that you've participated",
)
@click.option(
    "--host", is_flag=True, help="List the challenges that you've hosted"
)
def challenges(ctx, participant, host):
    """
    Lists challenges
    """
    """
    Invoked by running `evalai challenges`
    """
    if participant or host:
        display_participated_or_hosted_challenges(host, participant)
    elif ctx.invoked_subcommand is None:
        display_all_challenge_list()


@click.group(invoke_without_command=True)
@click.pass_context
@click.argument("CHALLENGE", type=int)
def challenge(ctx, challenge):
    """
    Display challenge specific details.
    """
    ctx.obj = Challenge(challenge=challenge)
    if ctx.invoked_subcommand is None:
        display_challenge_details(challenge)


@challenges.command(context_settings={"ignore_unknown_options": True})
@click.option("--file", type=click.File("rb"), required=True, help="Challenge Zip file.")
@click.argument("team", type=int)
def create(file, team):
    """
    Create challenge with Zip file & HostTeam ID.
    """
    """
    Invoked by running 'evalai challenges create --file FILE TEAM'
    """
    create_challenge(file, team)


@challenges.command()
def ongoing():
    """
    List all active challenges
    """
    """
    Invoked by running `evalai challenges ongoing`
    """
    display_ongoing_challenge_list()


@challenges.command()
def past():
    """
    List all past challenges
    """
    """
    Invoked by running `evalai challenges past`
    """
    display_past_challenge_list()


@challenges.command()
def future():
    """
    List all upcoming challenges
    """
    """
    Invoked by running `evalai challenges future`
    """
    display_future_challenge_list()


@challenge.command()
@click.pass_obj
def phases(ctx):
    """
    List all phases of a challenge
    """
    """
    Invoked by running `evalai challenges CHALLENGE phases`
    """
    display_challenge_phase_list(ctx.challenge_id)


@click.group(invoke_without_command=True, cls=PhaseGroup)
@click.pass_obj
@click.option("--json", is_flag=True, help="Get phase details in JSON format.")
@click.argument("PHASE", type=int)
def phase(ctx, json, phase):
    """
    List phase details of a phase
    """
    """
    Invoked by running `evalai challenges CHALLENGE phase PHASE`
    """
    ctx.phase_id = phase
    if len(ctx.subcommand) == 0:
        display_challenge_phase_detail(ctx.challenge_id, phase, json)


@phase.command()
@click.pass_obj
@click.option(
    "--start-date",
    "-s",
    type=Date(format="%m/%d/%y"),
    help="Start date for submissions in `mm/dd/yyyy` format.",
)
@click.option(
    "--end-date",
    "-e",
    type=Date(format="%m/%d/%y"),
    help="End date for submissions in `mm/dd/yyyy` format.",
)
def submissions(ctx, start_date, end_date):
    """
    Display submissions to a particular challenge.
    """
    """
    Invoked by running `evalai challenge CHALLENGE phase PHASE submissions`.
    """
    display_my_submission_details(
        ctx.challenge_id, ctx.phase_id, start_date, end_date
    )


@phase.command()
@click.pass_obj
def splits(ctx):
    """
    View the phase splits of a challenge.
    """
    """
    Invoked by running `evalai challenge CHALLENGE phase PHASE splits`
    """
    display_challenge_phase_split_list(ctx.challenge_id)


@challenge.command()
@click.pass_obj
@click.argument("CPS", type=int)
def leaderboard(ctx, cps):
    """
    Displays the Leaderboard to a Challenge Phase Split.
    """
    """
    Invoked by running `evalai challenge CHALLENGE leaderboard CPS`.
    """
    display_leaderboard(ctx.challenge_id, cps)


@challenge.command()
@click.pass_obj
@click.argument("TEAM", type=int)
def participate(ctx, team):
    """
    Participate in a challenge.
    """
    """
    Invoked by running `evalai challenge CHALLENGE participate TEAM`
    """
    terms_and_conditions_page_url = "{}{}".format(
        get_host_url(), URLS.terms_and_conditions_page.value
    )
    terms_and_conditions_page_url = terms_and_conditions_page_url.format(
        ctx.challenge_id
    )
    message = (
        "Please refer challenge terms and conditions here: {}"
        "\n\nBy agreeing to participate in the challenge, you are agreeing to terms and conditions."
        "\n\nDo you accept challenge terms and conditions?".format(
            terms_and_conditions_page_url
        )
    )
    if click.confirm(message):
        participate_in_a_challenge(ctx.challenge_id, team)
    else:
        message = "\nYou can't participate in the challenge without accepting terms and conditions"
        notify_user(message, color="red")


@phase.command()
@click.pass_obj
@click.option("--large", is_flag=True)
@click.option("--annotation", is_flag=True)
@click.option("--public", is_flag=True)
@click.option("--private", is_flag=True)
@click.option(
    "--file",
    type=click.File("rb"),
    required=True,
    help="File path to the submission or annotation file",
)
def submit(ctx, file, annotation, large, public, private):
    """
    For uploading submission files to evalai:
        - Invoked by running 'evalai challenge CHALLENGE phase PHASE submit --file FILE'
        - For large files, add a '--large' option at the end of the command

    For uploading test annotation files to evalai:
        - Invoked by running "evalai challenge CHALLENGE phase PHASE submit --file FILE --annotation"

    Arguments:
        ctx (class click.Context) --  The context object which holds state of the invocation
        file (str) -- the path of the file to be uploaded
        annotations (boolean) -- flag to denote if file is a test annotation file
        large (boolean) -- flag to denote if submission file is large (if large, presigned urls are used for uploads)
        public (boolean) -- flag to denote if submission is public
        private (boolean) -- flag to denote if submission is private
    Returns:
        None
    """
    if public and private:
        message = "\nError: Submission can't be public and private.\nPlease select either --public or --private"
        notify_user(message, color="red")
    else:
        if annotation:
            upload_file_using_presigned_url(ctx.phase_id, file, "annotation")
        else:
            submission_metadata = {}
            if public:
                submission_metadata["is_public"] = json.dumps(True)
            elif private:
                submission_metadata["is_public"] = json.dumps(False)
            else:
                submission_metadata["is_public"] = None
            if click.confirm("Do you want to include the Submission Details?"):
                submission_metadata["method_name"] = click.prompt(
                    style("Method Name", fg="yellow"), type=str, default=""
                )
                submission_metadata["method_description"] = click.prompt(
                    style("Method Description", fg="yellow"),
                    type=str,
                    default="",
                )
                submission_metadata["project_url"] = click.prompt(
                    style("Project URL", fg="yellow"), type=str, default=""
                )
                submission_metadata["publication_url"] = click.prompt(
                    style("Publication URL", fg="yellow"), type=str, default=""
                )
            submission_meta_attributes = get_submission_meta_attributes(
                ctx.challenge_id, ctx.phase_id
            )
            submission_attribute_metadata = []
            if (
                submission_meta_attributes
                and len(submission_meta_attributes) > 0
            ):
                if click.confirm(
                    "Do you want to include the Submission Metadata?"
                ):
                    for attribute in submission_meta_attributes:
                        attribute_type = attribute["type"]
                        attribute_name = attribute["name"]
                        attribute_description = attribute["description"]
                        attribute_required = attribute.get("required")
                        attribute_data = {
                            'name': attribute_name,
                            'type': attribute_type,
                            'description': attribute_description,
                            'required': attribute_required,
                        }
                        if attribute_required:
                            attribute_name = attribute_name + '*'
                        value = None
                        message = "{} ({})".format(
                            attribute_name, attribute_description
                        )
                        if attribute_type == "text":
                            while True:
                                value = click.prompt(
                                    style(message, fg="yellow"),
                                    type=str,
                                    default="",
                                )
                                if not attribute_required or value != "":
                                    break
                                echo(
                                    "Error: {} is a required field".format(
                                        attribute["name"]
                                    )
                                )
                            attribute_data['value'] = value
                        if attribute_type == "boolean":
                            while True:
                                value = click.prompt(
                                    style(message, fg="yellow"), type=bool, default=""
                                )
                                if not attribute_required or value != "":
                                    break
                                echo(
                                    "Error: {} is a required field".format(
                                        attribute["name"]
                                    )
                                )
                            attribute_data['value'] = value
                        if attribute_type == "radio":
                            while True:
                                value = click.prompt(
                                    style(
                                        "{}:\nChoices:{}".format(
                                            message, attribute["options"]
                                        ),
                                        fg="yellow",
                                    ),
                                    type=click.Choice(attribute["options"]),
                                    default=""
                                )
                                if not attribute_required or value != "":
                                    break
                                echo(
                                    "Error: {} is a required field".format(
                                        attribute["name"]
                                    )
                                )
                            attribute_data['options'] = attribute['options']
                            attribute_data['value'] = value
                        if attribute_type == "checkbox":
                            option_chosen = True
                            while option_chosen:
                                value = []
                                choices = click.prompt(
                                    style(
                                        "{}:\nChoices(separated by comma):{}".format(
                                            message, attribute["options"]
                                        ),
                                        fg="yellow",
                                    ),
                                    type=str,
                                    show_default=False,
                                    default=""
                                )
                                if choices != "":
                                    choices = [
                                        choice.strip(" ")
                                        for choice in choices.split(",")
                                    ]
                                else:
                                    choices = []
                                    option_chosen = False
                                if attribute_required and len(choices) == 0:
                                    echo(
                                        "Error: {} is a required field. Please select atleast one option".format(
                                            attribute["name"]
                                        )
                                    )
                                    option_chosen = True
                                for choice in choices:
                                    if choice in attribute["options"]:
                                        value.append(choice)
                                        option_chosen = False
                                    else:
                                        echo(
                                            "Error: Choose correct value(s) from the given options only"
                                        )
                                        option_chosen = True
                                        break
                            attribute_data['options'] = attribute['options']
                            attribute_data['values'] = value
                        submission_attribute_metadata.append(attribute_data)
            if large:
                upload_file_using_presigned_url(
                    ctx.phase_id, file, "submission", submission_metadata
                )
            else:
                make_submission(
                    ctx.challenge_id,
                    ctx.phase_id,
                    file,
                    submission_metadata,
                    submission_attribute_metadata,
                )


challenge.add_command(phase)
