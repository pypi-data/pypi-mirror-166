from unittest import TestCase
from unittest.mock import MagicMock, patch

from cloudshell.shell.flows.connectivity.parse_request_service import (
    ParseConnectivityRequestService,
)

from cloudshell.networking.arista.flows.arista_connectivity_flow import (
    AristaConnectivityFlow,
)


class TestAristaConnectivityOperations(TestCase):
    def setUp(self):
        connectivity_request_service = ParseConnectivityRequestService(
            is_vlan_range_supported=True, is_multi_vlan_supported=True
        )
        self.flow = AristaConnectivityFlow(
            connectivity_request_service, MagicMock(), MagicMock(), MagicMock()
        )

    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow."
        "AristaConnectivityFlow._remove_vlan"
    )
    @patch(
        "cloudshell.shell.flows.connectivity.basic_flow."
        "DriverResponseRoot.prepare_response"
    )
    def test_remove_vlan_triggered(self, prepare_resp_mock, rem_vlan_mock):
        success = MagicMock()
        json_mock = MagicMock()
        json_mock.json.return_value = success
        prepare_resp_mock.return_value = json_mock
        request = self._get_request().replace("vlan_config_type", "removeVlan")
        result = self.flow.apply_connectivity(request)
        rem_vlan_mock.assert_called_once()
        self.assertIs(result, success)

    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow."
        "AristaConnectivityFlow._set_vlan"
    )
    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow."
        "AristaConnectivityFlow._remove_vlan"
    )
    @patch(
        "cloudshell.shell.flows.connectivity.basic_flow."
        "DriverResponseRoot.prepare_response"
    )
    def test_set_vlan_triggered(self, prepare_resp_mock, rem_vlan_mock, set_vlan_mock):
        rem_vlan_mock.return_value = MagicMock()
        success = MagicMock()
        json_mock = MagicMock()
        json_mock.json.return_value = success
        prepare_resp_mock.return_value = json_mock
        request = self._get_request().replace("vlan_config_type", "setVlan")
        result = self.flow.apply_connectivity(request)
        rem_vlan_mock.assert_called_once()
        set_vlan_mock.assert_called_once()
        self.assertIs(result, success)

    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow."
        "AddRemoveVlanActions"
    )
    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow." "IFaceActions"
    )
    def test_execute_set_vlan_flow(self, iface_mock, vlan_actions_mock):
        port_mode = "trunk"
        port_name = "Ethernet4-5"
        converted_port_name = "Ethernet4/5"
        vlan_id = "45"
        qnq = False
        c_tag = ""
        iface_mock.return_value.get_port_name.return_value = converted_port_name
        actions = self.flow._parse_connectivity_request_service.get_actions(
            self._get_request(
                access_mode=port_mode,
                port_name=port_name,
                vlan_id=vlan_id,
                qnq=str(qnq),
                c_tag=c_tag,
            )
        )
        self.flow._set_vlan(actions[0])
        iface_obj_mock = iface_mock.return_value
        vlan_obj_mock = vlan_actions_mock.return_value

        iface_obj_mock.get_port_name.assert_called_once_with(port_name)
        vlan_obj_mock.create_vlan.assert_called_once_with(vlan_id)

        iface_obj_mock.get_current_interface_config.assert_called_with(
            converted_port_name
        )
        curr_conf_mock = iface_obj_mock.get_current_interface_config.return_value

        iface_obj_mock.enter_iface_config_mode.assert_called_once_with(
            converted_port_name
        )
        iface_obj_mock.clean_interface_switchport_config.assert_called_once_with(
            curr_conf_mock
        )
        vlan_obj_mock.set_vlan_to_interface.assert_called_once_with(
            vlan_id, port_mode, converted_port_name, qnq, c_tag
        )

        self.assertEqual(iface_obj_mock.get_current_interface_config.call_count, 2)

        vlan_obj_mock.verify_interface_configured.assert_called_once_with(
            vlan_id, curr_conf_mock
        )

    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow."
        "AddRemoveVlanActions"
    )
    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow." "IFaceActions"
    )
    def test_raise_exception_if_vlan_not_added(self, iface_mock, vlan_actions_mock):
        port_mode = "trunk"
        port_name = "Ethernet4-5"
        converted_port_name = "Ethernet4/5"
        vlan_id = "45"
        qnq = False
        c_tag = ""
        iface_mock.return_value.get_port_name.return_value = converted_port_name
        vlan_actions_mock.return_value.verify_interface_configured.return_value = False
        actions = self.flow._parse_connectivity_request_service.get_actions(
            self._get_request(
                action="setVlan",
                access_mode=port_mode,
                port_name=port_name,
                vlan_id=vlan_id,
                qnq=str(qnq),
                c_tag=c_tag,
            )
        )
        with self.assertRaises(Exception):
            self.flow._set_vlan(actions[0])

        iface_obj_mock = iface_mock.return_value
        vlan_obj_mock = vlan_actions_mock.return_value

        iface_obj_mock.get_port_name.assert_called_once_with(port_name)
        vlan_obj_mock.create_vlan.assert_called_once_with(vlan_id)

        iface_obj_mock.get_current_interface_config.assert_called_with(
            converted_port_name
        )
        curr_conf_mock = iface_obj_mock.get_current_interface_config.return_value

        iface_obj_mock.enter_iface_config_mode.assert_called_once_with(
            converted_port_name
        )
        iface_obj_mock.clean_interface_switchport_config.assert_called_once_with(
            curr_conf_mock
        )
        vlan_obj_mock.set_vlan_to_interface.assert_called_once_with(
            vlan_id, port_mode, converted_port_name, qnq, c_tag
        )

        self.assertEqual(iface_obj_mock.get_current_interface_config.call_count, 2)

        vlan_obj_mock.verify_interface_configured.assert_called_once_with(
            vlan_id, curr_conf_mock
        )

    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow."
        "AddRemoveVlanActions"
    )
    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow." "IFaceActions"
    )
    def test_remove_vlan_flow(self, iface_mock, vlan_actions_mock):
        port_mode = "trunk"
        port_name = "Ethernet4-5"
        converted_port_name = "Ethernet4/5"
        qnq = False
        vlan_id = "45"
        c_tag = ""
        iface_mock.return_value.get_port_name.return_value = converted_port_name
        vlan_actions_mock.return_value.verify_interface_configured.return_value = False

        actions = self.flow._parse_connectivity_request_service.get_actions(
            self._get_request(
                action="removeVlan",
                access_mode=port_mode,
                port_name=port_name,
                vlan_id=vlan_id,
                qnq=str(qnq),
                c_tag=c_tag,
            )
        )
        self.flow._remove_vlan(actions[0])

        iface_obj_mock = iface_mock.return_value
        vlan_obj_mock = vlan_actions_mock.return_value

        iface_obj_mock.get_port_name.assert_called_once_with(port_name)

        iface_obj_mock.get_current_interface_config.assert_called_with(
            converted_port_name
        )
        curr_conf_mock = iface_obj_mock.get_current_interface_config.return_value

        iface_obj_mock.enter_iface_config_mode.assert_called_once_with(
            converted_port_name
        )
        iface_obj_mock.clean_interface_switchport_config.assert_called_once_with(
            curr_conf_mock
        )
        self.assertEqual(iface_obj_mock.get_current_interface_config.call_count, 2)

        vlan_obj_mock.verify_interface_configured.assert_called_once_with(
            vlan_id, curr_conf_mock
        )

    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow."
        "AddRemoveVlanActions"
    )
    @patch(
        "cloudshell.networking.arista.flows.arista_connectivity_flow." "IFaceActions"
    )
    def test_raise_exception_if_vlan_not_removed(self, iface_mock, vlan_actions_mock):
        port_mode = "trunk"
        port_name = "Ethernet4-5"
        converted_port_name = "Ethernet4/5"
        qnq = False
        vlan_id = "45"
        c_tag = ""
        iface_mock.return_value.get_port_name.return_value = converted_port_name
        vlan_actions_mock.return_value.verify_interface_configured.return_value = True

        actions = self.flow._parse_connectivity_request_service.get_actions(
            self._get_request(
                action="removeVlan",
                access_mode=port_mode,
                port_name=port_name,
                vlan_id=vlan_id,
                qnq=str(qnq),
                c_tag=c_tag,
            )
        )

        with self.assertRaises(Exception):
            self.flow._remove_vlan(actions[0])

        iface_obj_mock = iface_mock.return_value
        vlan_obj_mock = vlan_actions_mock.return_value

        iface_obj_mock.get_port_name.assert_called_once_with(port_name)

        iface_obj_mock.get_current_interface_config.assert_called_with(
            converted_port_name
        )
        curr_conf_mock = iface_obj_mock.get_current_interface_config.return_value

        iface_obj_mock.enter_iface_config_mode.assert_called_once_with(
            converted_port_name
        )
        iface_obj_mock.clean_interface_switchport_config.assert_called_once_with(
            curr_conf_mock
        )
        self.assertEqual(iface_obj_mock.get_current_interface_config.call_count, 2)

        vlan_obj_mock.verify_interface_configured.assert_called_once_with(
            vlan_id, curr_conf_mock
        )

    @staticmethod
    def _get_request(
        action: str = "setVlan",
        access_mode: str = "access",
        port_name: str = "Ethernet1",
        vlan_id: str = "3234",
        qnq: str = "False",
        c_tag: str = "",
    ) -> str:
        return (
            """{
                  "driverRequest": {
                    "actions": [
                      {
                        "connectionId": "6597fd2d-2483-45a9-aaac-72edd7a41dda",
                        "connectionParams": {
                          "vlanId": "__vlan_id__",
                          "mode": "__access_mode__",
                          "vlanServiceAttributes": [
                            {
                              "attributeName": "QnQ",
                              "attributeValue": "__qnq__",
                              "type": "vlanServiceAttribute"
                            },
                            {
                              "attributeName": "CTag",
                              "attributeValue": "__ctag__",
                              "type": "vlanServiceAttribute"
                            },
                            {
                              "attributeName": "Isolation Level",
                              "attributeValue": "Shared",
                              "type": "vlanServiceAttribute"
                            },
                            {
                              "attributeName": "Access Mode",
                              "attributeValue": "__access_mode__",
                              "type": "vlanServiceAttribute"
                            },
                            {
                              "attributeName": "VLAN ID",
                              "attributeValue": "3234",
                              "type": "vlanServiceAttribute"
                            },
                            {
                              "attributeName": "Pool Name",
                              "attributeValue": "",
                              "type": "vlanServiceAttribute"
                            },
                            {
                              "attributeName": "Virtual Network",
                              "attributeValue": "3234",
                              "type": "vlanServiceAttribute"
                            }
                          ],
                          "type": "setVlanParameter"
                        },
                        "connectorAttributes": [],
                        "actionTarget": {
                          "fullName": "__port_name__",
                          "fullAddress": "192.168.105.53/CH0/P1",
                          "type": "actionTarget"
                        },
                        "customActionAttributes": [],
                        "actionId": "6597fd2d-2483-45a9-aaac-72edd7a41dda",
                        "type": "__action__"
                      }
                    ]
                  }
                }""".replace(
                "__action__", action
            )
            .replace("__access_mode__", access_mode.capitalize())
            .replace("__port_name__", port_name)
            .replace("__vlan_id__", vlan_id)
            .replace("__qnq__", qnq)
            .replace("__ctag__", c_tag)
        )
