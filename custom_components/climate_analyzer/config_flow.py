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
    CONF_WINDOW_SENSOR,
    CONF_IDEAL_TEMP,
    CONF_IDEAL_ABS_HUM,
    CONF_MAX_ABS_HUM
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
                selector.EntitySelectorConfig(domain="binary_sensor")
            ),
            # Neue Felder für die Idealwerte mit Standardwerten
            vol.Required(CONF_IDEAL_TEMP, default=21.0): selector.NumberSelector(
                selector.NumberSelectorConfig(mode="box", step=0.5, unit_of_measurement="°C")
            ),
            vol.Required(CONF_IDEAL_ABS_HUM, default=9.0): selector.NumberSelector(
                selector.NumberSelectorConfig(mode="box", step=0.1, unit_of_measurement="g/m³")
            ),
            vol.Required(CONF_MAX_ABS_HUM, default=12.0): selector.NumberSelector(
                selector.NumberSelectorConfig(mode="box", step=0.1, unit_of_measurement="g/m³")
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
