"""Switch platform for wallbox_modbus."""

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .const import DOMAIN
from .entity import WallboxModbusEntity

AutoChargingSwitchEntityDescription = SwitchEntityDescription(
    key="is_auto_charging_discharging_enabled",
    name="Automatically start (dis)charging",
    icon="mdi:battery-charging",
)
StartChargingSwitchEntityDescription = SwitchEntityDescription(
    key="charge_discharge",
    name="Start (dis)charging",
    icon="mdi:battery-charging",
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([
        WallboxModbusAutoChargingSwitch(
            coordinator=coordinator,
            entity_description=AutoChargingSwitchEntityDescription,
        ),
        WallboxModbusChargeDischargeSwitch(
            coordinator=coordinator,
            entity_description=StartChargingSwitchEntityDescription
        ),
    ])


class WallboxModbusAutoChargingSwitch(WallboxModbusEntity, SwitchEntity):
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


class WallboxModbusChargeDischargeSwitch(WallboxModbusEntity, SwitchEntity):
    """wallbox_modbus switch class."""

    @property
    def available(self) -> bool:
        return self.has_control()

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.get("charger_state") == "charging"

    # States: "charging", "connected_not_charging", "no_car_connected", "connected_waiting_for_car_demand"

    async def async_turn_on(self, **_: any) -> None:
        await self.coordinator.client.start_charging_discharging()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: any) -> None:
        await self.coordinator.client.stop_charging_discharging()
        await self.coordinator.async_request_refresh()
