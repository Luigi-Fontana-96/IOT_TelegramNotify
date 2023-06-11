from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Flask, request, abort
from dotenv import load_dotenv
import os
from os.path import join, dirname
from threading import Thread
import requests
import base64
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env') # path per le var di ambiente
load_dotenv(dotenv_path)# carico le var di ambiente
api_key = os.environ.get('api_key') # settaggio dell'api key
app = Flask(__name__) # istanza flask

notify_users = [] # utenti che hanno richiesto la notifica
enabled_users = []# utenti abilitati alle notifiche
users_areas = [] # var di appoggio
final_diction = {}

def send_alert(id, img_bytes, info_cam):
    params = {'chat_id': id,
              'caption': str(info_cam)}
    files = {'photo': img_bytes}
    url = f'https://api.telegram.org/bot{api_key}/sendPhoto?chat_id={id}'
    requests.post(url, params, files=files)
    return '', 204

@app.route("/notify_telegram", methods=['POST'])
def notify_method():

    str_date_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    info_cam = f"Data : {str(str_date_time)}\n"
    if not request.json or 'image' not in request.json:
        abort(400)

    im_b64 = request.json['image']
    caption = request.json['caption']

    for key,value in caption.items(): # JSON formatting
        info_cam += f"{key} : {value}\n"
        if key == "Area di competenza":
            area_value = value.upper()

    img_bytes = base64.b64decode(im_b64.encode('utf-8'))
    for id in final_diction[area_value]:
        for observer in notify_users:
            if observer['id'] == id:
                send_alert(id, img_bytes, info_cam)
    return '', 204

def load_file():
        with open('users_areas.txt') as f:
            contents = f.readlines()
            for element in contents:
                try:
                    splitting = element.split(" ")
                    clearing = splitting[1].strip()
                    enabled_users.append(int(splitting[0]))
                    users_areas.append((clearing.upper(), int(splitting[0])))
                except (IndexError, ValueError):
                    continue

        for i in users_areas:
            if i[0] in final_diction.keys():
                nuova_lista = []
                old = final_diction[i[0]]
                new = i[1]
                old.append(new)
                nuova_lista.append(old)
                nuova_lista.append(new)
                final_diction[i[0]] = old
            else:
                final_diction[i[0]] = ['a', i[1]]

        for key, value in final_diction.items():
            value.pop(0)

        #print(f"Enabled users {enabled_users}\n")
        #print(f"Users areas : {users_areas}\n")
        #print(f"final diction: {final_diction}\n")

# Funzione /start per il bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f"Ciao {user['first_name']} premi /help per il menù dei comandi disponibili.")

# Funzione /help per il bot
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I comandi disponibili sono:\n "+\
                                    "/start -> Messaggio di Benvenuto\n"+\
                                    "/help -> Questo Messaggio\n"+\
                                    "/content -> Informazioni riguardanti il bot\n"+\
                                    "/notify -> Inizio invio notifiche\n"+\
                                    "/unnotify -> Termine invio notifiche\n")

# Funzione /content per il bot
async def content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Questo Bot è progettato per allertare quando una telecamera riconosce un abbondono di rifiuti\n"+\
                                    "Con il comando /notify puoi attivare le notifiche;\n"+\
                                    "Con il comando /unnotify puoi disattivarle")

# Funzione /notify per il bot
async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user['id'] in enabled_users:
        if user in notify_users:
            await update.message.reply_text(f"Sei già presente nella lista dei notificabili")
        else:
            notify_users.append(user)
            await update.message.reply_text(f"Sei stato aggiunto nella lista dei notificabili")
    else:
        await update.message.reply_text(f"Lei non è presente nella lista dei notificabili")

# Funzione /unnotify per il bot
async def unnotify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user['id'] in enabled_users:
        if user in notify_users:
            await update.message.reply_text("Sei Stato Rimosso dalla lista dei notificabili")
            notify_users.remove(user)
        else:
            await update.message.reply_text('Non sei presente nella lista degli osservatori, effettuare la /notify se si vuole ricevere le notifiche')
    else:
        await update.message.reply_text(f"Lei non è presente nella lista dei notificabili")

# Funzione echo dei messaggi per il bot
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


# debug Function
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    utenti = ''.join(str(notify_users))
    await update.message.reply_text(utenti) 


def main() -> None:
    load_file()
    """Start del bot."""
    # Crea l'applicazione e gli passa l'api token del proprio bot
    application = Application.builder().token(str(api_key)).build()

    # Comandi che rispondono
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("content", content))
    application.add_handler(CommandHandler("notify", notify))
    application.add_handler(CommandHandler("unnotify", unnotify))
    application.add_handler(CommandHandler("test", test))

    #Comando che fa una semplice echo
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

def task():
    # run the flask istance
    try:
        app.run()
    except:
        pass

if __name__ == "__main__":
    thread = Thread(target=task)
    thread.daemon = True
    thread.start()
    main()