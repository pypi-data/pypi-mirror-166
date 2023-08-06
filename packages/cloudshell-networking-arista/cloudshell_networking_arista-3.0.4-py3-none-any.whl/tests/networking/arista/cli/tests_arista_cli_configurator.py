from unittest import TestCase
from unittest.mock import MagicMock, patch

from cloudshell.cli.service.cli import CLI
from cloudshell.cli.service.session_manager_impl import SessionManagerException
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.session.telnet_session import TelnetSession

from cloudshell.networking.arista.cli.arista_cli_configurator import (
    AristaCLIConfigurator,
)
from cloudshell.networking.arista.cli.arista_command_modes import (
    AristaConfigCommandMode,
    AristaEnableCommandMode,
)
from cloudshell.networking.arista.cli.sessions.console_ssh_session import (
    ConsoleSSHSession,
)
from cloudshell.networking.arista.cli.sessions.console_telnet_session import (
    ConsoleTelnetSession,
)

from tests.networking.arista.base_test import (
    CONFIG_PROMPT,
    DEFAULT_PROMPT,
    ENABLE_PROMPT,
    BaseAristaTestCase,
    CliEmulator,
    Command,
)


class TestAristaSystemActions(TestCase):
    def setUp(self):
        AristaConfigCommandMode.ENTER_CONFIG_RETRY_TIMEOUT = 0.5

        self.api = MagicMock()
        self.api.DecryptPassword().Value.return_value = "password"
        self._cli = CLI()

    def tearDown(self):
        self._cli._session_pool._session_manager._existing_sessions = []
        while not self._cli._session_pool._pool.empty():
            self._cli._session_pool._pool.get()

    def get_cli_configurator(
        self, connection_type: str = "SSH"
    ) -> AristaCLIConfigurator:
        resource_config = MagicMock()
        resource_config.cli_connection_type = connection_type
        return AristaCLIConfigurator(resource_config, self.api, MagicMock(), self._cli)

    def test_enable_mode(self):
        cli_configurator = self.get_cli_configurator()
        self.assertIsInstance(cli_configurator.enable_mode, AristaEnableCommandMode)

    def test_config_mode(self):
        cli_configurator = self.get_cli_configurator()
        self.assertIsInstance(cli_configurator.config_mode, AristaConfigCommandMode)

    def test_get_ssh_session(self):
        cli_configurator = self.get_cli_configurator(connection_type="SSH")
        self.assertIsInstance(cli_configurator._defined_sessions()[0], SSHSession)

    def test_get_telnet_session(self):
        cli_configurator = self.get_cli_configurator(connection_type="TELNET")
        self.assertIsInstance(cli_configurator._defined_sessions()[0], TelnetSession)

    def test_get_console_sessions(self):
        cli_configurator = self.get_cli_configurator(connection_type="console")
        sessions = cli_configurator._defined_sessions()
        console_ssh, console_telnet, console_telnet2 = sessions

        self.assertIsInstance(console_ssh, ConsoleSSHSession)
        self.assertIsInstance(console_telnet, ConsoleTelnetSession)
        self.assertIsInstance(console_telnet2, ConsoleTelnetSession)

    def test_get_sessions_by_default(self):
        cli_configurator = self.get_cli_configurator(connection_type="")
        sessions = cli_configurator._defined_sessions()
        ssh, telnet, console_ssh, console_telnet, console_telnet2 = sessions

        self.assertIsInstance(ssh, SSHSession)
        self.assertIsInstance(telnet, TelnetSession)
        self.assertIsInstance(console_ssh, ConsoleSSHSession)
        self.assertIsInstance(console_telnet, ConsoleTelnetSession)
        self.assertIsInstance(console_telnet2, ConsoleTelnetSession)


@patch("cloudshell.cli.session.ssh_session.paramiko", MagicMock())
@patch(
    "cloudshell.cli.session.ssh_session.SSHSession._clear_buffer",
    MagicMock(return_value=""),
)
@patch("cloudshell.networking.arista.cli.arista_command_modes.time", MagicMock())
class TestCliCommandModes(BaseAristaTestCase):
    def setUp(self):
        self._setUp()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enter_config_mode_with_lock(self, send_mock, recv_mock):
        emu = CliEmulator(
            [
                Command(
                    "",
                    ENABLE_PROMPT,
                )
            ]
        )
        configuration_command = emu.commands[7]
        self.assertEqual(
            configuration_command.request,
            "configure terminal",
            "We have to change particular command",
        )
        configuration_lock_command = Command(
            configuration_command.request,
            f"configuration locked\n{ENABLE_PROMPT}",
            configuration_command.regexp,
        )

        check_config_mode_commands = [
            configuration_lock_command,
            Command("", ENABLE_PROMPT),
            configuration_command,
            Command("", CONFIG_PROMPT),
        ]
        emu.commands[7:8] = check_config_mode_commands

        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        with self.cli_configurator.enable_mode_service() as session:
            session.send_command("")

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enter_config_mode_with_multiple_retries(self, send_mock, recv_mock):
        emu = CliEmulator(
            [
                Command(
                    "",
                    ENABLE_PROMPT,
                )
            ]
        )
        configuration_command = emu.commands[7]
        self.assertEqual(
            configuration_command.request,
            "configure terminal",
            "We have to change particular command",
        )
        configuration_lock_command = Command(
            configuration_command.request,
            f"configuration locked\n{ENABLE_PROMPT}",
            configuration_command.regexp,
        )

        check_config_mode_commands = [
            configuration_lock_command,
            Command("", ENABLE_PROMPT),
        ]
        check_config_mode_commands.extend([configuration_lock_command] * 3)
        check_config_mode_commands.extend(
            [configuration_command, Command("", CONFIG_PROMPT)]
        )
        emu.commands[7:8] = check_config_mode_commands

        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        with self.cli_configurator.enable_mode_service() as session:
            session.send_command("")

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enter_config_mode_regular(self, send_mock, recv_mock):
        emu = CliEmulator(
            [
                Command(
                    "",
                    ENABLE_PROMPT,
                )
            ]
        )

        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        with self.cli_configurator.enable_mode_service() as session:
            session.send_command("")

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enter_config_mode_fail(self, send_mock, recv_mock):
        emu = CliEmulator(
            [
                Command(
                    "",
                    ENABLE_PROMPT,
                )
            ]
        )
        configuration_command = emu.commands[7]
        self.assertEqual(
            configuration_command.request,
            "configure terminal",
            "We have to change particular command",
        )
        configuration_lock_command = Command(
            configuration_command.request,
            f"configuration locked\n{ENABLE_PROMPT}",
            configuration_command.regexp,
        )

        check_config_mode_commands = [
            configuration_lock_command,
            Command("", ENABLE_PROMPT),
        ]
        check_config_mode_commands.extend([configuration_lock_command] * 5)
        emu.commands[7 : len(emu.commands) + 1] = check_config_mode_commands

        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        with self.assertRaisesRegex(
            SessionManagerException,
            "Failed to create new session for type SSH, see logs for details",
        ):
            with self.cli_configurator.config_mode_service() as session:
                session.send_command("")

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enter_enable_and_config_mode_with_parentheses(self, send_mock, recv_mock):
        default_prompt = "fgs-7508-a1-2(b3)>"
        enable_prompt = "fgs-7508-a1-2(b3)#"
        conf_prompt = "fgs-7508-a1-2(b3)(config)#"

        prompts_map = {
            DEFAULT_PROMPT: default_prompt,
            ENABLE_PROMPT: enable_prompt,
            CONFIG_PROMPT: conf_prompt,
        }

        emu = CliEmulator(
            [
                Command(
                    "",
                    ENABLE_PROMPT,
                )
            ]
        )

        for command in emu.commands:
            prompt = prompts_map.get(command.response, command.response)
            command.response = prompt

        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        with self.cli_configurator.enable_mode_service() as session:
            session.send_command("")

        emu.check_calls()
