from wordlebot import WordleBot
import asyncio

async def main():
    bot = WordleBot("WordleMaster")
    for i in range(10000):
        await bot.initialize()
        stats = await bot.play_game("http://127.0.0.1:9009")
        print(f"Final Stats: {stats}")
        if stats["games_won"] > 0:
            print("We freaking did it, bros")
            exit()

if __name__ == "__main__":
        asyncio.run(main())