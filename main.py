from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
import math
import pyttsx3
from pydub import AudioSegment
import os

app = Flask(__name__)
DATE_FORMAT = '%Y%m%d_%H%M%S'

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        affirmations = request.form['affirmations']
        return redirect(url_for("create_audio", affirmations=affirmations))

def clean_up(affrs_file, audio_file):
    os.remove(affrs_file)
    os.remove(audio_file)

@app.route('/create_audio?affirmations=<affirmations>')
def create_audio(affirmations):
    audio_length = 120 * 15
    file_name = None
    text = affirmations
    overlay_type = None
    # best is 10
    overlay_volume = 15
    # default rate is 200
    # best is 300
    rate = 250
    speaker = None

    affrs_file = create_affirmations_file(text, rate, speaker)
    audio_file = mix_audios(affrs_file, audio_length, file_name, overlay_type, overlay_volume)

    return send_file(audio_file, as_attachment=True)
    # clean_up(affrs_file, audio_file)

def create_affirmations_file(text, rate, speaker):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[speaker_type(speaker)].id)

    engine.setProperty('rate', rate)
    # engine.setProperty('volume',1.0)

    file_name = f'affirmations_{datetime.now().strftime(DATE_FORMAT)}.mp3'

    engine.save_to_file(text, file_name)
    engine.runAndWait()
    engine.stop()

    return file_name

def mix_audios(affrs_file, audio_length, filename, overlay_type, overlay_volume):
    affirmations = AudioSegment.from_file(affrs_file)
    overlay = AudioSegment.from_file(overlay_file(overlay_type))

    multiplier = math.ceil(audio_length / overlay.duration_seconds)

    overlay = overlay * multiplier
    overlay = overlay[:(audio_length * 1000)]

    affirmations = affirmations - overlay_volume

    combined = overlay.overlay(affirmations, gain_during_overlay=overlay_volume, loop=True)

    file_name = f'{filename}.mp3' if filename else f'subliminal_{datetime.now().strftime(DATE_FORMAT)}.mp3'

    combined.export(file_name, format='mp3')

    return file_name

def overlay_file(overlay):
    # both of these sounds are royalty free
    return 'sounds/fireplace.mp3' if overlay == 'fire' else 'sounds/rain.mp3'

def speaker_type(speaker):
    # <Voice id=com.apple.speech.synthesis.voice.Alex
    #     name=Alex
    #     languages=['en_US']
    #     gender=VoiceGenderMale
    #     age=35>
    #
    # <Voice id=com.apple.speech.synthesis.voice.Victoria
    #     name=Victoria
    #     languages=['en_US']
    #     gender=VoiceGenderFemale
    #     age=35>
    #
    return 0 if speaker == 'male' else 41

if __name__ == "__main__":
    # if you don't want to use flask, uncomment me & comment `app.run()`
    # affirmations = ''
    # create_audio(affirmations)

    app.run()
