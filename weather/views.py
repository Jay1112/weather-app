from django.shortcuts import render
import requests

from .forms import *

def index(request):
	form = CityForm()
	if request.method == "POST":
		form_ = CityForm(request.POST)

		city_name = None

		if form_.is_valid():
			city_name = form_.cleaned_data['name']
		
		url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID=a3a594661e0f4804e2f40e6759b10b1e'

		r = None
		city_weather = None

		try:
			r = requests.get(url).json()

			city_weather = {
				'city': city_name,
				'temperature': format(r["main"]["temp"]-273.15,'.2f'),
				'description': r["weather"][0]['description'],
				'icon': r["weather"][0]['icon'],
				'ur':url,
			}
		except KeyError:
			message = "City is not found."
			return render(request,"index.html",{
					'message':message,
					'form':form,
			})

		context = {'city_weather':city_weather,'form':form}
		return render(request,"index.html",context)

	context = {"nothing":"nothing",'form':form}
	return render(request,"index.html",context)