from fastapi import HTTPException
from typing import List
import requests
import random


DICTIONARY_FILE = "words.txt"

def get_random_word() -> str:
    """Fetch a random 5-letter word from the dictionary API."""
    try:
        all_words = []
        with open('words.txt', 'r') as words_file:
            for word in words_file:
                all_words.append(word.strip())
        random_word = random.choice(all_words)
        return random_word
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch word")

# def validate_guess(guess: str, target: str) -> List[str]:
#     result = []
#     target_letters = list(target)
    
#     # Check correct positions first
#     for i, letter in enumerate(guess):
#         if letter == target[i]:
#             result.append("correct")
#             target_letters[i] = None
    
#     # Then check incorrect positions
#     for i, letter in enumerate(guess):
#         if result[i:] and result[i] != "correct":
#             if letter in target_letters:
#                 result.append("wrong_position")
#                 target_letters[target_letters.index(letter)] = None
#             else:
#                 result.append("incorrect")
    
#     return result

def validate_guess(guess: str, target: str) -> List[str]:
    """Validate a guess against the target word."""
    result = [None] * 5
    # Convert target to list for easier manipulation
    target_letters = list(target)
    
    # First pass: Check correct positions
    for i, letter in enumerate(guess):
        if letter == target[i]:
            result[i] = "correct"

    # Second pass: Check wrong positions
    for i, letter in enumerate(guess):
        if result[i] != "correct":
            if letter in target_letters:
                result[i] = "wrong_position"
            else:
                result[i] = "incorrect"
                # result.append("incorrect")
    
    return result