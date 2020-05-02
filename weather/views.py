from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f7e2f8fe3a88d9c86993f1605d398ba9'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count==0:
                r = requests.get(url.format(new_city)).json()

                if r['cod']==200:
                    form.save()
                else:
                    err_msg = 'City does not exists in world!'

            else:
                err_msg = 'City already exists in database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'

        else:
            message = 'Succesfully created'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        
        weather_city = {
            'name' : city.name,
            'temperature' : r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather_city)

    context = {'weather_data' : weather_data, 'form': form, 'message': message, 'message_class': message_class}

    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')