"""Number platform for wallbox_modbus."""

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfPower,
)
from .const import DOMAIN
from .entity import WallboxModbusEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    max_current = coordinator.data.get('max_available_current', 32)
    entity_description = NumberEntityDescription(
        key="current_setpoint",
        name="Current setpoint",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=NumberDeviceClass.CURRENT,
        native_min_value=6,
        native_max_value=max_current,
        native_step=1,
        mode=NumberMode.SLIDER,
    )
    current_entity = WallboxModbusCurrentSetpoint(
        coordinator=coordinator,
        entity_description=entity_description,
    )

    max_power = coordinator.data.get('max_available_power', 7400)
    entity_description = NumberEntityDescription(
        key="power_setpoint",
        name="Power setpoint",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=NumberDeviceClass.POWER,
        native_min_value=1380,
        native_max_value=max_power,
        native_step=10,
        mode=NumberMode.BOX,
    )
    power_entity = WallboxModbusPowerSetpoint(
        coordinator=coordinator,
        entity_description=entity_description,
    )

    async_add_devices([current_entity, power_entity])


class WallboxModbusNumber(WallboxModbusEntity, NumberEntity):
    """wallbox_modbus Number class."""

    @property
    def native_value(self) -> float:
        return abs(self.coordinator.data[self.entity_description.key])


class WallboxModbusCurrentSetpoint(WallboxModbusNumber):

    @property
    def available(self) -> bool:
        return self.has_control() and self.coordinator.data['setpoint_type'] == 'current'

    async def async_set_native_value(self, value: float) -> None:
        charger_state = self.coordinator.data.get("charger_state")
        factor = -1 if charger_state == "discharging" else 1
        await self.coordinator.client.set_current_setpoint(factor * int(value))
        await self.coordinator.async_request_refresh()


class WallboxModbusPowerSetpoint(WallboxModbusNumber):

    @property
    def available(self) -> bool:
        return self.has_control() and self.coordinator.data['setpoint_type'] == 'power'

    async def async_set_native_value(self, value: float) -> None:
        charger_state = self.coordinator.data.get("charger_state")
        factor = -1 if charger_state == "discharging" else 1
        await self.coordinator.client.set_power_setpoint(factor * int(value))
        await self.coordinator.async_request_refresh()
