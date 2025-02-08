import json
import time
import wave

from vosk import KaldiRecognizer, Model


def convert_audio_to_text(audio_file):
    try:
        # Load model
        model = Model("vosk-model-small-en-us-0.15")

        # Đọc file âm thanh
        wf = wave.open(audio_file, "rb")
        if wf.getnchannels() != 1:
            return "File âm thanh phải là mono"

        recognizer = KaldiRecognizer(model, wf.getframerate())
        text = ""

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text += result.get("text", "") + " "

        return text.strip()
    except FileNotFoundError:
        return f"Không tìm thấy tệp âm thanh: {audio_file}"
    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"
