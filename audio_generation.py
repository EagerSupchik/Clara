import requests
from config import TTS_IP_HOST, TTS_PORT, TTS_REF_AUDIO_PATH, TTS_PROMPT_TEXT

url = f'http://{TTS_IP_HOST}:{TTS_PORT}/tts'

def generate_audio(text):
    params = {
        'text': text,
        'text_lang': 'en',
        'ref_audio_path': TTS_REF_AUDIO_PATH,
        'prompt_lang': 'en',
        'prompt_text': TTS_PROMPT_TEXT,
        'text_split_method': 'cut0',
        'batch_size': 1,
        'media_type': 'wav',
        'streaming_mode': False,
        'top_k': 5,
        'top_p': 1.0,
        'temperature': 1.0,
        'batch_size': 1,
        'batch_threshold': 0.75,
        'split_bucket': True,
        'speed_factor': 1.0,
        'fragment_interval': 0.3,
        'seed': 2855904637,
        'return_fragment': True,
        'parallel_infer': False,
        'repetition_penalty': 1.35,
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            with open('static/output.wav', 'wb') as f:
                f.write(response.content)
            print('Audio saved to static/output.wav')
        else:
            print(f'Error: {response.status_code}')
            print(response.json())
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')