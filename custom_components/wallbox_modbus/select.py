"""Number platform for wallbox_modbus."""

from homeassistant.components.select import (
    SelectEntity,
    SelectEntityDescription,
)

from .const import DOMAIN
from .entity import WallboxModbusEntity

SetpointEntityDescription = SelectEntityDescription(
    key="setpoint_type",
    name="Setpoint",
    options=["Current", "Power"],
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([
        WallboxModbusSetpointSelect(
            coordinator=coordinator,
            entity_description=SetpointEntityDescription,
        ),
    ])


class WallboxModbusSetpointSelect(WallboxModbusEntity, SelectEntity):
    """wallbox_modbus Setpoint Select class."""

    @property
    def available(self) -> bool:
        return self.has_control()

    @property
    def current_option(self) -> str | None:
        return self.coordinator.data[self.entity_description.key].capitalize()

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.client.set_setpoint_type(0 if option == "Current" else 1)
        await self.coordinator.async_request_refresh()
