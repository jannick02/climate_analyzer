# ... (Imports bleiben gleich wie in deinem File)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup Sensoren."""
    # Wir übergeben das ganze config_entry Objekt, um auf data und options zuzugreifen
    async_add_entities([ClimateAnalyzerEntity(hass, config_entry)])

# ... (calculate_abs_hum bleibt gleich)

class ClimateAnalyzerEntity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, hass, config_entry):
        self.hass = hass
        self._entry = config_entry
        room = config_entry.data.get(CONF_ROOM_NAME)
        
        self._attr_name = "Status"
        self._attr_unique_id = f"climate_analyzer_{room.lower()}"
        self._attr_icon = "mdi:home-analytics"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=f"Klima Analyse {room}",
            manufacturer="Climate Analyzer",
            model="Raumsensor"
        )

    @property
    def _config(self):
        """Kombiniert Basis-Konfiguration und Optionen."""
        # Priorisiert Optionen (vom Options Flow) über die Initialdaten
        return {**self._entry.data, **self._entry.options}

    # ... (Hilfsmethoden _get_float_state und _get_window_state bleiben gleich)

    @property
    def native_value(self):
        """Hauptstatus mit Fallback-Werten."""
        conf = self._config
        t_in = self._get_float_state(conf.get(CONF_TEMP_IN), 21.0)
        t_out = self._get_float_state(conf.get(CONF_TEMP_OUT), 15.0)
        h_in = self._get_float_state(conf.get(CONF_HUM_IN), 50.0)
        h_out = self._get_float_state(conf.get(CONF_HUM_OUT), 50.0)
        win = self._get_window_state()

        abs_in = calculate_abs_hum(t_in, h_in)
        abs_out = calculate_abs_hum(t_out, h_out)
        
        # Sicherer Zugriff auf die neuen Felder
        temp_comfort = float(conf.get(CONF_IDEAL_TEMP, 21.0))
        hum_max = float(conf.get(CONF_MAX_ABS_HUM, 12.0))

        if win:
            if t_in > temp_comfort and t_out > t_in: return "Fenster zu! (Hitze)"
            if abs_in > hum_max and abs_out > abs_in: return "Fenster zu! (Feuchte)"
            return "Fenster offen lassen"
        else:
            if t_in > temp_comfort and t_out < t_in: return "Fenster auf! (Abkühlen)"
            if abs_in > hum_max and abs_out < abs_in: return "Fenster auf! (Entfeuchten)"
            return "Fenster zu lassen"

    @property
    def extra_state_attributes(self):
        """Attribute mit dynamischen Idealwerten."""
        conf = self._config
        t_in = self._get_float_state(conf.get(CONF_TEMP_IN), 21.0)
        h_in = self._get_float_state(conf.get(CONF_HUM_IN), 50.0)
        t_out = self._get_float_state(conf.get(CONF_TEMP_OUT), 15.0)
        h_out = self._get_float_state(conf.get(CONF_HUM_OUT), 50.0)

        abs_in = calculate_abs_hum(t_in, h_in)
        abs_out = calculate_abs_hum(t_out, h_out)

        temp_comfort = float(conf.get(CONF_IDEAL_TEMP, 21.0))
        ideal_abs = float(conf.get(CONF_IDEAL_ABS_HUM, 9.0))
        hum_max = float(conf.get(CONF_MAX_ABS_HUM, 12.0))

        t_pen = abs(t_in - temp_comfort) * 6
        h_pen = abs(abs_in - ideal_abs) * 9
        score = max(0, round(100 - t_pen - h_pen))

        return {
            "score": score,
            "score_unit": "%",
            "absolute_humidity_in": round(abs_in, 2),
            "absolute_humidity_out": round(abs_out, 2),
            "window_open": self._get_window_state(),
            "configured_ideal_temp": temp_comfort,
            "configured_ideal_abs_hum": ideal_abs,
            "configured_max_abs_hum": hum_max
        }
