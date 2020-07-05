import click
import os
import requests
import tempfile
import zipfile

from click import echo, style

from evalai.utils.config import STARTERS_ZIP_URL


@click.group(invoke_without_command=True)
def download_starters():
    """
    Download the EvalAI-Starters kit.
    """
    extract_path = click.prompt("Enter directory to store EvalAI-Starters in", type=str, hide_input=False)
    download_path = tempfile.mkstemp()[1]

    try:
        response = requests.get(STARTERS_ZIP_URL, stream=True)
    except Exception as e:
        echo(
            style(
                "Failed to fetch file from {}, error {}".format(STARTERS_ZIP_URL, e),
                bold=True,
                fg="red"
            )
        )

    if response and response.status_code == 200:
        with open(download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        with zipfile.ZipFile(download_path, "r") as z:
            z.extractall(extract_path)

        try:
            os.remove(download_path)
        except Exception as e:
            echo(
                style(
                    "Failed to remove zip file {}, error {}".format(download_path, e),
                    bold=True,
                    fg="red"
                )
            )
        else:
            echo(
                style(
                    "Successfully downloaded EvalAI-Starters and saved in {}".format(extract_path),
                    bold=True,
                    fg="green"
                )
            )
    else:
        echo(
            style(
                "Failed in connecting to the GitHub repository.",
                bold=True,
                fg="green"
            )
        )
