"""Sensor platform for dpf."""
from homeassistant.components.sensor import SensorEntity

from custom_components.dfp.coordinator import DfpDataUpdateCoordinator

from .const import (
    CONF_STATION_ID,
    DOMAIN,
    OPT_FUEL_TYPES,
    OPT_STATION_NAME
)
from .entity import DfpEntity

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.helpers.typing import StateType


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    print(entry.options[OPT_FUEL_TYPES], "FUEL TYPES")

    async_add_devices(
        DfpSensor(
            coordinator,
            entry.data.get(CONF_STATION_ID),
            fuel_type,
            entry.options[OPT_STATION_NAME],
        )
        for fuel_type in entry.options[OPT_FUEL_TYPES]
    )


class DfpSensor(DfpEntity, SensorEntity):
    """A class for the Dfp tankstation"""

    def __init__(
        self,
        coordinator: DfpDataUpdateCoordinator,
        tankstation_id: int,
        fuel_type: str,
        name: str,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = SensorEntityDescription(
            key=fuel_type,
            name=f"DFP {fuel_type} ({name})",
            icon="mdi:fuel",
            state_class=SensorStateClass.MEASUREMENT,
            unit_of_measurement="€/L",
        )
        self._attr_unique_id = f"sensor.dfp_{tankstation_id}_{fuel_type}"

    @property
    def native_value(self) -> StateType:
        if self.entity_description.key in self.coordinator.data:
            return self.coordinator.data[self.entity_description.key]
        return None
