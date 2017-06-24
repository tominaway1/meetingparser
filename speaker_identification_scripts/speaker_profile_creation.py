import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'dc67fc9d2c4241ab90d804ee9f8b7276'
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
#  conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % params, '{body}', headers)
    conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % params, body='{"locale": "en-us"}', headers=headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))