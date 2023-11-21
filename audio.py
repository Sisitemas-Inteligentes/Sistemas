from resemblyzer import preprocess_wav, VoiceEncoder
import numpy as np

#Carga los archivos de audio

def comparar_audiosNuevos(voz1, voz2):
    wav1 = preprocess_wav(voz1)
    wav2 = preprocess_wav(voz2)

    #Crea un codificador de voz y obtén los embeddings de las voces
    encoder = VoiceEncoder()
    embed1 = encoder.embed_utterance(wav1)
    embed2 = encoder.embed_utterance(wav2)

    #Calcula la similitud de las voces
    similarity = np.dot(embed1, embed2)
    if similarity >=0.80:
        print("La similitud entre las dos voces es: ", similarity)
    else:
        print("NO valid similarity, la similitud es de: ", similarity)


