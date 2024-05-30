import discord
from discord.ext import commands
import io

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'TOKEN'

@bot.event
async def on_ready():
    print(f'{bot.user} ha iniciado sesión.')

@bot.command()
async def export_msg(ctx, origin_channel_id: int, destination_server_id: int, destination_channel_id: int):
    origin_channel = bot.get_channel(origin_channel_id)
    if not origin_channel:
        await ctx.send(f'No se encontró el canal de origen con ID {origin_channel_id}')
        return
    
    destination_server = bot.get_guild(destination_server_id)
    if not destination_server:
        await ctx.send(f'No se encontró el servidor de destino con ID {destination_server_id}')
        return

    destination_channel = destination_server.get_channel(destination_channel_id)
    if not destination_channel:
        await ctx.send(f'No se encontró el canal de destino con ID {destination_channel_id}')
        return

    all_messages = []
    if isinstance(origin_channel, discord.TextChannel) and origin_channel.history is not None:
        async for message in origin_channel.history(limit=None):
            all_messages.append(message)

        await ctx.send(f'Comienza {origin_channel.mention} a {destination_channel.mention}')

        for message in reversed(all_messages):
            content = message.content
            if content:
                await destination_channel.send(f'{content}')
            
            if message.embeds:
                for embed in message.embeds:
                    await destination_channel.send(embed=embed)
                    
            for attachment in message.attachments:
                if attachment is not None:
                    data = await attachment.read()
                    await destination_channel.send(content='', file=discord.File(io.BytesIO(data), filename=attachment.filename))     

    await ctx.send(f'Mensajes exportados de {origin_channel.mention} a {destination_channel.mention}')


@bot.command()
async def get_channels_ids(ctx):
    guild = ctx.guild
    if not guild:
        await ctx.send("No estás en un servidor.")
        return
    
    channel_id = []

    for channel in guild.channels:
        channel_id.append(channel.id)

    with open('channel_id.txt', 'w') as f:
        f.write('\n'.join(map(str, channel_id)))

    await ctx.send("Aquí tienes la lista de IDs de los canales:", file=discord.File('channel_id.txt'))
    
@bot.command()
async def full_backup(ctx, actual_discord, discord_to_send):
    map_channels = []
    origin_channels, destination_channels = await get_channel_ids_and_names(ctx, actual_discord, discord_to_send)
    
    for obj in enumerate(origin_channels):
        channel_destination_data = search_by_channel_name(obj, destination_channels)
        if channel_destination_data:
            map_channels.append({"id_origin_channel": obj['id'], "id_destination_channel": channel_destination_data['id']})
        else:
            ctx.send("Los servidores no estan alineados")
            
    for obj in enumerate(map_channels):
        await export_msg(ctx, obj['id_origin_channel'], int(discord_to_send), obj['id_destination_channel'])
    
async def get_channel_ids_and_names(ctx, discord_1, discord_2):
    guild_origin = bot.get_guild(int(discord_1))
    guild_destination = bot.get_guild(int(discord_2))
    
    if guild_origin is not None and guild_destination is not None:
        origin_channels = get_channel(guild_origin)
        destination_channels = get_channel(guild_destination)
        return origin_channels, destination_channels
    else:
        await ctx.send("No estás en un servidor.")
    
def get_channel(guild): 
    channel_list = []
    if guild:
        for channel in guild.channels:
            channel_list.append({"id": channel.id, "name": channel.name})
    return channel_list

def search_by_channel_name(obj, destination_channels):
    for destination_obj in destination_channels:
        if obj is not None and destination_obj is not None and obj['name'] is not None and destination_obj['name'] is not None and obj['name'] == destination_obj['name']:
            return destination_obj
    return  

bot.run(TOKEN)