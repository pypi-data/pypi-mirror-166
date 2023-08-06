from __future__ import annotations

from typing import TYPE_CHECKING

from cloudshell.shell.flows.configuration.basic_flow import (
    AbstractConfigurationFlow,
    ConfigurationType,
    RestoreMethod,
)
from cloudshell.shell.flows.utils.url import BasicLocalUrl

from ..command_actions.system_actions import SystemActions

if TYPE_CHECKING:
    from logging import Logger
    from typing import Union

    from cloudshell.shell.flows.utils.url import RemoteURL
    from cloudshell.shell.standards.networking.resource_config import (
        NetworkingResourceConfig,
    )

    from ..cli.arista_cli_configurator import AristaCLIConfigurator

    Url = Union[RemoteURL, BasicLocalUrl]


class AristaConfigurationFlow(AbstractConfigurationFlow):
    SUPPORTED_CONFIGURATION_TYPES = {
        ConfigurationType.RUNNING,
        ConfigurationType.STARTUP,
    }
    SUPPORTED_RESTORE_METHODS = {RestoreMethod.OVERRIDE}
    FILE_SYSTEM_SCHEME = "flash:"

    def __init__(
        self,
        logger: Logger,
        resource_config: NetworkingResourceConfig,
        cli_configurator: AristaCLIConfigurator,
    ):
        super().__init__(logger, resource_config)
        self._cli_configurator = cli_configurator

    @property
    def file_system(self) -> str:
        return self.FILE_SYSTEM_SCHEME

    def _save_flow(
        self,
        file_dst_url: Url,
        configuration_type: ConfigurationType,
        vrf_management_name: str | None,
    ) -> str | None:
        conf_type = configuration_type.value
        with self._cli_configurator.enable_mode_service() as enable_session:
            save_action = SystemActions(enable_session, self._logger)
            action_map = save_action.prepare_action_map(
                BasicLocalUrl.from_str(f"{self.file_system}/{conf_type}"),
                file_dst_url,
            )
            save_action.copy(
                conf_type,
                str(file_dst_url),
                vrf=vrf_management_name,
                action_map=action_map,
            )
        return None

    def _restore_flow(
        self,
        config_path: Url,
        configuration_type: ConfigurationType,
        restore_method: RestoreMethod,
        vrf_management_name: str | None,
    ) -> None:
        path = str(config_path)

        with self._cli_configurator.enable_mode_service() as enable_session:
            restore_action = SystemActions(enable_session, self._logger)
            copy_action_map = restore_action.prepare_action_map(
                config_path,
                BasicLocalUrl.from_str(
                    f"{self.file_system}/{configuration_type.value}"
                ),
            )

            if configuration_type == ConfigurationType.RUNNING:
                restore_action.override_running(
                    path, vrf_management_name, action_map=copy_action_map
                )
            else:
                restore_action.copy(
                    path,
                    configuration_type.value + "-config",
                    vrf_management_name,
                    action_map=copy_action_map,
                )
