import discord
from discord import channel
from discord import client
from discord.utils import get
from dotenv.main import load_dotenv
from keep_alive import keep_alive
import os
from PIL import Image
import redis
import pickle
import io
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

garray = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
client = discord.Client()


@client.event
async def on_ready():
    print("Bot is up ")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    imsg = message.content
    if((r.get(str(message.channel))) is None):
        if(imsg.startswith("$tichelp")):
            async with message.channel.typing():
                await message.channel.send("$startgame to tictactoe")
        if(imsg.startswith("$tictactoe")):
            r.set(str(message.channel.id), 1)
            r.set(str(message.channel.id)+"garr", pickle.dumps(garray))
            r.set(str(message.channel.id)+"garr"+"movec", 'x')
            await message.reply("$game start")
    if((r.get(str(message.channel.id))).decode('utf-8') == "1"):
        if(imsg.startswith("$move")):
            p = imsg.split()
            pos = int(p[1])
            print(pos)
            piece = r.get(str(message.channel.id) +
                          "garr"+"movec").decode('utf=8')
            print(piece)
            if pos in range(1, 9, 1) and piece in ['x', 'o']:
                async with message.channel.typing():
                    if piece == 'x':
                        r.set((str(message.channel.id)+"garr"+"movec"), 'o')
                    if piece == 'o':
                        r.set((str(message.channel.id)+"garr"+"movec"), 'x')
                    # arr = io.BytesIO()
                    cgarr = pickle.loads(r.get(str(message.channel.id)+"garr"))
                    if(generate(pos, piece, cgarr) != -1):
                        cgarr = generate(pos, piece, cgarr)
                        r.set(str(message.channel.id) +
                              "garr", pickle.dumps(cgarr))
                        if piece == 'x':
                            r.set((str(message.channel.id)+"garr"+"movec"), 'o')
                        if piece == 'o':
                            r.set((str(message.channel.id)+"garr"+"movec"), 'x')
                        if check_win(cgarr, piece) == 1:
                            flushRedis(str(message.channel.id))
                            if(piece == 'x'):
                                await message.reply(discord.File("X final.gif"))
                            if(piece == 'o'):
                                await message.reply(discord.File("O final.gif"))
                        if(cgarr != garray):
                            if check_draw(cgarr) == 1:
                                flushRedis(str(message.channel.id))
                                await message.reply("GAME IS A DRAW")
                        if(check_win(cgarr, piece) == 0 and check_draw(cgarr) == 0):
                            img = render(cgarr)
                            img.save(str(message.channel.id)+'.png')
                            await message.reply(file=discord.File(str(message.channel.id)+'.png'))
                            os.remove(str(message.channel.id)+'.png')
                    if(generate(pos, piece, cgarr) == -1):
                        await message.reply("occupied position,enter an empty position")

            '''if(r.get(str(message.channel.id)+"garr"+"movec").decode('utf=8') != piece):
                await message.reply('game failure,botDev is checking')'''


def check_win(cgarr, piece):
    soln = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7],
            [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    if(piece == 'x'):
        val = 0
    if(piece == 'o'):
        val = 1
    c = 0
    for i in cgarr:
        for j in soln:
            if(c == 3):
                return 1
            c = 0
            for k in j:
                if(cgarr[k-1] == val):
                    c += 1
                else:
                    continue
    return 0


def check_draw(garr):
    if(garr.count(0)+garr.count(1)):
        return 1
    else:
        return 0


def generate(pos, piece, garray):
    if garray[pos-1] != -1:
        return(-1)
    else:
        if(piece == 'x'):
            garray[pos-1] == 0
        if(piece == 'o'):
            garray[pos-1] == 1
        return(garray)


def render(garray1):
    img0 = Image.open(r"Green grid.png")
    img1 = Image.open(r"cross white.png")
    img2 = Image.open(r"circle white.png")
    imar = [img1, img2]
    w = 131
    h = 129
    index = 0
    Pos = [(0, 0), (w, 0), (2*w, 0), (0, h), (w, h),
           (2*w, h), (0, 2*h), (w, 2*h), (2*w, 2*h)]
    for i in garray1:
        if (i != -1):
            img0.paste(imar[i], Pos[index], mask=imar[i])
        index += 1
    # img0.show()
    return img0


'''def render(garray):
    img0 = Image.open(r"Green grid.png")
    img1 = Image.open(r"cross white.png")
    img2 = Image.open(r"circle white.png")
    Pos=[(0,0),(w,0),(2*w,0),(0,h),(w,h),(2*w,h),(0,2*h),(w,2*h),(2*w,2*h)]
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
                # img0.save("Green grid.png")
                # img0.show()
                b += 1
        a += 1
    # img0.show()
    return(img0)'''


def readRedis(msgChan):
    game = pickle.loads(r.get(msgChan+'garray'))
    return game


def writeRedis(gArr):
    r.set(garray, pickle.dumps(gArr))


def flushRedis(key):
    r.delete(key)
    r.delete(key+"garr")
    r.delete(key+"garr"+"movec")


keep_alive()
load_dotenv()
my_secret = os.getenv('mtoken')
# print(my_secret)
client.run(my_secret)
