from dotenv import load_dotenv
import json
from data_extract.functions.methods import get_track_deezer, classifying_number_parameters_aubio, classifying_song_aubio, write_data
import os

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def orquestrator(jsons):
    files = os.listdir("./return")
    
    if len(files) >= 1:
        os.remove("./return/return_musics.json")
        
    with open("./return/return_musics.json",'a',encoding="utf-8") as callback:
        callback.write("[")
        
    for file in jsons:
        file_path = f"./json/{file}"
        with open(file_path,"r",encoding="utf-8") as file_data:
            data = json.load(file_data)
    
        for d in data:
            listening_timestamp = str(d["ts"])
            spotify_track_artist_name = str(d["master_metadata_album_artist_name"])
            spotify_track_name = str(d["master_metadata_track_name"])
            spotify_track_uri = str(d["spotify_track_uri"])

            preview = get_track_deezer(spotify_track_name,spotify_track_artist_name)
            
            if preview is not None:
                metrics = classifying_number_parameters_aubio(preview)
                classification = classifying_song_aubio(metrics)
                write_data(spotify_track_artist_name,spotify_track_uri,listening_timestamp,spotify_track_name,classification)
                
                
    with open("./return/return_musics.json",'a',encoding="utf-8") as callback:
        content = callback.read()
        content = content[:-1]
        callback.truncate()
        content+="\n]"
        callback.write(content)