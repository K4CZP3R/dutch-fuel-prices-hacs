"""Adds config flow for Blueprint."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
import requests

from .const import (
    CONF_API_URL,
    CONF_STATION_ID,
    DOMAIN,
    OPT_FUEL_TYPES,
    OPT_STATION_NAME,
    PLATFORMS,
)


class DfpFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Dfp."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_tankstation(
                user_input[CONF_API_URL], user_input[CONF_STATION_ID]
            )
            if valid is not None:
                return self.async_create_entry(
                    title=valid[OPT_STATION_NAME],
                    data=user_input,
                    options={
                        OPT_FUEL_TYPES: valid[OPT_FUEL_TYPES],
                        OPT_STATION_NAME: valid[OPT_STATION_NAME],
                    },
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_API_URL] = "https://dfp.k4czp3r.xyz"
        user_input[CONF_STATION_ID] = 0

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BlueprintOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_URL, default=user_input[CONF_API_URL]): str,
                    vol.Required(CONF_STATION_ID, default=user_input[CONF_STATION_ID]): int,
                }
            ),
            errors=self._errors,
        )

    async def _test_tankstation(self, api_url, station_id) -> None | str:
        """Return true if credentials is valid."""
        try:

            response = await self.hass.async_add_executor_job(
                requests.get, f"{api_url}/tankstation/by-id/{station_id}"
            )
            data = response.json()

            if "status" in data and data["status"] == 500:
                raise Exception("Invalid api_url or station_id")
            tank_station_name = "{} {}".format(
                data["data"]["city"], data["data"]["name"]
            )

            fuel_types = []

            prices = data["data"]["prices"]
            for price in prices:
                fuel_types.append(price["fuelType"])

            return {OPT_STATION_NAME: tank_station_name, OPT_FUEL_TYPES: fuel_types}
        except Exception:  # pylint: disable=broad-except
            pass
        return None


class BlueprintOptionsFlowHandler(config_entries.OptionsFlow):
    """Blueprint config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.options.get(OPT_STATION_NAME),
            data=self.options
        )
