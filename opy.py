from flask import Flask, request
from discord.ext import commands
import asyncio
import discord
from flask_cors import CORS
from geopy.geocoders import Nominatim
import random 
geolocator = Nominatim(user_agent='geoapiExercises')

TOKEN = 'MTIzNDMzMzQyNTc3OTg2NzY0OA.G4D4j-._uEA-16b3Pa4JrXQRJGTH-zA3MX7esIsdi1Ids'
llLink = 'https://s3340bei.github.io/sw47/'

app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:5500'])
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    rand = random.randint(0, 10000)
    channel = bot.get_channel(953439775786930209)
    await channel.send('請點擊此連結'+llLink+'\n並輸入以下驗證碼：'+str(rand))

@app.route('/post', methods=['POST'])
def handle_post():
    data = request.get_json()
    print(data)
    location = geolocator.reverse(("{}, {}".format(data['latitude'], data['longitude'])))
    print(location.address)
    if location.address.find("元智") == -1 :    print("not in YZU")
    else:  print("in YZU")
    mapLink = 'https://www.google.com/maps/dir//'+str(data['latitude'])+',%20'+str(data['longitude'])
    print(mapLink)
    asyncio.run_coroutine_threadsafe(send_to_discord(data), bot.loop)
    asyncio.run_coroutine_threadsafe(send_to_discord(mapLink), bot.loop)
    asyncio.run_coroutine_threadsafe(send_to_discord(location.address), bot.loop)
    return 'ok', 200

async def send_to_discord(data):
    channel = bot.get_channel(953439775786930209)  # replace CHANNEL_ID with your channel ID
    await channel.send(data)


import threading

def run_bot():
    bot.run(TOKEN)

def run_app():
    app.run(port=5000)

bot_thread = threading.Thread(target=run_bot)
app_thread = threading.Thread(target=run_app)

bot_thread.start()
app_thread.start()

bot_thread.join()
app_thread.join()
