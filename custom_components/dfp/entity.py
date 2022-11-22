"""DfpEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.dfp.coordinator import DfpDataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import DOMAIN, NAME, ATTRIBUTION, VERSION
from homeassistant.helpers.entity import DeviceInfo


class DfpEntity(CoordinatorEntity[DfpDataUpdateCoordinator]):
    """Representation of a Steam entity."""

    _attr_attribution = "Data provided by dfp.k4czp3r.xyz"

    @property
    def icon(self) -> str | None:
        return "mdi:fuel"

    def __init__(self, coordinator: DfpDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            configuration_url="https://github.com/K4CZP3R/dutch-fuel-prices-api",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer=NAME,
            name=NAME,
            model=VERSION
        )

        self._attr_extra_state_attributes = {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }


# class DfpEntity(CoordinatorEntity[DfpDataUpdateCoordinator]):
#     def __init__(self, coordinator: DfpDataUpdateCoordinator, config_entry):
#         super().__init__(coordinator)
#         self.config_entry = config_entry

#     @property
#     def device_info(self):
#         return {
#             "identifiers": {(DOMAIN, self.unique_id)},
#             "name": NAME,
#             "model": VERSION,
#             "manufacturer": NAME,
#             "entry_type": DeviceEntryType.SERVICE
#         }

#     @property
#     def extra_state_attributes(self):
#         """Return the state attributes."""
#         return {
#             "attribution": ATTRIBUTION,
#             "id": str(self.coordinator.data.get("id")),
#             "integration": DOMAIN,
#         }
