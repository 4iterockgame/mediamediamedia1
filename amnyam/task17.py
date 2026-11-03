import speech_recognition as sr


def audio_file_to_text():
    r = sr.Recognizer()
    file_path = "sample-3s.wav"

    try:
        with sr.AudioFile(file_path) as source:
            print("Читаємо аудіофайл...")
            audio = r.record(source)

            print("Відправляємо на сервер Google для розпізнавання...")
            text = r.recognize_google(audio, language="en-US")
            print(f"Успіх! Розпізнаний текст: {text}")

    except FileNotFoundError:
        print("Помилка: файл не знайдено.")
    except sr.UnknownValueError:
        print("Google не зміг розпізнати звук.")
    except sr.RequestError:
        print("Помилка з'єднання. Перевірте інтернет.")


if __name__ == "__main__":
    audio_file_to_text()