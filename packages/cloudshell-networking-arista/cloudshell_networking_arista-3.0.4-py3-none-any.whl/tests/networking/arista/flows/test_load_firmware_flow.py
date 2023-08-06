from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from cloudshell.shell.flows.utils.url import RemoteURL

from cloudshell.networking.arista.flows.arista_load_firmware_flow import (
    AristaLoadFirmwareFlow,
)


class TestAristaLoadFirmwareFlow(TestCase):
    def setUp(self):
        self.cli = MagicMock()
        self.firmware_flow = AristaLoadFirmwareFlow(MagicMock(), MagicMock(), self.cli)

    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow."
        "AristaLoadFirmwareFlow._load_firmware_flow"
    )
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow."
        "AristaLoadFirmwareFlow._get_firmware_url"
    )
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow."
        "AristaLoadFirmwareFlow._get_vrf_mgmt_name"
    )
    def test_load_firmware_triggered(
        self, get_vrf_mgmt_name, get_firmware_url, load_firmware_flow
    ):
        url = MagicMock()
        get_firmware_url.return_value = url
        vrf_name_mock = MagicMock()
        get_vrf_mgmt_name.return_value = vrf_name_mock
        path = MagicMock()
        vrf_name = MagicMock()
        self.firmware_flow.load_firmware(path, vrf_name)
        get_firmware_url.assert_called_once_with(path)
        get_vrf_mgmt_name.assert_called_once_with(vrf_name)
        load_firmware_flow.assert_called_once_with(
            url, vrf_name_mock, self.firmware_flow._timeout
        )

    @patch("cloudshell.networking.arista.flows.arista_load_firmware_flow.SystemActions")
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow.FirmwareActions"
    )
    def test_execute_flow(self, fw_actions_mock, sys_actions_mock):
        old_firmware = "flash:/old_firmware.bin"
        new_firmware = "filename.bin"
        timeout = 30
        vrf = ""
        firmware_url = f"ftp://10.0.0.1/{new_firmware}"
        firmware_dst_path = f"{self.firmware_flow.FLASH}/{new_firmware}"
        act_map_mock1 = MagicMock()
        act_map_mock2 = MagicMock()

        sys_action_obj = sys_actions_mock.return_value
        fw_action_obj = fw_actions_mock.return_value

        sys_action_obj.get_flash_folders_list.return_value = []
        sys_action_obj.get_current_boot_image.return_value = [old_firmware]
        sys_action_obj.get_current_boot_config.return_value = new_firmware
        sys_action_obj.get_current_os_version.return_value = new_firmware
        sys_action_obj.prepare_action_map.side_effect = [act_map_mock1, act_map_mock2]

        self.firmware_flow._load_firmware_flow(
            RemoteURL.from_str(firmware_url), vrf, timeout
        )

        sys_action_obj.get_flash_folders_list.assert_called_once_with()
        sys_action_obj.get_current_boot_image.assert_called_once_with()
        sys_action_obj.get_current_boot_config.assert_called_once_with()
        sys_action_obj.get_current_os_version.assert_called_once_with()
        self.assertEqual(sys_action_obj.prepare_action_map.call_count, 2)

        sys_action_obj.copy.assert_has_calls(
            (
                call(
                    firmware_url, firmware_dst_path, vrf=vrf, action_map=act_map_mock1
                ),
                call(
                    self.firmware_flow.RUNNING_CONFIG,
                    self.firmware_flow.STARTUP_CONFIG,
                    vrf=vrf,
                    action_map=act_map_mock2,
                ),
            )
        )

        sys_action_obj.reload_device.assert_called_once_with(timeout)

        fw_action_obj.clean_boot_config.assert_called_once_with(old_firmware)
        fw_action_obj.add_boot_config_file.assert_called_once_with(firmware_dst_path)
        fw_action_obj.add_boot_config.assert_called_once_with(old_firmware)

    @patch("cloudshell.networking.arista.flows.arista_load_firmware_flow.SystemActions")
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow.FirmwareActions"
    )
    def test_fail_add_firmware(self, fw_actions_mock, sys_actions_mock):
        old_firmware = "flash:/old_firmware.bin"
        new_firmware = "filename.bin"
        timeout = 30
        vrf = ""
        firmware_url = f"ftp://10.0.0.1/{new_firmware}"
        firmware_dst_path = f"{self.firmware_flow.FLASH}/{new_firmware}"
        act_map_mock1 = MagicMock()
        act_map_mock2 = MagicMock()

        sys_action_obj = sys_actions_mock.return_value
        fw_action_obj = fw_actions_mock.return_value

        sys_action_obj.get_flash_folders_list.return_value = []
        sys_action_obj.get_current_boot_image.return_value = [old_firmware]
        sys_action_obj.get_current_boot_config.return_value = old_firmware
        sys_action_obj.get_current_os_version.return_value = new_firmware
        sys_action_obj.prepare_action_map.side_effect = [act_map_mock1, act_map_mock2]

        with self.assertRaises(Exception):
            self.firmware_flow._load_firmware_flow(
                RemoteURL.from_str(firmware_url), vrf, timeout
            )

        sys_action_obj.get_flash_folders_list.assert_called_once_with()
        sys_action_obj.get_current_boot_image.assert_called_once_with()
        sys_action_obj.get_current_boot_config.assert_called_once_with()
        sys_action_obj.get_current_os_version.assert_not_called()
        self.assertEqual(sys_action_obj.prepare_action_map.call_count, 1)

        sys_action_obj.copy.assert_called_once_with(
            firmware_url, firmware_dst_path, vrf=vrf, action_map=act_map_mock1
        )

        sys_action_obj.reload_device.assert_not_called()

        fw_action_obj.clean_boot_config.assert_called_once_with(old_firmware)
        fw_action_obj.add_boot_config_file.assert_called_once_with(firmware_dst_path)
        fw_action_obj.add_boot_config.assert_called_once_with(old_firmware)

    @patch("cloudshell.networking.arista.flows.arista_load_firmware_flow.SystemActions")
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow.FirmwareActions"
    )
    def test_fail_load_firmware(self, fw_actions_mock, sys_actions_mock):
        old_firmware = "flash:/old_firmware.bin"
        new_firmware = ""
        timeout = 30
        vrf = ""
        firmware_url = "ftp://10.0.0.1/"

        act_map_mock1 = MagicMock()
        act_map_mock2 = MagicMock()

        sys_action_obj = sys_actions_mock.return_value

        sys_action_obj.get_flash_folders_list.return_value = []
        sys_action_obj.get_current_boot_image.return_value = [old_firmware]
        sys_action_obj.get_current_boot_config.return_value = new_firmware
        sys_action_obj.get_current_os_version.return_value = old_firmware
        sys_action_obj.prepare_action_map.side_effect = [act_map_mock1, act_map_mock2]

        with self.assertRaises(Exception):
            self.firmware_flow._load_firmware_flow(
                RemoteURL.from_str(firmware_url), vrf, timeout
            )

    @patch("cloudshell.networking.arista.flows.arista_load_firmware_flow.SystemActions")
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow.FirmwareActions"
    )
    def test_reload_via_console(self, fw_actions_mock, sys_actions_mock):
        enable_ses = MagicMock()
        self.cli.enable_mode_service.return_value.__enter__.return_value = enable_ses
        enable_ses.session.SESSION_TYPE = "CONSOLE"

        old_firmware = "flash:/old_firmware.bin"
        new_firmware = "filename.bin"
        timeout = 30
        vrf = ""
        firmware_url = f"ftp://10.0.0.1/{new_firmware}"
        firmware_dst_path = f"{self.firmware_flow.FLASH}/{new_firmware}"

        act_map_mock1 = MagicMock()
        act_map_mock2 = MagicMock()

        sys_action_obj = sys_actions_mock.return_value
        fw_action_obj = fw_actions_mock.return_value

        sys_action_obj.get_flash_folders_list.return_value = []
        sys_action_obj.get_current_boot_image.return_value = [old_firmware]
        sys_action_obj.get_current_boot_config.return_value = new_firmware
        sys_action_obj.get_current_os_version.return_value = new_firmware
        sys_action_obj.prepare_action_map.side_effect = [act_map_mock1, act_map_mock2]

        self.firmware_flow._load_firmware_flow(
            RemoteURL.from_str(firmware_url), vrf, timeout
        )

        sys_action_obj.get_flash_folders_list.assert_called_once_with()
        sys_action_obj.get_current_boot_image.assert_called_once_with()
        sys_action_obj.get_current_boot_config.assert_called_once_with()
        sys_action_obj.get_current_os_version.assert_called_once_with()
        self.assertEqual(sys_action_obj.prepare_action_map.call_count, 2)

        sys_action_obj.copy.assert_has_calls(
            (
                call(
                    firmware_url, firmware_dst_path, vrf=vrf, action_map=act_map_mock1
                ),
                call(
                    self.firmware_flow.RUNNING_CONFIG,
                    self.firmware_flow.STARTUP_CONFIG,
                    vrf=vrf,
                    action_map=act_map_mock2,
                ),
            )
        )

        sys_action_obj.reload_device_via_console.assert_called_once_with(timeout)

        fw_action_obj.clean_boot_config.assert_called_once_with(old_firmware)
        fw_action_obj.add_boot_config_file.assert_called_once_with(firmware_dst_path)
        fw_action_obj.add_boot_config.assert_called_once_with(old_firmware)

    @patch("cloudshell.networking.arista.flows.arista_load_firmware_flow.SystemActions")
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow.FirmwareActions"
    )
    def test_kickstart_image(self, fw_actions_mock, sys_actions_mock):
        old_firmware = "flash:/old_firmware.bin"
        new_firmware = "kickstart.bin"
        timeout = 30
        vrf = ""
        firmware_url = f"ftp://10.0.0.1/{new_firmware}"
        firmware_dst_path = f"{self.firmware_flow.FLASH}/{new_firmware}"

        act_map_mock1 = MagicMock()
        act_map_mock2 = MagicMock()

        sys_action_obj = sys_actions_mock.return_value
        fw_action_obj = fw_actions_mock.return_value

        sys_action_obj.get_flash_folders_list.return_value = []
        sys_action_obj.get_current_boot_image.return_value = [old_firmware]
        sys_action_obj.get_current_boot_config.return_value = new_firmware
        sys_action_obj.get_current_os_version.return_value = new_firmware
        sys_action_obj.prepare_action_map.side_effect = [act_map_mock1, act_map_mock2]

        self.firmware_flow._load_firmware_flow(
            RemoteURL.from_str(firmware_url), vrf, timeout
        )

        sys_action_obj.get_flash_folders_list.assert_called_once_with()
        sys_action_obj.get_current_boot_image.assert_called_once_with()
        sys_action_obj.get_current_boot_config.assert_called_once_with()
        sys_action_obj.get_current_os_version.assert_called_once_with()
        self.assertEqual(sys_action_obj.prepare_action_map.call_count, 2)

        sys_action_obj.copy.assert_has_calls(
            (
                call(
                    firmware_url, firmware_dst_path, vrf=vrf, action_map=act_map_mock1
                ),
                call(
                    self.firmware_flow.RUNNING_CONFIG,
                    self.firmware_flow.STARTUP_CONFIG,
                    vrf=vrf,
                    action_map=act_map_mock2,
                ),
            )
        )

        sys_action_obj.reload_device.assert_called_once_with(timeout)

        fw_action_obj.clean_boot_config.assert_not_called()
        fw_action_obj.add_boot_config_file.assert_called_once_with(firmware_dst_path)
        fw_action_obj.add_boot_config.assert_not_called()

    @patch("cloudshell.networking.arista.flows.arista_load_firmware_flow.SystemActions")
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow.FirmwareActions"
    )
    def test_kickstart_in_old_firmware(self, fw_actions_mock, sys_actions_mock):
        old_firmware = "flash:/kickstart.bin"
        new_firmware = "kickstart2.bin"
        timeout = 30
        vrf = ""
        firmware_url = f"ftp://10.0.0.1/{new_firmware}"
        firmware_dst_path = f"{self.firmware_flow.FLASH}/{new_firmware}"

        act_map_mock1 = MagicMock()
        act_map_mock2 = MagicMock()

        sys_action_obj = sys_actions_mock.return_value
        fw_action_obj = fw_actions_mock.return_value

        sys_action_obj.get_flash_folders_list.return_value = []
        sys_action_obj.get_current_boot_image.return_value = [old_firmware]
        sys_action_obj.get_current_boot_config.return_value = new_firmware
        sys_action_obj.get_current_os_version.return_value = new_firmware
        sys_action_obj.prepare_action_map.side_effect = [act_map_mock1, act_map_mock2]

        self.firmware_flow._load_firmware_flow(
            RemoteURL.from_str(firmware_url), vrf, timeout
        )

        sys_action_obj.get_flash_folders_list.assert_called_once_with()
        sys_action_obj.get_current_boot_image.assert_called_once_with()
        sys_action_obj.get_current_boot_config.assert_called_once_with()
        sys_action_obj.get_current_os_version.assert_called_once_with()
        self.assertEqual(sys_action_obj.prepare_action_map.call_count, 2)

        sys_action_obj.copy.assert_has_calls(
            (
                call(
                    firmware_url, firmware_dst_path, vrf=vrf, action_map=act_map_mock1
                ),
                call(
                    self.firmware_flow.RUNNING_CONFIG,
                    self.firmware_flow.STARTUP_CONFIG,
                    vrf=vrf,
                    action_map=act_map_mock2,
                ),
            )
        )

        sys_action_obj.reload_device.assert_called_once_with(timeout)

        fw_action_obj.clean_boot_config.assert_called_once_with(old_firmware)
        fw_action_obj.add_boot_config_file.assert_called_once_with(firmware_dst_path)
        fw_action_obj.add_boot_config.assert_called_once_with(old_firmware)

    @patch("cloudshell.networking.arista.flows.arista_load_firmware_flow.SystemActions")
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow.FirmwareActions"
    )
    def test_bootfolder(self, fw_actions_mock, sys_actions_mock):
        old_firmware = "flash:/old_firmware.bin"
        new_firmware = "filename.bin"
        timeout = 30
        vrf = ""
        firmware_url = f"ftp://10.0.0.1/{new_firmware}"
        firmware_dst_path = f"bootflash:/{new_firmware}"
        act_map_mock1 = MagicMock()
        act_map_mock2 = MagicMock()

        sys_action_obj = sys_actions_mock.return_value
        fw_action_obj = fw_actions_mock.return_value

        sys_action_obj.get_flash_folders_list.return_value = ["bootflash:"]
        sys_action_obj.get_current_boot_image.return_value = [old_firmware]
        sys_action_obj.get_current_boot_config.return_value = new_firmware
        sys_action_obj.get_current_os_version.return_value = new_firmware
        sys_action_obj.prepare_action_map.side_effect = [act_map_mock1, act_map_mock2]

        self.firmware_flow._load_firmware_flow(
            RemoteURL.from_str(firmware_url), vrf, timeout
        )

        sys_action_obj.get_flash_folders_list.assert_called_once_with()
        sys_action_obj.get_current_boot_image.assert_called_once_with()
        sys_action_obj.get_current_boot_config.assert_called_once_with()
        sys_action_obj.get_current_os_version.assert_called_once_with()
        self.assertEqual(sys_action_obj.prepare_action_map.call_count, 2)

        sys_action_obj.copy.assert_has_calls(
            (
                call(
                    firmware_url, firmware_dst_path, vrf=vrf, action_map=act_map_mock1
                ),
                call(
                    self.firmware_flow.RUNNING_CONFIG,
                    self.firmware_flow.STARTUP_CONFIG,
                    vrf=vrf,
                    action_map=act_map_mock2,
                ),
            )
        )

        sys_action_obj.reload_device.assert_called_once_with(timeout)

        fw_action_obj.clean_boot_config.assert_called_once_with(old_firmware)
        fw_action_obj.add_boot_config_file.assert_called_once_with(firmware_dst_path)
        fw_action_obj.add_boot_config.assert_called_once_with(old_firmware)

    @patch("cloudshell.networking.arista.flows.arista_load_firmware_flow.SystemActions")
    @patch(
        "cloudshell.networking.arista.flows.arista_load_firmware_flow.FirmwareActions"
    )
    def test_flash_folders(self, fw_actions_mock, sys_actions_mock):
        old_firmware = "flash:/old_firmware.bin"
        new_firmware = "filename.bin"
        timeout = 30
        vrf = ""
        flash_folders = ["flash-1a", "flash-1b"]
        firmware_url = f"ftp://10.0.0.1/{new_firmware}"
        firmware_dst_path = f"{self.firmware_flow.FLASH}/{new_firmware}"
        firmware_dst_file_path1 = f"{flash_folders[0]}/{new_firmware}"
        firmware_dst_file_path2 = f"{flash_folders[1]}/{new_firmware}"
        act_map_mock1 = MagicMock()
        act_map_mock2 = MagicMock()
        act_map_mock3 = MagicMock()

        sys_action_obj = sys_actions_mock.return_value
        fw_action_obj = fw_actions_mock.return_value

        sys_action_obj.get_flash_folders_list.return_value = ["flash-1a", "flash-1b"]
        sys_action_obj.get_current_boot_image.return_value = [old_firmware]
        sys_action_obj.get_current_boot_config.return_value = new_firmware
        sys_action_obj.get_current_os_version.return_value = new_firmware
        sys_action_obj.prepare_action_map.side_effect = [
            act_map_mock1,
            act_map_mock2,
            act_map_mock3,
        ]

        self.firmware_flow._load_firmware_flow(
            RemoteURL.from_str(firmware_url), vrf, timeout
        )

        sys_action_obj.get_flash_folders_list.assert_called_once_with()
        sys_action_obj.get_current_boot_image.assert_called_once_with()
        sys_action_obj.get_current_boot_config.assert_called_once_with()
        sys_action_obj.get_current_os_version.assert_called_once_with()
        self.assertEqual(sys_action_obj.prepare_action_map.call_count, 3)

        sys_action_obj.copy.assert_has_calls(
            (
                call(
                    firmware_url,
                    firmware_dst_file_path1,
                    vrf=vrf,
                    action_map=act_map_mock1,
                ),
                call(
                    firmware_url,
                    firmware_dst_file_path2,
                    vrf=vrf,
                    action_map=act_map_mock2,
                ),
                call(
                    self.firmware_flow.RUNNING_CONFIG,
                    self.firmware_flow.STARTUP_CONFIG,
                    vrf=vrf,
                    action_map=act_map_mock3,
                ),
            )
        )

        sys_action_obj.reload_device.assert_called_once_with(timeout)

        fw_action_obj.clean_boot_config.assert_called_once_with(old_firmware)
        fw_action_obj.add_boot_config_file.assert_called_once_with(firmware_dst_path)
        fw_action_obj.add_boot_config.assert_called_once_with(old_firmware)

    def test_empty_filename(self):
        with self.assertRaises(Exception):
            self.firmware_flow._load_firmware_flow(
                RemoteURL.from_str("ftp://10.0.1.1/"), MagicMock(), MagicMock()
            )
