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
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the lock platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        WallboxModbusLock(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class WallboxModbusLock(WallboxModbusEntity, LockEntity):
    """wallbox_modbus Lock class."""

    def __init__(
        self,
        coordinator: WallboxModbusDataUpdateCoordinator,
        entity_description: LockEntityDescription,
    ) -> None:
        """Initialize the lock class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._unique_id = f"{self._unique_id}-{self.entity_description.key}"

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
