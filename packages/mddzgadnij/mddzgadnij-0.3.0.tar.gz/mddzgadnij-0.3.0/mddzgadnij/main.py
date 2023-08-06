import random


def guess():
    input("Please think of a number from 1 to 100 and press enter.")
    minimum = 1
    maximum = 100
    predict = 50

    while True:
        ans = input(f"Is {predict} your number? (y - yes, m - more, l - less): ")
        ans = ans.lower()
        if ans == 'y':
            break
        elif ans == 'm':
            minimum = predict + 1
            predict = (predict + maximum) // 2
        elif ans == 'l':
            maximum = predict - 1
            predict = (predict + minimum) // 2
        else:
            print("Error, use 'y', 'm' or 'l'.\n")

    print("Yes I have guessed correctly!")


if __name__ == "__main__":
    guess()
