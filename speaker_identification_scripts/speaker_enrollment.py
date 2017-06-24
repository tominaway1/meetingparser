import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'multipart/form-data',
    'Ocp-Apim-Subscription-Key': 'dc67fc9d2c4241ab90d804ee9f8b7276',
}

params = urllib.parse.urlencode({
    # Request parameters
    'shortAudio': 'true',
})

with open('/Users/shuyangsun/Desktop/shuyang_enrollment_audio.wav', 'rb') as audio_file:
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