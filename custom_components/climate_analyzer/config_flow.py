import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_ROOM_NAME

class ClimateAnalyzerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_ROOM_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_ROOM_NAME): str,
                vol.Required("temp_in"): str,
                vol.Required("hum_in"): str,
                vol.Required("temp_out"): str,
                vol.Required("hum_out"): str,
                vol.Required("window_sensor"): str,
            })
        )
