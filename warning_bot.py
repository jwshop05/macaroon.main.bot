import os
import discord
from discord.ext import commands
import sqlite3

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

# 토큰 환경 변수로 불러오기
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

# 데이터베이스 접속
db = sqlite3.connect("database.db")
SQL = db.cursor()

@bot.event
async def on_ready():
    print('마카롱_경고봇으로_로그인_완료')

@bot.command()
@commands.has_permissions(administrator=True)
async def 경고(ctx, user: discord.Member, *, arg):

    ch = bot.get_channel(id=1014428204020269072) #경고
    chs = bot.get_channel(id=1014428204020269071) #처벌

    author = ctx.message.author.display_name
    author1 = ctx.message.author
    USER_NAME = str(ctx.message.author)
    USER_ID = user.id
    roles_check = discord.utils.get(ctx.guild.roles, name="역할이름")
    SQL.execute(f'select user_id from warn where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()  
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')

    if result_userID is None:
        SQL.execute('insert into warn(user_name, user_id, warn) values(?,?,?)', (USER_NAME, USER_ID, 0))
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
            em.set_footer(icon_url=author1.avatar_url, text=f'{author}')
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


bot.run(TOKEN)