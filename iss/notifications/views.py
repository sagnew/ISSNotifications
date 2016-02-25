from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'notifications/index.html')


def subscribe(request):
    return HttpResponse("Thanks for subscribing")
