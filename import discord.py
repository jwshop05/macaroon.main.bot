from dotenv import load_dotenv
load_dotenv()
import discord
import asyncio
import requests
import os

# ====== 환경 변수에서 불러오기 ======
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # GitHub Secret에 넣기
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))  # 채널 ID도 Secret 또는 .env에서 불러오기
BJ_ID = os.getenv("BJ_ID", "qkrqjatn098")     # BJ ID
# ==================================

THUMB_URL = f"https://liveimg.sooplive.co.kr/{BJ_ID}_thumb.jpg"
is_live = False

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_streaming():
    global is_live
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
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

@client.event
async def on_ready():
    print(f"✅ 로그인 완료: {client.user}")

client.loop.create_task(check_streaming())
client.run(DISCORD_TOKEN)