"""DataUpdateCoordinator for wallbox_modbus."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from wallbox_modbus import WallboxModbus

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
        await self.client.connect()
        self.data = await self.client.get_all_values()
        #print(self.data)
        return self.data

    async def async_shutdown(self) -> None:
        """Run shutdown clean up."""
        self.client.close()
        await super().async_shutdown()
