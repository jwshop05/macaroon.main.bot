import os
import discord
from captcha.image import ImageCaptcha
import random
import asyncio

token = os.environ.get('DISCORD_BOT_TOKEN')
_channel = '1014428203231752217'

client = discord.Client()

@client.event
async def on_ready():
    print(client.user)

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

client.run(token)