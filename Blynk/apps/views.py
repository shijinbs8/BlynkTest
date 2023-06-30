import time

import requests
from django.shortcuts import render, get_object_or_404
from .models import Classroom, Bulb

Userver = "blr1.blynk.cloud"  # Replace with your actual server

def index(request):
    classrooms = Classroom.objects.all()
    return render(request, 'index.html', {'classrooms': classrooms})

def bulb_control(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    bulbs = Bulb.objects.filter(classroom=classroom)

    return render(request, 'bulb_control.html', {'classroom': classroom, 'bulbs': bulbs})

def update_pin(request, classroom_id, bulb_id):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        status = request.POST.get('status')

        # Update the bulb status
        bulb = get_object_or_404(Bulb, id=bulb_id)
        bulb.status = 1 if status.lower() == 'on' else 0
        bulb.save()

        # Send API request to update the physical bulb
        classroom = get_object_or_404(Classroom, id=classroom_id)
        token = classroom.token  # Access the token from the Classroom model
        url = f"https://{Userver}/external/api/update?token={token}&{pin}={bulb.status}"
        requests.get(url)
        print(url)
    classroom = get_object_or_404(Classroom, id=classroom_id)
    bulbs = Bulb.objects.filter(classroom=classroom)
    while True:
        for bulb in bulbs:
            url = f"https://{Userver}/external/api/get?token={classroom.token}&pin={bulb.pin}"
            response = requests.get(url)
            status = response.text
            # Process the status or perform any necessary actions
            print(f"Bulb {bulb.id} status: {status}")

        time.sleep(5)
    return render(request, 'bulb_control.html', {'classroom': classroom, 'bulbs': bulbs})
