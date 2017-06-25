from django.http import HttpResponse
from django.shortcuts import render
import os.path
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json, uuid
from . import parse_audio, speaker
from apps.texthandler.models import *
from apps.texthandler.wrapper import *

headers = {
    # Request headers
    'Content-Type': 'multipart/form-data',
    'Ocp-Apim-Subscription-Key': 'dc67fc9d2c4241ab90d804ee9f8b7276',
}

headers1 = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'dc67fc9d2c4241ab90d804ee9f8b7276',
}


params = urllib.parse.urlencode({
    # Request parameters
    'shortAudio': 'true',
})

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

def index(request):
    return HttpResponse("App is running")

def identify(request):
    filename = '{}/{}/{}'.format(SITE_ROOT, 'audio_files','shuyang_enrollment_audio.wav')
    print(filename)
    with open(filename, 'rb') as audio_file:
        try:
            bin_data = audio_file.read()
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/spid/v1.0/identificationProfiles/289d7b68-f72f-4478-979d-e1245422c958/enroll?%s" % params, body=bin_data, headers=headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return HttpResponse("[Errno {0}] {1}".format(e.errno, e.strerror))
    return HttpResponse(data)

def get_all_profile(request):
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("GET", "/spid/v1.0/identificationProfiles?%s" % params, body='', headers=headers1)
        response = conn.getresponse()

        # Get profile information received from the get all profiles portion of api
        data = response.read()
        j = json.loads(data)
        for i in j:
            print (i["identificationProfileId"])

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        HttpResponse("[Errno {0}] {1}")

    return HttpResponse(data, content_type="application/json")

def split_audio_file(request, audio_uuid):
    parse_audio.split_file(audio_uuid, '{}/{}/'.format(SITE_ROOT, 'audio_files'))
    return HttpResponse("Success")

def identify_audio_file(request, audio_uuid):
    audio = Audio.objects.filter(uuid=uuid.UUID(audio_uuid))[0]
    profiles = speaker.get_all_profiles()
    print(profiles)
    text_blocks = TextBlock.objects.filter(audio=audio)

    for text_block in text_blocks:
        filename = text_block.filename
        filepath = '{}/{}/{}'.format(SITE_ROOT, 'audio_files', filename)
        print(filepath)
        result = speaker.identify(profiles, filepath)
        identifer = result['identifiedProfileId']
        users = UserProfile.objects.filter(identification_profile_id=identifer)
        if users is not None and len(users) > 0:
            text_block.user = users[0]
            text_block.save()

    return HttpResponse("Success")

def translate_audio_file(request, audio_uuid):
    audio = Audio.objects.filter(uuid=uuid.UUID(audio_uuid))[0]
    text_blocks = TextBlock.objects.filter(audio=audio)
    ms_asr = Microsoft_ASR()
    ms_asr.get_speech_token()

    for text_block in text_blocks:
        filename = text_block.filename
        filepath = '{}/{}/{}'.format(SITE_ROOT, 'audio_files', filename)
        print(filepath)
        text, confidence = ms_asr.transcribe(filepath)
        print("text:" + text)
        text_block.content = text
        text_block.save()

    return HttpResponse("Success")
