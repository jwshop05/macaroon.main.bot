import os
import discord
from discord.ext import commands, tasks
import random
import asyncio
import sqlite3
import requests
from discord.utils import get
from datetime import datetime
from captcha.image import ImageCaptcha
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
IDLE_CHANNEL_ID = 1404443419308462101
IDLE_TIMEOUT = 6000
DELETE_TIMEOUT = 10
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))
BJ_ID = os.getenv("BJ_ID", "qkrqjatn098")

THUMB_URL = f"https://liveimg.sooplive.co.kr/{BJ_ID}_thumb.jpg"
is_live = False

db = sqlite3.connect("database.db")
SQL = db.cursor()

SQL.execute('''
CREATE TABLE IF NOT EXISTS warn (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    user_id INTEGER UNIQUE,
    warn INTEGER
)
''')
db.commit()

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

activity_timers = {}  
channel_timers = {}

CHANNEL_A_ID = 1404454103643324577
CHANNEL_B_ID = 1017537139484934214

async def handle_channel_a(member, channel):
    guild = member.guild
    category = channel.category

    new_channel = await guild.create_voice_channel(
        name=f'{member.name}의 채널 ',
        category=category
    )

    await member.move_to(new_channel)

async def handle_channel_b(member, channel):
    guild = member.guild
    category = channel.category

    new_channel = await guild.create_voice_channel(
        name=f'{member.name}의 채널 ',
        category=category
    )

    await member.move_to(new_channel)


async def check_streaming():
    global is_live
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)

    while not bot.is_closed():
        try:
            res = requests.get(THUMB_URL)

            # 방송 켜짐
            if res.status_code == 200 and not is_live:
                is_live = True
                embed = discord.Embed(
                    title="🔴 방송 시작!",
                    description=f"[시청하기](https://ch.sooplive.co.kr/{BJ_ID})",
                    color=discord.Color.red()
                )
                embed.set_image(url=THUMB_URL)
                await channel.send(embed=embed)

            # 방송 꺼짐
            elif res.status_code != 200 and is_live:
                is_live = False
                embed = discord.Embed(
                    title="📴 방송 종료",
                    description="방송이 종료되었습니다.",
                    color=discord.Color.dark_gray()
                )
                await channel.send(embed=embed)

        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(60)  # 1분마다 체크

@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")

@bot.event
async def on_ready():
    print('봇이 준비되었습니다!')

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and before.channel != after.channel:
        if after.channel.id == CHANNEL_A_ID:
            await handle_channel_a(member, after.channel)
        elif after.channel.id == CHANNEL_B_ID:
            await handle_channel_b(member, after.channel)
    elif before.channel and len(before.channel.members) == 0:
        start_delete_timer(before.channel)

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and before.channel != after.channel:
        if after.channel.id == CHANNEL_A_ID:
            await handle_channel_a(member, after.channel)
        elif after.channel.id == CHANNEL_B_ID:
            await handle_channel_b(member, after.channel)
    elif before.channel and len(before.channel.members) == 0:
        start_delete_timer(before.channel)

@bot.event
async def on_message(message):
    if message.author.voice and message.author.voice.channel:
        reset_activity_timer(message.author, message.author.voice.channel)
    await bot.process_commands(message)

def reset_activity_timer(member, channel):
    if member.id in activity_timers:
        activity_timers[member.id].cancel()
    task = asyncio.create_task(check_idle(member, channel))
    activity_timers[member.id] = task
    print(f'{member.name}님의 새 타이머 시작 ({IDLE_TIMEOUT}초)')

def start_delete_timer(channel):
    if channel.id not in channel_timers:
        task = asyncio.create_task(delete_channel(channel))
        channel_timers[channel.id] = task
        print(f'{channel.name} 채널 삭제 타이머 시작 ({DELETE_TIMEOUT}초)')

async def check_idle(member, channel):
    await asyncio.sleep(IDLE_TIMEOUT)
    if member.voice and member.voice.channel == channel:
        idle_channel = bot.get_channel(IDLE_CHANNEL_ID)
        if idle_channel:
            try:
                await member.move_to(idle_channel)
                print(f'{member.name}님이 {idle_channel.name} 채널로 이동하고 뮤트되었습니다.')
            except Exception as e:
                print(f"이동 및 뮤트 오류: {e}")
            start_delete_timer(channel)
        else:
            print(f"IDLE_CHANNEL_ID({IDLE_CHANNEL_ID})에 해당하는 채널을 찾을 수 없습니다.")
    del activity_timers[member.id]

async def delete_channel(channel):
    await asyncio.sleep(DELETE_TIMEOUT)
    try:
        await channel.delete()
        print(f'{channel.name} 채널 삭제됨')
    except Exception as e:
        print(f"채널 삭제 오류: {e}")
    if channel.id in channel_timers:
        del channel_timers[channel.id]

@bot.command()
async def 청소(ctx, amount=20):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    await ctx.channel.purge(limit=amount)
    msg = await ctx.send(f'{amount}개의 메시지 청소를 완료했어요.')
    await asyncio.sleep(8)
    await msg.delete()

@bot.command()
async def 처벌(ctx, user: discord.Member, *, arg):
        
    author = ctx.message.author.display_name
    author1 = ctx.message.author
    USER_NAME = str(ctx.message.author)
    USER_ID = user.id
    
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = bot.get_channel(1014428204020269071)
    embed = discord.Embed(title="🚨〔 마카롱 〕서버 차단", color=0xff0000)
    embed.add_field(name='디스코드 멘션', value=f'<@{user.id}>, {user}', inline=False)
    embed.add_field(name='디스코드 별명', value=f'{user.display_name}', inline=False)
    embed.add_field(name='디스코드 id', value=f'{user.id}', inline=False)
    embed.add_field(name='사유', value=arg, inline=False)
    embed.set_thumbnail(url="https://i.ibb.co/KzhQm5MS/123123123123.png")
    embed.set_footer(icon_url=author1.avatar.url, text=f'{author}')
    await user.ban(reason=arg)
    await channel.send("@everyone", embed=embed)
    pass

@bot.command()
async def 공지(ctx, *, arg):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = bot.get_channel(1014428203554709507)
    embed = discord.Embed(color=0xab19ae, timestamp=ctx.message.created_at, title="_마카롱_공지")
    embed.set_thumbnail(url="https://i.ibb.co/KzhQm5MS/123123123123.png")
    embed.add_field(name="내용", value=arg, inline=True)
    embed.set_footer(text=f'담당자 이름:{ctx.author.name}')
    await channel.send("@everyone", embed=embed)
    await ctx.send('공지등록 완료')
    pass

@bot.command()
async def 서버켜기(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = bot.get_channel(1014428203554709508)
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
    pass

@bot.command()
async def 서버끄기(ctx, *, arg):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = bot.get_channel(1014428203554709508)
    embed = discord.Embed(color=0xff0000, timestamp=datetime.utcnow(), title="서버 OFF")
    embed.add_field(name="상태", value="**OFF**", inline=False)
    embed.add_field(name="사유", value=arg, inline=False)
    embed.set_footer(text=f"마카롱서버")
    await channel.send("@here", embed=embed)
    await ctx.send('정상적으로 종료가 되었습니다')
    pass

@bot.command()
async def 인증(ctx):
    if ctx.channel.id != 1014428203231752217:
        return
    a = ""
    captcha_img = ImageCaptcha()
    for i in range(6):
        a += str(random.randint(0, 9))
    filename = f"{ctx.author.id}.png"
    captcha_img.write(a, filename)
    nummsg = await ctx.send(f"{ctx.author.mention} 아래 숫자를 10초 내에 입력해주세요.", file=discord.File(filename))
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    try:
        msg = await bot.wait_for('message', timeout=10, check=check)
    except:
        try:
            await nummsg.delete()
        except:
            pass
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
        embed.add_field(name='닉네임', value=ctx.author.mention, inline=False)
        embed.add_field(name='이유', value='시간초과', inline=False)
        msg_fail = await ctx.send(embed=embed)

        await asyncio.sleep(18)
        try:
            await msg_fail.delete()
        except:
            pass
        return

    if msg.content == a:
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else "https://i.ibb.co/KzhQm5MS/123123123123.png"
        role = get(ctx.guild.roles, name="*꧁༺친구༻꧂*")
        try:
            await nummsg.delete()
        except:
            pass
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            await msg.delete()
        except:
            pass

        embed = discord.Embed(title='인증성공', color=0x04FF00)
        embed.add_field(name='닉네임', value=ctx.author.mention, inline=False)
        embed.add_field(name='3초 후 인증 역할 부여', value='** **', inline=False)
        embed.set_thumbnail(url=avatar_url)
        msg_success = await ctx.send(embed=embed)
        await asyncio.sleep(18)
        try:
            await msg_success.delete()
        except:
            pass
        if role:
            await ctx.author.add_roles(role)
    else:

        try:
            await nummsg.delete()
        except:
            pass
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            await msg.delete()
        except:
            pass

        embed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
        embed.add_field(name='닉네임', value=ctx.author.mention, inline=False)
        embed.add_field(name='이유', value='잘못된 숫자', inline=False)
        msg_fail2 = await ctx.send(embed=embed)
        await asyncio.sleep(18)
        try:
            await msg_fail2.delete()
        except:
            pass

        
@bot.command(name="수동인증")
async def _HumanRole(ctx, member: discord.Member = None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = bot.get_channel(1014428203231752219)  # 채널 ID 수정
    member = member or ctx.message.author
    role = get(ctx.guild.roles, name="*꧁༺친구༻꧂*")
    if role:
        await member.add_roles(role)
    await channel.send(f"새로오신 친구님이다! 다들 환영해주세요, {member.mention}님 반가워요~💕  게임을 사랑하는 사람들끼리 규칙을 지키면서 소통해요!👍🏻")
    await ctx.send('인증완료')


@bot.command()
@commands.has_permissions(administrator=True)
async def 경고(ctx, user: discord.Member, *, arg):
    ch = bot.get_channel(1014428204020269072)
    chs = bot.get_channel(1014428204020269071)

    author = ctx.message.author.display_name
    USER_ID = user.id
    SQL.execute(f'select user_id from warn where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()

    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')

    if result_userID is None:
        SQL.execute('insert into warn(user_name, user_id, warn) values(?,?,?)', (str(user), USER_ID, 0))
        db.commit()
        SQL.execute('update warn set warn = warn + ? where user_id = ?', (1, USER_ID))
        db.commit()

        SQL.execute(f'select warn from warn where user_id="{USER_ID}"')
        result = SQL.fetchone()

        emb = discord.Embed(title='⚠️〔 마카롱 〕서버 경고', color=0xfff700)
        emb.add_field(name='경고자', value=f'<@{user.id}>', inline=False)
        emb.add_field(name='담당자', value=f'{ctx.author.name}', inline=True)
        emb.add_field(name='횟수', value=f'{result[0]}회', inline=False)
        emb.add_field(name='사유', value=arg, inline=True)
        emb.set_thumbnail(url="https://i.ibb.co/KzhQm5MS/123123123123.png")
        emb.set_footer(text=f'3회 누적 시 자동 차단됨을 알립니다.')
        await ch.send(embed=emb)
        await ctx.send(f'정상적으로 처리되었습니다. 경고횟수: {result[0]}번')
        if result[0] >= 3:
            em = discord.Embed(title="🚨〔 마카롱 〕서버 차단", color=0xff0000)
            em.add_field(name='디스코드 멘션', value=f'<@{user.id}>, {user}', inline=False)
            em.add_field(name='디스코드 별명', value=f'{user.display_name}', inline=False)
            em.add_field(name='디스코드 id', value=f'{user.id}', inline=False)
            em.add_field(name='사유', value=f'경고 3회 누적', inline=False)
            em.set_thumbnail(url="https://i.ibb.co/KzhQm5MS/123123123123.png")
            em.set_footer(icon_url=ctx.author.avatar_url, text=f'{author}')
            await chs.send("@everyone", embed=em)
            await ctx.send('경고자가 3회 누적으로 차단당하였습니다.')
            await user.ban(reason='경고 3회 누적')
    else:
        SQL.execute('update warn set warn = warn + ? where user_id = ?', (1, USER_ID))
        db.commit()
        SQL.execute(f'select warn from warn where user_id="{USER_ID}"')
        result = SQL.fetchone()
        emb = discord.Embed(title='⚠️〔 마카롱 〕서버 경고', color=0xfff700)        
        emb.add_field(name='경고자', value=f'<@{user.id}>', inline=False)
        emb.add_field(name='담당자', value=f'{ctx.author.name}', inline=True)
        emb.add_field(name='횟수', value=f'{result[0]}회', inline=False)
        emb.add_field(name='사유', value=arg, inline=True)
        emb.set_thumbnail(url="https://i.ibb.co/KzhQm5MS/123123123123.png")
        emb.set_footer(text=f'3회 누적 시 자동 차단됨을 알립니다.')
        await ch.send(embed=emb)
        await ctx.send(f'정상적으로 처리되었습니다. 경고횟수: {result[0]}번')
        if result[0] >= 3:
            em = discord.Embed(title="🚨〔 마카롱 〕서버 차단", color=0xff0000)
            em.add_field(name='디스코드 멘션', value=f'<@{user.id}>, {user}', inline=False)
            em.add_field(name='디스코드 별명', value=f'{user.display_name}', inline=False)
            em.add_field(name='디스코드 id', value=f'{user.id}', inline=False)
            em.add_field(name='사유', value=f'경고 3회 누적', inline=False)
            em.set_thumbnail(url="https://i.ibb.co/KzhQm5MS/123123123123.png")
            em.set_footer(icon_url=author1.avatar_url, text=f'{author}')
            await chs.send("@everyone", embed=em)
            await ctx.send('경고자가 3회 누적으로 차단당하였습니다.')
            await user.ban(reason='경고 3회 누적')

@bot.command()
async def 경고확인(ctx, user: discord.Member):
    USER_ID = user.id
    SQL.execute(f'select warn from warn where user_id="{USER_ID}"')
    warn = SQL.fetchone()
    if warn == None:
        await ctx.send('휴~ 다행히도 그 사람은 경고가 없어요!!!')
    else: 
        SQL.execute(f'select warn from warn where user_id="{USER_ID}"')
        warn1 = SQL.fetchall()[0]
        await ctx.send(f'어라..그 사람은 경고가 {warn1[0]}회가 있어요... ')

@bot.command()
@commands.has_permissions(administrator=True)
async def 경고초기화(ctx, user: discord.Member = None):
    if user is None:
        # 서버 전체 유저 경고 지우기
        SQL.execute('DELETE FROM warn')
        db.commit()
        await ctx.send("모든 사용자 경고 기록을 초기화했습니다.")
    else:
        USER_ID = user.id
        SQL.execute('DELETE FROM warn WHERE user_id=?', (USER_ID,))
        db.commit()
        await ctx.send(f"{user.mention}님의 경고 기록을 초기화했습니다.")


bot.run(os.environ.get('DISCORD_BOT_TOKEN'))