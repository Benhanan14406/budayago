import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import os

# --- INISIALISASI DI TINGKAT MODUL (Hanya sekali saat server dimulai) ---
# Muat processor dan model Wav2Vec2
wav2vec_processor = Wav2Vec2Processor.from_pretrained("indonesian-nlp/wav2vec2-indonesian-javanese-sundanese")
wav2vec_model = Wav2Vec2ForCTC.from_pretrained("indonesian-nlp/wav2vec2-indonesian-javanese-sundanese")

# Resampler, asumsikan audio input Anda mungkin 48kHz dan perlu di-resample ke 16kHz
# Jika audio Anda sudah 16kHz, resampler ini tidak akan banyak berpengaruh
wav2vec_resampler = torchaudio.transforms.Resample(48_000, 16_000)
# --- AKHIR INISIALISASI DI TINGKAT MODUL ---

def transcribe_audio_wav2vec(audio_file_path):
    """
    Fungsi untuk mengubah file audio menjadi teks menggunakan model Wav2Vec2.
    """
    if not os.path.exists(audio_file_path):
        print(f"Error: File audio tidak ditemukan di {audio_file_path}")
        return None

    try:
        # Muat file audio
        speech_array, sampling_rate = torchaudio.load(audio_file_path)

        # Resample jika sampling_rate tidak sesuai (misal dari 48kHz ke 16kHz)
        if sampling_rate != 16_000:
            print(f"Resampling audio dari {sampling_rate}Hz ke 16000Hz...")
            speech_array = wav2vec_resampler(speech_array)

        # Proses audio
        # Pastikan speech_array adalah numpy array dan memiliki dimensi yang benar
        inputs = wav2vec_processor(speech_array.squeeze().numpy(), sampling_rate=16_000, return_tensors="pt", padding=True)

        # Lakukan prediksi
        with torch.no_grad():
            logits = wav2vec_model(inputs.input_values, attention_mask=inputs.attention_mask).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = wav2vec_processor.batch_decode(predicted_ids)

        return transcription[0] # Mengembalikan hasil transkripsi pertama
    except Exception as e:
        print(f"Error during Wav2Vec2 transcription: {e}")
        return None

if __name__ == "__main__":
    audio_path_from_project = "techno.wav" # Pastikan file ini ada di root project Anda

    print(f"Mencoba transkripsi file: {audio_path_from_project}")
    transcribed_text = transcribe_audio_wav2vec(audio_path_from_project)

    if transcribed_text:
        print(f"Transkripsi dari {audio_path_from_project}: {transcribed_text}")
    else:
        print("Gagal melakukan transkripsi.")