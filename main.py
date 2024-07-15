import openai
import sounddevice as sd
import soundfile as sf
import wave
import queue
import threading
import os
import signal
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")


def transcribe_audio(filename):
    """音声ファイルをテキストに変換する関数"""
    try:
        with open(filename, "rb") as audio_file:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def generate_response(prompt):
    """テキストプロンプトに対するGPT-3.5の応答を生成する関数"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "短文で会話を続けてください。"},
                {"role": "user", "content": prompt},
            ],
            max_tokens=50
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return None


def text_to_speech(speech_file_path, text):
    """テキストを音声ファイルに変換する関数"""
    try:
        with openai.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=text
        ) as response:
            response.stream_to_file(speech_file_path)
    except Exception as e:
        print(f"Error converting text to speech: {e}")


def audio_callback(indata, frames, time, status, q):
    """音声入力ストリームのコールバック関数"""
    if status:
        print(status)
    q.put(indata.copy())


def save_audio_data(q, filename, sample_rate):
    """音声データを保存する関数"""
    try:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(sample_rate)
            while True:
                data = q.get()
                if data is None:
                    break
                wf.writeframes(data)
    except Exception as e:
        print(f"Error saving audio data: {e}")


def split_text(text, length=20):
    """テキストを指定の長さで区切る関数"""
    return [text[i:i + length] for i in range(0, len(text), length)]


def signal_handler(sig, frame, q, thread):
    """SIGINTシグナルを処理するハンドラー"""
    print("Exiting the program.")
    q.put(None)
    thread.join()
    exit(0)


def main():
    sample_rate = 16000
    q = queue.Queue()
    filename = 'tmp/input.wav'

    # Create the 'tmp' folder if it doesn't exist
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    while True:
        user_input = input(
            "Press Enter to start/stop recording or 'q' to quit...\n").strip().lower()
        if user_input == 'q':
            print("Exiting the program.")
            break
        elif user_input == '':
            try:
                with sd.InputStream(
                        callback=lambda indata,
                        frames,
                        time,
                        status: audio_callback(indata, frames, time, status, q),
                        channels=1,
                        samplerate=sample_rate,
                        dtype='int16'
                ):
                    print("Recording... Press Enter to stop.")
                    thread = threading.Thread(
                        target=save_audio_data,
                        args=(q, filename, sample_rate)
                    )
                    thread.start()

                    signal.signal(
                        signal.SIGINT,
                        lambda sig,
                        frame: signal_handler(sig, frame, q, thread)
                    )
                    input()  # Wait for user to press Enter to stop recording

                    q.put(None)
                    thread.join()
                    print("Recording stopped.")

                    # 音声ファイルをテキストに変換
                    transcription_text = transcribe_audio(filename)
                    if transcription_text is None:
                        continue
                    print("Transcription text:", transcription_text)

                    # テキストを区切る
                    prompt_text = transcription_text[:20]
                    print("Transcription split text:", prompt_text)

                    # 会話生成
                    response = generate_response(prompt_text)
                    if response is None:
                        continue
                    print("Response:", response)

                    # 生成されたテキストを音声に変換
                    speech_file_path = "tmp/output.wav"
                    text_to_speech(speech_file_path, response)

                    # 音声を再生
                    try:
                        data, samplerate = sf.read(speech_file_path)
                        sd.play(data, samplerate=samplerate)
                        sd.wait()
                        print("Speaking...")
                    except Exception as e:
                        print(f"Error playing speech: {e}")

            except Exception as e:
                print(f"Error during recording process: {e}")


if __name__ == "__main__":
    main()
