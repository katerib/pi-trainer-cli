import prompts as P
from helpers import *

MAX_DIGITS = 500

def pi_memorizer():
    print(P.WELCOME)
    pi_digits = generate_pi(MAX_DIGITS)

    while True:
        known = get_input(P.ASK_KNOWN).replace(" ", "")
        cmd = check_for_command(known)
        if cmd == "restart":
            clear_screen()
            return pi_memorizer()
        elif cmd == "help":
            continue
        if known is False or not validate_input(known):
            continue
        digits_only = known.replace(".", "")
        if known != pi_digits[:len(known)]:
            print(P.INCORRECT_KNOWN)
            known = ""
            print(P.CONFIRM_KNOWN.format(0))
        else:
            print(P.CONFIRM_KNOWN.format(len(digits_only)))
        break

    while True:
        goal_input = get_input(P.ASK_GOAL)
        if goal_input is False: 
            continue
        cmd = check_for_command(goal_input)
        if cmd == "restart":
            clear_screen()
            return pi_memorizer()
        elif cmd == "help":
            continue
        try:
            goal = int(goal_input)
            if goal > len(pi_digits):
                print(P.GOAL_TOO_HIGH.format(len(pi_digits)))
                continue
            break
        except ValueError:
            print(P.INVALID_NUMBER)

    while digit_len(known) < goal:
        print(P.PROGRESS.format(digit_len(known), goal))
        preview_len = min(20, goal - digit_len(known))
        print(P.PREVIEW)
        start = digit_len(known)
        remaining = pi_digits[start+1:start+1 + preview_len]
        print(green(pi_digits[:len(known)]), ' ', remaining)

        if len(remaining) <= 3:
            print(f"There are only {len(remaining)} digits left! You got this.")
            chunk = remaining
        else:
            chunk = get_input(P.ASK_CHUNK)
            if chunk is False: 
                continue
            cmd = check_for_command(chunk)
            if cmd == "restart":
                clear_screen()
                return pi_memorizer()
            elif cmd == "help":
                continue
        
        memorize_value = normalize_chunk_input(chunk, known, remaining)

        print(P.MEMORIZE_PROMPT)
        while True:
            if input() == "":
                break
        clear_screen()

        attempt = get_input(P.ATTEMPT_PROMPT)
        if attempt is False: 
            continue 
        cmd = check_for_command(attempt)
        if cmd == "restart":
            return pi_memorizer()
        elif cmd == "help":
            continue
        
        if attempt == memorize_value:
            print(P.CHUNK_CORRECT)
            known = memorize_value
        else:
            print(P.CHUNK_INCORRECT.format(memorize_value))
            retry = get_input(P.RETRY_PROMPT).lower()
            if retry is False: 
                continue 
            elif retry != 'y':
                return

    print(P.COMPLETE.format(goal))
    print(P.SHOW_FINAL_PI.format(green(pi_digits[:goal+1])))

if __name__ == "__main__":
    pi_memorizer()
