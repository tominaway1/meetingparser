import http.client, urllib,json

def get_tone(text):
    """ Returns dictionary for tones for each section
    emotion
        anger
        disgust
        fear
        joy
        sadness

    language   
        analytical
        confidence
        tentative

    social
        openness
        conscientiousness
        extraversion    
        agreeableness   
        emotional range or neuroticism  
    """
    conn = http.client.HTTPSConnection("gateway.watsonplatform.net")

    headers = {
        'authorization':'Basic Y2JiNGJjOTQtZGJjOC00NzBlLWJhNTktODQ5MDQ4MjAyMTQ0OjdTMUhKUmRqbjZydg==',
    }
    #convert given string into a parsible search query
    text=urllib.parse.quote(text)
    url="/tone-analyzer/api/v3/tone?text="+text+"&sentences=true&version=2016-05-19"

    conn.request("GET",url,headers=headers )

    res = conn.getresponse()
    data = res.read()
    data=json.loads(data)
    d=data['document_tone']
    
    tone_categories=d['tone_categories']
    #print(tone_categories)
    # for a in tone_categories[0]['tones']:
    #     print(a)
    count=1
    dic={}
    for a in tone_categories:
        if count==1:
            dic['emotion']=a['tones']
        elif count==2:
            dic['language']=a['tones']
        elif count==3:
            dic['social']=a['tones']
        count=count+1
    # print(dic['emotion'])
    # print(dic['language'])
    # print(dic['social'])
    #print_score(dic)

    return dic
def print_score(dic):
    print("emotion: ")
    for a in dic['emotion']:
        print('\t Tone: '+a['tone_id'] +'| Score: '+str(a['score']))
    print("Language: ")
    for a in dic['language']:
        print('\t Tone: '+a['tone_id'] +'| Score: '+str(a['score']))
    print("Social: ")
    for a in dic['social']:
        print('\t Tone: '+a['tone_id'] +'| Score: '+str(a['score']))
    

if __name__=='__main__':
    get_tone("I am very angry")
