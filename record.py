import pyaudio
import audioop
import math
from twilio.rest import Client
import sys

def start_recording():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 3
    chunk = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=chunk)
    recording = True
    audio_spike_count = 0
    baseVolume = 0
    trigger_count = 0

    # Sets base volume in room (useful if you have white noise playing)
    print("Setting room volume...")
    for i in range(0, 44100 // chunk * RECORD_SECONDS):
        data = stream.read(chunk)
        rms = audioop.rms(data, 2)
        baseVolume = (20 * math.log10(rms)) if rms > 0 else 60

    # Begins infinite loop for recording
    print("Current Room Volume: ", baseVolume)
    print("Now listening for your baby...")
    print("Make about 5 to 10 loud noises and it should trigger a message")
    while recording:
        data = stream.read(chunk)
        rms = audioop.rms(data, 2)
        decibels = (20 * math.log10(rms)) if rms > 0 else 60


        # Uncomment this to see the steady stream of decibel logs
        # print(f'decibel level: {decibels}')


        # If current decibel level is 15 above the baseVolume, add 1 to the spike count. Every 40 spikes adds one to the trigger_count.
        # The message displayed changes based on how many trigger_counts there are
        if rms > 0 and decibels > baseVolume + 15:
            audio_spike_count += 1
            trigger_count = audio_spike_count // 40
        
        if audio_spike_count % 40 == 0:
            # I'll most likely split up the messages to be time based rather than just by total audio spikes.
            # Probably a combination of both though, if the audio spike count is high and 5 minutes has passed,
            # send an alert. If after 10/20 minutes and there are lots more spikes then send a final reminder.
            # The user will also have an option to set a timer for when the first alert should be sent. So basically
            # the loop that starts the recording won't be executed for 'x' amount of time set by the user.
            message = 'Final reminder that your baby may be awake' if trigger_count == 10 \
                else 'Reminder that your baby may be awake' if trigger_count == 5 \
                else 'It sounds like your baby is awake!' if trigger_count == 1 \
                else ''
            message and print(message)
            # This next line would send the text message. API keys need to be updated though
            # message and send_message(message)
            if trigger_count > 10:
                break

    stream.stop_stream()
    stream.close()
    p.terminate()


def send_message(message):
    client = Client("AC2ba79eb039e423ebccf9d81d4aebe90a", "bd5c1fa15dfa36df8122e319c2cf99b3")
    client.messages.create(to="+14066335122", from_="+12513062189", body=message)


texts_sent = 0
start_recording()
# start = input('Type "1" and press "ENTER" to set the room volume')
# if start:
#     start_recording()
