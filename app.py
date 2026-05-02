import streamlit as st
import requests

# ── Translations ───────────────────────────────────────────────────────────────

TRANSLATIONS = {
    "English": {
        "title": "🌤️ Weather App",
        "subtitle": "Real-time weather with automatic location detection",
        "search_label": "Search city or country",
        "search_placeholder": "e.g. Bengaluru, Paris, New York, Japan...",
        "search_button": "Search",
        "detecting": "Detecting your location...",
        "auto_location": "📍 Auto-detected your location",
        "feels_like": "Feels like",
        "humidity": "Humidity",
        "wind_speed": "Wind Speed",
        "visibility": "Visibility",
        "pressure": "Pressure",
        "sunrise": "Sunrise",
        "sunset": "Sunset",
        "weather_in": "Weather in",
        "error_city": "❌ City not found. Please check the spelling and try again.",
        "error_api": "❌ Unable to fetch weather data. Please try again later.",
        "error_location": "⚠️ Could not detect location. Please search manually.",
        "loading": "Fetching weather data...",
        "temp_unit": "°C",
        "wind_unit": "km/h",
        "humidity_unit": "%",
        "visibility_unit": "km",
        "pressure_unit": "hPa",
        "forecast_title": "5-Day Forecast",
        "search_results": "Search Results",
        "select_city": "Select a city from results:",
        "no_results": "No results found. Try a different name.",
        "condition_map": {
            0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
            45: "Foggy", 48: "Icy Fog",
            51: "Light Drizzle", 53: "Moderate Drizzle", 55: "Heavy Drizzle",
            61: "Slight Rain", 63: "Moderate Rain", 65: "Heavy Rain",
            71: "Slight Snow", 73: "Moderate Snow", 75: "Heavy Snow",
            77: "Snow Grains",
            80: "Slight Showers", 81: "Moderate Showers", 82: "Violent Showers",
            85: "Snow Showers", 86: "Heavy Snow Showers",
            95: "Thunderstorm", 96: "Thunderstorm w/ Hail", 99: "Thunderstorm w/ Heavy Hail",
        },
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "🌤️ ಹವಾಮಾನ ಅಪ್ಲಿಕೇಶನ್",
        "subtitle": "ಸ್ವಯಂಚಾಲಿತ ಸ್ಥಳ ಪತ್ತೆಯೊಂದಿಗೆ ನೈಜ-ಸಮಯ ಹವಾಮಾನ",
        "search_label": "ನಗರ ಅಥವಾ ದೇಶ ಹುಡುಕಿ",
        "search_placeholder": "ಉದಾ: ಬೆಂಗಳೂರು, ಮುಂಬೈ, ದೆಹಲಿ, ಭಾರತ...",
        "search_button": "ಹುಡುಕಿ",
        "detecting": "ನಿಮ್ಮ ಸ್ಥಳ ಪತ್ತೆ ಮಾಡಲಾಗುತ್ತಿದೆ...",
        "auto_location": "📍 ನಿಮ್ಮ ಸ್ಥಳ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಪತ್ತೆಯಾಗಿದೆ",
        "feels_like": "ಅನಿಸಿಕೆ ತಾಪಮಾನ",
        "humidity": "ತೇವಾಂಶ",
        "wind_speed": "ಗಾಳಿ ವೇಗ",
        "visibility": "ದೃಶ್ಯಮಾನತೆ",
        "pressure": "ಒತ್ತಡ",
        "sunrise": "ಸೂರ್ಯೋದಯ",
        "sunset": "ಸೂರ್ಯಾಸ್ತ",
        "weather_in": "ಹವಾಮಾನ -",
        "error_city": "❌ ನಗರ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಕಾಗುಣಿತ ಪರಿಶೀಲಿಸಿ.",
        "error_api": "❌ ಹವಾಮಾನ ಮಾಹಿತಿ ತರಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ನಂತರ ಪ್ರಯತ್ನಿಸಿ.",
        "error_location": "⚠️ ಸ್ಥಳ ಪತ್ತೆ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಹಸ್ತಚಾಲಿತವಾಗಿ ಹುಡುಕಿ.",
        "loading": "ಹವಾಮಾನ ಮಾಹಿತಿ ತರಲಾಗುತ್ತಿದೆ...",
        "temp_unit": "°ಸೆ",
        "wind_unit": "ಕಿಮೀ/ಗಂ",
        "humidity_unit": "%",
        "visibility_unit": "ಕಿಮೀ",
        "pressure_unit": "hPa",
        "forecast_title": "5-ದಿನಗಳ ಮುನ್ಸೂಚನೆ",
        "search_results": "ಹುಡುಕಾಟ ಫಲಿತಾಂಶಗಳು",
        "select_city": "ಫಲಿತಾಂಶಗಳಿಂದ ನಗರ ಆಯ್ಕೆ ಮಾಡಿ:",
        "no_results": "ಯಾವುದೇ ಫಲಿತಾಂಶ ಕಂಡುಬಂದಿಲ್ಲ. ಬೇರೆ ಹೆಸರು ಪ್ರಯತ್ನಿಸಿ.",
        "condition_map": {
            0: "ಸ್ಪಷ್ಟ ಆಕಾಶ", 1: "ಮುಖ್ಯವಾಗಿ ಸ್ಪಷ್ಟ", 2: "ಭಾಗಶಃ ಮೋಡ", 3: "ಮೋಡ ಕವಿದ",
            45: "ಮಂಜು", 48: "ಮಂಜಿನ ಮಂಜು",
            51: "ಹಗುರ ಹನಿಮಳೆ", 53: "ಮಧ್ಯಮ ಹನಿಮಳೆ", 55: "ಭಾರೀ ಹನಿಮಳೆ",
            61: "ಸ್ವಲ್ಪ ಮಳೆ", 63: "ಮಧ್ಯಮ ಮಳೆ", 65: "ಭಾರೀ ಮಳೆ",
            71: "ಸ್ವಲ್ಪ ಹಿಮ", 73: "ಮಧ್ಯಮ ಹಿಮ", 75: "ಭಾರೀ ಹಿಮ",
            77: "ಹಿಮ ಕಣಗಳು",
            80: "ಸ್ವಲ್ಪ ಮಳೆ ಝರಿ", 81: "ಮಧ್ಯಮ ಮಳೆ ಝರಿ", 82: "ತೀವ್ರ ಮಳೆ ಝರಿ",
            85: "ಹಿಮ ಝರಿ", 86: "ಭಾರೀ ಹಿಮ ಝರಿ",
            95: "ಗುಡುಗು ಸಹಿತ ಮಳೆ", 96: "ಆಲಿಕಲ್ಲು ಸಹಿತ ಗುಡುಗು", 99: "ಭಾರೀ ಆಲಿಕಲ್ಲು ಸಹಿತ ಗುಡುಗು",
        },
    },
}

WEATHER_ICONS = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️",
    51: "🌦️", 53: "🌦️", 55: "🌧️",
    61: "🌧️", 63: "🌧️", 65: "🌧️",
    71: "🌨️", 73: "🌨️", 75: "❄️",
    77: "🌨️",
    80: "🌦️", 81: "🌦️", 82: "⛈️",
    85: "🌨️", 86: "❄️",
    95: "⛈️", 96: "⛈️", 99: "⛈️",
}

WEEK_DAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEK_DAYS_KN = ["ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ", "ಭಾನುವಾರ"]


def detect_location_by_ip():
    try:
        resp = requests.get("https://ipapi.co/json/", timeout=5)
        data = resp.json()
        if data.get("city"):
            return {
                "name": data.get("city"),
                "country": data.get("country_name", ""),
                "lat": float(data.get("latitude", 0)),
                "lon": float(data.get("longitude", 0)),
                "timezone": data.get("timezone", "auto"),
            }
    except Exception:
        pass
    return None


def search_cities(query: str):
    try:
        resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": query, "count": 10, "language": "en", "format": "json"},
            timeout=10,
        )
        results = resp.json().get("results", [])
        return [
            {
                "name": r.get("name"),
                "country": r.get("country", ""),
                "admin": r.get("admin1", ""),
                "lat": r["latitude"],
                "lon": r["longitude"],
                "timezone": r.get("timezone", "auto"),
            }
            for r in results
        ]
    except Exception:
        return []


def get_weather(lat: float, lon: float, timezone: str):
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m", "apparent_temperature", "relative_humidity_2m",
                "wind_speed_10m", "visibility", "surface_pressure",
                "weather_code", "is_day",
            ],
            "daily": [
                "weather_code", "temperature_2m_max", "temperature_2m_min",
                "sunrise", "sunset",
            ],
            "timezone": timezone,
            "forecast_days": 6,
            "wind_speed_unit": "kmh",
        },
        timeout=10,
    )
    return resp.json()


def format_time(iso_str: str) -> str:
    try:
        parts = iso_str.split("T")
        return parts[1][:5] if len(parts) > 1 else iso_str
    except Exception:
        return "—"


def get_day_name(date_str: str, lang: str) -> str:
    import datetime
    try:
        idx = datetime.date.fromisoformat(date_str).weekday()
        return WEEK_DAYS_KN[idx] if "ಕನ್ನಡ" in lang else WEEK_DAYS_EN[idx]
    except Exception:
        return date_str


def display_weather(location: dict, t: dict, lang: str):
    weather = get_weather(location["lat"], location["lon"], location["timezone"])
    current = weather.get("current", {})
    daily = weather.get("daily", {})

    if not current:
        st.error(t["error_api"])
        return

    wcode = current.get("weather_code", 0)
    icon = WEATHER_ICONS.get(wcode, "🌡️")
    condition_map = t["condition_map"]
    condition = condition_map.get(wcode, condition_map.get(0, ""))

    st.subheader(f"{t['weather_in']} {location['name']}, {location['country']}")

    temp_col, detail_col = st.columns([1, 2])
    with temp_col:
        st.markdown(f"<h1 style='font-size:5rem;margin:0'>{icon}</h1>", unsafe_allow_html=True)
        st.markdown(
            f"<h2 style='margin:0'>{round(current.get('temperature_2m', 0))}{t['temp_unit']}</h2>",
            unsafe_allow_html=True,
        )
        st.write(f"**{condition}**")
    with detail_col:
        st.metric(t["feels_like"], f"{round(current.get('apparent_temperature', 0))}{t['temp_unit']}")
        st.metric(t["humidity"], f"{current.get('relative_humidity_2m', 0)}{t['humidity_unit']}")
        st.metric(t["wind_speed"], f"{round(current.get('wind_speed_10m', 0))} {t['wind_unit']}")

    st.divider()

    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        st.metric(t["visibility"], f"{round(current.get('visibility', 0) / 1000, 1)} {t['visibility_unit']}")
    with ec2:
        st.metric(t["pressure"], f"{round(current.get('surface_pressure', 0))} {t['pressure_unit']}")
    with ec3:
        sr = format_time(daily.get("sunrise", ["—"])[0] if daily.get("sunrise") else "—")
        ss = format_time(daily.get("sunset", ["—"])[0] if daily.get("sunset") else "—")
        st.write(f"🌅 {t['sunrise']}: **{sr}**")
        st.write(f"🌇 {t['sunset']}: **{ss}**")

    st.divider()
    st.subheader(t["forecast_title"])

    forecast_days = list(zip(
        daily.get("time", []),
        daily.get("temperature_2m_max", []),
        daily.get("temperature_2m_min", []),
        daily.get("weather_code", []),
    ))[1:6]

    fcols = st.columns(len(forecast_days))
    for i, (date, tmax, tmin, wc) in enumerate(forecast_days):
        with fcols[i]:
            st.markdown(
                f"""
                <div style='text-align:center;padding:8px;border-radius:10px;
                            background:rgba(100,149,237,0.12);'>
                    <div style='font-weight:bold;font-size:0.85rem'>{get_day_name(date, lang)}</div>
                    <div style='font-size:2rem'>{WEATHER_ICONS.get(wc, "🌡️")}</div>
                    <div style='font-size:0.75rem;color:gray'>{condition_map.get(wc, "")}</div>
                    <div style='font-weight:bold'>{round(tmax)}{t['temp_unit']}</div>
                    <div style='color:gray;font-size:0.85rem'>{round(tmin)}{t['temp_unit']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── Page config ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Weather App / ಹವಾಮಾನ ಅಪ್ಲಿಕೇಶನ್",
    page_icon="🌤️",
    layout="centered",
)

selected_lang = st.sidebar.selectbox(
    "🌐 Language / ಭಾಷೆ",
    list(TRANSLATIONS.keys()),
    index=0,
)
t = TRANSLATIONS[selected_lang]

st.title(t["title"])
st.caption(t["subtitle"])
st.divider()

# ── Session state init ─────────────────────────────────────────────────────────

if "auto_location_done" not in st.session_state:
    st.session_state.auto_location_done = False
    st.session_state.current_location = None
    st.session_state.search_results = []

# ── Auto-detect location on first load ────────────────────────────────────────

if not st.session_state.auto_location_done:
    with st.spinner(t["detecting"]):
        loc = detect_location_by_ip()
    st.session_state.auto_location_done = True
    if loc:
        st.session_state.current_location = loc
        st.success(f"{t['auto_location']}: **{loc['name']}, {loc['country']}**")
    else:
        st.warning(t["error_location"])

# ── Search bar ────────────────────────────────────────────────────────────────

col_input, col_btn = st.columns([4, 1])
with col_input:
    search_query = st.text_input(
        t["search_label"],
        placeholder=t["search_placeholder"],
        label_visibility="collapsed",
        key="search_input",
    )
with col_btn:
    search_clicked = st.button(t["search_button"], use_container_width=True)

if search_clicked and search_query.strip():
    with st.spinner(t["loading"]):
        results = search_cities(search_query.strip())
    st.session_state.search_results = results
elif search_clicked:
    st.session_state.search_results = []

# ── Search results picker ─────────────────────────────────────────────────────

if st.session_state.search_results:
    results = st.session_state.search_results
    if len(results) == 1:
        st.session_state.current_location = results[0]
        st.session_state.search_results = []
        st.rerun()
    else:
        st.subheader(t["search_results"])
        options = [
            f"{r['name']}{', ' + r['admin'] if r['admin'] else ''}, {r['country']}"
            for r in results
        ]
        chosen = st.selectbox(t["select_city"], options, key="city_select")
        if st.button("✅ " + chosen, use_container_width=True):
            idx = options.index(chosen)
            st.session_state.current_location = results[idx]
            st.session_state.search_results = []
            st.rerun()

# ── Display weather ───────────────────────────────────────────────────────────

if st.session_state.current_location and not st.session_state.search_results:
    st.divider()
    with st.spinner(t["loading"]):
        display_weather(st.session_state.current_location, t, selected_lang)
elif not st.session_state.current_location and not st.session_state.search_results:
    st.info(
        "👆 Enter a city or country name above and click Search!"
        if "ಕನ್ನಡ" not in selected_lang
        else "👆 ಮೇಲೆ ನಗರ ಅಥವಾ ದೇಶದ ಹೆಸರು ನಮೂದಿಸಿ ಮತ್ತು ಹುಡುಕಿ!"
    )
