import random
from collections import namedtuple
total_money = float(input("How much money are you betting today?"))
start_money = total_money
yn = "y"

num = namedtuple("num", ["name", "color", "evenOdd","range1", "range2", "column"]) 
bet = namedtuple("bet", ["type", "input", "price"])
bets = []
nums = [
    num("0", "SPECIAL", "SPECIAL", "SPECIAL", "SPECIAL", "SPECIAL"),
    num("1", "red", "odd", "first", "first", "1"),
    num("2", "black", "even", "first", "first", "2"),
    num("3", "red", "odd", "first", "first", "3"),
    num("4", "black", "even", "first", "first", "1"),
    num("5", "red", "odd", "first", "first", "2"),
    num("6", "black", "even", "first", "first", "3"),
    num("7", "red", "odd", "first", "first", "1"),
    num("8", "black", "even", "first", "first", "2"),
    num("9", "red", "odd", "first", "first", "3"),
    num("10", "black", "even", "first", "first", "1"),
    num("11", "black", "odd", "first", "first", "2"),
    num("12", "red", "even", "first", "first", "3"),
    num("13", "black", "odd", "second", "first", "1"),
    num("14", "red", "even", "second", "first", "2"),
    num("15", "black", "odd", "second", "first", "3"),
    num("16", "red", "even", "second", "first", "1"),
    num("17", "black", "odd", "second", "first", "2"),
    num("18", "red", "even", "second", "first", "3"),
    num("19", "red", "odd", "second", "second", "1"),
    num("20", "black", "even", "second", "second", "2"),
    num("21", "red", "odd", "second", "second", "3"),
    num("22", "black", "even", "second", "second", "1"),
    num("23", "red", "odd", "second", "second", "2"),
    num("24", "black", "even", "second", "second", "3"),
    num("25", "red", "odd", "third", "second", "1"),
    num("26", "black", "even", "third", "second", "2"),
    num("27", "red", "odd", "third", "second", "3"),
    num("28", "black", "even", "third", "second", "1"),
    num("29", "black", "odd", "third", "second", "2"),
    num("30", "red", "even", "third", "second", "3"),
    num("31", "black", "odd", "third", "second", "1"),
    num("32", "red", "even", "third", "second", "2"),
    num("33", "black", "odd", "third", "second", "3"),
    num("34", "red", "even", "third", "second", "1"),
    num("35", "black", "odd", "third", "second", "2"),
    num("36", "red", "even", "third", "second", "3"),
    num("00", "SPECIAL", "SPECIAL", "SPECIAL", "SPECIAL", "SPECIAL"),
]

while yn == "y":
    bets = []
    times = int(input("How many times would you like to bet?"))
    
    for x in range (0, times):
        money_bet = float(input("Enter how much you would like to bet."))
        while money_bet > total_money:
            money_bet = float(input("Not enough money. Please enter a lower number."))
        while money_bet <= 0:
            money_bet = float(input("Enter a value higher than 0."))
        total_money = total_money - money_bet
        type = input("Enter type: number, color, even/odd, range1 (1-12, 13-24, 25-36), range2 (1-18, 19-36), or column.")
        var = input("Enter what you want to bet on. (Ex: 3, first, 34, red, etc).")
        betHi = bet(type, var, money_bet)
        bets.append(betHi)
        number = random.randint(0, 37)
    print(f"The number was {nums[number].name}")
    
    

    for x in range(0, times):
        if bets[x].type == "number":
            if bets[x].input == nums[number].name:
                total_money = total_money + float(bets[x].price) + (17 * float(bets[x].price))
                print(f"Win! You got back ${float(bets[x].price) + (17 * float(bets[x].price))}")
            else:
                print(f"Bet failed. You lost {bets[x].price}")
        elif bets[x].type == "color":
            if bets[x].input == nums[number].color:
                total_money = total_money + float(bets[x].price) + (1 * float(bets[x].price))
                print(f"Win! You got back ${float(bets[x].price) + (1 * float(bets[x].price))}")
            else:
                print(f"Bet failed. You lost {bets[x].price}")
        elif bets[x].type == "even/odd":
            if bets[x].input == nums[number].evenOdd:
                total_money = total_money + float(bets[x].price) + (1 * float(bets[x].price))
                print(f"Win! You got back ${float(bets[x].price) + (1 * float(bets[x].price))}")
            else:
                print(f"Bet failed. You lost {bets[x].price}")
        elif bets[x].type == "range1":
            if bets[x].input == nums[number].range1:
                total_money = total_money + float(bets[x].price) + (2 * float(bets[x].price))
                print(f"Win! You got back ${float(bets[x].price) + (2 * float(bets[x].price))}")
            else:
                print(f"Bet failed. You lost {bets[x].price}")
        elif bets[x].type == "range2":
            if bets[x].input == nums[number].range2:
                total_money = total_money + float(bets[x].price) + (2 * float(bets[x].price))
                print(f"Win! You got back ${float(bets[x].price) + (2 * float(bets[x].price))}")
            else:
                print(f"Bet failed. You lost {bets[x].price}")
        elif bets[x].type == "column":
            if bets[x].input == nums[number].column:
                total_money = total_money + float(bets[x].price) + (2 * float(bets[x].price))
                print(f"Win! You got back ${float(bets[x].price) + (2 * float(bets[x].price))}")
            else:
                print(f"Bet failed. You lost {bets[x].price}")
    print(f"You now have ${total_money}left.")
    yn = input("Play another round? (y/n)")

print(f"You left the roulette table with ${total_money}")