import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN, CONF_ROOM_NAME, CONF_TEMP_IN, CONF_HUM_IN, CONF_TEMP_OUT, CONF_HUM_OUT, CONF_WINDOW_SENSOR

class ClimateAnalyzerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_ROOM_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_ROOM_NAME): str,
                # Selektor für den Innentemperatur-Sensor
                vol.Required(CONF_TEMP_IN): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                # Selektor für Luftfeuchtigkeit Innen
                vol.Required(CONF_HUM_IN): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                # Selektor für Außentemperatur
                vol.Required(CONF_TEMP_OUT): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                # Selektor für Luftfeuchtigkeit Außen
                vol.Required(CONF_HUM_OUT): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                # Selektor für den Fensterkontakt
                vol.Required(CONF_WINDOW_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="binary_sensor")
                ),
            })
        )
