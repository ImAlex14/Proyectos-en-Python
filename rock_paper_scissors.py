import random

rival_choices = ["rock", "paper", "scissors"]

print("#################################################################\n")
print("################## ROCK, PAPER, SCISSORS GAME ###################\n")
print("#################################################################\n")

while True:
    your_choice = input("Write your choice, rock, paper or scissors: ").lower()
    rival_choice = random.choice(rival_choices)
    print(f"alright, you selected {your_choice}.")
    print(f"your rival selected {rival_choice})")
    if your_choice == "rock" and rival_choice == "paper" or your_choice == "paper" and rival_choice == "scissors" or your_choice == "scissors" and rival_choice == "rock":
        print("##### You lost! #####\n")
        play_again = input("Game finished, write continue or surrender: ").lower()
    elif your_choice == rival_choice:
        print("##### Draw! #####\n")
        play_again = input("Game finished, write continue or surrender: ").lower()
    else:
        print("##### You won! #####\n")
        play_again = input("Game finished, write continue or surrender: ").lower()
    if play_again == "continue":
        continue
    else:
        break