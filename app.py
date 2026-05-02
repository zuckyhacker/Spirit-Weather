import streamlit as st
import requests
import datetime
from streamlit_js_eval import get_geolocation

TRANSLATIONS = {
    "English": {
        "title": "Spirit Weather",
        "search_placeholder": "Search city or country...",
        "search_button": "Search",
        "detecting": "Detecting your location...",
        "allow_location": "📍 Allow location access for automatic detection",
        "error_location": "Could not detect location. Search manually.",
        "loading": "Loading...",
        "feels_like": "Feels Like",
        "humidity": "Humidity",
        "wind": "Wind",
        "visibility": "Visibility",
        "pressure": "Pressure",
        "sunrise": "Sunrise",
        "sunset": "Sunset",
        "hourly_title": "Hourly Forecast",
        "daily_title": "7-Day Forecast",
        "select_city": "Multiple results — choose one:",
        "no_results": "No results found.",
        "high": "H",
        "low": "L",
        "condition_map": {
            0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
            45: "Foggy", 48: "Icy Fog",
            51: "Light Drizzle", 53: "Moderate Drizzle", 55: "Heavy Drizzle",
            61: "Slight Rain", 63: "Moderate Rain", 65: "Heavy Rain",
            71: "Slight Snow", 73: "Moderate Snow", 75: "Heavy Snow",
            77: "Snow Grains",
            80: "Slight Showers", 81: "Moderate Showers", 82: "Violent Showers",
            85: "Snow Showers", 86: "Heavy Snow Showers",
            95: "Thunderstorm", 96: "Thunderstorm + Hail", 99: "Severe Thunderstorm",
        },
        "days_short": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "days_full": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "months": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "ಸ್ಪಿರಿಟ್ ವೆದರ್",
        "search_placeholder": "ನಗರ ಅಥವಾ ದೇಶ ಹುಡುಕಿ...",
        "search_button": "ಹುಡುಕಿ",
        "detecting": "ಸ್ಥಳ ಪತ್ತೆ ಮಾಡಲಾಗುತ್ತಿದೆ...",
        "allow_location": "📍 ಸ್ವಯಂಚಾಲಿತ ಪತ್ತೆಗಾಗಿ ಸ್ಥಳ ಅನುಮತಿ ನೀಡಿ",
        "error_location": "ಸ್ಥಳ ಕಂಡುಬಂದಿಲ್ಲ. ಹಸ್ತಚಾಲಿತವಾಗಿ ಹುಡುಕಿ.",
        "loading": "ಲೋಡ್...",
        "feels_like": "ಅನಿಸಿಕೆ",
        "humidity": "ತೇವಾಂಶ",
        "wind": "ಗಾಳಿ",
        "visibility": "ದೃಶ್ಯ",
        "pressure": "ಒತ್ತಡ",
        "sunrise": "ಸೂರ್ಯೋದಯ",
        "sunset": "ಸೂರ್ಯಾಸ್ತ",
        "hourly_title": "ಗಂಟೆಯ ಮುನ್ಸೂಚನೆ",
        "daily_title": "7-ದಿನ ಮುನ್ಸೂಚನೆ",
        "select_city": "ಹಲವು ಫಲಿತಾಂಶ — ಒಂದು ಆಯ್ಕೆ ಮಾಡಿ:",
        "no_results": "ಫಲಿತಾಂಶ ಕಂಡುಬಂದಿಲ್ಲ.",
        "high": "ಗ",
        "low": "ಕ",
        "condition_map": {
            0: "ಸ್ಪಷ್ಟ ಆಕಾಶ", 1: "ಮುಖ್ಯವಾಗಿ ಸ್ಪಷ್ಟ", 2: "ಭಾಗಶಃ ಮೋಡ", 3: "ಮೋಡ ಕವಿದ",
            45: "ಮಂಜು", 48: "ಮಂಜಿನ ಮಂಜು",
            51: "ಹಗುರ ಹನಿಮಳೆ", 53: "ಮಧ್ಯಮ ಹನಿಮಳೆ", 55: "ಭಾರೀ ಹನಿಮಳೆ",
            61: "ಸ್ವಲ್ಪ ಮಳೆ", 63: "ಮಧ್ಯಮ ಮಳೆ", 65: "ಭಾರೀ ಮಳೆ",
            71: "ಸ್ವಲ್ಪ ಹಿಮ", 73: "ಮಧ್ಯಮ ಹಿಮ", 75: "ಭಾರೀ ಹಿಮ",
            77: "ಹಿಮ ಕಣಗಳು",
            80: "ಸ್ವಲ್ಪ ಮಳೆ ಝರಿ", 81: "ಮಧ್ಯಮ ಮಳೆ ಝರಿ", 82: "ತೀವ್ರ ಮಳೆ ಝರಿ",
            85: "ಹಿಮ ಝರಿ", 86: "ಭಾರೀ ಹಿಮ ಝರಿ",
            95: "ಗುಡುಗು ಮಳೆ", 96: "ಆಲಿಕಲ್ಲು + ಗುಡುಗು", 99: "ತೀವ್ರ ಗುಡುಗು",
        },
        "days_short": ["ಸೋ","ಮಂ","ಬು","ಗು","ಶು","ಶನಿ","ಭಾ"],
        "days_full": ["ಸೋಮವಾರ","ಮಂಗಳವಾರ","ಬುಧವಾರ","ಗುರುವಾರ","ಶುಕ್ರವಾರ","ಶನಿವಾರ","ಭಾನುವಾರ"],
        "months": ["ಜನ","ಫೆಬ್","ಮಾರ್","ಏಪ್ರಿ","ಮೇ","ಜೂನ್","ಜುಲೈ","ಆಗ","ಸೆಪ್","ಅಕ್ಟೋ","ನವ","ಡಿಸೆ"],
    },
}

WEATHER_ICONS = {
    0:"☀️",1:"🌤️",2:"⛅",3:"☁️",45:"🌫️",48:"🌫️",
    51:"🌦️",53:"🌦️",55:"🌧️",61:"🌧️",63:"🌧️",65:"🌧️",
    71:"🌨️",73:"🌨️",75:"❄️",77:"🌨️",
    80:"🌦️",81:"🌦️",82:"⛈️",85:"🌨️",86:"❄️",
    95:"⛈️",96:"⛈️",99:"⛈️",
}

def get_gradient(wcode, is_day=1):
    if wcode in [95,96,99]:   return "linear-gradient(160deg,#0d1117 0%,#1a1f35 50%,#1e2a4a 100%)"
    if wcode in [61,63,65,51,53,55,80,81,82]: return "linear-gradient(160deg,#0f1c33 0%,#1a3a5c 50%,#1565c0 100%)"
    if wcode in [71,73,75,77,85,86]: return "linear-gradient(160deg,#1c2b35 0%,#37474f 50%,#607d8b 100%)"
    if wcode in [45,48]: return "linear-gradient(160deg,#2e3b40 0%,#455a64 50%,#78909c 100%)"
    if wcode in [2,3]:   return "linear-gradient(160deg,#1a2535 0%,#2c3e50 50%,#546e7a 100%)"
    if is_day == 0:      return "linear-gradient(160deg,#020c18 0%,#0a1628 50%,#0d2044 100%)"
    return "linear-gradient(160deg,#0b3d7a 0%,#1565c0 40%,#1e88e5 70%,#42a5f5 100%)"

def inject_css(gradient):
    st.markdown(f"""
<style>
#MainMenu,header[data-testid="stHeader"],footer,
[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"]{{display:none!important;visibility:hidden!important;}}
section[data-testid="stSidebar"]{{display:none!important;}}
.stApp{{background:{gradient}!important;min-height:100vh;}}
.block-container{{max-width:660px!important;padding:1rem 1.2rem 4rem!important;margin:0 auto!important;}}
*{{box-sizing:border-box;}}
.stApp,.stApp p,.stApp span,.stApp div,.stApp label,.stMarkdown p,.stMarkdown span{{color:white!important;}}
.stTextInput>div>div>input{{background:rgba(255,255,255,0.12)!important;border:1.5px solid rgba(255,255,255,0.25)!important;border-radius:14px!important;color:white!important;padding:0.65rem 1rem!important;font-size:0.95rem!important;backdrop-filter:blur(12px);}}
.stTextInput>div>div>input:focus{{border-color:rgba(255,255,255,0.55)!important;box-shadow:none!important;}}
.stTextInput>div>div>input::placeholder{{color:rgba(255,255,255,0.5)!important;}}
.stButton>button{{background:rgba(255,255,255,0.16)!important;border:1.5px solid rgba(255,255,255,0.3)!important;border-radius:14px!important;color:white!important;font-weight:600!important;font-size:0.9rem!important;padding:0.6rem 1rem!important;backdrop-filter:blur(12px);width:100%;}}
.stButton>button:hover{{background:rgba(255,255,255,0.26)!important;border-color:rgba(255,255,255,0.55)!important;}}
.stSelectbox>div>div{{background:rgba(255,255,255,0.12)!important;border:1.5px solid rgba(255,255,255,0.25)!important;border-radius:14px!important;color:white!important;}}
.stSelectbox>div>div>div{{color:white!important;}}
[data-baseweb="select"] svg{{fill:white!important;}}
[data-baseweb="popover"] li{{background:#1a2a40!important;color:white!important;}}
[data-baseweb="popover"] li:hover{{background:#264460!important;}}
.stAlert{{background:rgba(255,255,255,0.1)!important;border:1px solid rgba(255,255,255,0.2)!important;border-radius:12px!important;color:white!important;}}
.stSpinner>div{{border-top-color:white!important;}}
hr{{border-color:rgba(255,255,255,0.15)!important;margin:0.6rem 0!important;}}
iframe{{border:none!important;}}
</style>
""", unsafe_allow_html=True)

def reverse_geocode(lat, lon):
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json", "zoom": 10},
            headers={"User-Agent": "SpiritWeather/1.0"},
            timeout=8,
        )
        d = resp.json()
        addr = d.get("address", {})
        city = (addr.get("city") or addr.get("town") or
                addr.get("village") or addr.get("county") or "Unknown")
        return city, addr.get("country", "")
    except Exception:
        return "Unknown", ""

def detect_location_by_ip():
    for url, check, extract in [
        ("https://ip-api.com/json/",
         lambda d: d.get("status")=="success" and d.get("city"),
         lambda d: {"name":d["city"],"country":d.get("country",""),
                    "lat":float(d.get("lat",0)),"lon":float(d.get("lon",0)),"timezone":d.get("timezone","auto")}),
        ("https://ipwho.is/",
         lambda d: d.get("success") and d.get("city"),
         lambda d: {"name":d["city"],"country":d.get("country",""),
                    "lat":float(d.get("latitude",0)),"lon":float(d.get("longitude",0)),"timezone":d.get("timezone",{}).get("id","auto")}),
        ("https://ipapi.co/json/",
         lambda d: d.get("city") and not d.get("error"),
         lambda d: {"name":d["city"],"country":d.get("country_name",""),
                    "lat":float(d.get("latitude",0)),"lon":float(d.get("longitude",0)),"timezone":d.get("timezone","auto")}),
    ]:
        try:
            d = requests.get(url, timeout=5).json()
            if check(d): return extract(d)
        except Exception:
            pass
    return None

def search_cities(query):
    try:
        resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name":query,"count":10,"language":"en","format":"json"},
            timeout=10,
        )
        return [{"name":r.get("name"),"country":r.get("country",""),
                 "admin":r.get("admin1",""),"lat":r["latitude"],
                 "lon":r["longitude"],"timezone":r.get("timezone","auto")}
                for r in resp.json().get("results",[])]
    except Exception:
        return []

def get_weather(lat, lon, timezone):
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude":lat,"longitude":lon,
            "current":["temperature_2m","apparent_temperature","relative_humidity_2m",
                       "wind_speed_10m","visibility","surface_pressure","weather_code","is_day"],
            "hourly":["temperature_2m","weather_code","precipitation_probability"],
            "daily":["weather_code","temperature_2m_max","temperature_2m_min","sunrise","sunset"],
            "timezone":timezone,"forecast_days":7,"wind_speed_unit":"kmh",
        },
        timeout=10,
    )
    return resp.json()

def fmt_time(iso_str):
    try:
        parts = iso_str.split("T")
        return parts[1][:5] if len(parts)>1 else iso_str
    except: return "—"

def short_day(date_str, t):
    try: return t["days_short"][datetime.date.fromisoformat(date_str).weekday()]
    except: return date_str

def full_day(date_str, t):
    try: return t["days_full"][datetime.date.fromisoformat(date_str).weekday()]
    except: return date_str

def fmt_hour(iso_str, is_kn=False):
    try:
        h = int(iso_str.split("T")[1][:2])
        if h==0:  return "12 AM" if not is_kn else "12 ರಾ"
        if h==12: return "12 PM" if not is_kn else "12 ಮ"
        if h<12:  return f"{h} AM" if not is_kn else f"{h} ರಾ"
        return f"{h-12} PM" if not is_kn else f"{h-12} ಸಂ"
    except: return iso_str

def render_weather(loc, weather, t, is_kn):
    current = weather.get("current",{})
    daily   = weather.get("daily",{})
    hourly  = weather.get("hourly",{})
    if not current:
        st.error("Unable to fetch weather data."); return

    wcode  = current.get("weather_code",0)
    is_day = current.get("is_day",1)
    temp   = round(current.get("temperature_2m",0))
    feels  = round(current.get("apparent_temperature",0))
    humid  = current.get("relative_humidity_2m",0)
    wind   = round(current.get("wind_speed_10m",0))
    vis    = round(current.get("visibility",0)/1000,1)
    press  = round(current.get("surface_pressure",0))
    cond   = t["condition_map"].get(wcode, t["condition_map"].get(0,""))
    icon   = WEATHER_ICONS.get(wcode,"🌡️")
    tmax   = round(daily.get("temperature_2m_max",[temp])[0])
    tmin   = round(daily.get("temperature_2m_min",[temp])[0])
    sr = fmt_time(daily.get("sunrise",["—"])[0] if daily.get("sunrise") else "—")
    ss = fmt_time(daily.get("sunset", ["—"])[0] if daily.get("sunset")  else "—")

    new_g = get_gradient(wcode, is_day)
    if new_g != st.session_state.get("gradient",""):
        st.session_state.gradient = new_g
        inject_css(new_g)

    now = datetime.datetime.now()
    date_str = f"{full_day(now.strftime('%Y-%m-%d'),t)}, {now.day} {t['months'][now.month-1]}"

    # Hero
    st.markdown(f"""
<div style="text-align:center;padding:1.8rem 0 1.4rem">
  <div style="font-size:0.9rem;opacity:0.75;letter-spacing:0.04em;margin-bottom:0.15rem">📍 {loc['name']}, {loc['country']}</div>
  <div style="font-size:0.78rem;opacity:0.55;margin-bottom:1.4rem">{date_str}</div>
  <div style="font-size:5.5rem;line-height:1;margin-bottom:0.3rem">{icon}</div>
  <div style="font-size:5.8rem;font-weight:200;line-height:1;letter-spacing:-3px;margin-bottom:0.2rem">{temp}°</div>
  <div style="font-size:1.15rem;font-weight:400;opacity:0.9;margin-bottom:0.4rem">{cond}</div>
  <div style="font-size:0.85rem;opacity:0.65">{t['high']}: {tmax}° &nbsp;·&nbsp; {t['low']}: {tmin}°</div>
</div>""", unsafe_allow_html=True)

    # Stats
    C = "background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.16);border-radius:16px;padding:14px 10px;text-align:center;backdrop-filter:blur(12px);"
    L = "font-size:0.7rem;opacity:0.6;margin-bottom:4px;letter-spacing:0.06em;text-transform:uppercase"
    V = "font-size:1.3rem;font-weight:600"
    S = "font-size:0.72rem;opacity:0.55;margin-top:2px"
    stats = [("🌡️",t["feels_like"],f"{feels}°",""),("💧",t["humidity"],f"{humid}%",""),
             ("💨",t["wind"],f"{wind}","km/h"),("👁️",t["visibility"],f"{vis}","km"),
             ("🔵",t["pressure"],f"{press}","hPa"),("🌅",t["sunrise"],sr,""),
             ("🌇",t["sunset"],ss,""),None]
    for row in [stats[:4], stats[4:]]:
        cols = "".join([
            f'<div style="{C}"><div style="{L}">{s[0]} {s[1]}</div><div style="{V}">{s[2]}</div><div style="{S}">{s[3]}</div></div>'
            if s else f'<div style="{C};opacity:0;pointer-events:none"></div>'
            for s in row])
        st.markdown(f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 8px">{cols}</div>', unsafe_allow_html=True)

    # Hourly
    h_times  = hourly.get("time",[])
    h_temps  = hourly.get("temperature_2m",[])
    h_codes  = hourly.get("weather_code",[])
    h_precip = hourly.get("precipitation_probability",[0]*len(h_times))
    now_str  = now.strftime("%Y-%m-%dT%H:00")
    si = next((i for i,ts in enumerate(h_times) if ts>=now_str),0)
    HC = "min-width:64px;background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.14);border-radius:14px;padding:10px 6px;text-align:center;backdrop-filter:blur(10px);flex-shrink:0;"
    hcards = ""
    for idx,(ts,ht,hc,hp) in enumerate(zip(h_times[si:si+24],h_temps[si:si+24],h_codes[si:si+24],h_precip[si:si+24])):
        lbl  = "Now" if idx==0 else fmt_hour(ts,is_kn)
        bold = "font-weight:700" if idx==0 else "font-weight:400"
        pr   = f'<div style="font-size:0.65rem;color:rgba(130,200,255,0.9);margin-top:3px">💧{int(hp)}%</div>' if hp and int(hp)>0 else '<div style="height:14px"></div>'
        hcards += f'<div style="{HC}"><div style="font-size:0.7rem;opacity:0.7;{bold}">{lbl}</div><div style="font-size:1.6rem;margin:4px 0">{WEATHER_ICONS.get(hc,"🌡️")}</div><div style="font-size:0.9rem;font-weight:600">{round(ht)}°</div>{pr}</div>'
    st.markdown(f'<div style="margin:16px 0 8px"><div style="font-size:0.72rem;opacity:0.55;letter-spacing:0.07em;text-transform:uppercase;margin-bottom:8px">🕐 {t["hourly_title"]}</div><div style="display:flex;gap:7px;overflow-x:auto;padding-bottom:6px;scrollbar-width:none;">{hcards}</div></div>', unsafe_allow_html=True)

    # Daily
    d_dates=daily.get("time",[]); d_codes=daily.get("weather_code",[])
    d_max=daily.get("temperature_2m_max",[]); d_min=daily.get("temperature_2m_min",[])
    rmax=max((m for m in d_max if m is not None),default=40)
    rmin=min((m for m in d_min if m is not None),default=0)
    rspan=max(rmax-rmin,1)
    rows=""
    for i,(dd,dc,dmx,dmn) in enumerate(zip(d_dates,d_codes,d_max,d_min)):
        lbl=("Today" if not is_kn else "ಇಂದು") if i==0 else short_day(dd,t)
        dicon=WEATHER_ICONS.get(dc,"🌡️")
        bl=round(((dmn-rmin)/rspan)*100); bw=max(round(((dmx-dmn)/rspan)*100),5)
        bc="#64b5f6" if dc not in [51,53,55,61,63,65,80,81,82,95,96,99] else "#42a5f5"
        rbg="rgba(255,255,255,0.06)" if i%2==0 else "rgba(255,255,255,0.03)"
        bld="font-weight:700" if i==0 else "font-weight:400"
        rows+=(f'<div style="display:grid;grid-template-columns:68px 28px 1fr 80px;align-items:center;gap:12px;padding:12px 14px;border-radius:12px;background:{rbg};margin-bottom:2px;">'
               f'<div style="font-size:0.88rem;{bld};opacity:{0.95 if i==0 else 0.8}">{lbl}</div>'
               f'<div style="font-size:1.4rem;text-align:center">{dicon}</div>'
               f'<div style="position:relative;height:6px;background:rgba(255,255,255,0.15);border-radius:3px;overflow:hidden">'
               f'<div style="position:absolute;left:{bl}%;width:{bw}%;height:100%;background:linear-gradient(90deg,{bc},{bc}cc);border-radius:3px"></div></div>'
               f'<div style="display:flex;justify-content:space-between;font-size:0.88rem">'
               f'<span style="opacity:0.55">{round(dmn)}°</span><span style="font-weight:600">{round(dmx)}°</span></div></div>')
    st.markdown(f'<div style="margin:16px 0 8px"><div style="font-size:0.72rem;opacity:0.55;letter-spacing:0.07em;text-transform:uppercase;margin-bottom:8px">📅 {t["daily_title"]}</div><div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);border-radius:18px;overflow:hidden;backdrop-filter:blur(12px);">{rows}</div></div>', unsafe_allow_html=True)


# ── App ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Spirit Weather / ಸ್ಪಿರಿಟ್ ವೆದರ್", page_icon="🌤️",
                   layout="centered", initial_sidebar_state="collapsed")

if "auto_done" not in st.session_state:
    st.session_state.auto_done      = False
    st.session_state.location       = None
    st.session_state.search_results = []
    st.session_state.wcode          = 0
    st.session_state.is_day         = 1
    st.session_state.gradient       = get_gradient(0,1)

inject_css(st.session_state.gradient)

tc1,tc2 = st.columns([3,1])
with tc2:
    selected_lang = st.selectbox("Language", list(TRANSLATIONS.keys()),
                                  key="lang_sel", label_visibility="collapsed")
t = TRANSLATIONS[selected_lang]
is_kn = "ಕನ್ನಡ" in selected_lang
with tc1:
    st.markdown(f"<h2 style='color:white;margin:0.3rem 0 0.1rem;font-size:1.3rem;font-weight:700;letter-spacing:0.02em'>🌤️ {t['title']}</h2>", unsafe_allow_html=True)

if not st.session_state.auto_done:
    st.markdown(f"<p style='font-size:0.82rem;opacity:0.65;margin:0.2rem 0 0.5rem'>{t['allow_location']}</p>", unsafe_allow_html=True)
    with st.spinner(t["detecting"]):
        geo = get_geolocation()
    if geo and geo.get("coords"):
        lat = geo["coords"]["latitude"]
        lon = geo["coords"]["longitude"]
        city, country = reverse_geocode(lat, lon)
        st.session_state.location = {"name":city,"country":country,"lat":lat,"lon":lon,"timezone":"auto"}
    else:
        loc = detect_location_by_ip()
        if loc: st.session_state.location = loc
        else:   st.warning(t["error_location"])
    st.session_state.auto_done = True
    st.rerun()

sc1,sc2 = st.columns([4,1])
with sc1:
    search_q = st.text_input("Search", placeholder=t["search_placeholder"],
                               label_visibility="collapsed", key="search_input")
with sc2:
    search_clicked = st.button(t["search_button"], use_container_width=True)

if search_clicked and search_q.strip():
    with st.spinner(t["loading"]):
        results = search_cities(search_q.strip())
    st.session_state.search_results = results
elif search_clicked:
    st.session_state.search_results = []

if st.session_state.search_results:
    results = st.session_state.search_results
    if len(results)==1:
        st.session_state.location = results[0]
        st.session_state.search_results = []
        st.rerun()
    else:
        options=[f"{r['name']}{', '+r['admin'] if r['admin'] else ''}, {r['country']}" for r in results]
        chosen = st.selectbox(t["select_city"], options, key="city_sel")
        if st.button(f"✅  {chosen}", use_container_width=True, key="pick_city"):
            st.session_state.location = results[options.index(chosen)]
            st.session_state.search_results = []
            st.rerun()

if st.session_state.location and not st.session_state.search_results:
    loc = st.session_state.location
    with st.spinner(t["loading"]):
        weather = get_weather(loc["lat"],loc["lon"],loc["timezone"])
    render_weather(loc, weather, t, is_kn)
elif not st.session_state.location and not st.session_state.search_results:
    st.markdown('<div style="text-align:center;padding:3rem 1rem;opacity:0.55"><div style="font-size:3rem;margin-bottom:1rem">🌍</div><div style="font-size:1rem">Enter a city or country above to get started</div></div>', unsafe_allow_html=True)
