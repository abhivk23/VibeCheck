from google.cloud import speech
import requests
from sentiment.py import .

def transcribe_model_selection(speech_file, model):
    """Transcribe the given audio file synchronously with
    the selected model."""
    from google.cloud import speech

    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="en-US",
        model=model,
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        print(u"Transcript: {}".format(alternative.transcript))

print(recording_url)
url = 'https://api.nexmo.com/v1/files/c598ae96-2f87-44ef-a412-f28544737585?api_key=657a6239&api_secret=ENKun12C4T8dsMfn'
r = requests.get(url, allow_redirects=True)

open('e2e393d7-d698-4fac-829d-6677db5c470a.mp3', 'wb').write(r.content)

transcribe_model_selection('e2e393d7-d698-4fac-829d-6677db5c470a.mp3', "phone_call")
