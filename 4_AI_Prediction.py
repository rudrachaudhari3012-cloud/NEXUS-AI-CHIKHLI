import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from nexus_common import page_header
from weather_service import get_chikhli_weather

st.set_page_config(page_title="NEXUS | AI Prediction", page_icon="🔮", layout="wide")
page_header("AI Weather Prediction Demo", "Educational ML demonstration; not a validated local flood forecast.")
data,error=get_chikhli_weather()
if data:
    cur=data.get("current",{})
    st.write("Current Chikhli API inputs (for context):", {k:cur.get(k) for k in ["temperature_2m","relative_humidity_2m","rain","wind_speed_10m"]})
else:
    st.caption("Live weather could not be fetched; the educational demo can still run.")
# Synthetic training data is deliberately labelled and must not be mistaken for a trained operational model.
X=pd.DataFrame({"rainfall":[0,5,10,15,20,25,30,35,40,45,50,55],
                "starting_level":[1.0,1.2,1.5,1.7,2.0,2.3,2.6,3.0,3.3,3.7,4.0,4.4]})
y=[1.0,1.1,1.3,1.5,1.8,2.0,2.3,2.6,2.9,3.2,3.5,3.9]
model=RandomForestRegressor(n_estimators=100,random_state=42).fit(X,y)
rain=st.slider("Hypothetical rainfall (mm)",0,100,25)
level=st.slider("Hypothetical starting river level (m)",0.0,10.0,2.5,0.1)
result=model.predict(pd.DataFrame({"rainfall":[rain],"starting_level":[level]}))[0]
st.metric("Illustrative model output",f"{result:.2f}")
st.warning("Model is trained on synthetic classroom values. Do not use its output as a real river-level prediction or safety warning.")
