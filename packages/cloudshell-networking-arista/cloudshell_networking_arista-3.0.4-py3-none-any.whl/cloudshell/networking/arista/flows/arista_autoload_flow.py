from __future__ import annotations

import os
from logging import Logger
from typing import TYPE_CHECKING

from cloudshell.shell.core.driver_context import AutoLoadDetails
from cloudshell.shell.flows.autoload.basic_flow import AbstractAutoloadFlow
from cloudshell.snmp.autoload.generic_snmp_autoload import GenericSNMPAutoload
from cloudshell.snmp.snmp_configurator import EnableDisableSnmpConfigurator

if TYPE_CHECKING:
    from cloudshell.shell.standards.networking.autoload_model import (
        NetworkingResourceModel,
    )


class AristaAutoloadFlow(AbstractAutoloadFlow):
    def __init__(
        self,
        snmp_configurator: EnableDisableSnmpConfigurator,
        logger: Logger,
    ):
        super().__init__(logger)
        self._snmp_configurator = snmp_configurator

    def _autoload_flow(
        self, supported_os: list[str], resource_model: NetworkingResourceModel
    ) -> AutoLoadDetails:
        with self._snmp_configurator.get_service() as snmp_service:
            autoload_handler = GenericSNMPAutoload(snmp_service, self._logger)
            snmp_service.add_mib_folder_path(
                os.path.join(os.path.dirname(__file__), "..", "snmp", "mibs")
            )
            return autoload_handler.discover(supported_os, resource_model)
