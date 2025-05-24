from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import requests
import uuid
import asyncio
from datetime import datetime
from game import get_random_word, validate_guess

app = FastAPI()

class GameState(BaseModel):
    target_word: str
    attempts: List[str]
    remaining_attempts: int
    game_status: str  # "active", "won", "lost"
    created_at: datetime

class GuessResponse(BaseModel):
    result: List[str]  # Array of "correct", "wrong_position", "incorrect"
    remaining_attempts: int
    game_status: str

class GameStartResponse(BaseModel):
    game_id: str

games: Dict[str, GameState] = {}

class GuessRequest(BaseModel):
    guess: str

class GameStatusResponse(BaseModel):
    result: list[str]
    remaining_attempts: int
    game_status: str
    full_state: GameState

@app.post("/api/v1/wordle/start", response_model=dict)
async def start_game():
    """Create a new Wordle game."""
    game_id = str(uuid.uuid4())
    target_word = get_random_word()
    games[game_id] = GameState(
        target_word=target_word,
        attempts=[],
        remaining_attempts=6,
        game_status="active",
        created_at=datetime.now()
    )
    return {"game_id": game_id}

@app.post("/api/v1/wordle/play/{game_id}", response_model=GameStatusResponse)
async def play_game(game_id: str, guess_data: GuessRequest):
    """Handle gameplay with POST requests."""
    # Validate game exists
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    
    # Get guess and validate format
    guess = guess_data.guess.lower()
    if not guess:
        raise HTTPException(status_code=400, detail="Missing required 'guess' field")
    
    # Validate guess format
    if len(guess) != 5:
        raise HTTPException(status_code=400, detail="Guess must be exactly 5 letters")
    
    # Validate remaining attempts
    if game.remaining_attempts <= 0:
        raise HTTPException(
            status_code=400,
            detail="Game over",
            headers={"X-Game-Status": game.game_status}
        )
    
    # Process guess
    result = validate_guess(guess, game.target_word)
    
    # Update game state
    game.attempts.append(guess)
    game.remaining_attempts -= 1
    
    # Check win condition
    if all(r == "correct" for r in result):
        game.game_status = "won"
    elif game.remaining_attempts <= 0:
        game.game_status = "lost"
    
    return {
        "result": result,
        "remaining_attempts": game.remaining_attempts,
        "game_status": game.game_status,
        "full_state": game
    }