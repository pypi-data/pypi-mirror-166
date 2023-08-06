import re
from unittest import TestCase
from unittest.mock import MagicMock, create_autospec

from cloudshell.cli.service.cli import CLI
from cloudshell.cli.service.session_pool_manager import SessionPoolManager
from cloudshell.shell.core.driver_context import (
    ResourceCommandContext,
    ResourceContextDetails,
)
from cloudshell.shell.standards.networking.resource_config import (
    NetworkingResourceConfig,
)

from cloudshell.networking.arista.cli.arista_cli_configurator import (
    AristaCLIConfigurator,
)

DEFAULT_PROMPT = "Arista>"
ENABLE_PROMPT = "Arista#"
CONFIG_PROMPT = "Arista(config)#"
VRF_PROMPT = "Arista(vrf:{vrf_name})#"

ENABLE_PASSWORD = "enable_password"


class Command:
    def __init__(self, request, response, regexp=False):
        self.request = request
        self.response = response
        self.regexp = regexp

    def is_equal_to_request(self, request):
        return (
            not self.regexp
            and self.request == request
            or self.regexp
            and re.search(self.request, request)
        )

    def __repr__(self):
        return "Command({!r}, {!r}, {!r})".format(
            self.request, self.response, self.regexp
        )


class CliEmulator:
    def __init__(self, commands=None):
        self.request = None

        self.commands = [
            Command(None, DEFAULT_PROMPT),
            Command("", DEFAULT_PROMPT),
            Command("enable", "Password:"),
            Command(ENABLE_PASSWORD, ENABLE_PROMPT),
            Command("terminal length 0", ENABLE_PROMPT),
            Command("terminal width 300", ENABLE_PROMPT),
            Command("terminal no exec prompt timestamp", ENABLE_PROMPT),
            Command("configure terminal", CONFIG_PROMPT),
            Command("no logging console", CONFIG_PROMPT),
            Command("end", ENABLE_PROMPT),
            Command("", ENABLE_PROMPT),
        ]

        if commands:
            self.commands.extend(commands)

        self.unexpected_requests = []

    def _get_response(self):
        try:
            command = self.commands.pop(0)
        except IndexError:
            self.unexpected_requests.append(self.request)
            raise IndexError(f'Not expected requests - "{self.unexpected_requests}"')

        if not command.is_equal_to_request(self.request):
            self.unexpected_requests.append(self.request)
            raise KeyError(
                'Unexpected request - "{}"\n'
                'Expected - "{}"'.format(self.unexpected_requests, command.request)
            )

        if isinstance(command.response, Exception):
            raise command.response
        else:
            return command.response

    def receive_all(self, timeout, logger):
        return self._get_response()

    def send_line(self, command, logger):
        self.request = command

    def check_calls(self):
        if self.commands:
            commands = "\n".join(
                f"\t\t- {command.request}" for command in self.commands
            )
            raise ValueError(f"Not executed commands: \n{commands}")


class BaseAristaTestCase(TestCase):
    SUPPORTED_OS = ["EOS"]
    SHELL_NAME = "AristaEosRouterShell2G"

    def create_context(self, attrs=None):
        context = create_autospec(ResourceCommandContext)
        context.resource = create_autospec(ResourceContextDetails)
        context.resource.name = "Arista"
        context.resource.fullname = "Arista"
        context.resource.family = "CS_Router"
        context.resource.address = "10.0.1.1"
        context.resource.attributes = {}
        context.resource.id = "test_id"

        attributes = {
            "User": "admin",
            "Password": "password",
            "Enable Password": ENABLE_PASSWORD,
            "host": "10.0.1.1",
            "CLI Connection Type": "ssh",
            "Sessions Concurrency Limit": "1",
        }
        attributes.update(attrs or {})

        for key, val in attributes.items():
            context.resource.attributes[f"{self.SHELL_NAME}.{key}"] = val

        return context

    def _setUp(self, attrs=None):
        if attrs is None:
            attrs = {}
        self.logger = MagicMock()
        self.api = MagicMock(DecryptPassword=lambda password: MagicMock(Value=password))

        self.resource_config = NetworkingResourceConfig.from_context(
            self.SHELL_NAME,
            self.create_context(attrs),
            self.api,
            self.SUPPORTED_OS,
        )
        self._cli = CLI(
            SessionPoolManager(
                max_pool_size=int(self.resource_config.sessions_concurrency_limit)
            )
        )

        self.cli_configurator = AristaCLIConfigurator(
            self.resource_config, self.api, self.logger, self._cli
        )

    def tearDown(self):
        self._cli._session_pool._session_manager._existing_sessions = []

        while not self._cli._session_pool._pool.empty():
            self._cli._session_pool._pool.get()
