import requests  
from dateutil import parser  
  
def fetch_weather(api_key, location_key):  
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={api_key}&language=id"  
    response = requests.get(url)  
    data = response.json()  
      
    headline = data['Headline']  
    daily_forecast = data['DailyForecasts'][0]  
      
    weather_info = {  
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
        "mobile_link": daily_forecast['MobileLink'],  
        "link": daily_forecast['Link']  
    }  
      
    return weather_info  
  
def fahrenheit_to_celsius(fahrenheit):  
    return (fahrenheit - 32) * 5.0 / 9.0  
  
def format_weather(weather_info):  
    temp_min_celsius = fahrenheit_to_celsius(weather_info['temperature_min'])  
    temp_max_celsius = fahrenheit_to_celsius(weather_info['temperature_max'])  
      
    formatted_weather = f"""  
<!DOCTYPE html>  
<html lang="id">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Ramalan Cuaca</title>  
    <style>  
        body {{  
            font-family: Arial, sans-serif;  
            background-color: #f4f4f9;  
            margin: 0;  
            padding: 20px;  
        }}  
        .container {{  
            background-color: #ffffff;  
            padding: 20px;  
            border-radius: 8px;  
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);  
        }}  
        h1 {{  
            color: #333333;  
        }}  
        .section {{  
            margin-bottom: 20px;  
        }}  
        .section h2 {{  
            color: #555555;  
            border-bottom: 2px solid #dddddd;  
            padding-bottom: 5px;  
            margin-bottom: 10px;  
        }}  
        .section p {{  
            color: #333333;  
        }}  
        .link {{  
            color: #007bff;  
            text-decoration: none;  
        }}  
        .link:hover {{  
            text-decoration: underline;  
        }}  
    </style>  
</head>  
<body>  
    <div class="container">  
        <h1>Ramalan Cuaca Hari Ini</h1>  
          
        <div class="section">  
            <h2>Judul Ramalan Cuaca</h2>  
            <p><strong>Teks:</strong> {weather_info['headline_text']}</p>  
            <p><strong>Tanggal Efektif:</strong> {weather_info['headline_effective_date']}</p>  
            <p><strong>Tanggal Berakhir:</strong> {weather_info['headline_end_date']}</p>  
            <p><strong>Severity:</strong> {weather_info['headline_severity']}</p>  
        </div>  
          
        <div class="section">  
            <h2>Suhu</h2>  
            <p><strong>Suhu Minimum:</strong> {temp_min_celsius:.1f} °C</p>  
            <p><strong>Suhu Maksimum:</strong> {temp_max_celsius:.1f} °C</p>  
        </div>  
          
        <div class="section">  
            <h2>Kondisi Cuaca Harian</h2>  
            <p><strong>Ikon Cuaca Siang:</strong> {weather_info['day_icon_phrase']}</p>  
            <p><strong>Deskripsi Cuaca Siang:</strong> {'Hujan' if weather_info['day_has_precipitation'] else 'Tidak Hujan'}</p>  
            <p><strong>Jenis Presipitasi Siang:</strong> {weather_info['day_precipitation_type'] if weather_info['day_has_precipitation'] else 'N/A'}</p>  
            <p><strong>Ikon Cuaca Malam:</strong> {weather_info['night_icon_phrase']}</p>  
            <p><strong>Deskripsi Cuaca Malam:</strong> {'Hujan' if weather_info['night_has_precipitation'] else 'Tidak Hujan'}</p>  
            <p><strong>Jenis Presipitasi Malam:</strong> {weather_info['night_precipitation_type'] if weather_info['night_has_precipitation'] else 'N/A'}</p>  
        </div>  
          
        <div class="section">  
            <h2>Link untuk Informasi Lebih Lanjut</h2>  
            <p><a href="{weather_info['mobile_link']}" class="link">Tautan ke Halaman Ramalan Cuaca</a></p>  
        </div>  
    </div>  
</body>  
</html>  
"""  
    return formatted_weather  
  
if __name__ == "__main__":  
    import os  
    api_key = os.getenv('ACCUWEATHER_API_KEY')  
    location_key = "202243"  
    weather_info = fetch_weather(api_key, location_key)  
    formatted_weather = format_weather(weather_info)  
    print(formatted_weather)  
