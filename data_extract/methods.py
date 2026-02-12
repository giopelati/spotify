from requests import post
import json
import base64

def get_token(client_id,client_secret):
    
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
    return(acess_token)    