from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import requests
# Loading bot token
load_dotenv()
TOKEN = os.environ.get('TOKEN')

POKE_URL = "https://pokeapi.co/api/v2/pokemon"
response = requests.get(POKE_URL + "?limit=10000")
all_pokemon_names = {pokemon['name'] for pokemon in response.json()['results']}


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to server, {member.name}!')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello there!")

@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return

    if "hey" in message.content.lower():
        await message.add_reaction("👋")

    ctx = await bot.get_context(message)
    if ctx.valid:
        return

    words = {word.lower() for word in message.content.split()}

    matching_pokemon_names = words.intersection(all_pokemon_names)

    for pokemon_name in matching_pokemon_names:
        response = requests.get(POKE_URL + "/" + pokemon_name)
        if response.status_code == 200:
            data = response.json()
            sprite_url = data.get('sprites').get('versions').get('generation-v').get('black-white').get('animated').get('front_default')

            if not sprite_url:
                sprite_url = data['sprites']['front_default']
            embed = discord.Embed(title=f"You mentioned {pokemon_name}!! ")
            embed.set_image(url=sprite_url)
            await message.channel.send(embed=embed)

bot.run(TOKEN)
