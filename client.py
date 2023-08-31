"""Client for the St Albans Veolia dashboard."""
import logging
from datetime import datetime
import requests
from homeassistant.core import HomeAssistant

from .const import ENDPOINT_URI

_LOGGER = logging.getLogger(__name__)


class StAlbansRubbishCollectionsClientException(Exception):
    """Base exception class."""


class StAlbansRubbishCollectionsClient:
    """Client for the St Albans Veolia dashboard."""

    def __init__(self, hass: HomeAssistant, uprn) -> None:
        self.hass = hass
        self.uprn = uprn
        self.headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br"
        }
        self.data = {
            "uprn": self.uprn,
            "noticeBoard": "default"
        }

    def _parse_date(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    
    def _camel_case(self, a_string):
        words = a_string.split()
        return words[0] + ''.join(i.capitalize() for i in words[1:])

    def _process_data(self, json_response):
        """Process the data from the API into something interesting"""

        collection_data = {}

        for collection in json_response["d"]:
            if collection["ServiceHeaders"] and len(collection["ServiceHeaders"]) > 0:
                collection = collection["ServiceHeaders"][0]

                collection_data[self._camel_case(collection["TaskType"])] = {
                    "name": collection["TaskType"],
                    "last": self._parse_date(collection["Last"]),
                    "next": self._parse_date(collection["Next"]),
                    "scheduleDescription": collection["ScheduleDescription"]
                }

        return collection_data
    
    def _sync_request(self):
        return requests.post(ENDPOINT_URI, headers=self.headers, json=self.data)

    async def async_get_data(self):
        """Data refresh request from the coordinator"""
        try:
            _LOGGER.info("Requesting data for %s", self.uprn)
            response = await self.hass.async_add_executor_job(self._sync_request)
        except Exception as err:
            _LOGGER.exception("Exception whilst fetching data: ")
            raise StAlbansRubbishCollectionsClientException("Unknown Error") from err

        try:
            _LOGGER.info("Processing response")
            data = self._process_data(response.json())
        except Exception as err:
            _LOGGER.exception("Exception whilst processing data: ")
            _LOGGER.debug("Response dump: %s", response)
            raise StAlbansRubbishCollectionsClientException("unexpected data from api") from err

        return data
