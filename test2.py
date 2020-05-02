import discord
from discord.ext import commands
from datetime import datetime
import os
today = datetime.now().date()
tm = datetime.now()
vrem = "   {}:{}".format(tm.hour, tm.minute)
today = datetime.now().date()
tm = datetime.now()
vrem = "   {}:{}".format(tm.hour, tm.minute)


Bot = commands.Bot(command_prefix = '!')


ploxie_slova = []


#ready
@Bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(Bot))

@Bot.event
async def on_message(msg):
    if msg.content == "qwe":
        await msg.delete()


@Bot.command()
async def kick(ctx, member: discord.Member, *, reason =None):
  await member.kick(reason = reason)
  await ctx.send(f"юзер {member.mention} кикнут за плохое поведение")
    await ctx.send(embed = emb)
    await member.ban(reason = reason)

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
