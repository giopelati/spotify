from requests import post, get
import json
import base64

def get_token_spotify(client_id,client_secret):
    
    # Criando a string de autenticação
    auth_string = client_id+":"+client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    # Definindo valores para metodo POST
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic "+auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data = {
        "grant_type" : "client_credentials"
    }
    
    # Transformação de variavel em json via post
    result = post(url=url,headers=headers,data=data)
    result = json.loads(result.content)

    # Atribuindo o valor 'access_token' do JSON result
    acess_token = result['access_token']

    # Retornando o token de acesso
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