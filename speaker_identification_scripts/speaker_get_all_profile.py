import http.client, urllib.request, urllib.parse, urllib.error, base64, json

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'dc67fc9d2c4241ab90d804ee9f8b7276',
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("GET", "/spid/v1.0/identificationProfiles?%s" % params, body='', headers=headers)
    response = conn.getresponse()

    # Get profile information received from the get all profiles portion of api
    data = response.read()
    j= json.loads(data)
    for i in j:
        print (i["identificationProfileId"])

    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

