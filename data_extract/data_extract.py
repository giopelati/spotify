from dotenv import load_dotenv
from methods.methods import get_token_spotify, get_auth_header_spotify, get_track_spotify, get_track_id_deezer, classifying_number_parameters_aubio, classifying_song_aubio
import os

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def orquestrator():
    token = get_token_spotify(client_id=spotify_client_id,client_secret=spotify_client_secret)
    auth_header = get_auth_header_spotify(token=token)
    track = get_track_spotify('40s4PAZc1lqzGk0LL1mMZh',auth_header)
    track_artist = track["artist"]
    track_name = track["song"]
    preview = get_track_id_deezer(track_name,track_artist)
    metrics = classifying_number_parameters_aubio(preview)
    classification = classifying_song_aubio(metrics)
    return classification