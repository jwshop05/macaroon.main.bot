import asyncio
from main_bot import bot as main_bot
from warning_bot import bot as warning_bot
from verification_bot2 import bot as verification_bot2
from verification_bot import bot as verification_bot

async def main():
    await asyncio.gather(
        main_bot.start(os.environ['DISCORD_BOT_TOKEN']),
        warning_bot.start(os.environ['DISCORD_BOT_TOKEN']),
        verification_bot2.start(os.environ['DISCORD_BOT_TOKEN']),
        verification_bot.start(os.environ['DISCORD_BOT_TOKEN']),
    )

if __name__ == '__main__':
    asyncio.run(main())