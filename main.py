import streamlit as st
import pandas as pd

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Arburg ↔ Thermoplay — Hot Runner Wiring",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — dark industrial theme ─────────────────────────────────────────
st.markdown("""
<style>
/* ----- global ----- */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif;
}
.stApp { background-color: #0f1117; color: #e0e4f0; }

/* ----- sidebar ----- */
[data-testid="stSidebar"] {
    background-color: #1a1c24 !important;
    border-right: 1px solid #2e3150;
}
[data-testid="stSidebar"] * { color: #e0e4f0 !important; }

/* ----- headings ----- */
h1 { color: #ffffff !important; font-size: 1.6rem !important; }
h2 { color: #ffffff !important; font-size: 1.25rem !important;
     border-bottom: 1px solid #2e3150; padding-bottom: 8px; }
h3 { color: #c8ccdf !important; font-size: 1rem !important; }

/* ----- metric cards ----- */
[data-testid="metric-container"] {
    background: #1e2130;
    border: 1px solid #2e3150;
    border-radius: 8px;
    padding: 14px !important;
}
[data-testid="stMetricLabel"]  > div { color: #8890b0 !important; font-size: 0.7rem !important; letter-spacing: 1px; text-transform: uppercase; }
[data-testid="stMetricValue"]  > div { color: #ffffff !important; font-family: 'IBM Plex Mono', monospace; }
[data-testid="stMetricDelta"]  > div { color: #00c8a0 !important; }

/* ----- dataframe / tables ----- */
[data-testid="stDataFrame"] { border: 1px solid #2e3150; border-radius: 8px; overflow: hidden; }
.dataframe thead th {
    background-color: #252840 !important;
    color: #8890b0 !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.dataframe tbody tr { background-color: #1e2130 !important; border-bottom: 1px solid #2e3150 !important; }
.dataframe tbody tr:hover { background-color: #252840 !important; }
.dataframe tbody td { color: #e0e4f0 !important; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; }

/* ----- callout boxes ----- */
.callout-warn  { background:#1e1a0d; border:1px solid rgba(255,165,0,.35);
                 border-radius:6px; padding:12px 16px; color:#ffa500;
                 font-size:0.88rem; line-height:1.6; margin:8px 0 16px; }
.callout-info  { background:#0d1e1a; border:1px solid rgba(0,200,160,.3);
                 border-radius:6px; padding:12px 16px; color:#00c8a0;
                 font-size:0.88rem; line-height:1.6; margin:8px 0 16px; }
.callout-error { background:#1e0d0d; border:1px solid rgba(255,75,75,.35);
                 border-radius:6px; padding:12px 16px; color:#ff4b4b;
                 font-size:0.88rem; line-height:1.6; margin:8px 0 16px; }

/* ----- badge chips ----- */
.badge { display:inline-block; font-family:'IBM Plex Mono',monospace;
         font-size:0.65rem; font-weight:700; letter-spacing:.5px;
         padding:3px 9px; border-radius:3px; margin:0 4px; }
.badge-red    { background:rgba(255,75,75,.15); color:#ff4b4b;
                border:1px solid rgba(255,75,75,.3); }
.badge-green  { background:rgba(0,200,160,.12); color:#00c8a0;
                border:1px solid rgba(0,200,160,.25); }
.badge-orange { background:rgba(255,165,0,.12); color:#ffa500;
                border:1px solid rgba(255,165,0,.25); }

/* ----- text input ----- */
input[type="text"], [data-baseweb="input"] input {
    background:#1e2130 !important; border:1px solid #2e3150 !important;
    color:#e0e4f0 !important; font-family:'IBM Plex Mono',monospace !important;
}

/* ----- buttons ----- */
.stButton > button {
    background:#ff4b4b !important; color:#fff !important;
    border:none !important; border-radius:5px !important;
    font-weight:600; letter-spacing:.3px;
}
.stButton > button:hover { background:#e03030 !important; }

/* ----- selectbox ----- */
[data-baseweb="select"] > div {
    background:#1e2130 !important;
    border-color:#2e3150 !important;
    color:#e0e4f0 !important;
}

/* ----- expander ----- */
[data-testid="stExpander"] {
    background:#1e2130 !important;
    border:1px solid #2e3150 !important;
    border-radius:8px !important;
}
[data-testid="stExpander"] summary { color:#ffffff !important; }

/* ----- tabs ----- */
[data-baseweb="tab-list"] { background:#1a1c24 !important; border-bottom:1px solid #2e3150; gap:4px; }
[data-baseweb="tab"]      { color:#8890b0 !important; border-radius:4px 4px 0 0; }
[aria-selected="true"]    { color:#ff4b4b !important; border-bottom:2px solid #ff4b4b !important; }

/* ----- divider ----- */
hr { border-color:#2e3150 !important; }

/* ----- footer note ----- */
.footer-note { color:#8890b0; font-family:'IBM Plex Mono',monospace;
               font-size:0.7rem; margin-top:40px;
               border-top:1px solid #2e3150; padding-top:12px;
               display:flex; justify-content:space-between; }
</style>
""", unsafe_allow_html=True)


# ── Shared data ─────────────────────────────────────────────────────────────────

THERMOPLAY_PINS = pd.DataFrame([
    {"Function": "Zone 1 Heater", "M-Side Pin (+)": 1,  "F-Side Pin (−)": 13, "Type": "Heater"},
    {"Function": "Zone 2 Heater", "M-Side Pin (+)": 2,  "F-Side Pin (−)": 14, "Type": "Heater"},
    {"Function": "Zone 3 Heater", "M-Side Pin (+)": 3,  "F-Side Pin (−)": 15, "Type": "Heater"},
    {"Function": "Zone 4 Heater", "M-Side Pin (+)": 4,  "F-Side Pin (−)": 16, "Type": "Heater"},
    {"Function": "Zone 5 Heater", "M-Side Pin (+)": 5,  "F-Side Pin (−)": 17, "Type": "Heater"},
    {"Function": "Zone 6 Heater", "M-Side Pin (+)": 6,  "F-Side Pin (−)": 18, "Type": "Heater"},
    {"Function": "TC 1",          "M-Side Pin (+)": 7,  "F-Side Pin (−)": 19, "Type": "J-Type TC"},
    {"Function": "TC 2",          "M-Side Pin (+)": 8,  "F-Side Pin (−)": 20, "Type": "J-Type TC"},
    {"Function": "TC 3",          "M-Side Pin (+)": 9,  "F-Side Pin (−)": 21, "Type": "J-Type TC"},
    {"Function": "TC 4",          "M-Side Pin (+)": 10, "F-Side Pin (−)": 22, "Type": "J-Type TC"},
    {"Function": "TC 5",          "M-Side Pin (+)": 11, "F-Side Pin (−)": 23, "Type": "J-Type TC"},
    {"Function": "TC 6",          "M-Side Pin (+)": 12, "F-Side Pin (−)": 24, "Type": "J-Type TC"},
])

ARBURG_HEATERS = pd.DataFrame([
    {"Zone": "Heater 1", "Pin L (Live)": 1,  "Pin N (Neutral)": 2},
    {"Zone": "Heater 2", "Pin L (Live)": 3,  "Pin N (Neutral)": 4},
    {"Zone": "Heater 3", "Pin L (Live)": 5,  "Pin N (Neutral)": 6},
    {"Zone": "Heater 4", "Pin L (Live)": 7,  "Pin N (Neutral)": 8},
    {"Zone": "Heater 5", "Pin L (Live)": 9,  "Pin N (Neutral)": 10},
    {"Zone": "Heater 6", "Pin L (Live)": 11, "Pin N (Neutral)": 12},
])

ARBURG_TC = pd.DataFrame([
    {"Channel": "TC 1", "Pin (+)": 13, "Pin (−)": 14, "Type": "J-Type"},
    {"Channel": "TC 2", "Pin (+)": 15, "Pin (−)": 16, "Type": "J-Type"},
    {"Channel": "TC 3", "Pin (+)": 17, "Pin (−)": 18, "Type": "J-Type"},
    {"Channel": "TC 4", "Pin (+)": 19, "Pin (−)": 20, "Type": "J-Type"},
    {"Channel": "TC 5", "Pin (+)": 21, "Pin (−)": 22, "Type": "J-Type"},
    {"Channel": "TC 6", "Pin (+)": 23, "Pin (−)": 24, "Type": "J-Type"},
])

CROSS_WIRE = pd.DataFrame([
    {"Signal": "Zone 1", "Pol": "+", "Arburg Pin": 1,  "Thermoplay Pin": 1,  "Type": "Heater"},
    {"Signal": "Zone 1", "Pol": "−", "Arburg Pin": 2,  "Thermoplay Pin": 13, "Type": "Heater"},
    {"Signal": "Zone 2", "Pol": "+", "Arburg Pin": 3,  "Thermoplay Pin": 2,  "Type": "Heater"},
    {"Signal": "Zone 2", "Pol": "−", "Arburg Pin": 4,  "Thermoplay Pin": 14, "Type": "Heater"},
    {"Signal": "Zone 3", "Pol": "+", "Arburg Pin": 5,  "Thermoplay Pin": 3,  "Type": "Heater"},
    {"Signal": "Zone 3", "Pol": "−", "Arburg Pin": 6,  "Thermoplay Pin": 15, "Type": "Heater"},
    {"Signal": "Zone 4", "Pol": "+", "Arburg Pin": 7,  "Thermoplay Pin": 4,  "Type": "Heater"},
    {"Signal": "Zone 4", "Pol": "−", "Arburg Pin": 8,  "Thermoplay Pin": 16, "Type": "Heater"},
    {"Signal": "Zone 5", "Pol": "+", "Arburg Pin": 9,  "Thermoplay Pin": 5,  "Type": "Heater"},
    {"Signal": "Zone 5", "Pol": "−", "Arburg Pin": 10, "Thermoplay Pin": 17, "Type": "Heater"},
    {"Signal": "Zone 6", "Pol": "+", "Arburg Pin": 11, "Thermoplay Pin": 6,  "Type": "Heater"},
    {"Signal": "Zone 6", "Pol": "−", "Arburg Pin": 12, "Thermoplay Pin": 18, "Type": "Heater"},
    {"Signal": "TC 1",   "Pol": "+", "Arburg Pin": 13, "Thermoplay Pin": 7,  "Type": "Thermocouple"},
    {"Signal": "TC 1",   "Pol": "−", "Arburg Pin": 14, "Thermoplay Pin": 19, "Type": "Thermocouple"},
    {"Signal": "TC 2",   "Pol": "+", "Arburg Pin": 15, "Thermoplay Pin": 8,  "Type": "Thermocouple"},
    {"Signal": "TC 2",   "Pol": "−", "Arburg Pin": 16, "Thermoplay Pin": 20, "Type": "Thermocouple"},
    {"Signal": "TC 3",   "Pol": "+", "Arburg Pin": 17, "Thermoplay Pin": 9,  "Type": "Thermocouple"},
    {"Signal": "TC 3",   "Pol": "−", "Arburg Pin": 18, "Thermoplay Pin": 21, "Type": "Thermocouple"},
    {"Signal": "TC 4",   "Pol": "+", "Arburg Pin": 19, "Thermoplay Pin": 10, "Type": "Thermocouple"},
    {"Signal": "TC 4",   "Pol": "−", "Arburg Pin": 20, "Thermoplay Pin": 22, "Type": "Thermocouple"},
    {"Signal": "TC 5",   "Pol": "+", "Arburg Pin": 21, "Thermoplay Pin": 11, "Type": "Thermocouple"},
    {"Signal": "TC 5",   "Pol": "−", "Arburg Pin": 22, "Thermoplay Pin": 23, "Type": "Thermocouple"},
    {"Signal": "TC 6",   "Pol": "+", "Arburg Pin": 23, "Thermoplay Pin": 12, "Type": "Thermocouple"},
    {"Signal": "TC 6",   "Pol": "−", "Arburg Pin": 24, "Thermoplay Pin": 24, "Type": "Thermocouple"},
])

EIGHT_PIN = pd.DataFrame([
    {"PIN": "1",    "Signal (SL)": "Grelec 1",     "Description": "Heater 1 – Live / Phase",      "Wire Color (K-Type)": "—"},
    {"PIN": "2",    "Signal (SL)": "Termočlen 1+",  "Description": "Thermocouple 1 – Positive",    "Wire Color (K-Type)": "Yellow / Green"},
    {"PIN": "3",    "Signal (SL)": "Grelec 2",     "Description": "Heater 2 – Live / Phase",      "Wire Color (K-Type)": "—"},
    {"PIN": "4",    "Signal (SL)": "Termočlen 2+",  "Description": "Thermocouple 2 – Positive",    "Wire Color (K-Type)": "Yellow / Green"},
    {"PIN": "5",    "Signal (SL)": "Grelec 1",     "Description": "Heater 1 – Neutral / Return",  "Wire Color (K-Type)": "—"},
    {"PIN": "6",    "Signal (SL)": "Termočlen 1−",  "Description": "Thermocouple 1 – Negative",    "Wire Color (K-Type)": "White / Red"},
    {"PIN": "7",    "Signal (SL)": "Grelec 2",     "Description": "Heater 2 – Neutral / Return",  "Wire Color (K-Type)": "—"},
    {"PIN": "8/PE", "Signal (SL)": "Termočlen 2−",  "Description": "Thermocouple 2 – Negative ⚠", "Wire Color (K-Type)": "White / Red"},
])

DIFFERENCES = pd.DataFrame([
    {"Property": "Heater pair logic",  "Arburg Side": "Adjacent pins — 1+2, 3+4, …",        "Thermoplay Side": "Split M/F halves — 1/13, 2/14, …"},
    {"Property": "TC logic",           "Arburg Side": "Sequential pairs from pin 13",         "Thermoplay Side": "Offset by 12 pins — 7/19, 8/20, …"},
    {"Property": "TC type",            "Arburg Side": "J-Type",                               "Thermoplay Side": "J-Type"},
    {"Property": "Zones supported",    "Arburg Side": "Up to 6",                              "Thermoplay Side": "Up to 6"},
    {"Property": "Total pins",         "Arburg Side": "24 (pins 1–24)",                       "Thermoplay Side": "24 (pins 1–24)"},
    {"Property": "Connector format",   "Arburg Side": "Machine integrated",                   "Thermoplay Side": "Han E 24-pos M/F"},
])

PART_NUMBERS = pd.DataFrame([
    {"Connector": "Thermoplay M", "Part Number": "09330242601", "Description": "Han E 24 Pos. M Insert Screw"},
    {"Connector": "Thermoplay F", "Part Number": "09330242701", "Description": "Han E 24 Pos. F Insert Screw"},
    {"Connector": "8-PIN M",      "Part Number": "09 36 008 2632", "Description": "Han 8D-M Quick Lock 1.5mm²"},
    {"Connector": "8-PIN F",      "Part Number": "09 36 008 2732", "Description": "Han 8D-F Quick Lock 1.5mm²"},
])


# ── Sidebar ─────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚡ Wiring Docs")
    st.markdown("**Arburg ↔ Thermoplay**  \nHot Runner Interface")
    st.caption("Rev. 11.11.2023")
    st.divider()

    pages = {
        "🏠  Overview":             "overview",
        "🔌  Thermoplay Connector": "thermoplay",
        "🔧  Arburg Connector":     "arburg",
        "↔  Cross-Wiring Table":   "crosswire",
        "⚖  Key Differences":      "differences",
        "🔩  8-PIN Connector":      "eightpin",
        "🔍  Pin Search":           "search",
    }

    choice = st.radio("Navigation", list(pages.keys()), label_visibility="collapsed")
    page = pages[choice]

    st.divider()
    st.markdown("""
<div class="callout-error">
⚠ <strong>Safety Note</strong><br>
Heater zones carry mains voltage.<br>
Always <strong>lock out / tag out</strong> before wiring.
</div>
""", unsafe_allow_html=True)


# ── Helper ───────────────────────────────────────────────────────────────────────

def show_df(df: pd.DataFrame):
    st.dataframe(df, use_container_width=True, hide_index=True)

def warn(msg):  st.markdown(f'<div class="callout-warn">⚠ {msg}</div>', unsafe_allow_html=True)
def info(msg):  st.markdown(f'<div class="callout-info">ℹ {msg}</div>', unsafe_allow_html=True)
def error(msg): st.markdown(f'<div class="callout-error">🚨 {msg}</div>', unsafe_allow_html=True)
def badge(label, kind="red"):
    st.markdown(f'<span class="badge badge-{kind}">{label}</span>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "overview":
    st.title("Arburg ↔ Thermoplay — Hot Runner Wiring")
    st.markdown(
        '<span class="badge badge-red">Hot Runner</span>'
        '<span class="badge badge-green">6 Zones</span>'
        '<span class="badge badge-orange">J-Type TC</span>',
        unsafe_allow_html=True,
    )
    st.write("")

    warn("<strong>Important:</strong> Heater zone pinouts and J-type thermocouple (TC) pinouts use "
         "<strong>different pin assignments</strong> on each side. Cross-reference carefully before connecting.")

    st.write(
        "This document describes the wiring between the **Arburg machine connectors** "
        "and the **Thermoplay hot runner** connector. The interface supports up to "
        "6 heating zones with individual J-type thermocouple feedback per zone."
    )

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Heating Zones",    "6",    "Zones 1–6")
    c2.metric("TC Type",          "J",    "IEC 60584")
    c3.metric("Thermoplay Pins",  "24",   "Han E 24-pos")
    c4.metric("Arburg Pins",      "24",   "-4X4 / -4X2")

    st.divider()
    st.subheader("Connector Part Numbers")
    show_df(PART_NUMBERS)

    st.divider()
    st.subheader("Wiring Logic Summary")
    st.markdown("""
- **Arburg heaters:** Adjacent pin pairs — (1,2), (3,4), (5,6), …
- **Thermoplay heaters:** Split M/F halves — pin 1 (+) and pin 13 (−), etc.
- **Arburg TCs:** Sequential pairs starting from pin 13 — (13,14), (15,16), …
- **Thermoplay TCs:** Offset by 12 — pin 7 (+) to pin 19 (−), etc.
""")

    error("<strong>TC Polarity:</strong> Reversed polarity on J-type thermocouples causes incorrect "
          "temperature readings and may lead to <strong>temperature runaway</strong> or zone shutdown. "
          "Always verify with a multimeter before powering up.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: THERMOPLAY CONNECTOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "thermoplay":
    st.title("Thermoplay Connector")
    st.markdown('<span class="badge badge-green">Han E 24-pos</span>', unsafe_allow_html=True)
    st.write("")

    st.write(
        "The Thermoplay connector uses a Han E 24-position format. "
        "Heater pins are split across M-side (pins 1–6) and F-side (pins 13–18). "
        "Thermocouple pins follow: TC+ on pins 7–12, TC− on pins 19–24."
    )

    st.subheader("Pinout Table")
    show_df(THERMOPLAY_PINS)

    info("<strong>Layout logic:</strong> Pins 1–12 are on the M-side (+), pins 13–24 on the F-side (−). "
         "Heater and TC signals share the same offset pattern (12 pins apart).")

    st.divider()
    st.subheader("Visual Layout (schematic)")
    st.caption("Han E 24-pin connector — M-side carries all (+) signals, F-side all (−) signals.")

    tab_face, tab_linear, tab_pair = st.tabs(["🔲  Connector Face", "📋  Linear Pin List", "🔗  Paired View"])

    with tab_face:
        st.code("""
  THERMOPLAY CONNECTOR — FACE VIEW (Han E 24-pos)

  M-SIDE  (+)  pins 1-12            F-SIDE  (-)  pins 13-24
  +-------------------------+       +-------------------------+
  |  Heater zones  1-6      |       |  Heater zones  1-6      |
  |  [1] [2] [3] [4] [5] [6]|       |[13][14][15][16][17][18] |
  |   +   +   +   +   +   + |       |  -   -   -   -   -   -  |
  |  Z1  Z2  Z3  Z4  Z5  Z6 |       |  Z1  Z2  Z3  Z4  Z5  Z6 |
  |-------------------------|       |-------------------------|
  |  TC inputs  1-6         |       |  TC inputs  1-6         |
  |  [7] [8] [9][10][11][12]|       |[19][20][21][22][23][24] |
  |   +   +   +   +   +   + |       |  -   -   -   -   -   -  |
  |  TC1 TC2 TC3 TC4 TC5 TC6|       | TC1 TC2 TC3 TC4 TC5 TC6 |
  +-------------------------+       +-------------------------+
          |                                     |
          +----------- mated pair --------------+
             pin N (M-side) <-> pin N+12 (F-side)

  Legend:
    +  = M-side positive / Live        -  = F-side negative / Neutral
    Z1-Z6  = Heater Zone 1-6 (mains voltage)
    TC1-TC6 = J-type thermocouple channels
""", language=None)

    with tab_linear:
        st.code("""
  THERMOPLAY — PIN-BY-PIN LIST
  ---------------------------------------------------------
  Pin  01  (M+)  |  Heater Zone 1  |  Live / Phase   (+)
  Pin  13  (F-)  |  Heater Zone 1  |  Neutral        (-)
  ---------------------------------------------------------
  Pin  02  (M+)  |  Heater Zone 2  |  Live / Phase   (+)
  Pin  14  (F-)  |  Heater Zone 2  |  Neutral        (-)
  ---------------------------------------------------------
  Pin  03  (M+)  |  Heater Zone 3  |  Live / Phase   (+)
  Pin  15  (F-)  |  Heater Zone 3  |  Neutral        (-)
  ---------------------------------------------------------
  Pin  04  (M+)  |  Heater Zone 4  |  Live / Phase   (+)
  Pin  16  (F-)  |  Heater Zone 4  |  Neutral        (-)
  ---------------------------------------------------------
  Pin  05  (M+)  |  Heater Zone 5  |  Live / Phase   (+)
  Pin  17  (F-)  |  Heater Zone 5  |  Neutral        (-)
  ---------------------------------------------------------
  Pin  06  (M+)  |  Heater Zone 6  |  Live / Phase   (+)
  Pin  18  (F-)  |  Heater Zone 6  |  Neutral        (-)
  =========================================================
  Pin  07  (M+)  |  TC 1  J-type   |  Positive       (+)
  Pin  19  (F-)  |  TC 1  J-type   |  Negative       (-)
  ---------------------------------------------------------
  Pin  08  (M+)  |  TC 2  J-type   |  Positive       (+)
  Pin  20  (F-)  |  TC 2  J-type   |  Negative       (-)
  ---------------------------------------------------------
  Pin  09  (M+)  |  TC 3  J-type   |  Positive       (+)
  Pin  21  (F-)  |  TC 3  J-type   |  Negative       (-)
  ---------------------------------------------------------
  Pin  10  (M+)  |  TC 4  J-type   |  Positive       (+)
  Pin  22  (F-)  |  TC 4  J-type   |  Negative       (-)
  ---------------------------------------------------------
  Pin  11  (M+)  |  TC 5  J-type   |  Positive       (+)
  Pin  23  (F-)  |  TC 5  J-type   |  Negative       (-)
  ---------------------------------------------------------
  Pin  12  (M+)  |  TC 6  J-type   |  Positive       (+)
  Pin  24  (F-)  |  TC 6  J-type   |  Negative       (-)
  ---------------------------------------------------------
""", language=None)

    with tab_pair:
        st.code("""
  THERMOPLAY — PAIRED WIRING VIEW
  +------------+--------------+--------------+--------------------------+
  |  Signal    |  M-Side (+)  |  F-Side (-)  |  Note                    |
  +------------+--------------+--------------+--------------------------+
  |  Zone 1    |    pin  1    |    pin 13    |  230 V AC heater         |
  |  Zone 2    |    pin  2    |    pin 14    |  230 V AC heater         |
  |  Zone 3    |    pin  3    |    pin 15    |  230 V AC heater         |
  |  Zone 4    |    pin  4    |    pin 16    |  230 V AC heater         |
  |  Zone 5    |    pin  5    |    pin 17    |  230 V AC heater         |
  |  Zone 6    |    pin  6    |    pin 18    |  230 V AC heater         |
  +------------+--------------+--------------+--------------------------+
  |  TC 1      |    pin  7    |    pin 19    |  J-type  ! polarity!    |
  |  TC 2      |    pin  8    |    pin 20    |  J-type  ! polarity!    |
  |  TC 3      |    pin  9    |    pin 21    |  J-type  ! polarity!    |
  |  TC 4      |    pin 10    |    pin 22    |  J-type  ! polarity!    |
  |  TC 5      |    pin 11    |    pin 23    |  J-type  ! polarity!    |
  |  TC 6      |    pin 12    |    pin 24    |  J-type  ! polarity!    |
  +------------+--------------+--------------+--------------------------+

  Key rule:  F-side pin = M-side pin + 12  (for all 12 pairs)
  Heater range:  M pins 1-6   <->  F pins 13-18
  TC range:      M pins 7-12  <->  F pins 19-24
""", language=None)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ARBURG CONNECTOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "arburg":
    st.title("Arburg Connector")
    st.markdown('<span class="badge badge-orange">-4X4 / -4X2</span>', unsafe_allow_html=True)
    st.write("")

    st.write(
        "The Arburg side uses adjacent pin pairs for heater zones, "
        "then sequential pairs for thermocouple inputs starting at pin 13."
    )

    tab1, tab2 = st.tabs(["🔴  Heater Zones", "🟢  Thermocouple Inputs"])

    with tab1:
        st.subheader("Heater Zones — Connectors -4X4 / -4X2")
        st.caption("Each heater zone uses a pair of adjacent pins (L + N).")
        show_df(ARBURG_HEATERS)
        warn("Heater zones carry <strong>mains voltage</strong>. Ensure machine is "
             "<strong>locked out / tagged out</strong> before working on wiring.")

    with tab2:
        st.subheader("Thermocouple Inputs")
        st.caption("TC signals start at pin 13. J-type polarity must be respected.")
        show_df(ARBURG_TC)
        error("Reversed TC polarity causes incorrect temperature readings. "
              "Verify with a multimeter before powering up.")

    st.divider()
    st.subheader("Visual Layout (schematic)")
    st.caption("Han E 24-pin connector — face view (mating side). Pins laid out in 2 rows of 12.")

    tab_face, tab_linear, tab_pair = st.tabs(["🔲  Connector Face", "📋  Linear Pin List", "🔗  Paired View"])

    with tab_face:
        st.code("""
  ARBURG CONNECTOR — FACE VIEW (mating side, 24-pin)
  ┌──────────────────────────────────────────────────────┐
  │  HEATER ZONES (adjacent pairs)                       │
  │                                                      │
  │   ①   ②   ③   ④   ⑤   ⑥   ⑦   ⑧   ⑨   ⑩   ⑪   ⑫  │
  │  [1] [2] [3] [4] [5] [6] [7] [8] [9][10][11][12]   │
  │   L   N   L   N   L   N   L   N   L   N   L   N     │
  │   └─Z1─┘  └─Z2─┘  └─Z3─┘  └─Z4─┘  └─Z5─┘  └─Z6─┘  │
  │                                                      │
  │  THERMOCOUPLE INPUTS (sequential pairs, J-type)      │
  │                                                      │
  │  [13][14][15][16][17][18][19][20][21][22][23][24]    │
  │   +   −   +   −   +   −   +   −   +   −   +   −     │
  │   └TC1┘   └TC2┘   └TC3┘   └TC4┘   └TC5┘   └TC6┘    │
  │                                                      │
  │  Connector: -4X4 / -4X2                              │
  └──────────────────────────────────────────────────────┘

  Legend:
    L = Live / Phase      N = Neutral / Return
    + = TC Positive (J)   − = TC Negative (J)
    Z1–Z6 = Heater Zone 1–6
""", language=None)

    with tab_linear:
        st.code("""
  ARBURG — PIN-BY-PIN LIST
  ─────────────────────────────────────────────
  Pin  01  │  Heater Zone 1  │  L  (Live/Phase)
  Pin  02  │  Heater Zone 1  │  N  (Neutral)
  ─────────────────────────────────────────────
  Pin  03  │  Heater Zone 2  │  L
  Pin  04  │  Heater Zone 2  │  N
  ─────────────────────────────────────────────
  Pin  05  │  Heater Zone 3  │  L
  Pin  06  │  Heater Zone 3  │  N
  ─────────────────────────────────────────────
  Pin  07  │  Heater Zone 4  │  L
  Pin  08  │  Heater Zone 4  │  N
  ─────────────────────────────────────────────
  Pin  09  │  Heater Zone 5  │  L
  Pin  10  │  Heater Zone 5  │  N
  ─────────────────────────────────────────────
  Pin  11  │  Heater Zone 6  │  L
  Pin  12  │  Heater Zone 6  │  N
  ═════════════════════════════════════════════
  Pin  13  │  TC 1  J-type   │  +  (Positive)
  Pin  14  │  TC 1  J-type   │  −  (Negative)
  ─────────────────────────────────────────────
  Pin  15  │  TC 2  J-type   │  +
  Pin  16  │  TC 2  J-type   │  −
  ─────────────────────────────────────────────
  Pin  17  │  TC 3  J-type   │  +
  Pin  18  │  TC 3  J-type   │  −
  ─────────────────────────────────────────────
  Pin  19  │  TC 4  J-type   │  +
  Pin  20  │  TC 4  J-type   │  −
  ─────────────────────────────────────────────
  Pin  21  │  TC 5  J-type   │  +
  Pin  22  │  TC 5  J-type   │  −
  ─────────────────────────────────────────────
  Pin  23  │  TC 6  J-type   │  +
  Pin  24  │  TC 6  J-type   │  −
  ─────────────────────────────────────────────
""", language=None)

    with tab_pair:
        st.code("""
  ARBURG — PAIRED WIRING VIEW
  ┌────────────┬──────────┬──────────┬─────────────────────────┐
  │  Signal    │  Pin (+) │  Pin (−) │  Note                   │
  ├────────────┼──────────┼──────────┼─────────────────────────┤
  │  Zone 1    │    1 (L) │    2 (N) │  230 V AC heater        │
  │  Zone 2    │    3 (L) │    4 (N) │  230 V AC heater        │
  │  Zone 3    │    5 (L) │    6 (N) │  230 V AC heater        │
  │  Zone 4    │    7 (L) │    8 (N) │  230 V AC heater        │
  │  Zone 5    │    9 (L) │   10 (N) │  230 V AC heater        │
  │  Zone 6    │   11 (L) │   12 (N) │  230 V AC heater        │
  ├────────────┼──────────┼──────────┼─────────────────────────┤
  │  TC 1      │   13 (+) │   14 (−) │  J-type  ⚠ polarity!   │
  │  TC 2      │   15 (+) │   16 (−) │  J-type  ⚠ polarity!   │
  │  TC 3      │   17 (+) │   18 (−) │  J-type  ⚠ polarity!   │
  │  TC 4      │   19 (+) │   20 (−) │  J-type  ⚠ polarity!   │
  │  TC 5      │   21 (+) │   22 (−) │  J-type  ⚠ polarity!   │
  │  TC 6      │   23 (+) │   24 (−) │  J-type  ⚠ polarity!   │
  └────────────┴──────────┴──────────┴─────────────────────────┘

  Heater pairs:  always adjacent  (odd = L, even = N)
  TC pairs:      always adjacent  (odd = +, even = −)
  TC start pin:  13  (heaters occupy pins 1–12)
""", language=None)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CROSS-WIRING TABLE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "crosswire":
    st.title("Cross-Wiring Table")
    st.markdown('<span class="badge badge-red">Arburg → Thermoplay</span>', unsafe_allow_html=True)
    st.write("")

    info("Pin numbers differ on each side. This table is the definitive mapping. "
         "Always use this when building or verifying the adapter cable.")

    # Filter controls
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.selectbox("Filter by type", ["All", "Heater", "Thermocouple"])
    with col2:
        filter_signal = st.selectbox(
            "Filter by signal",
            ["All"] + sorted(CROSS_WIRE["Signal"].unique().tolist())
        )

    df = CROSS_WIRE.copy()
    if filter_type != "All":
        df = df[df["Type"] == filter_type]
    if filter_signal != "All":
        df = df[df["Signal"] == filter_signal]

    show_df(df)
    st.caption(f"Showing {len(df)} of {len(CROSS_WIRE)} wire connections.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: KEY DIFFERENCES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "differences":
    st.title("Key Differences")
    st.markdown('<span class="badge badge-orange">Arburg vs Thermoplay</span>', unsafe_allow_html=True)
    st.write("")

    show_df(DIFFERENCES)

    st.divider()
    st.subheader("Why the Difference Matters")
    st.write(
        "Because the pin-numbering schemes differ, a straight 1:1 cable would mis-wire both "
        "heaters and thermocouples. The cross-wiring adapter must rearrange conductors to account for:"
    )
    st.markdown("""
- Heater return conductors jumping from adjacent pins to the M/F offset scheme
- TC signals remapping from sequential pairs to the ±12-pin split
- Maintaining J-type compensation material throughout TC signal paths
""")

    error("<strong>Never use a straight-through cable.</strong> Mislabelled or swapped TC wires "
          "will cause temperature runaway or zone shutdown. Reversed heater N/L could damage "
          "the proportional regulator output stage.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: 8-PIN CONNECTOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "eightpin":
    st.title("8-PIN Connector — 7+PE")
    st.markdown(
        '<span class="badge badge-green">Dual Zone</span>'
        '<span class="badge badge-orange">Han 8D</span>',
        unsafe_allow_html=True,
    )
    st.write("")

    st.write(
        "Connection scheme for a typical dual-zone heating system with two heaters and two "
        "thermocouples. Uses the Han 8D Quick Lock connector in 8-pin 7+PE configuration."
    )

    warn("Pin 8 is physically marked as <strong>PE</strong> on the connector housing, but in this "
         "application it is wired as <strong>TC2−</strong>. Do not connect to protective earth.")

    st.subheader("Pinout — Han 8D 7+PE")
    show_df(EIGHT_PIN)

    st.divider()
    st.subheader("Zone-to-Pin Details")

    with st.expander("🔴  Heater 1 — Pins 1 & 5"):
        st.write(
            "Pin 1 = Live/Phase, Pin 5 = Neutral/Return. "
            "Typically 230 V AC or 24 V DC depending on system design. "
            "Wire cross-section: **0.75–2.5 mm²** per current load."
        )

    with st.expander("🟠  Heater 2 — Pins 3 & 7"):
        st.write("Pin 3 = Live/Phase, Pin 7 = Neutral/Return. Same voltage class as Heater 1.")

    with st.expander("🟢  Thermocouple 1 — Pins 2 & 6"):
        st.write(
            "Pin 2 = TC+ (Yellow/Green), Pin 6 = TC− (White/Red). "
            "Use Type K compensating extension cable. Never use copper for TC signal paths."
        )

    with st.expander("🔵  Thermocouple 2 — Pins 4 & 8(PE)"):
        st.write(
            "Pin 4 = TC+ (Yellow/Green), Pin 8 = TC− (White/Red). "
            "Pin 8 is the PE position but is used here for TC2−. "
            "Ensure insulation class is adequate; do not bond to chassis ground."
        )

    st.divider()
    st.subheader("Wiring Recommendations")
    st.markdown("""
- Use **compensating cable** (Type K) or true TC extension wire for pins 2, 4, 6, 8
- **Never** substitute ordinary copper wire for TC connections — causes large measurement error
- Heater wires (1, 3, 5, 7): size according to current, typically **0.75–2.5 mm²**
- Recommended tightening torque: **0.5–0.6 Nm** (verify against connector spec sheet)
- Always verify with a multimeter before powering up
""")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PIN SEARCH
# ══════════════════════════════════════════════════════════════════════════════
elif page == "search":
    st.title("Pin Search")
    st.markdown('<span class="badge badge-green">Interactive</span>', unsafe_allow_html=True)
    st.write("")

    st.write("Look up any pin number or signal name to find its function and cross-wiring counterpart.")

    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(
            "Search",
            placeholder="Pin number (e.g. 13) or signal name (e.g. TC3, Zone 2)…",
            label_visibility="collapsed",
        )
    with col2:
        search_btn = st.button("🔍 Search", use_container_width=True)

    if query or search_btn:
        q = query.strip().lower()
        df = CROSS_WIRE.copy()

        # Try numeric pin match first
        try:
            num = int(q)
            results = df[(df["Arburg Pin"] == num) | (df["Thermoplay Pin"] == num)]
        except ValueError:
            results = df[
                df["Signal"].str.lower().str.contains(q) |
                df["Type"].str.lower().str.contains(q)
            ]

        if results.empty:
            st.error(f'No results for **"{query}"**. Try a pin number (1–24) or signal like "TC3" or "Zone 2".')
        else:
            st.success(f"Found **{len(results)}** result(s) for `{query}`")
            show_df(results)

            # Show counterpart info
            if len(results) == 1:
                row = results.iloc[0]
                st.info(
                    f"**{row['Signal']} {row['Pol']}** — "
                    f"Arburg pin **{row['Arburg Pin']}** → "
                    f"Thermoplay pin **{row['Thermoplay Pin']}** "
                    f"({row['Type']})"
                )

    st.divider()
    st.subheader("Quick Reference — All 24 Connections")
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        qr_type = st.selectbox("Show", ["All", "Heater", "Thermocouple"], key="qr_type")
    with filter_col2:
        qr_pol = st.selectbox("Polarity", ["Both", "+", "−"], key="qr_pol")

    qr_df = CROSS_WIRE.copy()
    if qr_type != "All":
        qr_df = qr_df[qr_df["Type"] == qr_type]
    if qr_pol != "Both":
        qr_df = qr_df[qr_df["Pol"] == qr_pol]
    show_df(qr_df)


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
  <span>Arburg ↔ Thermoplay Hot Runner Interface</span>
  <span>Rev. 11.11.2023</span>
</div>
""", unsafe_allow_html=True)
