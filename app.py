from flask import Flask, request, jsonify, render_template
import os
import re
import speech_recognition as sr
from openai import OpenAI
from text_generation import Bot
from audio_generation import generate_audio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    user_input = data.get('user_input', '')
    response = friend_bot.chat(user_input)
    match = re.search(r'^TONE:\s*(\w+)', response, re.MULTILINE)
    tone = match.group(1)
    clear_response = response[:match.start()].strip()

    ai_text = f'Clara: {clear_response}'

    generate_audio(clear_response)

    return jsonify({
        'background': f'static/{tone}.jpeg',
        'audio': 'static/output.wav',
        'ai_text': ai_text
    })


@app.route('/listen', methods=['GET'])
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for voice input...")
        try:
            audio = recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            return jsonify({"transcript": ""})
    try:
        text = recognizer.recognize_google(audio, language="en-EN")
    except sr.UnknownValueError:
        text = ""
    except sr.RequestError as e:
        print("Error: {0}".format(e))
        text = ""
    return jsonify({"transcript": text})


if __name__ == '__main__':
    client = OpenAI(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv('API_KEY'),
    )
    friend_bot = Bot(client)
    app.run(debug=True)