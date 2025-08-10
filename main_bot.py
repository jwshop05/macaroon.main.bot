import os
import discord
import asyncio
import random
from discord.ext import commands
from captcha.image import ImageCaptcha
from discord.utils import get
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
import sqlite3

load_dotenv()

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 

client = commands.Bot(command_prefix='!', intents=intents)

connection = sqlite3.connect("database.db")
cur = connection.cursor()
async def status_task():
    while(True):
        types = "1","2","3","4"
        choice = random.choice(types)
        if choice == "2":
            await client.change_presence(activity=discord.Activity(type=1, name="〔 마카롱 〕", url='https://twitch.tv/twitch'))
        elif choice == "3":
            await client.change_presence(activity=discord.Activity(type=1, name="Made by PJW#7947", url='https://twitch.tv/twitch'))
        else:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="〔 마카롱 〕"))
        await asyncio.sleep(15)

@client.event
async def on_ready():
    print('마카롱_메인봇으로_로그인_완료')
    await client.loop.create_task(status_task())

@client.event
async def on_message(message):
    if message.content.startswith("!인증"):  # 명령어 !인증
        if not message.channel.id == int(_channel):
            return
        a = ""
        Captcha_img = ImageCaptcha()
        for i in range(6):
            a += str(random.randint(0, 9))
        name = str(message.author.id) + ".png"
        Captcha_img.write(a, name)

        nummsg = await message.channel.send(f"{message.author.mention} 아래 숫자를 10초 내에 입력해주세요.", file=discord.File(name))

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            msg = await client.wait_for("message", timeout=10, check=check)  # 제한시간
        except:
            await nummsg.delete()
            await message.delete()
            chrhkEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            chrhkEmbed.add_field(name='닉네임', value=message.author, inline=False)
            chrhkEmbed.add_field(name='이유', value='시간초과', inline=False)
            await message.channel.send(embed=chrhkEmbed)
            print(f'{message.author} 님이 시간초과로 인증 실패')
            await msg.delete()
            return

        if msg.content == a:
            role = discord.utils.get(message.guild.roles, name="*꧁༺친구༻꧂*")
            await nummsg.delete()
            await message.delete()
            await msg.delete()
            tjdrhdEmbed = discord.Embed(title='인증성공', color=0x04FF00)
            tjdrhdEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tjdrhdEmbed.add_field(name='3초 후 인증 역할 부여', value='** **', inline=False)
            tjdrhdEmbed.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed=tjdrhdEmbed)
            await asyncio.sleep(3)
            await message.author.add_roles(role)
            await msg.delete()
        else:
            await nummsg.delete()
            await message.delete()
            await msg.delete()
            tlfvoEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            tlfvoEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tlfvoEmbed.add_field(name='이유', value='잘못된 숫자', inline=False)
            await message.channel.send(embed=tlfvoEmbed)
            print(f'{message.author} 님이 잘못된 숫자로 인증 실패')


@client.command(name='청소')
async def _clear(ctx, amount=20):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount}개의 메세지 청소를 완료했어요.')
    await asyncio.sleep(3)
    

    await message.delete()
    
    await ctx.message.delete()

@client.command(name='처벌')
async def _ban(ctx, user: discord.Member, *, arg):
    
    author = ctx.message.author.display_name
    author1 = ctx.message.author
    USER_NAME = str(ctx.message.author)
    USER_ID = user.id
    
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = client.get_channel(1014428204020269071)
    embed = discord.Embed(title="🚨〔 마카롱 〕서버 차단", color=0xff0000)
    embed.add_field(name='디스코드 멘션', value=f'<@{user.id}>, {user}', inline=False)
    embed.add_field(name='디스코드 별명', value=f'{user.display_name}', inline=False)
    embed.add_field(name='디스코드 id', value=f'{user.id}', inline=False)
    embed.add_field(name='사유', value=arg, inline=False)
    embed.set_thumbnail(url="https://i.ibb.co/KzhQm5MS/123123123123.png")
    embed.set_footer(icon_url=author1.avatar_url, text=f'{author}')
    await user.ban(reason=arg)
    await channel.send("@everyone", embed=embed)

@client.command(name='공지')
async def _notice(ctx, *, arg):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = client.get_channel(1014428203554709507)
    embed = discord.Embed(color=0xab19ae, timestamp=ctx.message.created_at, title="_마카롱_공지")
    embed.set_thumbnail(url="https://i.ibb.co/KzhQm5MS/123123123123.png")
    embed.add_field(name="내용", value=arg, inline=True)
    embed.set_footer(text=f'담당자 이름:{ctx.author.name}')
    await channel.send("@everyone", embed=embed)
    await ctx.send('공지등록 완료')
    await message.delete()
    
@client.command(name='서버켜기')
async def _notice(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = client.get_channel(1014428203554709508)
    embed = discord.Embed(color=0x12ff00, timestamp=datetime.utcnow(), title="서버 ON")
    embed.add_field(name="상태", value="**ON**", inline=True)
    embed.set_footer(text=f"마카롱서버*")
    await channel.send("@here", embed=embed)
    msg1 = await ctx.send('시스템 결함 확인중')
    msg2 = await ctx.send('발견된 결함 없음')

    await asyncio.sleep(2)

    await msg1.delete()
    await msg2.delete()

    await ctx.send('정상 작동중!')

@client.command(name='서버끄기')
async def _notice(ctx,*, arg):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = client.get_channel(1014428203554709508)
    embed = discord.Embed(color=0xff0000, timestamp=datetime.utcnow(), title="서버 OFF")
    embed.add_field(name="상태", value="**OFF**", inline=False)
    embed.add_field(name="사유", value=arg, inline=False)
    embed.set_footer(text=f"마카롱서버")
    await channel.send("@here", embed=embed)
    await ctx.send('정상적으로 종료가 되었습니다')
    
client.run(TOKEN)
