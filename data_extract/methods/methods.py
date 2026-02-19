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
#    Spotify     #
##################

def get_token_spotify(client_id,client_secret):
    auth_string = client_id+":"+client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic "+auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data = {
        "grant_type" : "client_credentials"
    }
    result = post(url=url,headers=headers,data=data)
    result = json.loads(result.content)
    acess_token = result['access_token']
    return acess_token    

def get_auth_header_spotify(token):
    return {"Authorization" : "Bearer "+token}


def get_track_spotify(music_id,headers):
    url = f"https://api.spotify.com/v1/tracks/{music_id}"
    result = get(url=url,headers=headers)
    result = result.json()
    song_name = result["name"]
    artist_name = result["artists"][0]["name"]
    return{'artist':artist_name,'song':song_name}

    
    

##################
#    Deezer      #
##################

def get_track_id_deezer(track_name, artist_name): 
    query = track_name 
    url = f"https://api.deezer.com/search?q={query}" 
    result = get(url) 
    result = result.json() 
    if result["data"]: 
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