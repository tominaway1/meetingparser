import http.client, urllib.request, urllib.parse, urllib.error, base64, json
def create_profile():
    """ 
        This will create a user profile within Microsoft Azure with default
        Locale as en-us and return the new user id as a string
    """
    key = "dc67fc9d2c4241ab90d804ee9f8b7276"

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key,
    }

    params = urllib.parse.urlencode({
    })
    body= '{"locale":"en-us"}'
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        j= json.loads(data)
        identification = j['identificationProfileId']

        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return identification

if __name__=="__main__":
    profile=create_profile()
    print profile
