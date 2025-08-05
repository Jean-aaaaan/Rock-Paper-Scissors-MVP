import random

def get_player_choice(valid_choices):
    while True:
        player_choice = input("Make your Choice: ").lower()
        if player_choice in valid_choices:
            return player_choice
        else:
            print("DISQUALIFIED, You now have a 1/6 chance of dying")
            return None

def gameplay(player_choice, gongyoo_input, winning_dict, stage):
    if player_choice == gongyoo_input:
        return "It's a Tie!"
    elif winning_dict[player_choice] == gongyoo_input:
        return "You Win!"
    else:
        chance_fraction = f"{stage}/6"
        return f"You now have a {chance_fraction} chance of dying"

def elimination_check(chance):
    return random.random() < chance

def play_final_round(prize_pool):
    print("\nThis is the final winner-takes-all round!")
    valid_choices = ["rock", "paper", "scissors"]
    winning_dict = {"paper": "rock", "scissors": "paper", "rock": "scissors"}

    player_choice = get_player_choice(valid_choices)
    if not player_choice:
        print("Invalid choice. You have been permanently eliminated!")
        return 0

    gongyoo_input = random.choice(valid_choices)
    print(f"Gong Yoo's choice is... {gongyoo_input}!")

    if player_choice == gongyoo_input:
        print("It's a Tie! You have been permanently eliminated!")
        return 0
    elif winning_dict[player_choice] == gongyoo_input:
        print("You Win! Your prize money has increased 600 times!")
        return prize_pool * 600
    else:
        print("You Lose! You have been permanently eliminated!")
        return 0

def play_stage(stage, prize_pool, is_final_stage):
    print(f"\nStage {stage}! Prize Pool: ${prize_pool}")
    print("Win a stage, and you can choose to leave with 40% of the prize pool or continue playing.")
    rounds = 0
    rounds_limit = 3
    wins = 0
    losses = 0
    ties = 0

    valid_choices = ["rock", "paper", "scissors"]
    winning_dict = {"paper": "rock", "scissors": "paper", "rock": "scissors"}

    while rounds < rounds_limit:
        print(f"\nRound {rounds + 1}!")
        rounds += 1
        player_choice = get_player_choice(valid_choices)
        if not player_choice:
            if elimination_check(stage / 6):
                print("You have been permanently eliminated!")
                return False, 0
            else:
                print("You narrowly avoided elimination. Focus!")
                continue

        gongyoo_input = random.choice(valid_choices)
        print(f"Gong Yoo's choice is... {gongyoo_input}!")

        result = gameplay(player_choice, gongyoo_input, winning_dict, stage)
        print(result)

        if result == "You Win!":
            wins += 1
            print("You won this round!")

        elif "chance of dying" in result:
            losses += 1
            if elimination_check(stage / 6):
                print("You have been permanently eliminated!")
                return False, 0
        else:
            ties += 1

    print("\nStage Over! Here are the results:")
    print(f"Wins: {wins}, Losses: {losses}, Ties: {ties}")

    if wins >= 2:
        print("You won 2/3 rounds and move on to the next stage. Well done!")
        prize_pool *= 6
        choice = input("Would you like to leave with 50% of the prize pool? (yes/no): ").strip().lower()
        if choice == "yes":
            print(f"You chose to leave with ${int(prize_pool * 0.5)}. Goodbye!")
            return False, int(prize_pool * 0.4)
        return True, prize_pool


    elif is_final_stage:
        print("You didn’t win enough rounds in the final stage. You now have two options:")
        print("1. Leave with 50% of your prize money.")
        print("2. Play a winner-takes-all game. Where if you win, you win 600 times the prize money, but any loss or tie kills you")

        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            print(f"You chose to leave with ${prize_pool // 2}. Goodbye!")
            return False, prize_pool // 2
        elif choice == "2":
            final_prize = play_final_round(prize_pool)
            if final_prize > 0:
                return False, final_prize
            else:
                return False, 0
        else:
            print("Invalid choice. You have been permanently eliminated!")
            return False, 0
    else:
        print("You didn’t win enough rounds to progress. You now have a 1/6 chance of dying.")
        if elimination_check(1 / 6):
            print("You have been permanently eliminated!")
            return False, 0
        else:
            print("You narrowly avoided elimination. You may continue to the next stage!")
            prize_pool *= 6
            return True, prize_pool

def main():
    print("Welcome to the Ultimate Rock-Paper-Scissors Challenge! Can you survive all 5 stages?")

    stage = 1
    max_stages = 5
    prize_pool = 100000

    while stage <= max_stages:
        is_final_stage = stage == max_stages
        survived, prize_pool = play_stage(stage, prize_pool, is_final_stage)
        if not survived:
            if prize_pool > 0:
                print(f"\nYou leave with a total prize of ${prize_pool}. Congratulations!")
            else:
                print("Game Over. Thank you for playing.")
            return
        stage += 1

    print(f"\nCongratulations! You survived all stages and won a total prize of ${prize_pool}!")

if __name__ == "__main__":
    main()

