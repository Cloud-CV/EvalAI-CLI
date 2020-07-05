import os
import click
import json

from click import echo, style
from evalai.utils.auth import get_user_auth_token_by_login
from evalai.utils.config import AUTH_TOKEN_PATH, AUTH_TOKEN_DIR

@click.command()

@click.option('--auth')
@click.option('--host')
def main(auth,host):
    
    
    a=click.prompt("AUTHENTICATION TOKEN")
    h=click.prompt("HOST ID             ")
    token = get_user_auth_token_by_login(a, h)
    
     if os.path.exists(AUTH_TOKEN_PATH):
        with open(str(AUTH_TOKEN_PATH), "w") as TokenFile:
            try:
                json.dump(token, TokenFile)
            except (OSError, IOError) as e:
                echo(e)
    else:
        if not os.path.exists(AUTH_TOKEN_DIR):
            os.makedirs(AUTH_TOKEN_DIR)
        with open(str(AUTH_TOKEN_PATH), "w+") as TokenFile:
            try:
                json.dump(token, TokenFile)
            except (OSError, IOError) as e:
                echo(e)

    echo(style("\nLogged in successfully!", bold=True))

if __name__=='__main__':
    main()
