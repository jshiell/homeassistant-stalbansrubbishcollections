"""Constants for the St Albans rubbish collection days component."""

DOMAIN = "stalbansrubbishcollections"
DOMAIN_DATA = f"{DOMAIN}_data"

SENSOR = "sensor"
PLATFORMS = [SENSOR]

ENDPOINT_URI = "https://gis.stalbans.gov.uk/NoticeBoard9/VeoliaProxy.NoticeBoard.asmx/GetServicesByUprnAndNoticeBoard"

CONF_UPRN = "uprn"

POLLING_INTERVAL_MINUTES = 2
DATA_REFRESH_MINUTES = 60
