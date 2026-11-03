import soundfile as sf
import os

src = "input.wav"

if not os.path.exists(src):
    print(f"Помилка: покладіть файл {src} у папку з проєктом!")
else:
    data, samplerate = sf.read(src)

    flac_path = "output.flac"
    sf.write(flac_path, data, samplerate, format='FLAC')

    ogg_path = "output.ogg"
    sf.write(ogg_path, data, samplerate, format='OGG', subtype='VORBIS')

    print(f"Оригінал WAV: {os.path.getsize(src)} байт")
    print(f"Стиснутий FLAC: {os.path.getsize(flac_path)} байт")
    print(f"Стиснутий OGG: {os.path.getsize(ogg_path)} байт")
    print("Готово! Файли створено.")