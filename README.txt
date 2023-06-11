Configurazione di telegram bot,versioni e librerie python:

Contenuto Elaborato:
- BackEnd.py : codice per il backend.
- .env :contenente le variabili d'ambiente che verranno caricate dal backend.
- requirements.txt : contenente i moduli da scaricare.
-users_areas.txt : contenente i chat_id degli account telegram seguiti dall'area di competenza.

Versione di python utilizzata: Python 3.8.10
Installare i moduli necessari con il comando: pip install -r requirements.txt


PASSI NECESSARI ALL'AVVIO DELL'APPLICAZIONE

Creazione del BOT:
Entrare nel proprio profilo Telegram e cercare il bot BotFather.
Questo bot permette di gestire i bot.
Una volta nella chat del BotFather, i passi da seguire sono i seguenti:
- Lanciare il comando /newbot
- Inserire il nome da associare al nuovo bot
- Inserire l'username con cui vi riferirete al bot
Verrà generata una schermata in cui potrete raggiungere il bot tramite link.

Inoltre vi verrà dato un API TOKEN che deve essere inserito nella voce api_key del file .env senza apici.
Non perdere l'API TOKEN, chiunque lo possiede può controllare il bot.

Infine, settare il file users_areas.txt con chat_id seguito dall'Area di competenza.
E' possibile trovare il proprio chat_id dal bot di telegram chiamato IDBot (@myidbot)


FUNZIONAMENTO GENERALE
Una volta lanciato il backend è possibile interagire con il bot da telegram; Per ricevere dei messaggi è necessario /notificarsi ed avere la propria area di competenza (del proprio chat_id) corrispondente all'area di competenza dell' info_cam in detector_garb .

