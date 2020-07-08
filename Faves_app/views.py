from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, City, Likes
from django.conf import settings
import bcrypt
import requests
import json
import os


# first page of app, login/registration #
def index(request):
    return render(request, 'loginPage.html')

# logs in a new user if validations pass #
def new_user(request):
    errors = User.objects.new_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        name= request.POST['name']
        home= request.POST['home']
        email= request.POST['email']
        password= request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(name=name, home=home, email=email, password=pw_hash)
        request.session['user_id'] = new_user.id
        return redirect(f'/main/{new_user.id}')

# logs in returning user if validations pass #
def login(request):
    errors = User.objects.return_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    login_user_list = User.objects.filter(name=request.POST['name'])  
    logged_in_user = login_user_list[0]
    request.session['user_id'] = logged_in_user.id
    return redirect(f'/main/{logged_in_user.id}')

API_KEY = settings.YELP_API_KEY
api_key= API_KEY
headers = {'Authorization': 'Bearer %s' % api_key}

# Dashboard page for logged in user #
def main(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')      
    user = User.objects.get(id=request.session['user_id'])
    home_town= user.home
    user_cities = user.users

# yelp API request for dashboard hometown get request #
    def foods(town):
        url='https://api.yelp.com/v3/businesses/search'
        Params = {'term':'food','location':town}
        req=requests.get(url, params=Params, headers=headers)
        parsed = json.loads(req.text)
        Fbusinesses = parsed["businesses"]
        return(Fbusinesses)

    def things(town):
        url='https://api.yelp.com/v3/businesses/search'
        Params = {'term':'to do','location':town}
        req=requests.get(url, params=Params, headers=headers)
        parsed = json.loads(req.text)
        Tbusinesses = parsed["businesses"]
        return(Tbusinesses)

    context ={
        'user':user,
        'Fbusinesses':foods(home_town),
        'Tbusinesses':things(home_town),
        'home_town':home_town,
        'user_cities' : user_cities.all(),
    }
    return render(request, 'main.html', context)

# Display add new city page #
def NewCity(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    user_cities = user.users

    context ={
        'user_cities' : user_cities.all(),
        'user':user,
    }
    return render(request, 'addCity.html', context)

# Add a new city #
def addNewCity(request):
    errors = City.objects.city_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        name= request.POST['name']
        new_city = City.objects.create(name=name, user=user)
        return redirect(f'/newcity/{user.id}')

# remove a city and assosiated likes #
def removeCity(request, city_id):
    user = User.objects.get(id=request.session['user_id'])
    city = City.objects.get(id=city_id)
    city.delete()
    return redirect(f'/newcity/{user.id}')

def removeFave(request, fave_id, city_id):
    city = City.objects.get(id=city_id)
    like = Likes.objects.get(id=fave_id)
    like.delete()
    return redirect(f'/citydetail/{city.id}')


def cityDetails(request, city_id):
    if 'user_id' not in request.session:
        return redirect('/')      
    user = User.objects.get(id=request.session['user_id'])
    city = City.objects.get(id=city_id)
    city_likes = city.l_cities
    if 'businesses' not in request.session:
        context={
        'city_likes': city_likes.all(),
        'user': user,
        'city': city,
    }
    else:
        businesses = request.session['businesses']
        context={
            'city_likes': city_likes.all(),
            'user': user,
            'city': city,
            'businesses': businesses
        }
        del request.session['businesses']
    return render(request, 'CityDetail.html', context)

def search(request, city_id):
    city = City.objects.get(id=city_id)
    value= request.POST['value']
    url='https://api.yelp.com/v3/businesses/search'
    Params = {'term':value,'location': city.name}
    req=requests.get(url, params=Params, headers=headers)
    parsed = json.loads(req.text)
    businesses = parsed["businesses"]
    request.session['businesses'] = businesses
    return redirect(f'/citydetail/{city.id}')

def faveIt(request, city_id, business_name):
    user = User.objects.get(id=request.session['user_id'])
    city = City.objects.get(id=city_id)
    new_Fave = Likes.objects.create(name=business_name, city=city, user=user)
    return redirect(f'/citydetail/{city.id}')

# Logout user and return to login page #
def logout(request):
    request.session.flush()
    return redirect('/')