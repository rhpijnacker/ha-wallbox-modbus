"""Number platform for wallbox_modbus."""

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfPower,
    UnitOfElectricPotential,
)
from .const import DOMAIN
from .entity import WallboxModbusEntity

CurrentSetpointEntityDescription = NumberEntityDescription(
    key="current_setpoint",
    name="Current setpoint",
    native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    device_class=NumberDeviceClass.CURRENT,
    native_min_value=-32,
    native_max_value=32,
    native_step=1,
    mode=NumberMode.BOX,
)
PowerSetpointEntityDescription = NumberEntityDescription(
    key="power_setpoint",
    name="Power setpoint",
    native_unit_of_measurement=UnitOfPower.WATT,
    device_class=NumberDeviceClass.POWER,
    native_min_value=-7400,
    native_max_value=7400,
    native_step=1,
    mode=NumberMode.BOX,
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([
        WallboxModbusCurrentSetpoint(
            coordinator=coordinator,
            entity_description=CurrentSetpointEntityDescription,
        ),
        WallboxModbusPowerSetpoint(
            coordinator=coordinator,
            entity_description=PowerSetpointEntityDescription,
        ),
    ])


class WallboxModbusNumber(WallboxModbusEntity, NumberEntity):
    """wallbox_modbus Number class."""

    @property
    def native_value(self) -> float:
        return self.coordinator.data[self.entity_description.key]


class WallboxModbusCurrentSetpoint(WallboxModbusNumber):

    @property
    def available(self) -> bool:
        return self.has_control() and self.coordinator.data['setpoint_type'] == 'current'

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.client.set_current_setpoint(int(value))
        await self.coordinator.async_request_refresh()


class WallboxModbusPowerSetpoint(WallboxModbusNumber):

    @property
    def available(self) -> bool:
        return self.has_control() and self.coordinator.data['setpoint_type'] == 'power'

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.client.set_power_setpoint(int(value))
        await self.coordinator.async_request_refresh()
