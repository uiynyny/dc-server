import os
import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

resend = {
    142557350346096640: {
        "channel": 996051310346518590,
        "hook": os.getenv('KUOKUO_HOOK')
    },
    998780763178795038: {
        "channel": 996051310346518590,
        "hook": os.getenv('KUOKUO_HOOK')
    },
    871922393701044255: {
        "channel": 998488472467816520,
        "hook": os.getenv('KATZ_HOOK')
    },
    507081000271216640: {
        "channel": 1008081094379319336,
        "hook": os.getenv("JIMMY_HOOK")
    },
    426972096820805640:{
      "channel":1008081094379319336,
      "hook":os.getenv("MAIN_HOOK")
    }
}

PUBLIC_CHANNEL = [
    999061469549309963,  #重要公告
    998488472467816520,  #交易訊號-katz
    996051310346518590,  #交易訊號-kuoyuching
    1008081094379319336,  #交易訊號-jimmy
    999722148497199125,  #資訊發布
    999722924435046430  #推廣鏈結
]

PIC_REQUIRED_CHANNEL = [
    976977208222548018,  #資料分享
    998725902156431400,  #法師世界
    990278903241248818,  #面壁檢討
    993925444065824892,  #幣種觀察
    991327731914657862,  #美股觀點
    998393727691264121,  #學習資源
    998394839815176273,  #盤面分析
    990273821191843910,  #外交前線
    998335063181754489, # fu pan
    1007928829664317460, #JIMMY
    1006215829114851328, #Doras
    1006216102856118362, #qie
    1006216000586403981, #skrr
    1001420638218629141, #mi jie
    998336106049318912, #yue
    998336728941211748, #mai mai
    998335833268555806, #jiang chen
    998336868913528944, #Kuo
    998337085050200154, #zuo ye
    998335601352904855, #katz
    998335710434181252, #gui ge
  
    1009344716153831464, #test
]

reactions = ['✍🏻', '❤️', '🧡', '💛', '💜', '🍚']

intents = discord.Intents.default()
intents.message_content = True
intents.webhooks=True
bot = commands.Bot(command_prefix='$',intents=intents)


@bot.event
async def on_ready():
    print(f"client online {bot.user} | watch {len(bot.guilds)} servers")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    
    # add reactions
    if message.channel.id in PUBLIC_CHANNEL or (message.channel.id
                                                in PIC_REQUIRED_CHANNEL
                                                and len(message.attachments) > 0):
        for r in reactions:
            await message.add_reaction(r)
    
    if message.author.id in resend and "📝" in message.content and message.channel.id not in [
            resend[author]['channel'] for author in resend
    ]:
        print(f"channel: {message.channel.id} | {message.content}")
        await send_to_webhook(resend[message.author.id]['hook'], message)
      
    await bot.process_commands(message)


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if after.author.id in resend and "📝" in after.content and "📝" not in before.content \
  and after.channel.id not in [resend[author]['channel'] for author in resend]:
        await send_to_webhook(resend[after.author.id]['hook'], after)
    await bot.process_commands(after)


async def send_to_webhook(hook, message):
  async with aiohttp.ClientSession() as sess:
    wh = discord.Webhook.from_url(hook,session=sess)
    for att in message.attachments:
        message.content += '\n' + att.url
    print(message.conent)
    await wh.send(message.content,username=message.author.display_name,avatar_url=message.author.avatar.url)


bot.run(os.environ['BOT'],log_handler=None)