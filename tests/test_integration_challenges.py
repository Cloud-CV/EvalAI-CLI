from click.testing import CliRunner

from evalai.add_token import set_token
from evalai.challenges import challenges, challenge


class TestIntegrationChallenges:
    def setup(self):
        self.url = "{}{}"
        self.undefined_token = "0" * 40
        # valid token for test user
        self.valid_testuser_token = "3c6dcbdb50b6edc2942f4629c0c1ca51fa80d88c"
        self.set_token_to(self.valid_testuser_token)

    def set_token_to(self, token):
        runner = CliRunner()
        runner.invoke(set_token, token)

    def set_token_to_undefined(self):
        self.set_token_to(self.undefined_token)

    def test_challenges_when_token_is_invalid(self):
        self.set_token_to_undefined()
        runner = CliRunner()
        expected = "\nThe authentication token you are using isn't valid. Please generate it again.\n\n"
        result = runner.invoke(challenges)
        assert expected == result.output

    def test_challenge_details_when_challenge_id_is_not_int(self):
        runner = CliRunner()
        expected = "{}{}".format(
            "Usage: challenge [OPTIONS] CHALLENGE COMMAND [ARGS]...\n\n",
            "Error: Invalid value for \"CHALLENGE\": x is not a valid integer\n"
        )
        result = runner.invoke(challenge, "x")
        assert expected == result.output
