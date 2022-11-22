from __future__ import annotations

from datetime import timedelta

import requests

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, PLATFORMS


class DfpDataUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for the DFP integration."""

    config_entry: ConfigEntry
    last_data = {}
    platforms = PLATFORMS


    def __init__(self, api_url: str, station_id: str, hass: HomeAssistant) -> None:
        super().__init__(
            hass=hass, logger=LOGGER, name=DOMAIN, update_interval=timedelta(seconds=60)
        )
        self.api_url = api_url
        self.station_id = station_id


    def _update(self):
        # tankstation_id = self.config_entry.options.get(CONF_STATION_ID)

        response = requests.get(
            f"{self.api_url}/tankstation/by-id/{self.station_id}", timeout=60
        ).json()

        if "status" in response and response["status"] == 500:
            if "message" in response and "Job already active" in response["message"]:
                return self.last_data
            raise Exception("Something went wrong!")

        update_data = {}

        for price_obj in response["data"]["prices"]:
            if price_obj["fuelType"] not in update_data:
                update_data[price_obj["fuelType"]] = price_obj["price"]
        self.last_data = update_data
        return update_data

    async def _async_update_data(self) -> dict[str, dict[str, str | int]]:
        try:
            return await self.hass.async_add_executor_job(self._update)
        except Exception as exc:
            raise UpdateFailed(exc) from exc
