import math
import wave
import struct
import uuid

from apps.texthandler.models import TextBlock, Audio

FRAME_SIZE = 100000

def split_file(audio_uuid, file_dir):
    audio = Audio.objects.filter(uuid=uuid.UUID(audio_uuid))[0]

    filename = audio.filename
    filename = filename.split(".")[0]
    ifile = wave.open(file_dir + filename + ".wav")

    sampwidth = ifile.getsampwidth()
    fmts = (None, "=B", "=h", None, "=l")
    fmt = fmts[sampwidth]

    dcs = (None, 128, 0, None, 0)
    dc = dcs[sampwidth]

    j = 1
    first_file = "{}{}_{}.wav".format(file_dir,filename, j)
    ofile = wave.open(first_file, "w")
    text_block = TextBlock(sequence_number=j, audio=audio, filename=first_file.split('/')[-1])
    text_block.save()

    ofile.setparams(ifile.getparams())
    ofile.setframerate(16000)
    ofile.setsampwidth(2)
    ofile.setnchannels(1)
    for i in range(ifile.getnframes()):
        if math.floor(i / j) == FRAME_SIZE:
            j += 1
            ofile.close()
            new_filename = "{}{}_{}.wav".format(file_dir,filename, j)
            text_block = TextBlock(sequence_number=j, audio=audio, filename=new_filename.split('/')[-1])
            text_block.save()
            ofile = wave.open(new_filename, "w")
            ofile.setparams(ifile.getparams())

        iframe = ifile.readframes(1)
        iframe = struct.unpack(fmt, iframe)[0]
        iframe -= dc

        oframe = iframe / 2
        oframe += dc
        oframe = struct.pack(fmt, math.ceil(oframe))

        ofile.writeframes(oframe)
        ofile.writeframes(oframe)

    ifile.close()
    ofile.close()
