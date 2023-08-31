# Home Assistant - St Albans Rubbish Collection

This is a simple integration to pull rubbish collection information from St Albans Council's [notice board](https://gis.stalbans.gov.uk/NoticeBoard9/NoticeBoard.aspx). 

# Installation

1. [Find your UPRN](https://www.findmyaddress.co.uk/)
2. Clone this into your `config/custom_components` directory and restart Home Assistant
3. Add the integration, providing your UPRN.

You'll need some sensors to expose the state:

```yaml
template:
  - sensor:
     - unique_id: rubbish_recycling_next
       state: "{{as_timestamp(state_attr('sensor.stalbans_rubbish_collection_<your uprn>', 'CollectDomesticRecycling')['next']) | timestamp_custom('%d/%m/%Y %H:%M') }}"
       attributes:
         friendly_name: "Next recycling collection date"
  - sensor:
     - unique_id: rubbish_recycling_last
       state: "{{as_timestamp(state_attr('sensor.stalbans_rubbish_collection_<your uprn>', 'CollectDomesticRecycling')['last']) | timestamp_custom('%d/%m/%Y %H:%M') }}"
       attributes:
         friendly_name: "Last recycling collection date"
  - sensor:
     - unique_id: rubbish_refuse_next
       state: "{{as_timestamp(state_attr('sensor.stalbans_rubbish_collection_<your uprn>', 'CollectDomesticRefuse')['next']) | timestamp_custom('%d/%m/%Y %H:%M') }}"
       attributes:
         friendly_name: "Next refuse collection date"
  - sensor:
     - unique_id: rubbish_refuse_last
       state: "{{as_timestamp(state_attr('sensor.stalbans_rubbish_collection_<your uprn>', 'CollectDomesticRefuse')['last']) | timestamp_custom('%d/%m/%Y %H:%M') }}"
       attributes:
         friendly_name: "Last refuse collection date"
  - sensor:
     - unique_id: rubbish_food_next
       state: "{{as_timestamp(state_attr('sensor.stalbans_rubbish_collection_<your uprn>', 'CollectDomesticFood')['next']) | timestamp_custom('%d/%m/%Y %H:%M') }}"
       attributes:
         friendly_name: "Next food waste collection date"
  - sensor:
     - unique_id: rubbish_food_last
       state: "{{as_timestamp(state_attr('sensor.stalbans_rubbish_collection_<your uprn>', 'CollectDomesticFood')['last']) | timestamp_custom('%d/%m/%Y %H:%M') }}"
       attributes:
         friendly_name: "Last food waste collection date"
  - sensor:
     - unique_id: rubbish_garden_next
       state: "{{as_timestamp(state_attr('sensor.stalbans_rubbish_collection_<your uprn>', 'CollectDomesticPaidGarden')['next']) | timestamp_custom('%d/%m/%Y %H:%M') }}"
       attributes:
         friendly_name: "Next garden waste collection date"
  - sensor:
     - unique_id: rubbish_garden_last
       state: "{{as_timestamp(state_attr('sensor.stalbans_rubbish_collection_<your uprn>', 'CollectDomesticPaidGarden')['last']) | timestamp_custom('%d/%m/%Y %H:%M') }}"
       attributes:
         friendly_name: "Last garden waste collection date"
```
