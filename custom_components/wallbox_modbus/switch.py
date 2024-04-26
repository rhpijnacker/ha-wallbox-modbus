"""Switch platform for wallbox_modbus."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .const import DOMAIN
from .entity import WallboxModbusEntity

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="is_auto_charging_discharging_enabled",
        name="Automatically start (dis)charging",
        icon="mdi:battery-charging",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        WallboxModbusSwitch(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class WallboxModbusSwitch(WallboxModbusEntity, SwitchEntity):
    """wallbox_modbus switch class."""

    @property
    def available(self) -> bool:
        return self.has_control()

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.coordinator.data.get("is_auto_charging_discharging_enabled")

    async def async_turn_on(self, **_: any) -> None:
        """Turn on the switch."""
        await self.coordinator.client.enable_auto_charging_discharging()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: any) -> None:
        """Turn off the switch."""
        await self.coordinator.client.disable_auto_charging_discharging()
        await self.coordinator.async_request_refresh()
