"""Constants for dfp."""

import logging

LOGGER = logging.getLogger(__package__)

# Base component constants
NAME = "Dutch Fuel Prices"
DOMAIN = "dfp"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ATTRIBUTION = "Data provided by dutch-fuel-prices-api"
ISSUE_URL = "https://github.com/K4CZP3R/dutch-fuel-prices-hacs/issues"

# Icons
ICON = "mdi:fuel"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_API_URL = "api_url"
CONF_STATION_ID = "station_id"
OPT_FUEL_TYPES = "fuel_types"
OPT_STATION_NAME = "station_name"
# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
