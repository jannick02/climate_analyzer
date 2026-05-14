import math
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    DOMAIN, 
    CONF_ROOM_NAME, 
    CONF_TEMP_IN, 
    CONF_HUM_IN, 
    CONF_TEMP_OUT, 
    CONF_HUM_OUT, 
    CONF_WINDOW_SENSOR
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup Sensoren aus dem Config Flow."""
    config = config_entry.data
    room = config.get(CONF_ROOM_NAME)
    
    # Wir fügen nur noch EINEN Hauptsensor pro Raum hinzu
    async_add_entities([ClimateAnalyzerEntity(hass, config, room)])

def calculate_abs_hum(temp, hum):
    """Die mathematische Formel für absolute Feuchtigkeit."""
    try:
        t = float(temp)
        h = float(hum)
        return (13.247 * h * 10**((7.5 * t) / (237.3 + t)) / (273.15 + t))
    except (ValueError, TypeError):
        return 0.0

class ClimateAnalyzerEntity(SensorEntity):
    """Eine zusammengefasste Entität für die gesamte Klima-Analyse."""
    
    _attr_has_entity_name = True

    def __init__(self, hass, config, room):
        self.hass = hass
        self._config = config
        self._room = room
        
        self._attr_name = "Status" # Der Name der Entität innerhalb des Geräts
        self._attr_unique_id = f"climate_analyzer_{room.lower()}"
        self._attr_icon = "mdi:home-analytics"

        # Gruppiert die Entität in ein "Gerät" (Device) in der Home Assistant UI
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=f"Klima Analyse {room}",
            manufacturer="Climate Analyzer",
            model="Raumsensor"
        )

    async def async_added_to_hass(self):
        """Wird aufgerufen, wenn die Entität zu Home Assistant hinzugefügt wurde.
        Hier registrieren wir die automatischen Updates."""
        
        entities_to_track = [
            self._config.get(CONF_TEMP_IN),
            self._config.get(CONF_HUM_IN),
            self._config.get(CONF_TEMP_OUT),
            self._config.get(CONF_HUM_OUT),
            self._config.get(CONF_WINDOW_SENSOR)
        ]
        
        # Leere Einträge herausfiltern, falls z.B. kein Fensterkontakt definiert wurde
        entities_to_track = [e for e in entities_to_track if e is not None]

        @callback
        def async_update_callback(event):
            """Wird getriggert, sobald sich ein Quellsensor ändert."""
            self.async_schedule_update_ha_state(True)

        self.async_on_remove(
            async_track_state_change_event(
                self.hass, entities_to_track, async_update_callback
            )
        )

    def _get_float_state(self, entity_id, default=0.0):
        """Hilfsfunktion: Liest den Status sicher als Float aus und verhindert Abstürze."""
        if not entity_id:
            return default
        state = self.hass.states.get(entity_id)
        if state and state.state not in ("unknown", "unavailable", None):
            try:
                return float(state.state)
            except ValueError:
                pass
        return default

    def _get_window_state(self):
        """Hilfsfunktion: Prüft, ob das Fenster offen ist."""
        entity_id = self._config.get(CONF_WINDOW_SENSOR)
        if not entity_id:
            return False
        state = self.hass.states.get(entity_id)
        return state and state.state == "on"

    @property
    def native_value(self):
        """Der Hauptstatus der Entität (Die Empfehlung)."""
        t_in = self._get_float_state(self._config.get(CONF_TEMP_IN), 21.0)
        t_out = self._get_float_state(self._config.get(CONF_TEMP_OUT), 15.0)
        h_in = self._get_float_state(self._config.get(CONF_HUM_IN), 50.0)
        h_out = self._get_float_state(self._config.get(CONF_HUM_OUT), 50.0)
        win = self._get_window_state()

        abs_in = calculate_abs_hum(t_in, h_in)
        abs_out = calculate_abs_hum(t_out, h_out)
        
        temp_comfort = 22.0
        hum_max = 12.0

        if win:
            if t_out > t_in and t_in > temp_comfort: return "Fenster zu! (Hitze)"
            if abs_out > abs_in and abs_in > hum_max: return "Fenster zu! (Feuchte)"
            return "Fenster offen lassen"
        else:
            if t_in > temp_comfort and t_out < t_in: return "Fenster auf! (Abkühlen)"
            if abs_in > hum_max and abs_out < abs_in: return "Fenster auf! (Entfeuchten)"
            return "Fenster zu lassen"

    @property
    def extra_state_attributes(self):
        """Hier werden alle anderen Werte als Attribute angehängt."""
        t_in = self._get_float_state(self._config.get(CONF_TEMP_IN), 21.0)
        h_in = self._get_float_state(self._config.get(CONF_HUM_IN), 50.0)
        t_out = self._get_float_state(self._config.get(CONF_TEMP_OUT), 15.0)
        h_out = self._get_float_state(self._config.get(CONF_HUM_OUT), 50.0)

        abs_in = calculate_abs_hum(t_in, h_in)
        abs_out = calculate_abs_hum(t_out, h_out)

        # Score Berechnung
        t_pen = abs(t_in - 21) * 6
        h_pen = abs(abs_in - 9) * 9
        score = max(0, round(100 - t_pen - h_pen))

        # Delta Berechnung
        delta = round(t_out - t_in, 1)

        return {
            "score": score,
            "score_unit": "%",
            "absolute_humidity_in": round(abs_in, 2),
            "absolute_humidity_out": round(abs_out, 2),
            "absolute_humidity_unit": "g/m³",
            "temp_delta": delta,
            "temp_delta_unit": "°C",
            "window_open": self._get_window_state()
        }
