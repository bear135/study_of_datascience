# p339 답입니다.
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from gtts import gTTS
import playsound

from micstream import MicrophoneStream

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
"g-speech-279210-cf6172674082.json" # 독자 여러분이 생성한 파일로!

# Audio recording parameters
RATE =44100
CHUNK =int(RATE /10)  # 100ms

def respond(text):
	if u'안녕'in text:
		playsound.playsound('greet.wav', True)
		playsound.playsound('order.wav', True)
	elif u'아메리카노'in text:
		playsound.playsound('americano.wav', True)
	elif u'카페라떼'in text:
		playsound.playsound('cafelatte.wav', True)
	elif u'에스프레소'in text:
		playsound.playsound('espresso.wav', True)

def listen_print_loop(responses):

    for response in responses:
        result = response.results[0]
        transcript = result.alternatives[0].transcript

        print(transcript)

        if u'종료'in transcript or u'그만'in transcript:
            print('종료합니다..')
            break

        respond(transcript)

language_code ='ko-KR'  # a BCP-47 language tag

client = speech.SpeechClient()
config = types.RecognitionConfig(
	encoding =enums.RecognitionConfig.AudioEncoding.LINEAR16,
	sample_rate_hertz =RATE,
	language_code =language_code)
streaming_config = types.StreamingRecognitionConfig(config =config)

with MicrophoneStream(RATE, CHUNK) as stream:
	audio_generator = stream.generator()
	requests = (types.StreamingRecognizeRequest(audio_content =content)
				for content in audio_generator)
	responses = client.streaming_recognize(streaming_config, requests)

	listen_print_loop(responses)
