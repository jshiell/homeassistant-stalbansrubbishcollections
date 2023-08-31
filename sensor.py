"""Platform for sensor integration."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
import time

import async_timeout

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .client import StAlbansRubbishCollectionsClient
from .const import CONF_UPRN, DOMAIN, POLLING_INTERVAL_MINUTES, DATA_REFRESH_MINUTES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Config for component."""

    uprn = entry.data.get(CONF_UPRN)

    _LOGGER.info(f"Setting up sensor for UPRN {uprn}")

    coordinator = StAlbansRubbishCollectionsScheduleCoordinator(hass, uprn)

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([StAlbansRubbishCollectionsSchedule(coordinator)])


class StAlbansRubbishCollectionsScheduleCoordinator(DataUpdateCoordinator):
    description: str = None
    friendly_name: str = None
    sensor_name: str = None

    def __init__(self, hass, uprn):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(minutes=POLLING_INTERVAL_MINUTES),
        )
        self.uprn = uprn
        self.api_client = StAlbansRubbishCollectionsClient(hass, uprn)

        self.last_data_refresh = None

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        # chek whether we should refresh the data of not
        if (
            self.last_data_refresh is None
            or (
                self.last_data_refresh is not None
                and (time.time() - self.last_data_refresh) > DATA_REFRESH_MINUTES * 60
            )
        ):
            async with async_timeout.timeout(30):
                data = await self.api_client.async_get_data()
                self.last_data_refresh = time.time()

            if self.sensor_name is None:
                self.sensor_name = f"stalbans_rubbish_collection_{self.uprn}"

            if self.description is None:
                self.description = (
                    f"Rubbish collection for UPRN {self.uprn}"
                )

            if self.friendly_name is None:
                self.friendly_name = f"Rubbish collection for UPRN {self.uprn}"

            data["name"] = self.sensor_name
            data["description"] = self.description
            data["friendly_name"] = self.friendly_name

        else:
            data = self.data

        return data


class StAlbansRubbishCollectionsSchedule(CoordinatorEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    attribution = "This uses National Rail Darwin Data Feeds"

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.entity_id = f"sensor.{coordinator.data['name'].lower()}"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return self.coordinator.data["name"]

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data["next_train_expected"]
