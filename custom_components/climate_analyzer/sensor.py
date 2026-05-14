import math
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from .const import DOMAIN, CONF_ROOM_NAME

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup Sensoren aus dem Config Flow."""
    config = config_entry.data
    room = config.get(CONF_ROOM_NAME)
    
    # Wir erstellen eine Liste von Sensoren für dieses "Gerät"
    sensors = [
        ClimateStateSensor(hass, config, room),
        ClimateScoreSensor(hass, config, room),
        AbsoluteHumiditySensor(hass, config, room, "Indoor", config.get("temp_in"), config.get("hum_in")),
        AbsoluteHumiditySensor(hass, config, room, "Outdoor", config.get("temp_out"), config.get("hum_out")),
        DeltaSensor(hass, config, room)
    ]
    async_add_entities(sensors)

def calculate_abs_hum(temp, hum):
    """Die mathematische Formel für absolute Feuchtigkeit."""
    try:
        t = float(temp)
        h = float(hum)
        return (13.247 * h * 10**((7.5 * t) / (237.3 + t)) / (273.15 + t))
    except (ValueError, TypeError):
        return 0

class ClimateStateSensor(SensorEntity):
    """Der Hauptsensor für die Empfehlung (Fenster auf/zu)."""
    def __init__(self, hass, config, room):
        self._hass = hass
        self._config = config
        self._attr_name = f"Klima Analyse {room}"
        self._attr_unique_id = f"climate_state_{config.get(CONF_ROOM_NAME).lower()}"
        self._attr_icon = "mdi:home-analytics"

    @property
    def state(self):
        t_in = float(self._hass.states.get(self._config.get("temp_in")).state or 0)
        h_in = float(self._hass.states.get(self._config.get("hum_in")).state or 0)
        t_out = float(self._hass.states.get(self._config.get("temp_out")).state or 0)
        h_out = float(self._hass.states.get(self._config.get("hum_out")).state or 0)
        win = self._hass.states.is_state(self._config.get("window_sensor"), "on")

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

class ClimateScoreSensor(SensorEntity):
    """Berechnet den 0-100 Score."""
    def __init__(self, hass, config, room):
        self._hass = hass
        self._config = config
        self._attr_name = f"Klima Score {room}"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_unique_id = f"climate_score_{room.lower()}"

    @property
    def native_value(self):
        t_in = float(self._hass.states.get(self._config.get("temp_in")).state or 21)
        h_in = float(self._hass.states.get(self._config.get("hum_in")).state or 50)
        a_in = calculate_abs_hum(t_in, h_in)
        
        t_pen = abs(t_in - 21) * 6
        h_pen = abs(a_in - 9) * 9
        return max(0, round(100 - t_pen - h_pen))

class AbsoluteHumiditySensor(SensorEntity):
    """Eigener Sensor für absolute Feuchtigkeit."""
    def __init__(self, hass, config, room, location, t_entity, h_entity):
        self._hass = hass
        self._t_entity = t_entity
        self._h_entity = h_entity
        self._attr_name = f"Abs Feuchte {location} {room}"
        self._attr_native_unit_of_measurement = "g/m³"
        self._attr_unique_id = f"abs_hum_{location.lower()}_{room.lower()}"

    @property
    def native_value(self):
        t = self._hass.states.get(self._t_entity).state
        h = self._hass.states.get(self._h_entity).state
        return round(calculate_abs_hum(t, h), 2)

class DeltaSensor(SensorEntity):
    """Temperaturdifferenz."""
    def __init__(self, hass, config, room):
        self._hass = hass
        self._config = config
        self._attr_name = f"Temp Delta {room}"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_unique_id = f"temp_delta_{room.lower()}"

    @property
    def native_value(self):
        t_in = float(self._hass.states.get(self._config.get("temp_in")).state or 0)
        t_out = float(self._hass.states.get(self._config.get("temp_out")).state or 0)
        return round(t_out - t_in, 1)
