NEXUS INFINITY — CHIKHLI WEATHER & AMBIKA RIVER STARTER

LOCATION
Chikhli town, Navsari District, Gujarat.
Weather grid coordinates: 20.75814, 73.05990.
River workspace: Ambika River, Bilimora.

INSTALL
1. Extract this ZIP.
2. Open folder in VS Code.
3. Terminal:
   pip install -r requirements.txt
4. Run:
   streamlit run app.py

FILES
app.py                         Main dashboard
nexus_common.py                Shared theme
weather_service.py              Open-Meteo API connector
pages/1_Weather.py              Current weather + 7-day forecast
pages/2_Rainfall.py             Hourly and daily rainfall forecast
pages/3_Ambika_River.py         Bilimora Ambika river gauge workspace
pages/4_AI_Prediction.py        Synthetic ML demonstration
pages/5_What_If_Simulation.py   Illustrative scenario calculator
pages/6_Decision_Advisor.py     General information checklist
pages/7_Reports.py              CSV export
pages/8_Settings.py             Data-source information

WEATHER DATA
This starter calls Open-Meteo Forecast API directly from Python using urllib.
It requests current conditions, hourly precipitation/rain probability and a 7-day forecast.
The Chikhli coordinate is an approximate town-centre coordinate. Rainfall is gridded model data, not a physical rain-gauge observation.
For official India weather warnings, also consult IMD:
https://api.imd.gov.in/public/

AMBICA RIVER LIMITATION
The river page is configured for Ambika River — Bilimora, but does not fabricate a live gauge reading.
A Gujarat Water Resources Department historical river-gauge availability list includes Harangam, Chikhali, Ambika River, with data period shown as 1999–2010. This does NOT establish a current Bilimora live telemetry feed.
The page allows clearly-labelled manual gauge observations until the correct live station/API is confirmed.
Official sources:
https://guj-nwrws.gujarat.gov.in/
https://swhydrology.gujarat.gov.in/
https://nwdp.nwic.gov.in/

SAFETY / VALIDATION
This is an educational prototype, not an official flood warning system.
Synthetic ML data and the what-if formula are demonstrations only.
Never use this app to make emergency or evacuation decisions. Follow IMD and district administration advisories.
