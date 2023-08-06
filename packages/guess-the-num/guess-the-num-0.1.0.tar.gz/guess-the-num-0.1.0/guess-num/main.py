import random


def guess():
    input("Please think of a number from 1 to 10 and press enter.")
    ans = input(f"Did you think about {random.randint(1, 10)}? (y/n): ")
    if ans.lower() == "y":
        print("Yes i won!!")
    else:
        print("I have lost again :(")

