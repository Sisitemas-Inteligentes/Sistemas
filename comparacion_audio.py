import librosa
import numpy as np


def extraer_caracteristicas_audio(wav_path):
    try:
        # Cargar el archivo de audio con librosa
        y, sr = librosa.load(wav_path)

        # Extraer características del audio
        caracteristicas_audio = librosa.feature.mfcc(y=y, sr=sr)

        return caracteristicas_audio

    except FileNotFoundError:
        print(f"Error: No se pudo abrir el archivo de audio '{wav_path}'")
        return None


def comparar_audios(audio1_path, audio2_path):
    # Extraer características de los audios

    caracteristicas_audio1 = extraer_caracteristicas_audio(audio1_path)
    caracteristicas_audio2 = extraer_caracteristicas_audio(audio2_path)

    # Verificar si se pudieron extraer las características
    if caracteristicas_audio1 is not None and caracteristicas_audio2 is not None:
        # Obtener la longitud mínima de las características
        min_length = min(caracteristicas_audio1.shape[1], caracteristicas_audio2.shape[1])

        # Truncar las características al mínimo común
        caracteristicas_audio1 = caracteristicas_audio1[:, :min_length]
        caracteristicas_audio2 = caracteristicas_audio2[:, :min_length]

        # Calcular la distancia euclidiana entre las características de audio
        distancia_euclidiana = np.linalg.norm(caracteristicas_audio1 - caracteristicas_audio2)

        # Imprimir la distancia euclidiana (puedes ajustar esto según tus necesidades)
        print(f"Distancia Euclidiana entre los archivos de audio: {distancia_euclidiana}")

    else:
        print("Error: No se pudieron extraer características de uno o ambos archivos de audio.")
