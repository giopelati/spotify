from dotenv import load_dotenv
from methods import get_token_spotify, get_auth_header_spotify,get_track_spotify
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")



token = get_token_spotify(client_id=client_id,client_secret=client_secret)
auth_header = get_auth_header_spotify(token=token)

track = get_track_spotify('4uLU6hMCjMI75M1A2tKUQC',auth_header)

print(track)