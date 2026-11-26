# River Watch
Flood response decision-support page (NCI BDAIB CA2). Static page: `index.html`. No API key is stored in this repository; users paste their own Anthropic key into the settings box (kept in browser localStorage only).
- `build_history.py` – one-off script that computes `data/history_summary.json` (2016-2025 percentiles and winter high-flow event counts) from the Open-Meteo Flood API.
- Live at read time: Google Sheet, Open-Meteo forecast, Met Éireann warnings.
