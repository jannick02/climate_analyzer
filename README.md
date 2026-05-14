# Klima Analyse
Erhalte einen Klima Score Basierend auf deinen Sensor Werten
# 🏠 Climate Analyzer für Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/github/v/release/DEIN_GITHUB_NAME/climate_analyzer)
![License](https://img.shields.io/github/license/DEIN_GITHUB_NAME/climate_analyzer)

Diese Integration hilft dir, dein Raumklima intelligent zu analysieren. Basierend auf der Innen- und Außentemperatur sowie der Luftfeuchtigkeit berechnet sie die **absolute Feuchtigkeit** und gibt präzise Empfehlungen, ob ein Fenster geöffnet oder geschlossen werden sollte, um Schimmel zu vermeiden oder die Temperatur zu optimieren.

## ✨ Funktionen

- **Lüftungsempfehlung:** Dynamischer Status (z. B. "Fenster auf! (Entfeuchten)" oder "Fenster zu! (Hitze kommt rein)").
- **Klima-Score:** Ein Wert von 0 bis 100%, der angibt, wie nah der Raum am Idealwert (21°C, 9g/m³ absolute Feuchte) liegt.
- **Absolute Feuchtigkeit:** Separate Sensoren für Innen und Außen (g/m³).
- **Temperatur-Delta:** Zeigt die Differenz zwischen Außen- und Innentemperatur auf einen Blick.
- **Multi-Raum-Support:** Erstelle pro Raum ein eigenes Gerät mit individuellen Sensoren.

## 🚀 Installation

### Weg 1: Über HACS (Empfohlen)

1. Öffne **HACS** in deinem Home Assistant.
2. Klicke auf die drei Punkte oben rechts und wähle **Benutzerdefinierte Repositories**.
3. Füge die URL dieses Repositories hinzu: `https://github.com/DEIN_GITHUB_NAME/climate_analyzer`
4. Wähle die Kategorie **Integration** und klicke auf **Hinzufügen**.
5. Suche nach "Climate Analyzer", klicke auf **Herunterladen**.
6. **WICHTIG:** Starte Home Assistant neu.

### Weg 2: Manuelle Installation

1. Lade diesen Repository als ZIP herunter.
2. Kopiere den Ordner `custom_components/climate_analyzer` in deinen `config/custom_components/` Ordner.
3. Starte Home Assistant neu.

## ⚙️ Konfiguration

Nach dem Neustart kannst du die Integration ganz einfach über die Benutzeroberfläche einrichten:

1. Gehe zu **Einstellungen** -> **Geräte & Dienste**.
2. Klicke auf **Integration hinzufügen**.
3. Suche nach **"Climate Analyzer"**.
4. Gib die geforderten Daten im Konfigurationsfenster ein:
   - **Raumname:** (z. B. Wohnzimmer)
   - **Sensoren:** Wähle deine vorhandenen Sensoren für Temperatur, Feuchtigkeit und Fensterkontakt aus den Dropdown-Listen.

## 📊 Sensoren & Logik

Die Integration erstellt pro konfiguriertem Raum ein Gerät mit folgenden Entitäten:

| Sensor | Beschreibung |
| :--- | :--- |
| `sensor.klima_analyse_[raum]` | Die Hauptempfehlung (Fenster auf/zu) |
| `sensor.klima_score_[raum]` | Bewertung der Luftqualität in % |
| `sensor.abs_feuchte_indoor_[raum]` | Absolute Feuchtigkeit Innen in g/m³ |
| `sensor.abs_feuchte_outdoor_[raum]` | Absolute Feuchtigkeit Außen in g/m³ |
| `sensor.temp_delta_[raum]` | Differenz Außen- zu Innentemperatur |

### Die Logik hinter dem Score
Der Score startet bei 100 Punkten. Abzüge gibt es für:
- Abweichung von der Idealtemperatur (**21°C**)
- Abweichung von der idealen absoluten Feuchtigkeit (**9 g/m³**)

## 🛡️ Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe die [LICENSE](LICENSE) Datei für Details.

---
*Entwickelt mit ❤️ für eine bessere Luftqualität.*
