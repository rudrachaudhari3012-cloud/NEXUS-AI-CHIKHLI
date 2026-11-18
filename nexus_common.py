import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: Inter, sans-serif; }
    .stApp { background: radial-gradient(circle at 15% 0%, #102e50 0%, #06172b 42%, #041020 100%); color: #f4f8ff; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg,#06172b,#091e36); border-right: 1px solid #16466b; }
    h1,h2,h3,h4 { color:#f4f8ff !important; }
    .hero { padding: 25px; border:1px solid #1677ff; border-radius:20px; background:linear-gradient(115deg,rgba(8,35,65,.98),rgba(5,22,42,.94)); box-shadow:0 0 24px rgba(0,217,255,.13); margin-bottom:18px; }
    .hero h1 { font-size:46px; margin:0; letter-spacing:2px; }
    .hero h1 span { color:#00d9ff; }
    .hero h3 { color:#39bdf8 !important; margin:0 0 8px 0; }
    .hero p { color:#d7eaff; margin:4px 0; }
    .eyebrow { color:#00d9ff; font-size:12px; letter-spacing:3px; font-weight:800; }
    .small { font-size:13px; color:#8fdcff !important; }
    .panel,.module-card { background:linear-gradient(145deg,#0b2948,#081b31); border:1px solid #14517a; border-radius:15px; padding:16px; margin-bottom:12px; }
    .module-card h4 { color:#39bdf8 !important; margin:0 0 8px 0; }
    .module-card p,.panel p { color:#c5d9ee; margin:4px 0; }
    div.stButton > button, div.stDownloadButton > button { background:linear-gradient(90deg,#1677ff,#00bde8); color:white; border:0; border-radius:10px; font-weight:700; }
    [data-testid="stMetric"] { background:#0b2948; border:1px solid #16466b; padding:12px; border-radius:12px; }
    a { color:#39bdf8 !important; }
    </style>
    """, unsafe_allow_html=True)

def page_card(title, description):
    st.markdown(f'<div class="module-card"><h4>{title}</h4><p>{description}</p></div>', unsafe_allow_html=True)

def page_header(title, subtitle):
    apply_theme()
    st.markdown(f'<div class="hero"><div class="eyebrow">NEXUS ∞ • CHIKHLI, NAVSARI</div><h1 style="font-size:34px">{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)
