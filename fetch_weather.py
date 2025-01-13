import requests  
import json  
from datetime import datetime  
  
def fetch_weather(api_key, location_key):  
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={api_key}&language=id"  
    response = requests.get(url)  
    data = response.json()  
      
    headline = data['Headline']  
    daily_forecast = data['DailyForecasts'][0]  
      
    weather_info = {  
        "headline_text": headline['Text'],  
        "headline_effective_date": datetime.fromisoformat(headline['EffectiveDate'][:-1]).strftime('%d-%m-%Y %H:%M'),  
        "headline_end_date": datetime.fromisoformat(headline['EndDate'][:-1]).strftime('%d-%m-%Y %H:%M'),  
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
  
def format_weather(weather_info):  
    formatted_weather = f"""  
Judul Ramalan Cuaca:  
    Teks: {weather_info['headline_text']}  
    Tanggal Efektif: {weather_info['headline_effective_date']}  
    Tanggal Berakhir: {weather_info['headline_end_date']}  
    Severity: {weather_info['headline_severity']}  
  
Suhu:  
    Suhu Minimum: {weather_info['temperature_min']} F  
    Suhu Maksimum: {weather_info['temperature_max']} F  
  
Kondisi Cuaca Harian:  
    Ikon Cuaca Siang: {weather_info['day_icon_phrase']}  
    Deskripsi Cuaca Siang: {'Hujan' if weather_info['day_has_precipitation'] else 'Tidak Hujan'}  
    Jenis Presipitasi Siang: {weather_info['day_precipitation_type'] if weather_info['day_has_precipitation'] else 'N/A'}  
    Ikon Cuaca Malam: {weather_info['night_icon_phrase']}  
    Deskripsi Cuaca Malam: {'Hujan' if weather_info['night_has_precipitation'] else 'Tidak Hujan'}  
    Jenis Presipitasi Malam: {weather_info['night_precipitation_type'] if weather_info['night_has_precipitation'] else 'N/A'}  
  
Link untuk Informasi Lebih Lanjut:  
    Tautan ke Halaman Ramalan Cuaca: {weather_info['mobile_link']}  
    """  
    return formatted_weather  
  
if __name__ == "__main__":  
    import os  
    api_key = os.getenv('ACCUWEATHER_API_KEY')  
    location_key = "202243"  
    weather_info = fetch_weather(api_key, location_key)  
    formatted_weather = format_weather(weather_info)  
    print(formatted_weather)  
