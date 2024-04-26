"""WallboxModbusEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, VERSION
from .coordinator import WallboxModbusDataUpdateCoordinator


class WallboxModbusEntity(CoordinatorEntity):
    """WallboxModbusEntity class."""

    def __init__(self, coordinator: WallboxModbusDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        data = coordinator.config_entry.data
        self._unique_id = f"{data['serial_number']}-{data['part_number']}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._unique_id)},
            name=NAME,
            model=VERSION,
            manufacturer="Wallbox",
        )

    @property
    def unique_id(self):
        return self._unique_id