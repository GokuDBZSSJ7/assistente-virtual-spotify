from spotipy.oauth2 import SpotifyOAuth
import spotipy
import speech_recognition as sr

client_id = '6bef68b73e584fbb9c5132a48cba430d'
client_secret = 'ce6396dabb884ce793c248909cd9ae93'
redirect_uri = 'http://localhost:8000/callback'
scope = 'user-modify-playback-state user-read-playback-state'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

listener = sr.Recognizer()

def beep():
    """Emite um som simples para feedback."""
    print("\a")

def listen():
    """Escuta o comando do usuário e retorna o texto reconhecido."""
    rec = ""
    try:
        with sr.Microphone() as source:
            print("Aguardando comando...")
            audio = listener.listen(source)
            rec = listener.recognize_google(audio, language='pt-BR').lower()
    except Exception as e:
        print(f"Erro ao ouvir: {str(e)}")
    return rec

def verificar_dispositivo_ativo():
    """Verifica se há dispositivos ativos e retorna o ID do dispositivo."""
    try:
        devices = sp.devices()
        active_devices = [device for device in devices['devices'] if device['is_active']]
        
        if active_devices:
            return active_devices[0]['id']
        elif devices['devices']:
            return devices['devices'][0]['id']
        else:
            print("Nenhum dispositivo disponível. Abra o Spotify em algum dispositivo.")
            return None
    except Exception as e:
        print(f"Erro ao verificar dispositivos: {str(e)}")
        return None

def tocar_musica(song, artist=None):
    """Busca e toca uma música no Spotify."""
    try:
        device_id = verificar_dispositivo_ativo()
        if not device_id:
            return

        query = f"{song} {artist}" if artist else song
        result = sp.search(query, limit=1, type='track')

        if result['tracks']['items']:
            track_uri = result['tracks']['items'][0]['uri']
            sp.start_playback(device_id=device_id, uris=[track_uri])
        else:
            print("Música não encontrada.")
    except Exception as e:
        print(f"Erro ao buscar ou tocar a música: {str(e)}")

def ouvir_comando():
    while True:
        rec = listen()
        if "computador" in rec:
            beep()
            print("Aguardando o nome da música...")
            rec = listen()
            if rec:
                print(f"Comando recebido: {rec}")
                partes = rec.split("por")
                song = partes[0].strip()
                artist = partes[1].strip() if len(partes) > 1 else None
                tocar_musica(song, artist)

ouvir_comando()
