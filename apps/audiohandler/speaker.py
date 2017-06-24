import http.client, urllib.request, urllib.parse, urllib.error, base64, json

__subscription_key = 'dc67fc9d2c4241ab90d804ee9f8b7276'

__headers = {
    'Ocp-Apim-Subscription-Key': __subscription_key,
}

__params = urllib.parse.urlencode({
    
})

__headers_with_audio = {
    'Ocp-Apim-Subscription-Key': __subscription_key,
    'Content-Type': 'multipart/form-data'
}

__params_with_audio = urllib.parse.urlencode({
    'shortAudio': 'true'
})

__connection_url = 'westus.api.cognitive.microsoft.com'

key_status = 'status'
key_processing_result = 'processingResult'
key_confidence = 'confidence'
key_identified_profile_id = 'identifiedProfileId'

class SpeakerProfile:
    def __init__(self, profile):
        self.json_data = profile
        self.identification = profile['identificationProfileId']
        self.locale = profile['locale']
        self.enrollment_speech_duration = profile['enrollmentSpeechTime']
        self.remaining_enrollment_speech_duration = profile['remainingEnrollmentSpeechTime']
        self.date_created = profile['createdDateTime']
        self.date_last_activation = profile['lastActionDateTime']
        self.enrollment_status = profile['enrollmentStatus']
    
    def __repr__(self):
        return '{0}: enrolled={1}'.format(self.identification, self.is_enrolled())
        
    def is_enrolled(self):
        return self.enrollment_status == 'Enrolled'

    
def get_profile_id(profile):
    profile_id = None
    if isinstance(profile, SpeakerProfile):
        profile_id = profile.identification
    elif isinstance(profile, str):
        profile_id = profile
    else:
        print('Invalid argument {0}.'.format(profile))
    return profile_id

def get_profile_ids(profiles):
    return [get_profile_id(profile) for profile in profiles]

def create_profile():
    """ 
    This will create a user profile within Microsoft Azure with default
    locale as en-us and return the new user id as a string
    """
    print('Creating profile...')
    body= '{"locale":"en-us"}'
    try:
        conn = http.client.HTTPSConnection(__connection_url)
        conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % __params, body=body, headers=__headers)
        response = conn.getresponse()
        data = response.read()
        profile = json.loads(data)
        identification = profile['identificationProfileId']
        conn.close()
        profile = get_profile(identification)
        print('Finished creating profile [{0}].'.format(identification))
        return profile
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return identification


def delete_profile(profile):
    profile_id = get_profile_id(profile)
    print('Deleting profile [{0}]...'.format(profile_id))
    try:
        conn = http.client.HTTPSConnection(__connection_url)
        conn.request("DELETE", "/spid/v1.0/identificationProfiles/{0}?{1}".format(profile_id, __params), body=None, headers=__headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
        print('Finished deleting profile [{0}].'.format(profile_id))
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_profile(profile):
    profile_id = get_profile_id(profile)
    print('Getting profile [{0}]...'.format(profile_id))
    try:
        conn = http.client.HTTPSConnection(__connection_url)
        conn.request("GET", "/spid/v1.0/identificationProfiles/{0}?{1}".format(profile_id, __params), body=None, headers=__headers)
        response = conn.getresponse()
        data = response.read()
        dictionary = json.loads(data)
        conn.close()
        print('Finished getting profile [{0}]...'.format(profile_id))
        return SpeakerProfile(dictionary)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_all_profiles():
    print('Getting all profiles...')
    try:
        conn = http.client.HTTPSConnection(__connection_url)
        conn.request("GET", "/spid/v1.0/identificationProfiles?%s" % __params, body=None, headers=__headers)
        response = conn.getresponse()

        # Get profile information received from the get all profiles portion of api
        data = response.read()
        result = json.loads(data)
        conn.close()
        print('Finished getting all profiles.')
        return [SpeakerProfile(profile) for profile in result]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def enroll(profile, audio_file_path):
    profile_id = get_profile_id(profile)
    print('Enrolling for profile [{0}]...'.format(profile_id))
    with open(audio_file_path, 'rb') as audio_file:
        try:
            bin_data = audio_file.read()
            conn = http.client.HTTPSConnection(__connection_url)
            conn.request("POST", "/spid/v1.0/identificationProfiles/{0}/enroll?{1}".format(profile_id, __params_with_audio), body=bin_data, headers=__headers_with_audio)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
            print('Finished enrollment for profile [{0}].'.format(profile_id))
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
    

def op_location_to_identify(profiles, audio_file_path):
    print('Identifying audio file...')
    profile_ids = get_profile_ids(profiles)
    with open(audio_file_path, 'rb') as audio_file:
        try:
            bin_data = audio_file.read()
            conn = http.client.HTTPSConnection(__connection_url)
            ids_str = ','.join(profile_ids)
            conn.request("POST", "/spid/v1.0/identify?identificationProfileIds={0}&{1}".format(ids_str, __params_with_audio), body=bin_data, headers=__headers_with_audio)
            response = conn.getresponse()
            header = response.getheader('Operation-Location')
            if header is not None:
                op_location = header.rsplit('/', 1)[-1]
                conn.close()
                print('Retrived operation location {0}.'.format(op_location))
                return op_location
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_operation_status(operation_id):
    try:
        conn = http.client.HTTPSConnection(__connection_url)
        conn.request("GET", "/spid/v1.0/operations/{0}?{1}".format(operation_id, __params), body=None, headers=__headers)
        response = conn.getresponse()
        data = response.read()
        dictionary = json.loads(data)
        conn.close()
        key_processing_result = 'processingResult'
        if not key_status in dictionary:
            return None
        if key_processing_result in dictionary:
            return {
                key_status: dictionary[key_status],
                key_identified_profile_id: dictionary[key_processing_result][key_identified_profile_id],
                key_confidence: dictionary[key_processing_result][key_confidence]
            }
        else:
            return {
                key_status: dictionary[key_status]
            }
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def is_result_status_succeeded(result):
    return (result is not None) and (result['status'] == 'succeeded')
    
def identify(profiles, audio_file_path):
    op_id = op_location_to_identify(profiles, audio_file_path)
    result = get_operation_status(op_id)
    while not is_result_status_succeeded(result):
        result = get_operation_status(op_id)
    print(result)
    return result

if __name__=='__main__':
    profiles = get_all_profiles()
    for ele in profiles:
        print()
        print(ele)

    print()
    
    file_path_start = '/Users/shuyangsun/Developer/hackathon_projects/meetingparser/apps/audiohandler/audio_files/'
    
    for name in ('shuayng', 'sean', 'shan'):
        print('Identifying {0}...'.format(name))
        identify(profiles, file_path_start + '{0}_enrollment.wav'.format(name))
        identify(profiles, file_path_start + 'arts_{0}.wav'.format(name))
        print()

