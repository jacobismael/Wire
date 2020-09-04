# bot.py
import os

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('>help'))
    print("Wire is active")

@bot.command(name="clr", help='cleares the specified messages')
@commands.has_role('admin')
async def clr(ctx, amount=5):
    if(amount == -1):
        amount = 1000000000
    await ctx.channel.purge(limit=amount+1)

bot.remove_command("help")
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Wire Commands", description="List of Wire commands", color=0xffff00)
    embed.set_thumbnail(url='https://icons.iconarchive.com/icons/xenatt/the-circle/512/App-Terminal-icon.png')
    embed.set_author(name="Wire", icon_url='https://icons.iconarchive.com/icons/xenatt/the-circle/512/App-Terminal-icon.png')
    embed.add_field(name="Admin Commands", value=" - `mkdir`\tcreates a new channel\n - `rmdir`\tdeletes the channel you are currently in\n - `clear`\tclears a specified amount of messages", inline=False)
    embed.add_field(name="General Commands", value=" - `help`\tShows this message\n - `ls`\tlists the members of the server\n - `info`\tshows about info", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='cc', help='creates a new channel')
@commands.has_role('admin')
async def rc(ctx, channel_name='new-channel'):
    server = ctx.message.guild
    existing_channel = discord.utils.get(server.channels, name=channel_name)
    if not existing_channel:
        await ctx.send("```Created new channel \"{}\"```".format(channel_name))
        await server.create_text_channel(channel_name)
    else:
        await ctx.send("```Error: Channel with same name already exists```")

@bot.command(name="rc", help='deletes the current channel you are in')
@commands.has_role('admin')
async def rc(ctx):
    await ctx.channel.delete()

@bot.command(name='kick')
@commands.has_role('admin')
async def kick(ctx, member : discord.Member, reason=None):
    await member.kick(reason=reason)
    ctx.send("Kicked " + member)

@bot.command(name='ban')
@commands.has_role('admin')
async def ban(ctx, member : discord.Member, reason=None):
    await member.ban(reason=reason)
    ctx.send("Banned " + member)
        

# Peasant Commands

@bot.command(help="lists the members of the server")
async def ls(ctx):
    guild = ctx.guild
    members = '\n - '.join([member.name for member in guild.members])
    message = '- ' + members
    await ctx.send("```list of members on the {} server: \n {}```".format(guild.name, message))

@bot.command(help='display about info')
async def info(ctx):
    embed = discord.Embed(title="About Wire", description="Wire is a discord bot created by [Jacob Ismael](https://github.com/jacobismael)", color=0xffff00)
    embed.set_thumbnail(url='https://avatars1.githubusercontent.com/u/48426248?s=460&u=82650bc8f2dcb28c15f168c14d06833089720afa&v=4')
    embed.set_author(name="Wire", icon_url='https://icons.iconarchive.com/icons/xenatt/the-circle/512/App-Terminal-icon.png')

    embed.set_footer(text='Wire v1.0')
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('```Error: You do not have the correct role for this command.```')


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)