from requests import post, get
import os
import numpy as np
import aubio
import unicodedata
import json
import base64

##################
#    Config      #
##################

def normalize(text): 
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn' 
    ).lower()

##################
#    Deezer      #
##################

def get_track_deezer(track_name, artist_name): 
    query = track_name 
    url = f"https://api.deezer.com/search?q={query}" 
    result = get(url) 
    result = result.json() 
    if "data" in result and result["data"]: 
        for track in result["data"]: 
            if normalize(track["artist"]["name"]) == normalize(artist_name): 
                return track["preview"]
    return None


##################
#   Aubio-LedFx  #
##################

def classifying_number_parameters_aubio(preview):
    response = get(preview) 
    with open("preview.mp3", "wb") as f: 
        f.write(response.content)
    preview = "preview.mp3"
    win_s = 2048
    hop_s = win_s//2
    samplerate = 0
    pitch_o = aubio.pitch("yin",win_s,hop_s,samplerate)
    pitch_o.set_unit("Hz")
    pitch_o.set_silence(-40)
    tempo_o = aubio.tempo("default", win_s, hop_s, samplerate) 
    onset_o = aubio.onset("default", win_s, hop_s, samplerate) 
    source = aubio.source(preview,samplerate,hop_s)
    samplerate = source.samplerate
    pitches,tempos,onsets,mfccs = [],[],[],[]
    total_frames = 0
    while True: 
        samples, read = source() 
        pitch = pitch_o(samples)[0] 
        total_frames += read
        if pitch > 0:  
            pitches.append(pitch) 
        if tempo_o(samples):
            tempos.append(tempo_o.get_bpm())
        if tempo_o(samples):
            tempos.append(tempo_o.get_bpm())
        if onset_o(samples):
            position_seconds = total_frames / float(source.samplerate) 
            onsets.append(position_seconds)
        if read < hop_s:
            break        
    del source
    os.remove(preview)
    return { 
            "pitch_mean": float(np.mean(pitches)) if pitches else 0, 
            "tempo_mean": float(np.mean(tempos)) if tempos else 0, 
            "onset_count": len(onsets), 
            }

def classifying_song_aubio(metrics):
    if metrics["tempo_mean"] > 120 and metrics["pitch_mean"] > 200: 
        return "Feliz/Energético" 
    elif metrics["tempo_mean"] < 80 and metrics["pitch_mean"] < 150: 
        return "Triste/Calmo" 
    elif metrics["onset_count"] > 50: 
        return "Agressivo/Intenso" 
    else: 
        return "Neutro/Relaxado"
    
    
##################
#  Callback Json #
##################
def write_data(track_artist,track_uri,listening_timestamp,track_name,emotion):
    data = {
            "user":"Not implemented yet",
            "track_artist":normalize(track_artist),
            "track_uri":track_uri,
            "listening_timestamp":listening_timestamp,
            "track_name":normalize(track_name),
            "track_emotion":emotion
    }
    data = json.dumps(data,indent=4)
    data = "\n"+data+","    
    with open("./return/return_musics.json",'a',encoding="utf-8") as file:
        file.write(data)
