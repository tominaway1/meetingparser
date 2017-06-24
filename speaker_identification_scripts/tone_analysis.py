import http.client, urllib,json

def get_tone(text):
    conn = http.client.HTTPSConnection("gateway.watsonplatform.net")

    headers = {
        'authorization':'Basic Y2JiNGJjOTQtZGJjOC00NzBlLWJhNTktODQ5MDQ4MjAyMTQ0OjdTMUhKUmRqbjZydg==',
    }
    #convert given string into a parsible search query
    text=urllib.parse.quote(text)
    url="/tone-analyzer/api/v3/tone?text="+text+"&tones=emotion&sentences=true&version=2016-05-19"
    
    conn.request("GET",url,headers=headers )

    res = conn.getresponse()
    data = res.read()
    data=json.loads(data)
    d=data['document_tone']
    tone_categories=d['tone_categories']

    # for a in tone_categories[0]['tones']:
    #     print(a)
    return tone_categories[0]['tones']
    
if __name__=='__main__':
    get_tone("I am very angry")
