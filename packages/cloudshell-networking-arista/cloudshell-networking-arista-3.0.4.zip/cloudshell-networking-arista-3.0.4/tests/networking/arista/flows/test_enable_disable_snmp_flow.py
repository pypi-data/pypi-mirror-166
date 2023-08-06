from unittest.mock import MagicMock, patch

from cloudshell.snmp.snmp_parameters import SnmpParametersHelper

from cloudshell.networking.arista.flows.enable_disable_snmp import (
    AristaEnableDisableSNMPFlow,
)

from tests.networking.arista.base_test import (
    CONFIG_PROMPT,
    BaseAristaTestCase,
    CliEmulator,
    Command,
)


@patch(
    "cloudshell.networking.arista.flows.arista_autoload_flow.AristaAutoloadFlow",
    MagicMock(),
)
@patch("cloudshell.cli.session.ssh_session.paramiko", MagicMock())
@patch(
    "cloudshell.cli.session.ssh_session.SSHSession._clear_buffer",
    MagicMock(return_value=""),
)
class TestEnableDisableSnmp(BaseAristaTestCase):
    def _setUp(self, attrs=None):
        attrs = attrs or {}
        snmp_attrs = {
            "SNMP Version": "v2c",
            "SNMP Read Community": "public",
            "SNMP V3 User": "quali_user",
            "SNMP V3 Password": "password",
            "SNMP V3 Private Key": "private_key",
            "SNMP V3 Authentication Protocol": "No Authentication Protocol",
            "SNMP V3 Privacy Protocol": "No Privacy Protocol",
            "Enable SNMP": "True",
            "Disable SNMP": "False",
        }
        snmp_attrs.update(attrs)
        super()._setUp(snmp_attrs)
        self.snmp_parameters = SnmpParametersHelper(
            self.resource_config
        ).get_snmp_parameters()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enable_snmp_v2(self, send_mock, recv_mock):
        self._setUp()

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command("show snmp community", CONFIG_PROMPT),
                Command("snmp-server community public ro", CONFIG_PROMPT),
                Command(
                    "show snmp community",
                    "Community name: public\n"
                    "Community access: read-only\n"
                    "{}".format(CONFIG_PROMPT),
                ),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        enable_disable_snmp_flow.enable_snmp(self.snmp_parameters)

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enable_snmp_v2_with_vrf(self, send_mock, recv_mock):
        self._setUp(
            {
                "VRF Management Name": "management",
            }
        )

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command(
                    "show snmp",
                    "0 SNMP packets input\n"
                    "    0 Bad SNMP version errors\n"
                    "    0 Unknown community name\n"
                    "    0 Illegal operation for community name supplied\n"
                    "    0 Encoding errors\n"
                    "    0 Number of requested variables\n"
                    "    0 Number of altered variables\n"
                    "    0 Get-request PDUs\n"
                    "    0 Get-next PDUs\n"
                    "    0 Set-request PDUs\n"
                    "...\n"
                    "SNMP logging: disabled\n"
                    "SNMP agent enabled in VRFs: default\n"
                    "{}".format(CONFIG_PROMPT),
                ),
                Command("snmp-server vrf management", CONFIG_PROMPT),
                Command("show snmp community", CONFIG_PROMPT),
                Command("snmp-server community public ro", CONFIG_PROMPT),
                Command(
                    "show snmp community",
                    "Community name: public\n"
                    "Community access: read-only\n"
                    "{}".format(CONFIG_PROMPT),
                ),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger, vrf_name="management"
        )
        enable_disable_snmp_flow.enable_snmp(self.snmp_parameters)

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enable_snmp_v2_with_vrf_already_enabled(self, send_mock, recv_mock):
        self._setUp(
            {
                "VRF Management Name": "management",
            }
        )

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command(
                    "show snmp",
                    "0 SNMP packets input\n"
                    "    0 Bad SNMP version errors\n"
                    "    0 Unknown community name\n"
                    "    0 Illegal operation for community name supplied\n"
                    "    0 Encoding errors\n"
                    "    0 Number of requested variables\n"
                    "    0 Number of altered variables\n"
                    "    0 Get-request PDUs\n"
                    "    0 Get-next PDUs\n"
                    "    0 Set-request PDUs\n"
                    "...\n"
                    "SNMP logging: disabled\n"
                    "SNMP agent enabled in VRFs: default, management\n"
                    "{}".format(CONFIG_PROMPT),
                ),
                Command("show snmp community", CONFIG_PROMPT),
                Command("snmp-server community public ro", CONFIG_PROMPT),
                Command(
                    "show snmp community",
                    "Community name: public\n"
                    "Community access: read-only\n"
                    "{}".format(CONFIG_PROMPT),
                ),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger, vrf_name="management"
        )
        enable_disable_snmp_flow.enable_snmp(self.snmp_parameters)
        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enable_snmp_v2_already_enabled(self, send_mock, recv_mock):
        self._setUp()

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command(
                    "show snmp community",
                    "Community name: public\n"
                    "Community access: read-only\n"
                    "{}".format(CONFIG_PROMPT),
                ),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        enable_disable_snmp_flow.enable_snmp(self.snmp_parameters)

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enable_snmp_v2_not_enabled(self, send_mock, recv_mock):
        self._setUp()

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command("show snmp community", CONFIG_PROMPT),
                Command("snmp-server community public ro", CONFIG_PROMPT),
                Command("show snmp community", CONFIG_PROMPT),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all
        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        with self.assertRaisesRegex(Exception, "Failed to create SNMP community"):
            enable_disable_snmp_flow.enable_snmp(self.snmp_parameters)

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_enable_snmp_v2_write_community(self, send_mock, recv_mock):
        self._setUp({"SNMP Write Community": "private"})

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command("show snmp community", CONFIG_PROMPT),
                Command("snmp-server community private ro", CONFIG_PROMPT),
                Command(
                    "show snmp community",
                    "Community name: private\n"
                    "Community access: read-only\n"
                    "{}".format(CONFIG_PROMPT),
                ),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        enable_disable_snmp_flow.enable_snmp(self.snmp_parameters)
        emu.check_calls()

    @patch("tests.networking.arista.base_test.AristaCLIConfigurator")
    def test_enable_snmp_without_community(self, cli_configurator_mock):
        self._setUp({"SNMP Read Community": ""})
        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        with self.assertRaisesRegex(Exception, "SNMP community cannot be empty"):
            enable_disable_snmp_flow.enable_snmp(self.snmp_parameters)

        cli_configurator_mock.get_cli_service.assert_not_called()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_disable_snmp_v2(self, send_mock, recv_mock):
        self._setUp(
            {
                "Enable SNMP": "False",
                "Disable SNMP": "True",
            }
        )

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command("no snmp-server community public", CONFIG_PROMPT),
                Command("show snmp community", CONFIG_PROMPT),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        enable_disable_snmp_flow.disable_snmp(self.snmp_parameters)

        emu.check_calls()

    @patch("tests.networking.arista.base_test.AristaCLIConfigurator")
    def test_disable_snmp_without_community(self, cli_handler_mock):
        self._setUp(
            {
                "Enable SNMP": "False",
                "Disable SNMP": "True",
                "SNMP Read Community": "",
            }
        )

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )

        with self.assertRaisesRegex(Exception, "SNMP community cannot be empty"):
            enable_disable_snmp_flow.disable_snmp(self.snmp_parameters)

        cli_handler_mock.get_cli_service.assert_not_called()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_disable_snmp_v2_already_disabled(self, send_mock, recv_mock):
        self._setUp(
            {
                "Enable SNMP": "False",
                "Disable SNMP": "True",
            }
        )

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command("no snmp-server community public", CONFIG_PROMPT),
                Command("show snmp community", CONFIG_PROMPT),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        enable_disable_snmp_flow.disable_snmp(self.snmp_parameters)

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_disable_snmp_v2_is_not_disabled(self, send_mock, recv_mock):
        self._setUp(
            {
                "Enable SNMP": "False",
                "Disable SNMP": "True",
            }
        )

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command("no snmp-server community public", CONFIG_PROMPT),
                Command(
                    "show snmp community",
                    "Community name: public\n"
                    "Community access: read-only\n"
                    "{}".format(CONFIG_PROMPT),
                ),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        with self.assertRaisesRegex(Exception, "Failed to remove SNMP community"):
            enable_disable_snmp_flow.disable_snmp(self.snmp_parameters)

        emu.check_calls()

    @patch("cloudshell.cli.session.ssh_session.SSHSession._receive_all")
    @patch("cloudshell.cli.session.ssh_session.SSHSession.send_line")
    def test_disable_snmp_v2_write_community(self, send_mock, recv_mock):
        self._setUp(
            {
                "Enable SNMP": "False",
                "Disable SNMP": "True",
                "SNMP Write Community": "private",
            }
        )

        emu = CliEmulator(
            [
                Command("configure terminal", CONFIG_PROMPT),
                Command("no snmp-server community private", CONFIG_PROMPT),
                Command("show snmp community", CONFIG_PROMPT),
            ]
        )
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        enable_disable_snmp_flow.disable_snmp(self.snmp_parameters)

        emu.check_calls()

    @patch("tests.networking.arista.base_test.AristaCLIConfigurator")
    def test_enable_snmp_v3(self, cli_handler_mock):
        cli_instance_mock = MagicMock()
        cli_handler_mock.return_value = cli_instance_mock
        self._setUp({"SNMP Version": "v3"})

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )
        with self.assertRaisesRegex(Exception, "Do not support SNMP V3"):
            enable_disable_snmp_flow.disable_snmp(self.snmp_parameters)

        cli_instance_mock.get_cli_service.assert_not_called()

    @patch("tests.networking.arista.base_test.AristaCLIConfigurator")
    def test_disable_snmp_v3(self, cli_handler_mock):
        cli_instance_mock = MagicMock()
        cli_handler_mock.return_value = cli_instance_mock
        self._setUp(
            {
                "SNMP Version": "v3",
                "SNMP V3 Authentication Protocol": "SHA",
                "SNMP V3 Privacy Protocol": "AES-128",
                "Enable SNMP": "False",
                "Disable SNMP": "True",
            }
        )

        enable_disable_snmp_flow = AristaEnableDisableSNMPFlow(
            self.cli_configurator, self.logger
        )

        with self.assertRaisesRegex(Exception, "Do not support SNMP V3"):
            enable_disable_snmp_flow.disable_snmp(self.snmp_parameters)

        cli_instance_mock.get_cli_service.assert_not_called()
