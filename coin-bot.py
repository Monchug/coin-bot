import discord
from bs4 import BeautifulSoup as BS
import requests
from discord.ext import commands

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
client = commands.Bot("!")

@client.event
async def on_ready():  
    print(f"{client.user} botu Discorda bağlandı!\n")
    price = get_price("bitcoin")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= "Bitcoin "+price))

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Merhaba {member.name}, sunucuma hoşgeldin.")

@client.command(name="price")
async def on_message(ctx,arg):
    if client.user  == ctx.message.author:
        return    
    try:
        response = get_price(arg)
    except AttributeError:
        response = "Wrong coin name."
    await ctx.message.channel.send(response)
    
@client.command(name = "historical")
async def on_message(ctx,arg):
    if client.user  == ctx.message.author:
        return    
    try:
        response = get_price_historical(arg)
    except AttributeError:
        response = "Wrong date."
    await ctx.message.channel.send(response)

@client.command(name="status")
async def change_status(ctx,arg):
    price = get_price(arg)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=arg+' '+price))
    await ctx.message.channel.send("Status changed.")

@client.command(name="clear")
async def clear(ctx, number=50):
    await ctx.channel.purge(limit=number)    

client.run(TOKEN)     
