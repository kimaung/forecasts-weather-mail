import requests  
from dateutil import parser  
import os  
  
def fetch_weather(api_key, location_key):  
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={api_key}&language=id"  
    response = requests.get(url)  
    data = response.json()  
  
    headline = data['Headline']  
    daily_forecast = data['DailyForecasts'][0]  
  
    return {  
        "headline_text": headline['Text'],  
        "headline_effective_date": parser.parse(headline['EffectiveDate']).strftime('%d-%m-%Y %H:%M'),  
        "headline_end_date": parser.parse(headline['EndDate']).strftime('%d-%m-%Y %H:%M'),  
        "headline_severity": headline['Severity'],  
        "temperature_min": daily_forecast['Temperature']['Minimum']['Value'],  
        "temperature_max": daily_forecast['Temperature']['Maximum']['Value'],  
        "day_icon_phrase": daily_forecast['Day']['IconPhrase'],  
        "day_has_precipitation": daily_forecast['Day']['HasPrecipitation'],  
        "day_precipitation_type": daily_forecast['Day']['PrecipitationType'] if daily_forecast['Day']['HasPrecipitation'] else None,  
        "night_icon_phrase": daily_forecast['Night']['IconPhrase'],  
        "night_has_precipitation": daily_forecast['Night']['HasPrecipitation'],  
        "night_precipitation_type": daily_forecast['Night']['PrecipitationType'] if daily_forecast['Night']['HasPrecipitation'] else None,  
        "mobile_link": daily_forecast['MobileLink']  
    }  
  
def fahrenheit_to_celsius(fahrenheit):  
    return (fahrenheit - 32) * 5.0 / 9.0  
  
def format_weather(weather_info, sender_name):  
    temp_min_celsius = fahrenheit_to_celsius(weather_info['temperature_min'])  
    temp_max_celsius = fahrenheit_to_celsius(weather_info['temperature_max'])  
  
    return f"""  
<!DOCTYPE html>  
<html lang="id">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Ramalan Cuaca</title>  
</head>  
<body style="font-family: 'Arial', sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">  
    <div class="weather-forecast" style="background: white; border-radius: 10px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); padding: 20px; max-width: 600px; margin: auto;">  
        <h2 style="text-align: center; color: #333; font-size: 24px; margin-bottom: 20px;">Ramalan Cuaca di Serang</h2>  
        <div class="headline" style="background-color: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 20px;">  
            <p><strong>Tanggal Efektif:</strong> {weather_info['headline_effective_date']}</p>  
            <p><strong>Tanggal Berakhir:</strong> {weather_info['headline_end_date']}</p>  
            <p><strong>Tingkat Keparahan:</strong> {weather_info['headline_severity']}</p>  
            <p><strong>Deskripsi:</strong> {weather_info['headline_text']}</p>  
        </div>  
          
        <h3 style="background-color: #ffcc00; color: #333; padding: 10px; border-radius: 5px;">Temperatur</h3>  
        <p><strong>Minimum:</strong> {temp_min_celsius:.1f} °C</p>  
        <p><strong>Maksimum:</strong> {temp_max_celsius:.1f} °C</p>  
          
        <h3 style="background-color: #ffcc00; color: #333; padding: 10px; border-radius: 5px;">Kondisi Cuaca</h3>  
        <p><strong>Cuaca Siang:</strong> {weather_info['day_icon_phrase']}</p>  
        <p><strong>Cuaca Malam:</strong> {weather_info['night_icon_phrase']}</p>  
          
        <h3 style="background-color: #ffcc00; color: #333; padding: 10px; border-radius: 5px;">Probabilitas Presipitasi</h3>  
        <p>Hujan di siang hari: <strong>{'Ya' if weather_info['day_has_precipitation'] else 'Tidak'}</strong></p>  
        <p>Hujan di malam hari: <strong>{'Ya' if weather_info['night_has_precipitation'] else 'Tidak'}</strong></p>  
        <p><strong>Jenis Presipitasi:</strong> {weather_info['day_precipitation_type'] if weather_info['day_has_precipitation'] else 'N/A'}</p>  
          
        <h3 style="background-color: #ffcc00; color: #333; padding: 10px; border-radius: 5px;">Informasi Lebih Lanjut</h3>  
        <p><a href="{weather_info['mobile_link']}" target="_blank" style="display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; transition: background-color 0.3s;">Lihat lebih lanjut</a></p>  
          
        <p style="text-align: center; margin-top: 20px;"><strong>Pengirim:</strong> {sender_name}</p>  
    </div>  
</body>  
</html>  
"""  
  
if __name__ == "__main__":  
    api_key = os.getenv('ACCUWEATHER_API_KEY')  
    location_key = "202243"  
    sender_name = "Dukun Cabhul 👻"
    weather_info = fetch_weather(api_key, location_key)  
    formatted_weather = format_weather(weather_info, sender_name)  
    with open('email_body.html', 'w') as f:  
        f.write(formatted_weather)  
