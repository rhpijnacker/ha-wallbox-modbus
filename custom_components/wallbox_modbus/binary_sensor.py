"""Binary sensor platform for wallbox_modbus."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import DOMAIN
from .coordinator import WallboxModbusDataUpdateCoordinator
from .entity import WallboxModbusEntity

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="wallbox_modbus",
        name="Wallbox Modbus Binary Sensor",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        WallboxModbusBinarySensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class WallboxModbusBinarySensor(WallboxModbusEntity, BinarySensorEntity):
    """wallbox_modbus binary_sensor class."""

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get("title", "") == "foo"
