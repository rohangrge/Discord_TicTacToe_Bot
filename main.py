import discord
from discord import channel
from discord import client
from dotenv.main import load_dotenv
from redis.connection import msg
from keep_alive import keep_alive
import os
from PIL import Image
import redis
import pickle
r = redis.Redis()
img0 = Image.open(r"Green grid.png")
img1 = Image.open(r"cross white.png")
img2 = Image.open(r"circle white.png")
imar = [img1, img2]
w = 131
h = 129
Pos = [[(0, 0), (w, 0), (2*w, 0)],
       [(0, h), (w, h), (2*w, h)],
       [(0, 2*h), (w, 2*h), (2*w, 2*h)]]

garray = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
client = discord.Client()


@client.event
async def on_ready():
    print("Bot is up ")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    imsg = message.content

    if(imsg.startswith("$tichelp")):
        async with message.channel.typing():
            await message.channel.send("$startgame to tictactoe")
    if(imsg.startswith("$tictactoe")):
        r.set(str(message.channel), 1)
        await message.reply("$game start")


def render(garray):
    img0 = Image.open(r"Green grid.png")
    img1 = Image.open(r"cross white.png")
    img2 = Image.open(r"circle white.png")
    imar = [img1, img2]
    w = 131
    h = 129
    Pos = [[(0, 0), (w, 0), (2*w, 0)],
           [(0, h), (w, h), (2*w, h)],
           [(0, 2*h), (w, 2*h), (2*w, 2*h)]]
    a = 0
    for i in garray:
        b = 0
        for j in i:
            if(j == -1):
                b += 1
            else:
                img0.paste(imar[j], Pos[a][b], mask=imar[j])
                #img0.save("Green grid.png")
                # img0.show()
                b += 1
        a += 1
    # img0.show()
    return(img0)


def readRedis():
    game = pickle.loads(r.get('garray'))
    return game


def writeRedis(gArr):
    r.set(garray, pickle.dumps(gArr))


def flushRedis():
    r.flushdb


keep_alive()
load_dotenv()
my_secret = os.getenv('mtoken')
# print(my_secret)
client.run(my_secret)
