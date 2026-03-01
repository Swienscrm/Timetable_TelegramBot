import requests

WEATHER_CODES = {
    0: "Ясно",
    1: "Малооблачно",
    2: "Малооблачно",
    3: "Пасмурно",
    45: "Туман",
    48: "Туман",
    51: "Морось",
    53: "Морось",
    55: "Морось",
    56: "Морось",
    57: "Морось",
    61: "Дождь",
    63: "Дождь",
    65: "Дождь",
    66: "Дождь",
    67: "Дождь",
    71: "Снег",
    73: "Снег",
    75: "Снег",
    77: "Снег",
}

def get_weather_text(weather_code: int) -> str:
    if weather_code >= 95:
        return "Гроза"
    return WEATHER_CODES.get(weather_code, "неизвестно")

def get_weather():
    lan = 55.06519
    lon = 82.92251

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lan}&longitude={lon}"
        f"&current=temperature_2m,weathercode"
    )

    r = requests.get(url)
    data = r.json()

    temp = data["current"]["temperature_2m"]
    weather_code = data["current"]["weathercode"]
    weather = get_weather_text(weather_code)

    return f"Сейчас на улице: {int(temp)}°C, {weather}"