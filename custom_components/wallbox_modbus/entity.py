"""WallboxModbusEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, VERSION
from .coordinator import WallboxModbusDataUpdateCoordinator


class WallboxModbusEntity(CoordinatorEntity):
    """WallboxModbusEntity class."""

    def __init__(
        self,
        coordinator: WallboxModbusDataUpdateCoordinator,
        entity_description: EntityDescription
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        data = coordinator.config_entry.data
        self._device_id = f"{data['part_number']}-{data['serial_number']}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=NAME,
            model=VERSION,
            manufacturer="Wallbox",
        )
        self._attr_unique_id = f"{self._device_id}-{self.entity_description.key}"
        self.entity_id = f"wallbox_modbus.{data['serial_number']}_{self.entity_description.key}"
