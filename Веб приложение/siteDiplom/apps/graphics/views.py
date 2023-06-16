import json
import os

from django.core import serializers
from django.shortcuts import render
from .models import Indicator
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib import pyplot as plt


def index(request):
    try:
        p = float(request.GET.get('p'))
        t = float(request.GET.get('t'))
        h = float(request.GET.get('h'))
        a = Indicator(pression=p, temperature=t, humidity=h)
        a.save()
        return HttpResponse("Успешно")
    except:
        return HttpResponse("Некорректные параметры")
    return render(request, 'graphics/base.html')


# Create your views here.
def show(request):
    def draw(t, p, h):
        X1 = range(len(t))
        Y1 = t
        X2 = range(len(p))
        Y2 = p
        X3 = range(len(h))
        Y3 = h
        plt.subplots_adjust(plt.subplots_adjust(wspace=1, hspace=0.3))
        ax1.plot(X1, Y1)
        ax1.set_title('График температуры')
        ax3.plot(X3, Y3)
        ax3.set_title('График влажности')
        plt.savefig(os.path.join(os.path.dirname(__file__) + '\media', 'graphics.png'))
        ax1.cla()
        ax3.cla()

    temperature = []
    pression = []
    humidity = []
    fig, (ax1, ax3) = plt.subplots(2, 1)
    try:
        print(request.GET.get('time'))
    except:
        pass
    if request.GET.get('time') == '1440':
        data = Indicator.objects.all().order_by('-id')[:1440]
        for el in data:
            temperature.insert(0, el.temperature)
            pression.insert(0, el.pression)
            humidity.insert(0, el.humidity)
        draw(temperature, pression, humidity)
    elif request.GET.get('time') == '10080':
        data = Indicator.objects.all().order_by('-id')[:10080]
        for el in data:
            temperature.insert(0, el.temperature)
            pression.insert(0, el.pression)
            humidity.insert(0, el.humidity)
        draw(temperature, pression, humidity)
    else:
        data = Indicator.objects.all().order_by('-id')[:60]
        for el in data:
            temperature.insert(0, el.temperature)
            pression.insert(0, el.pression)
            humidity.insert(0, el.humidity)
        draw(temperature, pression, humidity)

    print(os.path.join(os.path.dirname(__file__) + '\media', 'graphics.png'))
    print(os.path.join(os.path.dirname(__file__), '\media\graphics.png'))
    return render(request, 'graphics/list.html')


def main(request):
    data = Indicator.objects.all().order_by('-id')[:1]
    if float(data[0].temperature)>=25.0 or float(data[0].temperature)<=20.0 or float(data[0].humidity)<=55.0:
        danger=True
    else:
        danger=False
    return render(request, 'graphics/main.html', {'data': data[0],'danger': danger})


