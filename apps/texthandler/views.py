from django.http import HttpResponse
from django.shortcuts import render
from apps.texthandler.models import Audio, TextBlock
import uuid, json
from apps.texthandler.tone_analysis import *

def analyze_audio(request, audio_uuid):

    audio = Audio.objects.filter(uuid=uuid.UUID(audio_uuid))[0]
    text_blocks = TextBlock.objects.filter(audio=audio)

    conversation = [None] * len(text_blocks)

    for text_block in text_blocks:
        d = {}
        d['content'] = text_block.content
        d['speaker'] = 'unidentified'
        if text_block.user is not None:
            d['speaker'] = text_block.user.name
        d['insight']  = get_tone(d['content'])
        conversation[text_block.sequence_number - 1] = d


    return HttpResponse(json.dumps(conversation), content_type="application/json")