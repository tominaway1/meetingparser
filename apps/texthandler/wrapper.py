#Taken from https://gist.github.com/jellis505/973ea6de12508c7c720da4a074e7d065
import requests
# import httplib
import http
import uuid
import json
class Microsoft_ASR():
    def __init__(self):
        self.sub_key = 'f228789318114be78c8725dcc9086f60'
        self.token = None
        pass

    def get_speech_token(self):
        FetchTokenURI = "/sts/v1.0/issueToken"
        header = {'Ocp-Apim-Subscription-Key': self.sub_key}
        # conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        body = ""
        conn.request("POST", FetchTokenURI, body, header)
        response = conn.getresponse()
        str_data = response.read()
        conn.close()
        self.token = str_data.decode("utf-8") 
        #print "Got Token: ", self.token
        return True

    def transcribe(self,speech_file):

        # Grab the token if we need it
        if self.token is None:
            #print "No Token... Getting one"
            self.get_speech_token()

        endpoint = 'https://speech.platform.bing.com/recognize'
        request_id = uuid.uuid4()
        # Params form Microsoft Example 
        params = {'scenarios': 'ulm',
                  'appid': '06ad66c0-2b0f-4a03-9054-242cf9e520af',
                  'locale': 'en-US',
                  'version': '3.0',
                  'format': 'json',
                  'instanceid': '565D69FF-E928-4B7E-87DA-9A750B96D9E3',
                  'requestid': uuid.uuid4(),
                  'device.os': 'linux'}
        content_type = "audio/wav; codec=""audio/pcm""; samplerate=16000"

        def stream_audio_file(speech_file, chunk_size=1024):
            with open(speech_file, 'rb') as f:
                while 1:
                    data = f.read(1024)
                    if not data:
                        break
                    yield data

        headers = {'Authorization': 'Bearer ' + self.token, 
                   'Content-Type': content_type}
        resp = requests.post(endpoint, 
                            params=params, 
                            data=stream_audio_file(speech_file), 
                            headers=headers)
        val = json.loads(resp.text)
        if "results" not in val:
            return "", 100
        return val["results"][0]["name"], val["results"][0]["confidence"]

if __name__ == "__main__":
    ms_asr = Microsoft_ASR()
    ms_asr.get_speech_token()
    text, confidence = ms_asr.transcribe('weird_conversation.wav')
    print ("Text: ", text)
