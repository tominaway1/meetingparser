from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import Record, VoiceResponse
from apps.texthandler.models import Audio
import uuid

number = '+14752060691'

@csrf_exempt
def handle(request):
    if request.method == "POST" and 'RecordingUrl' in request.POST:
        url = request.POST['RecordingUrl']
        to = request.POST['To']
        print(url)
        print(to)
        create_audio(url)
        return HttpResponse(url)

    response = VoiceResponse()
    response.say("Yo, say some shit man")
    response.record(timeout=30, transcribe=True)

    return HttpResponse(response)


# @csrf_exempt
# def handle_recording(request):
#     if request.method == "POST":
#         url = request.POST['RecordingUrl']
#         print(url)

import http.client
from urllib.parse import urlparse

def create_audio(url):
    o = urlparse(url)
    domain = o.hostname
    path = o.path
    conn = http.client.HTTPSConnection(domain)

    headers = {

    }

    conn.request("GET", path, headers=headers)

    res = conn.getresponse()
    data = res.read()
    audio = Audio(uuid=uuid.uuid4())
    filename = "{}{}".format(str(audio.uuid),".wav")
    path = './apps/audiohandler/audio_files/{}'.format(filename)
    f = open(path, 'wb')
    f.write(data)

    audio.filename = filename
    audio.save()

