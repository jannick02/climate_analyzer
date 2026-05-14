"""Die Klima Analyse Integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Liste der Plattformen, die wir unterstützen (aktuell nur sensor)
PLATFORMS: list[str] = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Wird aufgerufen, wenn eine neue Instanz (ein Raum) hinzugefügt wird."""
    
    # Speichere die Konfigurationsdaten in hass.data, falls andere Teile der
    # Integration darauf zugreifen müssen.
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Leitet das Setup an die sensor.py weiter
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Wird aufgerufen, wenn eine Instanz (ein Raum) gelöscht wird."""
    
    # Entfernt die Sensoren wieder aus Home Assistant
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
