import random

rival_choices = ["rock", "paper", "scissors"]
win_cases = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}
def game (your_choice):
    rival_choice = random.choice(rival_choices)
    print(f"alright, you selected {your_choice}.")
    print(f"your rival selected {rival_choice}")
    if your_choice == rival_choice:
        return "##### Draw! #####\n"
    elif win_cases[your_choice] == rival_choice:
        return "##### You won! #####\n"
    else:
        return "##### You lost! #####\n"
print("#################################################################\n")
print("################## ROCK, PAPER, SCISSORS GAME ###################\n")
print("#################################################################\n")

while True:
    while True:
        your_choice = input("Write your choice, rock, paper or scissors: ").lower()
        if your_choice in rival_choices:
            break
        else:
            print("Invalid choice. Please enter rock, paper or scissors: ")
    print(game(your_choice))
    play_again = input("Game finished, write continue or surrender: ")
    if play_again == "continue":
        continue
    else:
        break