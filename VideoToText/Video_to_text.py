import sys
import os
import subprocess
from faster_whisper import WhisperModel

def extraer_audio(video_path, audio_path):
    print("🎧 Extrayendo audio con FFmpeg...")
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def transcribir(audio_path, salida_txt, modelo="small"):
    print("🧠 Cargando modelo Whisper...")
    model = WhisperModel(
        modelo,
        device="cpu",
        compute_type="int8"
    )

    print("✍️ Transcribiendo (video largo, paciencia)...")
    segments, info = model.transcribe(
        audio_path,
        language="es",
        vad_filter=True
    )

    with open(salida_txt, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(segment.text.strip() + "\n")

    print("✅ Transcripción terminada")

def main():
    if len(sys.argv) < 2:
        print("❌ Arrastra un video o pásalo como argumento")
        return

    video_path = sys.argv[1].strip('"')

    if not os.path.exists(video_path):
        print("❌ El archivo no existe")
        return

    base = os.path.splitext(video_path)[0]
    audio_path = base + "_audio.wav"
    texto_path = base + "_transcripcion.txt"

    extraer_audio(video_path, audio_path)
    transcribir(audio_path, texto_path)

    print(f"\n📄 Archivo generado:\n{texto_path}")

if __name__ == "__main__":
    main()
