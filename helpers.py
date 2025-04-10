import os
import re
from mpmath import mp
import prompts as P

VALID_CMD = ['help', 'clear', 'restart', 'y', 'n']

def green(text):
    return f"\033[92m{text}\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt):
    user_input = input(prompt).strip()
    valid_input = validate_input(user_input)

    if not valid_input:     
        print(P.INVALID_PI_INPUT)
        return False
    return user_input

def validate_input(input):
    if input in VALID_CMD:
        return True
    if input.count('.') > 1:
        return False
    if '.' in input and input.index('.') != 1:
        return False
    if not all(c.isdigit() or c == '.' for c in input):
        return False
    return True

def generate_pi(digits):
    mp.dps = digits + 1
    return str(mp.pi)[:digits+2]

def digit_len(s:str):
    return len(s.replace(".", ""))

def check_for_command(input:str):
    if input.lower() in ("clear", "restart"):
        clear_screen()
        return "restart"
    if input.lower() == "help":
        P.HELP()
        return "help"
    return None

def normalize_chunk_input(chunk, known, remaining):
    if not chunk.startswith(known) and chunk == remaining[:digit_len(chunk)]:
        return known + chunk
    return chunk
