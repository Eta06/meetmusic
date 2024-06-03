import pyaudio
import wave
import sounddevice as sd


def list_virtual_audio_devices():
    print("Available virtual audio devices:")
    for i, device in enumerate(sd.query_devices()):
        # Check if the device is a virtual output device
        if device['max_output_channels'] > 0 and "virtual" in device['name'].lower():
            print(f"{i}: {device['name']}")

def stream_audio_to_device(file_path, device_index):
    # Open the audio file
    wf = wave.open(file_path, 'rb')

    # Instantiate PyAudio
    p = pyaudio.PyAudio()

    # Open a stream with the correct settings for the audio file
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=device_index)

    # Read data in chunks and stream to the virtual device
    chunk = 1024
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()


"""
if __name__ == "__main__":
    # List virtual audio devices and allow user to select one
    list_virtual_audio_devices()
    device_index = int(input("Select the device index to stream audio to: "))

    # Stream audio to the selected device
    audio_file = 'music.wav'
    stream_audio_to_device(audio_file, device_index)
"""