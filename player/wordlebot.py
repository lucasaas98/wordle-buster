import random
from lifecycle import BotLifecycle, BotState

class WordleBot(BotLifecycle):
    def __init__(self, bot_name: str):
        super().__init__(bot_name)

    def select_word(self) -> str:
        """Select a word from the word list"""
        last_word = None

        if len(self.attempts) > 0:
            last_word = self.attempts[-1]
        
        if len(self.attempts) == 0:
            self.word_list.remove("heats")
            return "heats"

        smaller_list = self.word_list[:]
        if self.last_result and last_word:
            for i, result in enumerate(self.last_result['result']):
                if result == "correct":
                    for word in smaller_list[:]:
                        if word[i] != last_word[i]:
                            smaller_list.remove(word)
                if result == "wrong_position":
                    for word in smaller_list[:]:
                        if last_word[i] not in word:
                            smaller_list.remove(word)
                if result == "incorrect":
                    for word in smaller_list[:]:
                        if last_word[i] in word:
                            smaller_list.remove(word)
        
        self.word_list = smaller_list
        return random.choice(smaller_list)


    def play_game(self, base_url: str):
        """Play a complete game of Wordle"""
        self.start_game(base_url)

        while self.state == BotState.ACTIVE:
            word = self.select_word()
            # print("word:", word)
            result = self.make_guess(word)
            # print("result:", result)
            self.last_result = result

            # Simulate game logic based on result
            if result["game_status"] == "won":
                self.complete_game(won=True)
            elif result["remaining_attempts"] <= 0:
                self.complete_game(won=False)

        return self.stats