"""Sensor platform for wallbox_modbus."""

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfPower,
    UnitOfElectricPotential,
)
from .const import DOMAIN
from .entity import WallboxModbusEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="max_available_current",
        name="Max available current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="max_available_power",
        name="Max available power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ac_current_rms",
        name="AC current RMS",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ac_voltage_rms",
        name="AC voltage RMS",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ac_active_power_rms",
        name="AC active power RMS",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="charger_state",
        name="Charger state",
        translation_key="charger_state",
    ),
    SensorEntityDescription(
        key="state_of_charge",
        name="State of charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        WallboxModbusSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class WallboxModbusSensor(WallboxModbusEntity, SensorEntity):
    """wallbox_modbus Sensor class."""

    def __init__(self, coordinator, entity_description) -> None:
        super().__init__(coordinator, entity_description)
        self._last_good_value = 0

    def _is_state_of_charge(self) -> bool:
        return self.entity_description.key == "state_of_charge"

    @property
    def assumed_state(self) -> bool:
        """Return True if unable to access real state of the entity."""
        return self._is_state_of_charge() and self.coordinator.data[self.entity_description.key] == 0

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        value = self.coordinator.data[self.entity_description.key]
        if self._is_state_of_charge():
            if value == 0:
                value = self._last_good_value
            else:
                self._last_good_value = value
        return value
