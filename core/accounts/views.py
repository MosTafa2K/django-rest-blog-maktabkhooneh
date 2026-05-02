import time  # noqa
import requests
from django.shortcuts import render  # noqa
from django.http import HttpResponse, JsonResponse
from .tasks import send_email_task


# Create your views here.
def send_email(request):
    send_email_task.delay()
    return HttpResponse("<h1>Email has been sent..please check your inbox</h1>")


def test(request):
    response = requests.get("http://localhost:3000/users")
    return JsonResponse(response.json())