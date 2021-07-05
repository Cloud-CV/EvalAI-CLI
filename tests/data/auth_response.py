valid_login_body = """
{
    "username": "host",
    "password": "password"
}
"""

valid_login_response = """
{
    "token": "test_token"
}
"""

invalid_login_body = """
{
    "username": "notahost",
    "password": "notapassword"
}
"""

invalid_login_response = """
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
"""

get_access_token_response = """
{
    "token": "test_access_token"
}
"""

get_access_token_headers = """
{
    "Authorization": "Token test_token"
}
"""
