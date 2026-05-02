import streamlit as st
import requests
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(
    page_title="Grand Line Weather",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ONE_PIECE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: linear-gradient(160deg, #0a1628 0%, #0d2444 40%, #0f2d54 70%, #112040 100%) !important;
    min-height: 100vh;
}
[data-testid="stAppViewContainer"] { background: transparent !important; }
[data-testid="stMain"] { background: transparent !important; }
[data-testid="block-container"] { padding-top: 1rem !important; }

h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: #f0a500 !important;
    text-shadow: 0 0 20px rgba(240, 165, 0, 0.4) !important;
}
p, span, label, div { font-family: 'Crimson Text', serif !important; color: #f5e6c8 !important; }

.stTextInput > div > div > input {
    background: rgba(10, 30, 60, 0.8) !important;
    border: 1px solid rgba(240, 165, 0, 0.4) !important;
    border-radius: 4px !important;
    color: #f5e6c8 !important;
    font-family: 'Crimson Text', serif !important;
    font-size: 1.1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #f0a500 !important;
    box-shadow: 0 0 10px rgba(240, 165, 0, 0.3) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1a3a5c, #0a1628) !important;
    border: 1px solid rgba(240, 165, 0, 0.5) !important;
    color: #f0a500 !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 1px !important;
    border-radius: 4px !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #f0a500, #c8860a) !important;
    color: #0a1628 !important;
    border-color: #f0a500 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(240, 165, 0, 0.4) !important;
}
[data-testid="stSidebar"] {
    background: rgba(10, 22, 40, 0.95) !important;
    border-right: 1px solid rgba(240, 165, 0, 0.2) !important;
}
.weather-card {
    background: linear-gradient(135deg, rgba(15, 35, 65, 0.9), rgba(10, 25, 50, 0.95));
    border: 1px solid rgba(240, 165, 0, 0.25);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5), inset 0 1px 0 rgba(240,165,0,0.1);
    position: relative;
    overflow: hidden;
}
.weather-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(240,165,0,0.6), transparent);
}
.temp-display {
    font-family: 'Cinzel', serif;
    font-size: 5rem;
    font-weight: 900;
    color: #f0a500;
    text-shadow: 0 0 30px rgba(240,165,0,0.5);
    line-height: 1;
    margin: 0.5rem 0;
}
.city-name {
    font-family: 'Cinzel', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #f5e6c8;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.condition-text {
    font-family: 'Cinzel', serif;
    font-size: 1.2rem;
    color: #a8c8e8;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.stat-label {
    font-family: 'Cinzel', serif;
    font-size: 0.7rem;
    color: rgba(240,165,0,0.7);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.stat-value { font-family: 'Crimson Text', serif; font-size: 1.4rem; color: #f5e6c8; font-weight: 600; }
.forecast-card {
    background: linear-gradient(135deg, rgba(15,35,65,0.8), rgba(10,25,50,0.9));
    border: 1px solid rgba(240,165,0,0.2);
    border-radius: 6px;
    padding: 1rem 0.75rem;
    text-align: center;
    transition: all 0.3s ease;
}
.forecast-card:hover {
    border-color: rgba(240,165,0,0.5);
    box-shadow: 0 4px 15px rgba(240,165,0,0.15);
    transform: translateY(-2px);
}
.forecast-day { font-family: 'Cinzel', serif; font-size: 0.75rem; color: rgba(240,165,0,0.8); letter-spacing: 1px; text-transform: uppercase; }
.forecast-icon { font-size: 1.8rem; margin: 0.4rem 0; }
.forecast-temp { font-family: 'Crimson Text', serif; font-size: 1.1rem; color: #f5e6c8; font-weight: 600; }
.header-title {
    font-family: 'Cinzel', serif;
    font-size: 1.8rem;
    font-weight: 900;
    color: #f0a500;
    text-shadow: 0 0 20px rgba(240,165,0,0.5);
    letter-spacing: 4px;
    text-transform: uppercase;
    text-align: center;
}
.header-subtitle {
    font-family: 'Crimson Text', serif;
    font-size: 1rem;
    color: rgba(168,200,232,0.7);
    letter-spacing: 3px;
    text-transform: uppercase;
    text-align: center;
    font-style: italic;
}
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(240,165,0,0.4), transparent);
    margin: 1rem 0;
}
.section-title {
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    color: rgba(240,165,0,0.8);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.location-error {
    background: rgba(180,50,50,0.2);
    border: 1px solid rgba(240,100,100,0.4);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    color: #ffaaaa;
    font-family: 'Crimson Text', serif;
    font-size: 1rem;
}
.hourly-bar {
    background: linear-gradient(135deg, rgba(15,35,65,0.8), rgba(10,25,50,0.9));
    border: 1px solid rgba(240,165,0,0.15);
    border-radius: 6px;
    padding: 0.75rem 0.5rem;
    text-align: center;
}
.hourly-time { font-family: 'Cinzel', serif; font-size: 0.65rem; color: rgba(240,165,0,0.7); letter-spacing: 1px; }
.hourly-temp { font-family: 'Crimson Text', serif; font-size: 1.1rem; color: #f5e6c8; font-weight: 600; margin-top: 0.3rem; }
[data-testid="stSelectbox"] label, [data-testid="stTextInput"] label {
    color: rgba(240,165,0,0.8) !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
.stSelectbox > div > div { background: rgba(10,30,60,0.8) !important; border: 1px solid rgba(240,165,0,0.3) !important; color: #f5e6c8 !important; }
[data-testid="stMarkdownContainer"] p { color: #f5e6c8; }
[data-testid="stSpinner"] p { color: #f0a500 !important; }
.stSpinner > div { border-top-color: #f0a500 !important; }
</style>
"""

WMO_CODES = {
    0:  ("Clear Skies",        "☀"),
    1:  ("Mostly Clear",       "🌤"),
    2:  ("Partly Cloudy",      "⛅"),
    3:  ("Overcast",           "☁"),
    45: ("Foggy Seas",         "🌫"),
    48: ("Icy Fog",            "🌫"),
    51: ("Light Drizzle",      "🌦"),
    53: ("Drizzle",            "🌦"),
    55: ("Heavy Drizzle",      "🌧"),
    61: ("Light Rain",         "🌧"),
    63: ("Rain",               "🌧"),
    65: ("Heavy Rain",         "🌧"),
    71: ("Light Snow",         "🌨"),
    73: ("Snow",               "❄"),
    75: ("Heavy Snow",         "❄"),
    77: ("Snow Grains",        "❄"),
    80: ("Rain Squall",        "🌦"),
    81: ("Heavy Rain Squall",  "🌧"),
    82: ("Violent Squall",     "⛈"),
    85: ("Snow Showers",       "🌨"),
    86: ("Heavy Snow Showers", "❄"),
    95: ("Thunderstorm",       "⛈"),
    96: ("Hailstorm",          "⛈"),
    99: ("Severe Hailstorm",   "⛈"),
}

WIND_DIRS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

def get_wind_direction(degrees):
    if degrees is None:
        return "—"
    idx = round(degrees / 22.5) % 16
    return WIND_DIRS[idx]

def get_condition(code):
    if code is None:
        return ("Unknown", "?")
    return WMO_CODES.get(int(code), ("Unknown Conditions", "?"))

def fetch_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        f"wind_speed_10m,wind_direction_10m,weather_code,precipitation,cloud_cover"
        f"&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum"
        f"&hourly=temperature_2m,weather_code&forecast_hours=24"
        f"&temperature_unit=celsius&wind_speed_unit=kmh&timezone=auto"
    )
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def fetch_geocoding(query):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=6&language=en&format=json"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json().get("results", [])

def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {"User-Agent": "OnePieceWeatherApp/1.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    addr = data.get("address", {})
    city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or "Unknown Port"
    return city, addr.get("country", "")

def render_current_weather(weather_data, city_name, country):
    current = weather_data.get("current", {})
    temp = current.get("temperature_2m")
    feels = current.get("apparent_temperature")
    humidity = current.get("relative_humidity_2m")
    wind_speed = current.get("wind_speed_10m")
    wind_dir_deg = current.get("wind_direction_10m")
    code = current.get("weather_code")
    precip = current.get("precipitation", 0)
    cloud = current.get("cloud_cover", 0)
    condition, _ = get_condition(code)
    wind_dir = get_wind_direction(wind_dir_deg)
    location_str = f"{city_name}, {country}" if country else city_name
    st.markdown(f"""
    <div class="weather-card">
        <div class="city-name">{location_str}</div>
        <div class="condition-text">{condition}</div>
        <div class="temp-display">{round(temp) if temp is not None else "—"}°</div>
        <div style="font-family:'Crimson Text',serif;color:rgba(168,200,232,0.8);font-size:1.1rem;margin-top:-0.5rem;margin-bottom:1rem;">
            Feels like {round(feels) if feels is not None else "—"}°C
        </div>
        <hr class="divider">
        <div style="display:flex;gap:2rem;flex-wrap:wrap;margin-top:0.5rem;">
            <div><div class="stat-label">Humidity</div><div class="stat-value">{humidity}%</div></div>
            <div><div class="stat-label">Wind</div><div class="stat-value">{wind_speed} km/h {wind_dir}</div></div>
            <div><div class="stat-label">Cloud Cover</div><div class="stat-value">{cloud}%</div></div>
            <div><div class="stat-label">Precipitation</div><div class="stat-value">{precip} mm</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_hourly(weather_data):
    hourly = weather_data.get("hourly", {})
    times = hourly.get("time", [])[:24]
    temps = hourly.get("temperature_2m", [])[:24]
    codes = hourly.get("weather_code", [])[:24]
    if not times:
        return
    st.markdown('<div class="section-title">24-Hour Forecast</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(times), 12))
    step = max(1, len(times) // 12)
    visible = list(range(0, len(times), step))[:12]
    for i, idx in enumerate(visible):
        if i >= len(cols):
            break
        time_str = times[idx][11:16] if len(times[idx]) > 10 else times[idx]
        temp_val = round(temps[idx]) if idx < len(temps) and temps[idx] is not None else "—"
        _, hour_icon = get_condition(codes[idx] if idx < len(codes) else 0)
        with cols[i]:
            st.markdown(f"""
            <div class="hourly-bar">
                <div class="hourly-time">{time_str}</div>
                <div style="font-size:1.2rem;margin:0.2rem 0;">{hour_icon}</div>
                <div class="hourly-temp">{temp_val}°</div>
            </div>
            """, unsafe_allow_html=True)

def render_forecast(weather_data):
    from datetime import datetime
    daily = weather_data.get("daily", {})
    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    codes = daily.get("weather_code", [])
    precips = daily.get("precipitation_sum", [])
    if not dates:
        return
    st.markdown('<div class="section-title" style="margin-top:1.5rem;">7-Day Voyage Log</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(dates), 7))
    for i, col in enumerate(cols):
        if i >= len(dates):
            break
        try:
            dt = datetime.strptime(dates[i], "%Y-%m-%d")
            day_label = "TODAY" if i == 0 else dt.strftime("%a").upper()
        except Exception:
            day_label = f"DAY {i+1}"
        _, icon = get_condition(codes[i] if i < len(codes) else 0)
        max_t = round(max_temps[i]) if i < len(max_temps) and max_temps[i] is not None else "—"
        min_t = round(min_temps[i]) if i < len(min_temps) and min_temps[i] is not None else "—"
        rain = round(precips[i], 1) if i < len(precips) and precips[i] is not None else 0
        with col:
            st.markdown(f"""
            <div class="forecast-card">
                <div class="forecast-day">{day_label}</div>
                <div class="forecast-icon">{icon}</div>
                <div class="forecast-temp">{max_t}° / {min_t}°</div>
                <div style="font-family:'Cinzel',serif;font-size:0.6rem;color:rgba(168,200,232,0.6);letter-spacing:1px;margin-top:0.3rem;">{rain}mm</div>
            </div>
            """, unsafe_allow_html=True)

def main():
    st.markdown(ONE_PIECE_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem 0;">
        <div class="header-title">&#9749; Grand Line Weather</div>
        <div class="header-subtitle">Navigator's Report — Know the Seas Before You Sail</div>
    </div>
    <hr class="divider">
    """, unsafe_allow_html=True)

    for key in ["weather_data", "city_name", "country", "search_results", "error_msg"]:
        if key not in st.session_state:
            st.session_state[key] = None if key == "weather_data" else ([] if key == "search_results" else "")

    col_loc, col_search, col_btn = st.columns([1, 3, 1])
    with col_loc:
        st.markdown('<div class="section-title" style="margin-bottom:0.3rem;">Current Location</div>', unsafe_allow_html=True)
        location_data = streamlit_geolocation()
    with col_search:
        st.markdown('<div class="section-title" style="margin-bottom:0.3rem;">Search a Port</div>', unsafe_allow_html=True)
        search_query = st.text_input("search_port", placeholder="Enter city name...", label_visibility="collapsed", key="city_search_input")
    with col_btn:
        st.markdown('<div style="margin-top:1.4rem;"></div>', unsafe_allow_html=True)
        if st.button("Chart Course", key="search_btn", use_container_width=True):
            if search_query.strip():
                with st.spinner("Charting the seas..."):
                    try:
                        results = fetch_geocoding(search_query.strip())
                        st.session_state.search_results = results
                        st.session_state.error_msg = "" if results else f"No port named '{search_query}' found on the charts."
                    except Exception as e:
                        st.session_state.error_msg = f"Could not reach the navigation charts: {e}"

    if location_data and location_data.get("latitude") and location_data.get("longitude"):
        lat, lon = location_data["latitude"], location_data["longitude"]
        if st.session_state.weather_data is None or st.session_state.get("last_lat") != lat or st.session_state.get("last_lon") != lon:
            with st.spinner("Reading the skies at your location..."):
                try:
                    city, country = reverse_geocode(lat, lon)
                    weather = fetch_weather(lat, lon)
                    st.session_state.weather_data = weather
                    st.session_state.city_name = city
                    st.session_state.country = country
                    st.session_state.last_lat = lat
                    st.session_state.last_lon = lon
                    st.session_state.search_results = []
                    st.session_state.error_msg = ""
                except Exception as e:
                    st.session_state.error_msg = f"Failed to read the weather scroll: {e}"

    if st.session_state.search_results:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Select Your Port</div>', unsafe_allow_html=True)
        results = st.session_state.search_results
        result_cols = st.columns(min(len(results), 3))
        for i, result in enumerate(results):
            name = result.get("name", "Unknown")
            admin = result.get("admin1", "")
            country_r = result.get("country", "")
            label = name + (f", {admin}" if admin else "") + (f" — {country_r}" if country_r else "")
            with result_cols[i % 3]:
                if st.button(label, key=f"result_{i}", use_container_width=True):
                    with st.spinner(f"Setting course for {name}..."):
                        try:
                            weather = fetch_weather(result.get("latitude"), result.get("longitude"))
                            st.session_state.weather_data = weather
                            st.session_state.city_name = name
                            st.session_state.country = country_r
                            st.session_state.search_results = []
                            st.session_state.error_msg = ""
                            st.rerun()
                        except Exception as e:
                            st.session_state.error_msg = f"Could not fetch weather for {name}: {e}"

    if st.session_state.error_msg:
        st.markdown(f'<div class="location-error">{st.session_state.error_msg}</div>', unsafe_allow_html=True)

    if st.session_state.weather_data:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        render_current_weather(st.session_state.weather_data, st.session_state.city_name, st.session_state.country)
        st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
        render_hourly(st.session_state.weather_data)
        render_forecast(st.session_state.weather_data)
    elif not st.session_state.error_msg:
        st.markdown("""
        <div style="text-align:center;padding:3rem 0;opacity:0.6;">
            <div style="font-size:3rem;margin-bottom:1rem;">🧭</div>
            <div style="font-family:'Cinzel',serif;color:rgba(240,165,0,0.7);font-size:1rem;letter-spacing:3px;">
                ALLOW LOCATION ACCESS OR SEARCH A PORT TO BEGIN
            </div>
            <div style="font-family:'Crimson Text',serif;color:rgba(168,200,232,0.5);margin-top:0.5rem;font-style:italic;">
                Every great voyage starts with reading the skies
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <hr class="divider" style="margin-top:3rem;">
    <div style="text-align:center;padding-bottom:1rem;">
        <div style="font-family:'Cinzel',serif;font-size:0.65rem;color:rgba(240,165,0,0.3);letter-spacing:3px;">
            POWERED BY OPEN-METEO &mdash; WEATHER DATA OF THE GRAND LINE
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
