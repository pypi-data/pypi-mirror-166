from unittest.mock import MagicMock, patch

from cloudshell.shell.flows.configuration.basic_flow import (
    ConfigurationType,
    RestoreMethod,
)
from cloudshell.shell.flows.utils.url import RemoteURL

from cloudshell.networking.arista.flows.arista_configuration_flow import (
    AristaConfigurationFlow,
)

from tests.networking.arista.base_test import (
    ENABLE_PROMPT,
    VRF_PROMPT,
    BaseAristaTestCase,
    CliEmulator,
    Command,
)


@patch("cloudshell.cli.session.ssh_session.paramiko", MagicMock())
@patch(
    "cloudshell.cli.session.ssh_session.SSHSession._clear_buffer",
    MagicMock(return_value=""),
)
class TestSaveRestoreFlow(BaseAristaTestCase):
    def _setUp(self, attrs=None):
        super()._setUp(attrs)
        self.flow = AristaConfigurationFlow(
            self.logger, self.resource_config, self.cli_configurator
        )

    def setUp(self):
        self._setUp(
            {
                "Backup Location": "Test-running-081018-215424",
                "Backup Type": AristaConfigurationFlow.FILE_SYSTEM_SCHEME,
            }
        )

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_save_anonymous(self, send_mock, recv_mock):
        self._setUp()
        host = "192.168.122.10"
        ftp_path = f"ftp://{host}"
        configuration_type = "running"

        emu = CliEmulator(
            [
                Command(
                    r"^copy {0} {1}/Arista-{0}-\d+-\d+$".format(
                        configuration_type, ftp_path
                    ),
                    "Copy complete\n" "{}".format(ENABLE_PROMPT),
                    regexp=True,
                ),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.flow.save(ftp_path, configuration_type, "")

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_save_ftp(self, send_mock, recv_mock):
        self._setUp()
        user = "user"
        password = "password"
        host = "192.168.122.10"
        ftp_path = f"ftp://{user}:{password}@{host}"
        configuration_type = "running"

        emu = CliEmulator(
            [
                Command(
                    r"^copy {0} {1}/Arista-{0}-\d+-\d+$".format(
                        configuration_type, ftp_path
                    ),
                    "Copy complete\n" "{}".format(ENABLE_PROMPT),
                    regexp=True,
                )
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.flow.save(ftp_path, configuration_type, "")

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_save_with_vrf(self, send_mock, recv_mock):
        vrf_name = "vrf_name"
        self._setUp({"VRF Management Name": vrf_name})
        user = "user"
        password = "password"
        host = "192.168.122.10"
        ftp_path = f"ftp://{user}:{password}@{host}"
        configuration_type = "running"

        emu = CliEmulator(
            [
                Command(
                    f"routing-context vrf {vrf_name}",
                    VRF_PROMPT.format(vrf_name=vrf_name),
                ),
                Command(
                    r"^copy {0} {1}/Arista-{0}-\d+-\d+$".format(
                        configuration_type, ftp_path
                    ),
                    "Copy complete\n" "{}".format(VRF_PROMPT.format(vrf_name=vrf_name)),
                    regexp=True,
                ),
                Command("routing-context vrf default", ENABLE_PROMPT),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.flow.save(ftp_path, configuration_type, vrf_name)

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_save_startup(self, send_mock, recv_mock):
        self._setUp()
        user = "user"
        password = "password"
        host = "192.168.122.10"
        ftp_path = f"ftp://{user}:{password}@{host}"
        configuration_type = "startup"

        emu = CliEmulator(
            [
                Command(
                    r"^copy {0} {1}/Arista-{0}-\d+-\d+$".format(
                        configuration_type, ftp_path
                    ),
                    "Copy complete\n" "{}".format(ENABLE_PROMPT),
                    regexp=True,
                )
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.flow.save(ftp_path, configuration_type, "")

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_fail_to_save(self, send_mock, recv_mock):
        self._setUp()
        host = "192.168.122.10"
        ftp_path = f"ftp://{host}"
        configuration_type = "running"

        emu = CliEmulator(
            [
                Command(
                    r"^copy {0} {1}/Arista-{0}-\d+-\d+$".format(
                        configuration_type, ftp_path
                    ),
                    "Error\n" "{}".format(ENABLE_PROMPT),
                    regexp=True,
                )
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        with self.assertRaisesRegex(Exception, "Copy Command failed"):
            self.flow.save(ftp_path, configuration_type, "")

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_save_to_device(self, send_mock, recv_mock):
        self._setUp(
            {
                "Backup Location": "",
                "Backup Type": AristaConfigurationFlow.FILE_SYSTEM_SCHEME,
            }
        )
        path = ""
        configuration_type = "running"

        emu = CliEmulator(
            [
                Command(
                    r"copy {0} flash:/Arista-{0}-\d+-\d+".format(configuration_type),
                    "Copy complete\n" "{}".format(ENABLE_PROMPT),
                    regexp=True,
                )
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.flow.save(path, configuration_type)

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_restore_running_override(self, send_mock, recv_mock):
        self._setUp()
        host = "192.168.122.10"
        file_name = "Test-running-100418-163658"
        remote_path = f"ftp://{host}/{file_name}"

        emu = CliEmulator([Command(f"configure replace {remote_path}", ENABLE_PROMPT)])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.flow._restore_flow(
            RemoteURL.from_str(remote_path),
            ConfigurationType.RUNNING,
            RestoreMethod.OVERRIDE,
            "",
        )

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_restore_startup(self, send_mock, recv_mock):
        self._setUp()
        host = "192.168.122.10"
        file_name = "Test-startup-100418-163658"
        remote_path = f"ftp://{host}/{file_name}"
        configuration_type = "startup"

        emu = CliEmulator(
            [
                Command(
                    f"copy {remote_path} {configuration_type}-config",
                    "Copy completed successfully.\n" "{}".format(ENABLE_PROMPT),
                )
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.flow._restore_flow(
            RemoteURL.from_str(remote_path),
            ConfigurationType.STARTUP,
            RestoreMethod.OVERRIDE,
            "",
        )

        emu.check_calls()
