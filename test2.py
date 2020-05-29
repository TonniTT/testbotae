#UPD 03.05.2020: Добавлена функция выдачи роли, повикшены недочеты, обновлено меню !help. Добавлены emb в команды: !mute, !unmute, !kick. Команда !banan переименована в !ban.
#UPD 03.05.2020(2): Приветствие пользвоателя при входе не сервере. Комада !giverole and !removerole добавлены(использовать могут только с ролью).
#UPD 04.05.2020: Обновлено приветствие. Добавлено сообщение при выходе с сервера. Если выйти с серва с ролью mute = бан.
#UPD 05.05.2020: Обновлено меню !help
#UPD 16.05.2020: Добавлена система рангов.(beta)
#UPD 29.05.2020: Добавлены игры.
import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import os
import json
import random

today = datetime.now().date()
tm = datetime.now()
vrem = "   {}:{}".format(tm.hour, tm.minute)
today = datetime.now().date()
tm = datetime.now()
vrem = "   {}:{}".format(tm.hour, tm.minute)
PREFIX = '!'
Bot = commands.Bot(command_prefix = '!')
Bot.remove_command ('help')
#список запрещенных слов.
EXROLE = 714531560459599903

YOURGUILDSID = 714531560459599903
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
            m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0, "money" : 0, "days" : 0, "car" : 0, "house" : 0, "phone" : 0}
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
        if m[str(message.author.id)]["xp"] <= 610:
            await message.channel.send('Твой ранг: Новичок.' + '\n' ' XP = ' + str(m[str(message.author.id)]["xp"]))
        elif  m[str(message.author.id)]["xp"] <= 1400:
        	await message.channel.send('Твой ранг: Страж.' + '\n' ' XP = ' + str(m[str(message.author.id)]["xp"]))
        elif  m[str(message.author.id)]["xp"] <= 2150:
        	await message.channel.send('Твой ранг: Рыцарь.' + '\n' ' XP = ' + str(m[str(message.author.id)]["xp"]))
        elif  m[str(message.author.id)]["xp"] <= 2930:
        	await message.channel.send('Твой ранг: Герой.' + '\n' ' XP = ' + str(m[str(message.author.id)]["xp"]))
        elif  m[str(message.author.id)]["xp"] <= 3700:
        	await message.channel.send('Твой ранг: Легенда.' + '\n' ' XP = ' + str(m[str(message.author.id)]["xp"]))
        elif  m[str(message.author.id)]["xp"] <= 4460:
        	await message.channel.send('Твой ранг: Властелин.' + '\n' ' XP = ' + str(m[str(message.author.id)]["xp"]))
        elif  m[str(message.author.id)]["xp"] <= 5420:
        	await message.channel.send('Твой ранг: Божество.' + '\n' ' XP = ' + str(m[str(message.author.id)]["xp"]))
        elif  m[str(message.author.id)]["xp"] <= 5421:
        	await message.channel.send('Твой ранг: Чёрт.' + '\n' ' XP = ' + str(m[str(message.author.id)]["xp"]))
    elif message.content == "list":
        for member in Bot.get_guild(YOURGUILDSID).members:
            if m[str(member.id)]["xp"] > 0:
                await message.channel.send(str(m[str(member.id)]["xp"]) + ' ' + str(member.mention))        
    elif message.author != Bot.user:
        if m[str(message.author.id)]["messageCountdown"] <= 0:
            m[str(message.author.id)]["xp"] += 5
            m[str(message.author.id)]["messageCountdown"] = 15

@Bot.event
async def on_member_join(member):
	m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0}
	for channel in member.guild.channels:
		if str(channel) == "chat":
			await channel.send(f"""К нам присоединился {member.mention}""")

#leave
@Bot.event
async def on_member_remove(member):
	for channel in member.guild.channels:
		if str(channel) == "chat":
			await channel.send(f"""Нас покинул {member.mention}""")
	roli = member.roles #Список ролей КОНКРЕТНОГО юзера
	for rol in roli:
		if rol.id == EXROLE: #ЕСЛИ РОЛЬ = EVERYONE =>
			continue #ПРОПУСКАЕМ(СЛЕДУЮЩАЯ ИТЕРАЦИЯ)
		else:
			if str(rol.id) == '714775091178766336':
				await member.ban(reason = 'ОБХОД МУТА')
			
#Help
@Bot.command()
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
	emb.add_field( name = '{}работать'.format(PREFIX), value='Начать работать.')
	emb.add_field( name = '{}казино summa'.format(PREFIX), value='Игра в казино.')
	emb.add_field( name = '{}стакан 1-3 сумма'.format(PREFIX), value='Игра в стаканчики.')
	emb.add_field( name = '{}курс вверх/вниз сумма'.format(PREFIX), value='Угадать курс.')

	await ctx.send(embed = emb)

#game1
@Bot.command( pass_context = True )
async def казино(ctx,  *, stavka: int):
	member = ctx.message.author
	global m
	if int(stavka) < m[str(ctx.message.author.id)]["money"]:
		kazino = random.randint(1, 2)
		coefficient = random.randint(1, 15)
		if kazino == 1:
			if coefficient == 1 or coefficient == 3 or coefficient == 5 or coefficient == 7 or coefficient == 9 or coefficient == 11 or coefficient == 15:
				await ctx.message.channel.send(f'{member.mention}, Вы выйграли:' + str(stavka*2) + '$' +'!')
				m[str(ctx.message.author.id)]["money"] += stavka*2
			elif coefficient == 2 or coefficient == 4 or coefficient == 6 or coefficient == 8 or coefficient == 10 or coefficient == 12 or coefficient == 14:
				await ctx.message.channel.send(f'{ member.mention }, Вы выйграли:' + str(stavka*3) + '$' +'!')
				m[str(ctx.message.author.id)]["money"] += stavka*3
			elif coefficient == 13:
				await ctx.message.channel.send(f'{ member.mention }, Вы выйграли:' + str(stavka*7) + '$' +'!')
				m[str(ctx.message.author.id)]["money"] += stavka*7
		elif kazino == 2:
			await ctx.message.channel.send(f'{ member.mention }, Вы проиграли ' + str(stavka) + '$' + '!')
			m[str(ctx.message.author.id)]["money"] -= stavka 

	else:
		await ctx.message.channel.send(f'{member.mention}, недостаточно денег.')
#game2
@Bot.command( pass_context = True )
async def стакан(ctx, stakan: int, summa: int):
	member = ctx.message.author
	global m
	truestakan = random.randint(1, 3)
	caf = random.choice([2,2.01,2.02,2.03,2.04,2.05,2.06,2.07,2.08,2.09,2.1])
	if int(truestakan) == int(stakan):
		await ctx.message.channel.send(f'{member.mention}, Вы угадали. Приз: ' + str(summa*caf) + "$!" )
		m[str(ctx.message.author.id)]["money"] += summa*caf
	else:
		await ctx.message.channel.send(f'{member.mention}, Вы не угадали. Это был ' + str(truestakan) + "-й стакан." )
		m[str(ctx.message.author.id)]["money"] -= summa

#game3
@Bot.command( pass_context = True )
async def курс(ctx, updown: str, summa: int):
	member = ctx.message.author
	global m
	updowns = random.choice(['вверх', 'вниз'])
	caf = random.choice([2,2.01,2.02,2.03,2.04,2.05,2.06,2.07,2.08,2.09,2.1])
	if str(updowns) == str(updown):
		await ctx.message.channel.send(f'{member.mention}, Вы угадали. \n✅Заработано: ' + str(summa*caf) + "$!" )
		m[str(ctx.message.author.id)]["money"] += summa*caf
	else:
		if updowns == 'вниз':
			await ctx.message.channel.send(f'{member.mention}, Вы не угадали.\n Курс подешевел.' + '\n ❌Потеряно: ' + str(summa) + '$' )
		elif updowns == 'вверх':
			await ctx.message.channel.send(f'{member.mention}, Вы не угадали. \nКурс подорожал' + '\n ❌Потеряно: ' + str(summa) + '$')
		m[str(ctx.message.author.id)]["money"] -= summa

#work
@Bot.command( pass_context = True )
async def работать(ctx, ):
	global m
	member = ctx.message.author
	if m[str(ctx.message.author.id)]["days"] >= 5:
		await ctx.message.channel.send(f'{member.mention},  рабочая неделя завершена. \n ⏳ Вы сможете работать через час')
		await asyncio.sleep(25)
		await ctx.message.channel.send(f'{member.mention},  Можете снова работать!')
		m[str(ctx.message.author.id)]["days"] -= 5

	else:
		await ctx.message.channel.send(f'{member.mention}, рабочий день окончен. \n 💵 Вы заработали 500$.')
		m[str(ctx.message.author.id)]["money"] += 500
		m[str(ctx.message.author.id)]["days"] += 1
#shop
@Bot.command( pass_context = True )
async def магазин(ctx, ):
	await ctx.message.channel.send(f"🚗Автомобили: \n=============================\n🔸(ID: 1) Renault Logan - 500.000₽ \n 🔸(ID: 2) MAZDA MX-6 - 150.000₽\n 🔸(ID: 3) ВАЗ (Lada) 2131 - 200.000₽\n 🔸(ID: 4) Skoda Rapid - 1.000.000₽\n=============================\n ❓ Для покупки введите «!авто [ID]»")
	await ctx.message.channel.send("🏠Дома: \n=============================\n🔸(ID: 1) Домик в деревне - 600.000₽\n 🔸(ID: 2) Коттедж - 2.000.000₽\n 🔸(ID: 3) Дом на берегу моря - 10.000.000₽\n 🔸(ID: 4) Кремль - 21.000.000₽\n=============================\n ❓ Для покупки введите «!дом [ID]»")
	await ctx.message.channel.send("📱Телефоны: \n=============================\n🔸(ID: 1) NOKIA 3310 - 3000₽\n 🔸(ID: 2) Samsung Galaxy J5 - 20.000₽\n 🔸(ID: 3) MEIZU M6 - 30.000₽\n 🔸(ID: 4) IPHONE XS MAX - 100.000₽\n=============================\n ❓ Для покупки введите «!телефон [ID]»")

@Bot.command( pass_context = True )
async def авто(ctx, automobile: int):
	global m
	member = ctx.message.author
	if automobile == 1:
		if m[str(ctx.message.author.id)]["money"] >= 500000:
			m[str(ctx.message.author.id)]["car"] = 1
			m[str(ctx.message.author.id)]["money"] -= 500000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'Renault Logan' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")

	elif automobile == 2:
		if m[str(ctx.message.author.id)]["money"] >= 150000:
			m[str(ctx.message.author.id)]["car"] = 2
			m[str(ctx.message.author.id)]["money"] -= 150000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'MAZDA MX-6' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")
	elif automobile == 3:
		if m[str(ctx.message.author.id)]["money"] >= 200000:
			m[str(ctx.message.author.id)]["car"] = 3
			m[str(ctx.message.author.id)]["money"] -= 200000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'ВАЗ (Lada) 2131' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")
	elif automobile == 4:
		if m[str(ctx.message.author.id)]["money"] >= 1000000:
			m[str(ctx.message.author.id)]["car"] = 4
			m[str(ctx.message.author.id)]["money"] -= 1000000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'Skoda Rapid' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")

@Bot.command( pass_context = True )
async def дом(ctx, home: int):
	global m
	member = ctx.message.author
	if home == 1:
		if m[str(ctx.message.author.id)]["money"] >= 600000:
			m[str(ctx.message.author.id)]["house"] = 1
			m[str(ctx.message.author.id)]["money"] -= 600000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'Домик в деревне' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")

	elif home == 2:
		if m[str(ctx.message.author.id)]["money"] >= 2000000:
			m[str(ctx.message.author.id)]["house"] = 2
			m[str(ctx.message.author.id)]["money"] -= 2000000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'Коттедж' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")
	elif home == 3:
		if m[str(ctx.message.author.id)]["money"] >= 10000000:
			m[str(ctx.message.author.id)]["house"] = 3
			m[str(ctx.message.author.id)]["money"] -= 10000000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'Дом на берегу моря' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")
	elif home == 4:
		if m[str(ctx.message.author.id)]["money"] >= 21000000:
			m[str(ctx.message.author.id)]["house"] = 4
			m[str(ctx.message.author.id)]["money"] -= 21000000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'Кремль' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")

@Bot.command( pass_context = True )
async def телефон(ctx, phones: int):
	global m
	member = ctx.message.author
	if phones == 1:
		if m[str(ctx.message.author.id)]["money"] >= 3000:
			m[str(ctx.message.author.id)]["phone"] = 1
			m[str(ctx.message.author.id)]["money"] -= 3000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'NOKIA 3310' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")

	elif phones == 2:
		if m[str(ctx.message.author.id)]["money"] >= 20000:
			m[str(ctx.message.author.id)]["phone"] = 2
			m[str(ctx.message.author.id)]["money"] -= 20000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'Samsung Galaxy J5' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")
	elif phones == 3:
		if m[str(ctx.message.author.id)]["money"] >= 30000:
			m[str(ctx.message.author.id)]["phone"] = 3
			m[str(ctx.message.author.id)]["money"] -= 30000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'MEIZU M6' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")
	elif phones == 4:
		if m[str(ctx.message.author.id)]["money"] >= 100000:
			m[str(ctx.message.author.id)]["phone"] = 4
			m[str(ctx.message.author.id)]["money"] -= 100000
			await ctx.message.channel.send(f"{member.mention}, Вы купили 'IPHONE XS MAX' ")
		else:
			await ctx.message.channel.send(f"{member.mention}, недостаточно средств.")

@Bot.command( pass_context = True )
async def профиль(ctx, ):
    global m
    one = None
    two = None
    three = None
    member = ctx.message.author
    if m[str(ctx.message.author.id)]["car"] == 1:
    	one = 'Renault Logan'
    elif m[str(ctx.message.author.id)]["car"] == 2:
    	one = 'MAZDA MX-6'
    elif m[str(ctx.message.author.id)]["car"] == 3:
    	one = 'ВАЗ (Lada) 2131'
    elif m[str(ctx.message.author.id)]["car"] == 4:
    	one = 'Skoda Rapid'
    if m[str(ctx.message.author.id)]["house"] == 1:
    	two = 'Домик в деревне'
    elif m[str(ctx.message.author.id)]["house"] == 2:
    	two = 'Коттедж'
    elif m[str(ctx.message.author.id)]["house"] == 3:
    	two = 'Дом на берегу моря'
    elif m[str(ctx.message.author.id)]["house"] == 4:
    	two = 'Кремль'
    if m[str(ctx.message.author.id)]["phone"] == 1:
    	three = 'NOKIA 3310'
    elif m[str(ctx.message.author.id)]["phone"] == 2:
    	three = 'Samsung Galaxy J5'
    elif m[str(ctx.message.author.id)]["phone"] == 3:
    	three = 'MEIZU M6'
    elif m[str(ctx.message.author.id)]["phone"] == 4:
    	three = 'IPHONE XS MAX'
    emb = discord.Embed(title = 'Профиль', color = discord.Color.blue())
    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field(name = '💰 Баланс:', value = str(m[str(ctx.message.author.id)]["money"]) + '$')
    emb.add_field(name = '🚘Авто', value = str(one) )
    emb.add_field(name = '🏠Дом', value = str(two) )
    emb.add_field(name = '📱Телефон', value = str(three))
    await ctx.message.channel.send(embed = emb)

@Bot.command( pass_context = True )
@commands.has_any_role("Техник" )
async def деньги(ctx, member: discord.Member, mani: int ):
	m[str(member.id)]["money"] += int(mani)
	await ctx.message.channel.send('Бабло зачислено')



#kick
@Bot.command( pass_context = True )
@commands.has_any_role("Приблатнённый","Блатная" )
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
@commands.has_any_role("Приблатнённый","Блатная" )
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
@commands.has_any_role("Приблатнённый","Блатная" )
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
#@Bot.command()
#@commands.has_any_role("Приблатнённый","Блатная" )
#async def test(ctx):

#	await ctx.send(str("""```md\n#Пивет```"""))


#clear
@Bot.command()
@commands.has_any_role("Приблатнённый","Блатная")
async def clear(ctx, amount = 100):
	await ctx.channel.purge(limit = amount)
	emb = discord.Embed(title = 'Чат очищен администрацией.')
	await ctx.send(embed = emb)


#unmute
@Bot.command()
@commands.has_any_role("Приблатнённый","Блатная" )
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
@commands.has_any_role("Приблатнённый","Блатная" )
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
		if str(role) != "Кент" and str(role) != "Приблатнённый" and str(role) != "Блатная":
			await member.add_roles( role )
			await ctx.send(f"""  { member.mention } ```fix\n получил роль { role }!\n``` """)
		else:
			await ctx.send(str( f""" { member.mention } ```xl\n'Данную роль получить нельзя!'```"""))

	else:
		await ctx.send(str("""```xl\n'У вас слишком много ролей!'\n```"""))

#giverole
@Bot.command()
@commands.has_any_role("Приблатнённый","Блатная" )
async def giverole(ctx, member: discord.Member, role: str ):
	await ctx.channel.purge(limit = 1)
	role = discord.utils.get( ctx.message.guild.roles, name = role)
	await member.add_roles( role )
	await ctx.send(f"""  { member.mention } ```fix\n получил роль { role }!\n``` """)

#removerole
@Bot.command()
@commands.has_any_role("Приблатнённый","Блатная" )
async def removerole(ctx, member: discord.Member, role: str ):
	await ctx.channel.purge(limit = 1)
	role = discord.utils.get( ctx.message.guild.roles, name = role)
	await member.remove_roles( role )
	await ctx.send(f"""  { member.mention } ```diff\n -лишился  { role }!\n``` """)
	
token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
