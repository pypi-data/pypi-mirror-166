from __future__ import annotations

from typing import TYPE_CHECKING, Union

from cloudshell.snmp.snmp_configurator import EnableDisableSnmpFlowInterface
from cloudshell.snmp.snmp_parameters import SNMPV3Parameters

from ..command_actions.enable_disable_snmp_actions import EnableDisableSnmpActions

if TYPE_CHECKING:
    from logging import Logger

    from cloudshell.snmp.snmp_parameters import SNMPReadParameters, SNMPWriteParameters

    from ..cli.arista_cli_configurator import AristaCLIConfigurator

    SnmpParams = Union[SNMPReadParameters, SNMPWriteParameters, SNMPV3Parameters]


class AristaEnableDisableSNMPFlow(EnableDisableSnmpFlowInterface):
    def __init__(
        self,
        cli_configurator: AristaCLIConfigurator,
        logger: Logger,
        vrf_name: str = None,
    ):
        self._cli_configurator = cli_configurator
        self._logger = logger
        self._vrf_name = vrf_name

    def enable_snmp(self, snmp_parameters: SnmpParams):
        if (
            hasattr(snmp_parameters, "snmp_community")
            and not snmp_parameters.snmp_community
        ):
            message = "SNMP community cannot be empty"
            self._logger.error(message)
            raise Exception(self.__class__.__name__, message)

        if isinstance(snmp_parameters, SNMPV3Parameters):
            raise Exception(self.__class__.__name__, "Do not support SNMP V3")

        with self._cli_configurator.config_mode_service() as cli_service:
            snmp_actions = EnableDisableSnmpActions(cli_service, self._logger)

            if self._vrf_name and not snmp_actions.is_configured_vrf(self._vrf_name):
                snmp_actions.enable_vrf_for_snmp_server(self._vrf_name)

            if snmp_actions.is_configured(snmp_parameters.snmp_community):
                self._logger.debug(
                    'SNMP Community "{}" already configured'.format(
                        snmp_parameters.snmp_community
                    )
                )
                return

            snmp_actions.enable_snmp(snmp_parameters.snmp_community)

            self._logger.info("Start verification of SNMP config")
            if not snmp_actions.is_configured(snmp_parameters.snmp_community):
                raise Exception(
                    self.__class__.__name__,
                    "Failed to create SNMP community." " Please check Logs for details",
                )

    def disable_snmp(
        self,
        snmp_parameters: (SNMPReadParameters | SNMPWriteParameters | SNMPV3Parameters),
    ):
        if (
            hasattr(snmp_parameters, "snmp_community")
            and not snmp_parameters.snmp_community
        ):
            message = "SNMP community cannot be empty"
            self._logger.error(message)
            raise Exception(self.__class__.__name__, message)

        if isinstance(snmp_parameters, SNMPV3Parameters):
            raise Exception(self.__class__.__name__, "Do not support SNMP V3")

        with self._cli_configurator.config_mode_service() as config_service:
            snmp_actions = EnableDisableSnmpActions(config_service, self._logger)

            self._logger.debug("Start Disable SNMP")
            snmp_actions.disable_snmp(snmp_parameters.snmp_community)

            if snmp_actions.is_configured(snmp_parameters.snmp_community):
                raise Exception(
                    self.__class__.__name__,
                    "Failed to remove SNMP community." " Please check Logs for details",
                )
