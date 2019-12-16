# EvalAI-CLI

<b>Official Command Line utility to use EvalAI in your terminal.</b>

EvalAI-CLI is designed to extend the functionality of the EvalAI web application to command line to make the platform more accessible and terminal-friendly to its users.

------------------------------------------------------------------------------------------

[![Join the chat at https://gitter.im/Cloud-CV/EvalAI](https://badges.gitter.im/Cloud-CV/EvalAI.svg)](https://gitter.im/Cloud-CV/EvalAI?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/Cloud-CV/evalai-cli.svg?branch=master)](https://travis-ci.org/Cloud-CV/evalai-cli)
[![Coverage Status](https://coveralls.io/repos/github/Cloud-CV/evalai-cli/badge.svg?branch=master)](https://coveralls.io/github/Cloud-CV/evalai-cli?branch=master)
[![Documentation Status](https://readthedocs.org/projects/markdown-guide/badge/?version=latest)](https://evalai-cli.cloudcv.org)


## Contributing Guidelines

If you are interested in contributing to EvalAI-CLI, follow our [contribution guidelines](https://github.com/Cloud-CV/evalai-cli/blob/master/.github/CONTRIBUTING.md).

## Development Setup

1. Setup the development environment for EvalAI and make sure that it is running perfectly.

2. Clone the evalai-cli repository to your machine via git

    ```bash
    git clone https://github.com/Cloud-CV/evalai-cli.git evalai-cli
    ```

3. Create a virtual environment ([Mac users could easily use Homebrew](https://gist.github.com/apavamontri/4516816))

    - `virtualenv` installation guide: [guide](https://pythonforundergradengineers.com/virtualenv-in-osx-linux-windows.html)
    - If you're on a Mac, consider using Homebrew: [guide](https://gist.github.com/apavamontri/4516816)

    ```bash
    cd EvalAI-CLI
    virtualenv -p python3 venv
    source venv/bin/activate
    ```

4. Install the package locally

    ```bash
    pip install -e .
    ```

5. Configure your Auth Token
    1. Create an account on the production site (https://evalai.cloudcv.org/)
    2. Verify your email
    3. Go to your profile (https://evalai.cloudcv.org/web/profile)
    4. Click on `Get your Auth Token`
    5. Copy the token
    6. Set the token using the `evalai` CLI as shown below
    <br><br>
    ```bash
    evalai set_token <auth_token>
    ```

6. Login to cli using the command ``` evalai login```
Two users will be created by default which are listed below -

    ```bash
    Host User - username: host, password: password
    Participant User - username: participant, password: password
    ```
    
Or you could just login into your account just by typing `evalai` and putting in your username and your password, and there you have it.
