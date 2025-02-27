from django.shortcuts import render
import aiohttp
import asyncio
from .models import Photo


API_KEY = "790a747b54494fe0b4e120429252602"


# Асинхронная функция запроса температуры воздуха и воды
async def fetch_weather(city):
    url = f'https://api.weatherapi.com/v1/marine.json?key={API_KEY}&q={city},Turkey'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data_weather = await response.json()
            weather_dict = {
                'city': city,
                'air_temp': data_weather['forecast']['forecastday'][0]['day']['maxtemp_c'],
                'sea_temp': data_weather['forecast']['forecastday'][0]['hour'][0]['water_temp_c']
            }
            return weather_dict


# Асинхронный View для Django
async def index_page(request):
    CITIES = ['antalya', 'side', 'kemer']
    tasks = [fetch_weather(city) for city in CITIES]
    results = await asyncio.gather(*tasks)  # Запускаем все запросы параллельно
    context = {}
    for res in results:
        context[res['city']] = {
            'air_temp': res['air_temp'], 
            'sea_temp': res['sea_temp']
        }
    return render(request, 'vacation/index.html', context)


def antalya_list(request):
    context = {
        'photos': Photo.objects.filter(city=1)
    }
    return render(request, 'vacation/antalya_list.html', context)


def side_list(request):
    context = {
        'photos': Photo.objects.filter(city=2)
    }
    return render(request, 'vacation/side_list.html', context)


def kemer_list(request):
    context = {
        'photos': Photo.objects.filter(city=3)
    }
    return render(request, 'vacation/kemer_list.html', context)
