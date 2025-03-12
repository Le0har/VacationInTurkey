from django.shortcuts import render, redirect
import aiohttp
import asyncio
from .models import Photo
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserRegistrationForm, CommentForm 
from django.contrib import auth
from asgiref.sync import sync_to_async
from django.http import Http404


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
    is_auth = await sync_to_async(lambda: request.user.is_authenticated)()
    context['is_auth'] = is_auth
    return render(request, 'vacation/index.html', context)


def antalya_list(request):
    context = {
        'photos': Photo.objects.filter(city=1),
        'is_auth': request.user.is_authenticated
    }
    return render(request, 'vacation/antalya_list.html', context)


def side_list(request):
    context = {
        'photos': Photo.objects.filter(city=2),
        'is_auth': request.user.is_authenticated
    }
    return render(request, 'vacation/side_list.html', context)


def kemer_list(request):
    context = {
        'photos': Photo.objects.filter(city=3),
        'is_auth': request.user.is_authenticated
    }
    return render(request, 'vacation/kemer_list.html', context)


def photo_detail(request, photo_id):
    try:
        photo = Photo.objects.get(id=photo_id)
    except ObjectDoesNotExist:
        context = {
            'error': f'Фотография с ID = {photo_id} не найдена!'
        }
        return render(request, 'vacation/errors.html', context)
    else:
        comment_form = CommentForm()
        context = {
            'photo': photo,
            'comment_form': comment_form,
            'is_auth': request.user.is_authenticated
        }
        return render(request, 'vacation/photo_detail.html', context)
    

def create_user(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacation:index')
    context = {
        'form': form,
    }
    return render(request, 'vacation/registration.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'error': 'Неверные имя пользователя или пароль',
            }
            return render(request, 'vacation/index.html', context)
    return redirect('vacation:index')


def logout(request):
    auth.logout(request)
    return redirect('vacation:index')


def comment_add(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            photo_id = request.POST.get('photo_id')
            photo = Photo.objects.get(id=photo_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.photo = photo
            comment.save()
            return redirect('vacation:photo-detail', photo_id=photo.id)
        raise Http404
    