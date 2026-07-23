import sys
import time
import json
import queue
import serial
import textwrap
import sounddevice as sd

from vosk import Model, KaldiRecognizer

#vosk parameters
sample_rate = 16000
channel = 1
vosk_model = "vosk-model-small-en-us-0.15"

model = Model(vosk_model)
recognizer = KaldiRecognizer(model, sample_rate)
print("Vosk has successfully loaded!")

q = queue.Queue()

#arduino nano is connected to COM5, but this may differ on different operating systems
arduino = serial.Serial(port="COM5", baudrate=115200, timeout=0.1)
arduino.reset_output_buffer()

time.sleep(2)
print("Arduino is successfully connected!")

def callback_func(indata, frames, time, status):
    """This function is called for each audio block"""

    if status:
        print(status, file=sys.stderr)

    #places audio block into the queue
    q.put(bytes(indata))

#the entire sentence history will be stored below
final_sentence = ""

def process_stream(final_text, partial_text, char_per_line, num_lines):
    """
    Encodes the stream (both partial and the final sentence) into a custom Serial communication system
    < - denotes the start of the character stream
    > - denotes the end of the character stream
    """
    current_text = final_text + " " + partial_text

    #use 20 characters per line, since a defult character is 8x5
    wrapped = textwrap.wrap(current_text, char_per_line)
    #get the last num_lines (here, it's 4 lines)
    formatted = "<" + "\n".join(wrapped[-1 * num_lines:]) + ">"
    arduino.write(formatted.encode('utf-8'))

#open live audio stream
try:
    with sd.InputStream(samplerate=sample_rate, blocksize=8000, channels=channel, dtype="int16", callback=callback_func):
        print("Reading input stream...")

        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                final_json = json.loads(recognizer.FinalResult())
                if final_json:
                    final_text = final_json.get("text", "")
                    final_sentence += final_text + ""
                    process_stream(final_sentence, "", char_per_line=20, num_lines=4)
            else:
                partial_json = json.loads(recognizer.PartialResult())
                if partial_json:
                    partial_text = partial_json.get("partial", "")
                    process_stream(final_sentence, partial_text, char_per_line=20, num_lines=4)

except KeyboardInterrupt:
    print("\nDone!")
    arduino.close()
    print("Arduino port closed.")
    sys.exit(0)
except Exception as e:
   arduino.close()
   print("Arduino port closed.")
   print(type(e).__name__ + ": " + str(e))
   sys.exit(1)