from __future__ import annotations

from typing import TYPE_CHECKING

from cloudshell.shell.flows.connectivity.basic_flow import AbstractConnectivityFlow
from cloudshell.shell.flows.connectivity.models.driver_response import (
    ConnectivityActionResult,
)

from ..command_actions.add_remove_vlan_actions import AddRemoveVlanActions
from ..command_actions.iface_actions import IFaceActions

if TYPE_CHECKING:
    from logging import Logger

    from cloudshell.shell.flows.connectivity.models.connectivity_model import (
        ConnectivityActionModel,
    )
    from cloudshell.shell.flows.connectivity.parse_request_service import (
        AbstractParseConnectivityService,
    )
    from cloudshell.shell.standards.networking.resource_config import (
        NetworkingResourceConfig,
    )

    from ..cli.arista_cli_configurator import AristaCLIConfigurator


class AristaConnectivityFlow(AbstractConnectivityFlow):
    def __init__(
        self,
        parse_connectivity_request_service: AbstractParseConnectivityService,
        logger: Logger,
        resource_config: NetworkingResourceConfig,
        cli_configurator: AristaCLIConfigurator,
    ):
        super().__init__(parse_connectivity_request_service, logger)
        self._resource_config = resource_config
        self._cli_configurator = cli_configurator

    def _set_vlan(self, action: ConnectivityActionModel) -> ConnectivityActionResult:
        vlan_range = action.connection_params.vlan_id
        port_name = action.action_target.name
        qnq = action.connection_params.vlan_service_attrs.qnq
        c_tag = action.connection_params.vlan_service_attrs.ctag
        port_mode = action.connection_params.mode.name.lower()
        self._logger.info(
            f"Add VLAN(s) {vlan_range} for ports {port_name} configuration started"
        )
        self._logger.debug(
            f"Vlan range: {vlan_range}, Port name: {port_name}, "
            f"QNQ: {qnq}, C_tag: {c_tag}, Port_mode: {port_mode}"
        )

        with self._cli_configurator.config_mode_service() as config_service:
            iface_action = IFaceActions(config_service, self._logger)
            vlan_actions = AddRemoveVlanActions(config_service, self._logger)
            port_name = iface_action.get_port_name(port_name)
            vlan_actions.create_vlan(vlan_range)

            current_config = iface_action.get_current_interface_config(port_name)

            iface_action.enter_iface_config_mode(port_name)
            iface_action.clean_interface_switchport_config(current_config)
            vlan_actions.set_vlan_to_interface(
                vlan_range, port_mode, port_name, qnq, c_tag
            )
            current_config = iface_action.get_current_interface_config(port_name)
            if not vlan_actions.verify_interface_configured(vlan_range, current_config):
                raise Exception(
                    self.__class__.__name__,
                    f"[FAIL] VLAN(s) {vlan_range} configuration failed",
                )

        self._logger.info(f"VLAN(s) {vlan_range} configuration completed successfully")
        return ConnectivityActionResult.success_result(action, "Success")

    def _remove_vlan(self, action: ConnectivityActionModel) -> ConnectivityActionResult:
        vlan_range = action.connection_params.vlan_id
        port_name = action.action_target.name
        self._logger.info(
            f"Remove Vlan {vlan_range} for port {port_name} configuration started"
        )
        with self._cli_configurator.config_mode_service() as config_service:
            iface_action = IFaceActions(config_service, self._logger)
            vlan_actions = AddRemoveVlanActions(config_service, self._logger)
            port_name = iface_action.get_port_name(port_name)

            current_config = iface_action.get_current_interface_config(port_name)

            iface_action.enter_iface_config_mode(port_name)
            iface_action.clean_interface_switchport_config(current_config)
            current_config = iface_action.get_current_interface_config(port_name)
            if vlan_actions.verify_interface_configured(vlan_range, current_config):
                raise Exception(
                    self.__class__.__name__,
                    f"[FAIL] VLAN(s) {vlan_range} removing failed",
                )

        self._logger.info(f"VLAN(s) {vlan_range} removing completed successfully")
        return ConnectivityActionResult.success_result(action, "Success")
