"""Config flow for the St Albans rubbish collection days component."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .client import (
    StAlbansRubbishCollectionsClient,
    StAlbansRubbishCollectionsClientException
)
from .const import CONF_UPRN, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_UPRN): str
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    def _validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
        """Validate the user input allows us to connect.

        Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
        """

        try:
            StAlbansRubbishCollectionsClient(data[CONF_UPRN]).async_get_data()
        except StAlbansRubbishCollectionsClientException as err:
            _LOGGER.exception(err)
            raise InvalidUPRN() from err

        # Return info that you want to store in the config entry.
        return {"title": f'Rubbish collection for UPRN {data[CONF_UPRN]}'}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        user_input[CONF_UPRN] = user_input[CONF_UPRN].strip()

        errors = {}

        try:
            info = self._validate_input(self.hass, user_input)
        except InvalidUPRN:
            errors["base"] = "invalid_uprn"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class InvalidUPRN(HomeAssistantError):
    """Error to indicate the UPRN is invalid."""
