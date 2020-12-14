from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from farmify.mongoClient import MongoClient
from django.contrib import messages
import requests

client = MongoClient().getConnection()

def landing_view(request):
    return render(request,'farmify/index.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        res = client.Farmify.contacts.insert({"name":name,"email":email,"subject":subject,"message":message})
        if len(str(res))==24:
            messages.success(request,'Request Sent')
            return redirect('/')
    return render(request,'farmify/contact.html')


@login_required(login_url='/auth/login')
def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        context = {"q":search}
        if request.user.role == 'farmer':
            res = list(client.Farmify.farmers_crops.find({"cropname":search.capitalize()}))
            for r in res:
                r['id'] = r['_id']
        else:
            res = list(client.Farmify.dealers_deals.find({"cropname":search.capitalize()}))
            for r in res:
                r['id'] = r['_id']
        context['data'] = res

        return render(request,'farmify/search.html',context=context)
    else:
        return redirect('/')

def weather(request):

    res = requests.get('https://samples.openweathermap.org/agro/1.0/weather?polyid=5aaa8052cbbbb5000b73ff66&appid=b1b15e88fa797225412429c1c50c122a1')
    data = res.json()
    context = {}

    context['weather'] = data['weather'][0]['description']
    context['temp'] = data['main']['temp']
    context['pressure'] = data['main']['pressure']
    context['humidity'] = data['main']['humidity']
    context['temp_min'] = data['main']['temp_min']
    context['temp_max'] = data['main']['temp_max']
    context['sea_level'] = data['main']['sea_level']
    context['grnd_level'] = data['main']['grnd_level']
    context['wind_speed'] = data['wind']['speed']
    context['wind_deg'] = data['wind']['deg']

    return render(request,'farmify/weather.html',context=context)
        
        
    