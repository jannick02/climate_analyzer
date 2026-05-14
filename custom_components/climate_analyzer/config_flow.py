import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import (
    DOMAIN, 
    CONF_ROOM_NAME, 
    CONF_TEMP_IN, 
    CONF_HUM_IN, 
    CONF_TEMP_OUT, 
    CONF_HUM_OUT, 
    CONF_WINDOW_SENSOR
)

class ClimateAnalyzerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Behandelt den Konfigurationsfluss für die Klima-Analyse."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Erster Schritt der Einrichtung über die Benutzeroberfläche."""
        errors = {}

        if user_input is not None:
            # Überprüfung, ob der Raumname bereits vergeben ist
            await self.async_set_unique_id(user_input[CONF_ROOM_NAME])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input[CONF_ROOM_NAME], 
                data=user_input
            )

        # Definition des Eingabe-Schemas für den Dialog
        # Die Keys hier (z.B. CONF_TEMP_IN) müssen exakt mit den Keys in der strings.json übereinstimmen
        data_schema = vol.Schema({
            vol.Required(CONF_ROOM_NAME): str,
            vol.Required(CONF_TEMP_IN): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
            vol.Required(CONF_HUM_IN): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="humidity")
            ),
            vol.Required(CONF_TEMP_OUT): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
            vol.Required(CONF_HUM_OUT): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="humidity")
            ),
            vol.Optional(CONF_WINDOW_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="binary_sensor", device_class="window")
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
