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

@Bot.command()
async def clears(ctx, amount=5):
	await.ctx.channel.purge(limit=amount)

#kick
@Bot.command( pass_context = True )
@commands.has_any_role("kicker" )
async def  kick(ctx, member: discord.Member, *, reason = None):
	await ctx.channel.purge(limit = 1)#СТИРАЕМ СООБЩЕНИЕ С КОММАНДОЙ .kcik

	await member.kick(reason = reason)
	await ctx.send(f"юзер {member.mention} кикнут за плохое поведение")

#ban
@Bot.command( pass_context = True)
@commands.has_any_role("kicker" )
async def banan(ctx, member: discord.Member, *, reason = None):
    emb = discord.Embed(title = '{}  в {}'.format(today, vrem), color = discord.Color.red())
    await ctx.channel.purge(limit = 1)#удаляем сообщение с этой командой из чата

    emb.set_author(name = member.name, icon_url = member.avatar_url)#Показываем имя и аватар забаненого пользователя
    emb.add_field(name = 'Ban user', value = 'Юзер {}'.format(member) + ' забанен по причине "{}" '.format(reason))
    emb.set_footer(text ="Был забанен администратором {} 'ом".format(ctx.author.name) , icon_url = ctx.author.avatar_url)

    await ctx.send(embed = emb)
    await member.ban(reason = reason)

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
