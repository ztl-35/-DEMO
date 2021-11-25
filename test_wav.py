import wave
from pyaudio import PyAudio, paInt16
from voice import main

framerate = 8000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
TIME = 2
# test git command-ruxian-new

def save_wave_file(filename, data):
    '''save the date to the wavfile'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1,
                     rate=framerate, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    my_buf = []
    count = 0
    while count < TIME * 15:  # 控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count += 1
        print('.')
    save_wave_file('record_voice.wav', my_buf)
    stream.close()


chunk = 2014

def play():
    wf = wave.open(r"record_voice.wav", 'rb')
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=
    wf.getnchannels(), rate=wf.getframerate(), output=True)
    while True:
        data = wf.readframes(chunk)
        if data == "":
            break
        stream.write(data)
    stream.close()
    p.terminate()

def voice_record():
    my_record()
    print('Over!')
    record_result = main.voice_main()
    return record_result
