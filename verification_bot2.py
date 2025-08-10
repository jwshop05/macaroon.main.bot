import os
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.message_content = True 

app = commands.Bot(command_prefix='!', intents=intents)
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

@app.event
async def on_ready():
    print('마카롱_인증봇으로_로그인_완료')

@app.command(name="수동인증")
async def _HumanRole(ctx, member: discord.Member = None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(f'{ctx.author.mention}, 당신은 권한이 없습니다.')
    channel = app.get_channel(1014428203554709513)
    member = member or ctx.message.author
    role = get(ctx.guild.roles, name="*꧁༺친구༻꧂*")
    if role:
        await member.add_roles(role)
    await channel.send(f"새로오신 친구님이다! 다들 환영해주세요, {member.mention}님 반가워요~💕  게임를 사랑하는 사람들끼리 규칙을 지키면서 소통해요!👍🏻")
    await ctx.send('인증완료')

app.run(token)