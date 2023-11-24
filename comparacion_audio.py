import librosa
import numpy as np


def comparar_audios(audio1_path, audio2_path):
    # Cargar los archivos de audio usando librosa
    audio1, _ = librosa.load(audio1_path, sr=None)
    audio2, _ = librosa.load(audio2_path, sr=None)

    # Calcular las características MFCC de cada audio
    mfccs1 = librosa.feature.mfcc(audio1, sr=None)
    mfccs2 = librosa.feature.mfcc(audio2, sr=None)

    # Asegurarse de que ambos conjuntos de características tengan la misma longitud
    min_length = min(mfccs1.shape[1], mfccs2.shape[1])
    mfccs1 = mfccs1[:, :min_length]
    mfccs2 = mfccs2[:, :min_length]

    # Calcular la similitud mediante la distancia euclidiana
    euclidean_distance = np.linalg.norm(mfccs1 - mfccs2)

    # Normalizar la distancia euclidiana al rango [0, 1]
    max_distance = np.max([np.linalg.norm(mfccs1), np.linalg.norm(mfccs2)])
    normalized_similarity = 1 - euclidean_distance / max_distance

    print(f"La similitud es: {normalized_similarity}")
    return normalized_similarity
