"""Lock platform for wallbox_modbus."""

from homeassistant.components.lock import LockEntity, LockEntityDescription

from .const import DOMAIN
from .coordinator import WallboxModbusDataUpdateCoordinator
from .entity import WallboxModbusEntity

ENTITY_DESCRIPTIONS = (
    LockEntityDescription(
        key="control",
        name="Take control",
    ),
    LockEntityDescription(
        key="is_charger_locked",
        name="Lock charger",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the lock platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            WallboxModbusControl(
                coordinator=coordinator,
                entity_description=ENTITY_DESCRIPTIONS[0],
            ),
            WallboxModbusLock(
                coordinator=coordinator,
                entity_description=ENTITY_DESCRIPTIONS[1],
            ),
        ]
    )


class WallboxModbusControl(WallboxModbusEntity, LockEntity):
    """wallbox_modbus Control class."""

    @property
    def is_locked(self) -> bool:
        """Return the status of the lock."""
        return self.coordinator.data['control'] == 'remote'

    async def async_lock(self, **_: any) -> None:
        await self.coordinator.client.take_control()
        await self.coordinator.async_request_refresh()

    async def async_unlock(self, **_: any) -> None:
        await self.coordinator.client.release_control()
        await self.coordinator.async_request_refresh()


class WallboxModbusLock(WallboxModbusEntity, LockEntity):
    """wallbox_modbus Lock class."""

    @property
    def available(self) -> bool:
        return self.has_control()

    @property
    def is_locked(self) -> bool:
        """Return the status of the lock."""
        return self.coordinator.data['is_charger_locked']

    async def async_lock(self, **_: any) -> None:
        await self.coordinator.client.lock_charger()
        await self.coordinator.async_request_refresh()

    async def async_unlock(self, **_: any) -> None:
        await self.coordinator.client.unlock_charger()
        await self.coordinator.async_request_refresh()
