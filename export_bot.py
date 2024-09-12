import discord
import os
from discord.ext import commands
import io
from lenguage import load_settings, get_translation, set_language
import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
intents.guilds = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!', '/'), intents=intents)

TOKEN = ''

settings = load_settings()

@bot.event
async def on_ready():
    print(f'{bot.user}{get_translation(None ,"init_sesion", settings)}')

@bot.command()
async def export_msg(ctx, origin_channel_id: int, destination_server_id: int, destination_channel_id: int):
    origin_channel = bot.get_channel(origin_channel_id)
    if not origin_channel:
        await ctx.send(f'{get_translation(ctx, "origin_channel_not_found", settings)}{origin_channel_id}')
        return
    
    destination_server = bot.get_guild(destination_server_id)
    if not destination_server:
        await ctx.send(f'{get_translation(ctx, "destination_guild_not_found", settings)}{destination_server_id}')
        return

    destination_channel = destination_server.get_channel(destination_channel_id)
    if not destination_channel:
        await ctx.send(f'{get_translation(ctx, "destination_guild_not_found", settings)}{destination_channel_id}')
        return

    all_messages = []
    if isinstance(origin_channel, discord.TextChannel) and origin_channel.history is not None:
        async for message in origin_channel.history(limit=None):
            all_messages.append(message)

        await ctx.send(f'{get_translation(ctx, "start", settings)}{origin_channel.mention}{get_translation(ctx, "to", settings)}{destination_channel.mention}')

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

    await ctx.send(f'{get_translation(ctx, "msg_export", settings)}{origin_channel.mention}{get_translation(ctx, "to", settings)}{destination_channel.mention}')


@bot.command()
async def get_channels_ids(ctx):
    guild = ctx.guild
    if not guild:
        await ctx.send(get_translation(ctx, "server_not_found", settings))
        return
    
    channel_id = []

    for channel in guild.channels:
        channel_id.append(channel.id)

    with open('channel_id.txt', 'w') as f:
        f.write('\n'.join(map(str, channel_id)))

    await ctx.send(get_translation(ctx, 'id_list', settings), file=discord.File('channel_id.txt'))
    
@bot.command()
async def full_backup(ctx, discord_to_send):
    map_channels = []
    origin_channels, destination_channels = await get_channel_ids_and_names(ctx, str(ctx.guild.id), discord_to_send)
    
    for obj in enumerate(origin_channels):
        channel_destination_data = search_by_channel_name(obj, destination_channels)
        if channel_destination_data:
            map_channels.append({"id_origin_channel": obj['id'], "id_destination_channel": channel_destination_data['id']})
        else:
            ctx.send(get_translation(ctx, "servers_not_aligned", settings))
            
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
        await ctx.send(get_translation(ctx, "server_not_found", settings))
    
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

@bot.command()
async def clone_server_to_blank_server(ctx, servidor_destino_id: int):
    servidor_origen = str(ctx.guild.id)
    servidor_destino = bot.get_guild(servidor_destino_id)

    if not servidor_origen or not servidor_destino:
        await ctx.send(get_translation(ctx, "server_id_not_found", settings))
        return

    for role in servidor_origen.roles:
        if role.name != "@everyone":
            await servidor_destino.create_role(
                name=role.name,
                permissions=role.permissions,
                colour=role.colour,
                hoist=role.hoist,
                mentionable=role.mentionable
            )

    for category in servidor_origen.categories:
        new_category = await servidor_destino.create_category(category.name)
        for channel in category.channels:
            if isinstance(channel, discord.TextChannel):
                await new_category.create_text_channel(name=channel.name, topic=channel.topic, nsfw=channel.nsfw)
            elif isinstance(channel, discord.VoiceChannel):
                await new_category.create_voice_channel(name=channel.name, bitrate=channel.bitrate, user_limit=channel.user_limit)

    await ctx.send(f'{get_translation(ctx, "server_clone", settings)}{servidor_origen.name}{get_translation(ctx, "in", settings)}{servidor_destino.name}.')
    
@bot.command()
async def server_info(ctx):
    guild = ctx.guild
    info = f'**{get_translation(ctx, "server", settings)}:** {guild.name}\n\n'
    
    for category in guild.categories:
        info += f'**{get_translation(ctx, "category", settings)}:** {category.name}\n'
        for channel in category.channels:
            info += f'  - {channel.name} ({str(channel.type).split(".")[-1]})\n'
            
    info += f'\n**{get_translation(ctx, "roles", settings)}:**\n'
    for role in guild.roles:
        if role.name != "@everyone":
            info += f"- {role.name}\n"
    
    def split_message(message, max_length=2000):
        return [message[i:i+max_length] for i in range(0, len(message), max_length)]

    parts = split_message(info)
    for part in parts:
        await ctx.send(part)  

@bot.command()
async def create_template_guide(ctx):
    instructions = (
        f"{get_translation(ctx, 'template_msg_1', settings)}"
        f"{get_translation(ctx, 'template_msg_2', settings)}"
        f"{get_translation(ctx, 'template_msg_3', settings)}"
        f"{get_translation(ctx, 'template_msg_4', settings)}"
        f"{get_translation(ctx, 'template_msg_5', settings)}"
        f"{get_translation(ctx, 'template_msg_6', settings)}"
        f"{get_translation(ctx, 'template_msg_7', settings)}"
        f"{get_translation(ctx, 'template_msg_8', settings)}"
        f"{get_translation(ctx, 'template_msg_9', settings)}"
    )
    await ctx.send(instructions)

@bot.command()
@commands.has_permissions(administrator=True)
async def set_bot_language(ctx, language_code: str):
    set_language(ctx, language_code, settings) 
    await ctx.send(f"{get_translation(ctx,'translation_to', settings)}{language_code}")

@bot.command()
async def custom_help(ctx):
    help_text = f"""
    **{get_translation(ctx,'translation_to', settings)}**
    
    - {get_translation(ctx,'export_msg_text', settings)}
    - {get_translation(ctx,'full_backup_text', settings)}
    - {get_translation(ctx,'server_info_text', settings)}
    - {get_translation(ctx,'set_bot_language_text', settings)}
    - {get_translation(ctx,'create_template_guide_text', settings)}
    """
    await ctx.send(help_text)
    
@bot.command()
async def excel_asistencia(ctx, channel_id, event, rol_name = None):
    guild = ctx.guild
    channel = await bot.fetch_channel(channel_id)
    if not rol_name:
        rol_applicant_id = 1068070310148046878
        rol_member_id = 980418204901965834
        rol_applicant = discord.utils.get(guild.roles, id=rol_applicant_id)
        rol_member = discord.utils.get(guild.roles, id=rol_member_id)
        rol_applicant_list = [member for member in guild.members if rol_applicant in member.roles]
        rol_member_list = [member for member in guild.members if rol_member in member.roles]
        
        members_with_rol = rol_applicant_list + rol_member_list
    else:
        rol = discord.utils.get(guild.roles, name=rol_name)
        members_with_rol = [member for member in guild.members if rol in member.roles]

    message = await channel.fetch_message(event)
    embeds = message.embeds

    if not embeds or len(embeds[0].fields) < 3:
        await ctx.send("El mensaje no tiene la estructura esperada.")
        return

    yes_election_list = embeds[0].fields[1].value
    no_election_list = embeds[0].fields[2].value

    yes_election_list = yes_election_list[4:].replace('<@', '').replace('>', '').split('\n')
    no_election_list = no_election_list[4:].replace('<@', '').replace('>', '').split('\n')

    yes_election_member = [member.display_name for member in members_with_rol if str(member.id) in yes_election_list]
    no_election_member = [member.display_name for member in members_with_rol if str(member.id) in no_election_list]
    no_chose_election = [member.display_name for member in members_with_rol if str(member.id) not in yes_election_list and str(member.id) not in no_election_list]

    max_length = max(len(yes_election_member), len(no_election_member), len(no_chose_election))

    yes_election_member += [None] * (max_length - len(yes_election_member))
    no_election_member += [None] * (max_length - len(no_election_member))
    no_chose_election += [None] * (max_length - len(no_chose_election))

    df_combined = pd.DataFrame({
        'Apuntados sí': yes_election_member,
        'Apuntados no': no_election_member,
        'No apuntados': no_chose_election
    })

    excel_file = 'asistencias.xlsx'
    df_combined.to_excel(excel_file, sheet_name='Asistencia', index=False)
    
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active

    column_widths = {
        'A': 30,
        'B': 30,
        'C': 30
    }

    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    wb.save(excel_file)
    wb.close()

    await ctx.send(file=discord.File(excel_file))

    os.remove(excel_file)
    
bot.run(TOKEN)