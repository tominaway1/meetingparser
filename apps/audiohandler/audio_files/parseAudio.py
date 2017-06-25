import math
import wave
import struct

ifile = wave.open("shuyang_enrollment.wav")


FRAME_SIZE = 100000

def split_file(filename):
    filename = filename.split(".")[0]
    ifile = wave.open(filename + ".wav")

    sampwidth = ifile.getsampwidth()
    fmts = (None, "=B", "=h", None, "=l")
    fmt = fmts[sampwidth]

    dcs = (None, 128, 0, None, 0)
    dc = dcs[sampwidth]

    j = 1

    ofile = wave.open("{}_{}.wav".format(filename, j), "w")
    ofile.setparams(ifile.getparams())
    for i in range(ifile.getnframes()):
        if math.floor(i / j) == FRAME_SIZE:
            j += 1
            ofile.close()
            ofile = wave.open("{}_{}.wav".format(filename, j), "w")
            ofile.setparams(ifile.getparams())

        iframe = ifile.readframes(1)
        iframe = struct.unpack(fmt, iframe)[0]
        iframe -= dc

        oframe = iframe / 2;
        oframe += dc
        oframe = struct.pack(fmt, math.ceil(oframe))

        ofile.writeframes(oframe)

    ifile.close()
    ofile.close()

split_file("weird_conversation.wav")