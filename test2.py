#UPD 03.05.2020: Добавлена функция выдачи роли, повикшены недочеты, обновлено меню !help. Добавлены emb в команды: !mute, !unmute, !kick. Команда !banan переименована в !ban.
#UPD 03.05.2020(2): Приветствие пользвоателя при входе не сервере. Комада !giverole and !removerole добавлены(использовать могут только с ролью).
#UPD 04.05.2020: Обновлено приветствие. Добавлено сообщение при выходе с сервера. Если выйти с серва с ролью mute = бан.
#UPD 05.05.2020: Обновлено меню !help
#UPD 16.05.2020: Добавлена система рангов.(beta)
import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import os
import json

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
EXROLE = 705126936539693058

YOURGUILDSID = 705126936539693058
YOURID = 302315861916516354
YOURFILENAME = "xp.json" # with .json (or txt, etc. at the and)

# it may throw an error when a member joins when the bot isn't running

m = {}

@Bot.event
async def on_ready():
    global m
    with open(YOURFILENAME, "r") as j:
        m = json.load(j)
        j.close()
    if len(m) == 0:
        m = {}
        for member in Bot.get_guild(YOURGUILDSID).members:
            m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0}
    print("ready")
    while True:
        try:
            for member in Bot.get_guild(YOURGUILDSID).members:
                m[str(member.id)]["messageCountdown"] -= 1
        except:
            pass
        await asyncio.sleep(1)


@Bot.event
async def on_message( message ):
    await Bot.process_commands( message )
    global m
    if message.content == "-stop" and message.author.id == YOURID:
        with open(YOURFILENAME, "w") as j:
            j.write( json.dumps(m) )
            j.close()
        await Bot.close()
    elif message.content == "rank":
        if m[str(message.author.id)]["xp"] <= 100:
            await message.channel.send('Твой ранг: нуб👶' + '\n' ' XP = ' + str(m[str(message.author.id)]["xp"]))
    elif message.content == "list":
        for member in Bot.get_guild(YOURGUILDSID).members:
            if m[str(member.id)]["xp"] > 0:
                await message.channel.send(str(m[str(member.id)]["xp"]) + ' ' + str(member.mention))        
    elif message.author != Bot.user:
        if m[str(message.author.id)]["messageCountdown"] <= 0:
            m[str(message.author.id)]["xp"] += 10
            m[str(message.author.id)]["messageCountdown"] = 10


@Bot.event
async def on_member_join(member):
	m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0}
	for channel in member.guild.channels:
		if str(channel) == "flood":
			await channel.send(f"""К нам присоединился {member.mention}""")

#leave
@Bot.event
async def on_member_remove(member):
	for channel in member.guild.channels:
		if str(channel) == "flood":
			await channel.send(f"""Нас покинул {member.mention}""")
	roli = member.roles #Список ролей КОНКРЕТНОГО юзера
	for rol in roli:
		if rol.id == EXROLE: #ЕСЛИ РОЛЬ = EVERYONE =>
			continue #ПРОПУСКАЕМ(СЛЕДУЮЩАЯ ИТЕРАЦИЯ)
		else:
			if str(rol.id) == '706195044498931783':
				await member.ban(reason = 'ОБХОД МУТА')
			
#Help
@Bot.command()
@commands.has_any_role("kicker" )
async def help ( ctx ):
	await ctx.channel.purge(limit = 1)

	emb = discord.Embed( title = 'Навигация по командам')

	emb.add_field( name = '{}clear'.format(PREFIX), value='очистка чата')
	emb.add_field( name = '{}ban @name reason'.format(PREFIX), value='Ограничение доступа к серверу. ')
	emb.add_field( name = '{}unban name#xxxx'.format(PREFIX), value='Удаление ограничения доступа к серверу.')
	emb.add_field( name = '{}mute @name time reason'.format(PREFIX), value='Запретить писать в чат.')
	emb.add_field( name = '{}unmute @name'.format(PREFIX), value='Разрешить писать в чат.')
	emb.add_field( name = '{}kick @name'.format(PREFIX), value='Удаление участника с сервера.')
	emb.add_field( name = '{}role rolename'.format(PREFIX), value='Получить роль.')
	emb.add_field( name = '{}help'.format(PREFIX), value='Показать это сообщение.')
	emb.add_field( name = '{}giverole/removerole @name role'.format(PREFIX), value='Снять/выдать роль')

	await ctx.send(embed = emb)

#kick
@Bot.command( pass_context = True )
@commands.has_any_role("kicker" )
async def  kick(ctx, member: discord.Member, *, reason = None):
	await ctx.channel.purge(limit = 1)#СТИРАЕМ СООБЩЕНИЕ С КОММАНДОЙ .kcik
	emb = discord.Embed(title = '{}  в {}'.format(today, vrem), color = discord.Color.red())
	emb.set_author(name = member.name, icon_url = member.avatar_url)
	emb.add_field(name = 'Kick user', value = 'Юзер {}'.format(member) + ' кикнут по причине "{}" '.format(reason))
	emb.set_footer(text ="Был кикнут администратором {} 'ом".format(ctx.author.name) , icon_url = ctx.author.avatar_url)
	await ctx.send(embed = emb)
	await member.kick(reason = reason)

#ban
@Bot.command( pass_context = True)
@commands.has_any_role("kicker" )
async def ban(ctx, member: discord.Member, *, reason = None):
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


#clear
@Bot.command()
@commands.has_any_role("kicker" )
async def test(ctx):

	await ctx.send(str("""```md\n#Пивет```"""))


#clear
@Bot.command()
@commands.has_any_role("kicker" )
async def clear(ctx, amount = 100):
	await ctx.channel.purge(limit = amount)
	emb = discord.Embed(title = 'Чат очищен администрацией.')
	await ctx.send(embed = emb)


#unmute
@Bot.command()
@commands.has_any_role("kicker" )
async def unmute(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute')
	emb = discord.Embed(title = '{}  в {}'.format(today, vrem), color = discord.Color.green())
	emb.set_author(name = member.name, icon_url = member.avatar_url)
	emb.add_field(name = 'Unmute user', value = 'Юзеру {}'.format(member) + ' снят мут.')
	emb.set_footer(text ="Мут снят администратором {} 'ом".format(ctx.author.name) , icon_url = ctx.author.avatar_url)
	await ctx.send(embed = emb)
	await member.remove_roles( mute_role )


#mute
@Bot.command()
@commands.has_any_role("kicker" )
async def mute(ctx,  member: discord.Member, time: int, reason = None):
	await ctx.channel.purge(limit = 1)
	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute')
	await member.add_roles( mute_role )
	

	if time > 0:
		emb = discord.Embed(title = '{}  в {}'.format(today, vrem), color = discord.Color.red())
		emb.set_author(name = member.name, icon_url = member.avatar_url)
		emb.add_field(name = 'Mute user', value = 'Юзеру {}'.format(member) + ' выдан мут на {} минут.'.format(time) + 'Причина: "{}"'.format(reason))
		emb.set_footer(text ="Мут выдан администратором {} 'ом".format(ctx.author.name) , icon_url = ctx.author.avatar_url)
		await ctx.send(embed = emb)
		await asyncio.sleep(time * 60)
		await member.remove_roles( mute_role )
		await ctx.send(f'y { member.mention } снят мут, больше не нарушай!')




#role
@Bot.command()
async def role(ctx, role: str ):
	member = ctx.message.author
	roli = member.roles #Список ролей КОНКРЕТНОГО юзера
	role = discord.utils.get( ctx.message.guild.roles, name = role)
	k = 0
	for rol in roli:
		if rol.id == EXROLE: #ЕСЛИ РОЛЬ = EVERYONE =>
			k = k+1
			continue #ПРОПУСКАЕМ(СЛЕДУЮЩАЯ ИТЕРАЦИЯ)
		else:
			k = k+1
	if k < 3:
		if str(role) != "Atlant RP" and str(role) != "Гл.Модератор" and str(role) != "kicker" and str(role) != "Модератор" and str(role) != "Администрация" and str(role) != "Следящий за госс" and str(role) != "Следящий за мафиями" and str(role) != "Следящий за бизами" and str(role) != "Следящий за гетто" and str(role) != "Supports" and str(role) != "Лидеры":
			await member.add_roles( role )
			await ctx.send(f"""  { member.mention } ```fix\n получил роль { role }!\n``` """)
		else:
			await ctx.send(str( f""" { member.mention } ```xl\n'Данную роль получить нельзя!'```"""))

	else:
		await ctx.send(str("""```xl\n'У вас слишком много ролей!'\n```"""))

#giverole
@Bot.command()
@commands.has_any_role("kicker" )
async def giverole(ctx, member: discord.Member, role: str ):
	await ctx.channel.purge(limit = 1)
	role = discord.utils.get( ctx.message.guild.roles, name = role)
	await member.add_roles( role )
	await ctx.send(f"""  { member.mention } ```fix\n получил роль { role }!\n``` """)

#removerole
@Bot.command()
@commands.has_any_role("kicker" )
async def removerole(ctx, member: discord.Member, role: str ):
	await ctx.channel.purge(limit = 1)
	role = discord.utils.get( ctx.message.guild.roles, name = role)
	await member.remove_roles( role )
	await ctx.send(f"""  { member.mention } ```diff\n -лишился  { role }!\n``` """)

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
