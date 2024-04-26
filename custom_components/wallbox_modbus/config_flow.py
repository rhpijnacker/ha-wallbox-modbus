"""Adds config flow for WallboxModbus."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers import selector

from .api import (
    WallboxModbusApiClient,
    WallboxModbusApiClientAuthenticationError,
    WallboxModbusApiClientCommunicationError,
    WallboxModbusApiClientError,
)
from .const import DOMAIN, LOGGER

import wallbox_modbus

class WallboxModbusFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for WallboxModbus."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                data = await self._connect_to_wallbox(
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                )
            except WallboxModbusApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except WallboxModbusApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=f"Wallbox {data['part_number']}-{data['serial_number']}",
                    data={
                        CONF_HOST: user_input[CONF_HOST],
                        CONF_PORT: user_input[CONF_PORT],
                        'serial_number': data['serial_number'],
                        'part_number': data['part_number'],
                    }
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(CONF_HOST),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {CONF_PORT: 502}).get(CONF_PORT),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            mode=selector.NumberSelectorMode.BOX
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _connect_to_wallbox(self, host: str, port: str) -> None:
        """ Validate connection details. """
        client = wallbox_modbus.WallboxModbus(host=host, port=port)
        await client.connect()
        return await client.get_all_values()
