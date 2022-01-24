import discord
from bs4 import BeautifulSoup as BS
import requests

def get_price(coin_name):
    url = f"https://coinmarketcap.com/currencies/{coin_name}/"
    data = requests.get(url)
    soup = BS(data.text, 'html.parser')
    price = soup.find("div", class_ ="priceValue").text
    return price

def get_price_historical(date):
    url = f"https://coinmarketcap.com/historical/{date}/"
    data = requests.get(url)
    soup = BS(data.text, 'html.parser')
    price = soup.find("td", class_ ="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price").text
    return price    

TOKEN = ""
client = discord.Client()

@client.event
async def on_ready():  
    print(f"{client.user} botu Discorda bağlandı!\n")

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Merhaba {member.name}, sunucuma hoşgeldin.")

@client.event
async def on_message(message):
    if client.user  == message.author:
        return

    if message.content[0:6] == "!price":      
        try:
            response = get_price(message.content[7:])
        except AttributeError:
            response = "Hatalı coin adı girdiniz."
        await message.channel.send(response)
    
    if message.content[0:7] == "!hprice":      
        try:
            response = get_price_historical(message.content[8:])
        except AttributeError:
            response = "Hatalı tarih girdiniz."
        await message.channel.send(response)

@client.event
async def clear(ctx, number=50):
    if ctx.message.content[0:6] == "!clear":
        await ctx.channel.purge(limit=number)    

client.run(TOKEN)        