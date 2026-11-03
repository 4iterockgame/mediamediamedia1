import glob
import os
import soundfile as sf

def convert_files(input_pattern):
    files = glob.glob(input_pattern)
    if not files:
        print(f"Файлів за шляхом '{input_pattern}' не знайдено.")
        return

    for file_path in files:
        print(f"Конвертація: {file_path}...")
        data, samplerate = sf.read(file_path)
        out_path = os.path.splitext(file_path)[0] + ".flac"
        sf.write(out_path, data, samplerate, format='FLAC')
        print(f"Успішно збережено: {out_path}")

if __name__ == "__main__":
    print("Початок конвертації...")
    convert_files("audio/*.wav")
    print("Готово!")