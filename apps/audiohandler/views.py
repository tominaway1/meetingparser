from django.http import HttpResponse
from django.shortcuts import render
import os.path
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

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
        j= json.loads(data)
        for i in j:
            print (i["identificationProfileId"])

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        HttpResponse("[Errno {0}] {1}")

    return HttpResponse(j)