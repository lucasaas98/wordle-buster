from enum import Enum
from typing import Dict, List, Optional
import asyncio
import random
from datetime import datetime
import requests

class BotState(Enum):
    INITIALIZED = "initialized"
    WAITING_TO_START = "waiting_to_start"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

class BotLifecycle:
    def __init__(self, bot_name: str):
        self.url = None
        self.bot_name = bot_name
        self.state = BotState.INITIALIZED
        self.current_game_id: Optional[str] = None
        self.attempts: List[str] = []
        self.stats = {
            "games_played": 0,
            "games_won": 0,
            "average_attempts": 0,
            "total_attempts": 0
        }
        self.last_result = []
        
    async def initialize(self):
        """Initialize the bot lifecycle"""
        self.state = BotState.WAITING_TO_START
        print(f"\n{self.bot_name} initialized")
        
    async def start_game(self, base_url: str) -> bool:
        """Start a new Wordle game"""
        if self.state != BotState.WAITING_TO_START:
            raise ValueError("Bot must be waiting to start a game")

        self.url = base_url

        # call the api to start a game
        url = f"{self.url}/api/v1/wordle/start"
        response = requests.post(url)
            
        self.current_game_id = response.json()["game_id"]
        self.state = BotState.ACTIVE
        self.attempts = []
        self.last_result = []
        return True
        
    async def make_guess(self, word: str) -> Dict:
        """Make a guess in the current game"""
        if self.state != BotState.ACTIVE:
            raise ValueError("Bot must be active to make guesses")


        url = f"{self.url}/api/v1/wordle/play/{self.current_game_id}"

        payload = { "guess": word }
        headers = {"content-type": "application/json"}

        result = requests.post(url, json=payload, headers=headers).json()
        
        self.attempts.append(word)
        return result
        
    async def complete_game(self, won: bool):
        """Complete the current game and update statistics"""
        if self.state != BotState.ACTIVE:
            raise ValueError("Cannot complete inactive game")
            
        self.stats["games_played"] += 1
        if won:
            self.stats["games_won"] += 1
            
        self.stats["total_attempts"] += len(self.attempts)
        self.stats["average_attempts"] = (
            self.stats["total_attempts"] / self.stats["games_played"]
        )
        
        self.state = BotState.COMPLETED
        
    async def pause(self):
        """Pause the current game"""
        if self.state == BotState.ACTIVE:
            self.state = BotState.PAUSED
            
    async def resume(self):
        """Resume a paused game"""
        if self.state == BotState.PAUSED:
            self.state = BotState.ACTIVE