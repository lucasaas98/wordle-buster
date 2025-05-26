from wordlebot import WordleBot
import asyncio
from joblib import Parallel, delayed
import random

def main():
    bot = WordleBot(f"WordleMaster-{random.random()}")
    for i in range(1000000):
        bot.initialize()
        stats = bot.play_game("http://127.0.0.1:9009")
        if stats["games_won"] > 10:
            print(f"Final Stats: {stats}")
            return


if __name__ == "__main__":
        Parallel(n_jobs=9)(
            delayed(main)() for i in range(9)
        )
        # asyncio.run(main())

        # delayed(create_data_vector)(ticker, interval) for ticker in all_tickers for interval in all_intervals