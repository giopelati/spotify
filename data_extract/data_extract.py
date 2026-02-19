from dotenv import load_dotenv
import json
from data_extract.functions.methods import get_token_spotify, get_auth_header_spotify, get_track_spotify, get_track_id_deezer, classifying_number_parameters_aubio, classifying_song_aubio, write_data
import os

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def orquestrator(json_musics):
    os.remove("./return/return_musics.json")
    with open("./return/return_musics.json",'a',encoding="utf-8") as callback:
        callback.write("{\n")

    with open(json_musics,"r",encoding="utf-8") as file:
        data = json.load(file)
    
    for d in data:
        spotify_track_uri = str(d["spotify_track_uri"])
        spotify_track_uri = spotify_track_uri.removeprefix("spotify:track:")
        
    
        token = get_token_spotify(client_id=spotify_client_id,client_secret=spotify_client_secret)
        auth_header = get_auth_header_spotify(token=token)
        track = get_track_spotify(spotify_track_uri,auth_header)
        track_artist = track["artist"]
        track_name = track["song"]
        preview = get_track_id_deezer(track_name,track_artist)
        metrics = classifying_number_parameters_aubio(preview)
        classification = classifying_song_aubio(metrics)
        write_data(track_artist,spotify_track_uri,track_name,classification)
        
    with open("./return/return_musics.json",'a',encoding="utf-8") as callback:
        callback.write("}")