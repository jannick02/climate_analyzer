from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

# Liste der Plattformen, die geladen werden sollen
PLATFORMS: list[str] = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setzt die Integration für einen Config Entry (einen Raum) auf."""
    
    # Leitet das Setup an sensor.py weiter
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Wird aufgerufen, wenn ein Raum gelöscht wird."""
    
    # Entfernt alle Sensoren dieses Raums sauber aus HA
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
