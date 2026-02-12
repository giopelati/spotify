from dotenv import load_dotenv
from methods import get_token, get_auth_header,get_artists,get_track,get_track_infos
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")



token = get_token(client_id=client_id,client_secret=client_secret)
auth_header = get_auth_header(token=token)
print(auth_header)

track = get_track_infos('4uLU6hMCjMI75M1A2tKUQC',auth_header)