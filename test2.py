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

PREFIX = '!'

Bot = commands.Bot(command_prefix = '!')

Bot.remove_command ('help')
ploxie_slova = ['мать ебал', 'м']#список запрещенных слов.


#ready
@Bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(Bot))

#Help
@Bot.command()
@commands.has_any_role("kicker" )
async def help ( ctx ):
	await ctx.channel.purge(limit = 1)

	emb = discord.Embed( title = 'Навигация по командам')

	emb.add_field( name = '{}clear'.format(PREFIX), value='очистка чата')
	emb.add_field( name = '{}ban @name'.format(PREFIX), value='Ограничение доступа к серверу. ')
	emb.add_field( name = '{}unban'.format(PREFIX), value='Удаление ограничения доступа к серверу.')
	emb.add_field( name = '{}mute time @name'.format(PREFIX), value='Запретить писать в чат.')
	emb.add_field( name = '{}unmute @name'.format(PREFIX), value='Разрешить писать в чат.')
	emb.add_field( name = '{}kick @name'.format(PREFIX), value='Удаление участника с сервера.')
	emb.add_field( name = '_', value='_')
	emb.add_field( name = '{}help'.format(PREFIX), value='Показать это сообщение.')
	emb.add_field( name = '_', value='_')

	await ctx.send(embed = emb)

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
    await member.send( 'You banned from server' )
    await member.ban(reason = reason)


#unban
@Bot.command(pass_context = True)
@commands.has_any_role("kicker" )
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.mention}')
			return

#filter
@Bot.event
async def on_message( message ):
	await Bot.process_commands( message )

	msg = message.content.lower()

	if msg in ploxie_slova:
		await message.delete()


#clear
@Bot.command()
@commands.has_any_role("kicker" )
async def clear(ctx, amount = 100):
	await ctx.channel.purge(limit = amount)

#mute
@Bot.command()
@commands.has_any_role("kicker" )
async def mute(ctx, time: int, member: discord.Member):
	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute')
	await member.add_roles( mute_role )
	await member.add_roles( mute_role )
	

	if time > 0:
		await ctx.send(f'y { member.mention } ограничение чата, за нарушение правил! На {time} минут!')
		await asyncio.sleep(time * 60)
		await member.remove_roles( mute_role )
		await ctx.send(f'y { member.mention } снят мут, больше не нарушай!')



#unmute
@Bot.command()
@commands.has_any_role("kicker" )
async def unmute(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute')

	await member.remove_roles( mute_role )
	await ctx.send(f'y { member.mention } снят мут, больше не нарушай!')

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
