"""DataUpdateCoordinator for wallbox_modbus."""
from __future__ import annotations

import asyncio
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from wallbox_modbus import WallboxModbus

from .api import (
    WallboxModbusApiClientAuthenticationError,
    WallboxModbusApiClientError,
)
from .const import DOMAIN, LOGGER


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class WallboxModbusDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    client: WallboxModbus
    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: WallboxModbus,
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            await self.client.connect()
            data = await self.client.get_all_values()
            print(data)
            return data
        except WallboxModbusApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except WallboxModbusApiClientError as exception:
            raise UpdateFailed(exception) from exception
