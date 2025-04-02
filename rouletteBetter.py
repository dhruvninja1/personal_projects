import tkinter as tk
from collections import namedtuple
from functools import partial
import random


# Setup
root = tk.Tk()
root.title("Roulette")
root.geometry("1200x1000")
root.resizable(False, False)
num = namedtuple("num", ["name", "color", "evenOdd","range1", "range2", "column"]) 
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
bet = namedtuple("bet", ["type", "input", "price"])
bets = []

total_money = 10000
money_label = tk.Label(root, text=total_money, font=("Arial", 18))
money_label.place(x=800, y=800)
bets_text = tk.Text(root, height = 40, width = 70)
bets_text.insert(tk.END, "Bets: \n")
bets_text.place(x=650, y=200)
bets_text.config(state=tk.DISABLED)
number_widget = tk.Label(root, text = "The number was: None", font = ("Arial", 18))
number_widget.place(x=650, y=100)
betEntry = tk.Entry(root)
submit_button = tk.Button(root, text="Submit", height=3, width=3, command=lambda: hide_bet_entry())








def hide_bet_entry():
    global total_money
    betEntry.place_forget()
    submit_button.place_forget()
    price = betEntry.get()
    price = float(price)
    betEntry.delete(0, tk.END)
    betTemp = bet(type_global, input_global, price)
    bets.append(betTemp)
    total_money = total_money - price
    money_label.place_forget()
    money_label.config(text=total_money)
    money_label.place(x=800, y=800)
    bets_text.config(state=tk.NORMAL)
    bets_text.insert(tk.END, f"Bet: {type_global}, {input_global}.       Amount bet: ${round(price, 2)} \n")
    bets_text.config(state=tk.DISABLED)

type_global = " "
input_global = " "

def startBetting(typev, inpv):
    global type_global, input_global
    betEntry.place(x=375, y=950)
    submit_button.place(x=550, y=935)
    input_global = inpv
    type_global = typev


# Main function
def spin():
    global total_money
    global bets
    number = random.randint(0, 37)
    number_widget.config(text=f"The number was: {nums[number].name}")
    bets_text.config(state=tk.NORMAL)
    bets_text.delete("1.0", tk.END)
    bets_text.place(x=650, y=200)

    for x in range(0, len(bets)):
        if bets[x].type == "number":
            if bets[x].input == nums[number].name:
                bets_text.insert(tk.END, f"You won on your {bets[x].type}: {bets[x].input} bet! + ${(bets[x].price)*36} \n")
                total_money = total_money + ((bets[x].price)*36)
                money_label.config(text=total_money)
            else:
                bets_text.insert(tk.END, f"You lost on your {bets[x].type}: {bets[x].input} bet. - ${(bets[x].price)} \n")
        elif bets[x].type == "color":
            if bets[x].input == nums[number].color:
                bets_text.insert(tk.END, f"You won on your {bets[x].type}: {bets[x].input} bet! + ${(bets[x].price)*2} \n")
                total_money = total_money + ((bets[x].price)*2)
                money_label.config(text=total_money)
            else:
                bets_text.insert(tk.END, f"You lost on your {bets[x].type}: {bets[x].input} bet. - ${(bets[x].price)} \n")
        elif bets[x].type == "evenOdd":
            if bets[x].input == nums[number].evenOdd:
                bets_text.insert(tk.END, f"You won on your {bets[x].type}: {bets[x].input} bet! + ${(bets[x].price)*2} \n")
                total_money = total_money + ((bets[x].price)*2)
                money_label.config(text=total_money)
            else:
                bets_text.insert(tk.END, f"You lost on your {bets[x].type}: {bets[x].input} bet. - ${(bets[x].price)} \n")
        elif bets[x].type == "range1":
            if bets[x].input == nums[number].range1:
                bets_text.insert(tk.END, f"You won on your {bets[x].type}: {bets[x].input} bet! + ${(bets[x].price)*3} \n")
                total_money = total_money + ((bets[x].price)*3)
                money_label.config(text=total_money)
            else:
                bets_text.insert(tk.END, f"You lost on your {bets[x].type}: {bets[x].input} bet. - ${(bets[x].price)} \n")
        elif bets[x].type == "range2":
            if bets[x].input == nums[number].range2:
                bets_text.insert(tk.END, f"You won on your {bets[x].type}: {bets[x].input} bet! + ${(bets[x].price)*2} \n")
                total_money = total_money + ((bets[x].price)*2)
                money_label.config(text=total_money)
            else:
                bets_text.insert(tk.END, f"You lost on your {bets[x].type}: {bets[x].input} bet. - ${(bets[x].price)} \n")
        elif bets[x].type == "column":
            if bets[x].input == nums[number].column:
                bets_text.insert(tk.END, f"You won on your {bets[x].type}: {bets[x].input} bet! + ${(bets[x].price)*3} \n")
                total_money = total_money + ((bets[x].price)*3)
                money_label.config(text=total_money)
            else:
                bets_text.insert(tk.END, f"You lost on your {bets[x].type}: {bets[x].input} bet. - ${(bets[x].price)} \n")
    

    bets_text.insert(tk.END, "\n \nBets: \n")
    bets_text.config(state=tk.DISABLED)
    bets = []
    

            

go_button = tk.Button(root, text = "Go", fg = 'green', height = 5, width = 6, command=partial(spin))
go_button.place(x=1000, y=800)



# Creating elements

button_0 = tk.Button(root, text = "0", width = 8, height = 3, font=("Courier", 12, "bold"), fg = 'blue', command=partial(startBetting, "number", "0"))
button_00 = tk.Button(root, text = "00", width = 8, height = 3, font=("Courier", 12, "bold"), fg = 'blue', command=partial(startBetting, "number", "00"))
button_1 = tk.Button(root, text = "1", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[1].color, command=partial(startBetting, "number", "1"))
button_2 = tk.Button(root, text = "2", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[2].color, command=partial(startBetting, "number", "2"))
button_3 = tk.Button(root, text = "3", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[3].color, command=partial(startBetting, "number", "3"))
button_4 = tk.Button(root, text = "4", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[4].color, command=partial(startBetting, "number", "4"))
button_5 = tk.Button(root, text = "5", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[5].color, command=partial(startBetting, "number", "5"))
button_6 = tk.Button(root, text = "6", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[6].color, command=partial(startBetting, "number", "6"))
button_7 = tk.Button(root, text = "7", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[7].color, command=partial(startBetting, "number", "7"))
button_8 = tk.Button(root, text = "8", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[8].color, command=partial(startBetting, "number", "8"))
button_9 = tk.Button(root, text = "9", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[9].color, command=partial(startBetting, "number", "9"))
button_10 = tk.Button(root, text = "10", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[10].color, command=partial(startBetting, "number", "10"))
button_11 = tk.Button(root, text = "11", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[11].color, command=partial(startBetting, "number", "11"))
button_12 = tk.Button(root, text = "12", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[12].color, command=partial(startBetting, "number", "12"))
button_13 = tk.Button(root, text = "13", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[13].color, command=partial(startBetting, "number", "13"))
button_14 = tk.Button(root, text = "14", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[14].color, command=partial(startBetting, "number", "14"))
button_15 = tk.Button(root, text = "15", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[15].color, command=partial(startBetting, "number", "15"))
button_16 = tk.Button(root, text = "16", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[16].color, command=partial(startBetting, "number", "16"))
button_17 = tk.Button(root, text = "17", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[17].color, command=partial(startBetting, "number", "17"))
button_18 = tk.Button(root, text = "18", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[18].color, command=partial(startBetting, "number", "18"))
button_19 = tk.Button(root, text = "19", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[19].color, command=partial(startBetting, "number", "19"))
button_20 = tk.Button(root, text = "20", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[20].color, command=partial(startBetting, "number", "20"))
button_21 = tk.Button(root, text = "21", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[21].color, command=partial(startBetting, "number", "21"))
button_22 = tk.Button(root, text = "22", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[22].color, command=partial(startBetting, "number", "22"))
button_23 = tk.Button(root, text = "23", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[23].color, command=partial(startBetting, "number", "23"))
button_24 = tk.Button(root, text = "24", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[24].color, command=partial(startBetting, "number", "24"))
button_25 = tk.Button(root, text = "25", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[25].color, command=partial(startBetting, "number", "25"))
button_26 = tk.Button(root, text = "26", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[26].color, command=partial(startBetting, "number", "26"))
button_27 = tk.Button(root, text = "27", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[27].color, command=partial(startBetting, "number", "27"))
button_28 = tk.Button(root, text = "28", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[28].color, command=partial(startBetting, "number", "28"))
button_29 = tk.Button(root, text = "29", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[29].color, command=partial(startBetting, "number", "29"))
button_30 = tk.Button(root, text = "30", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[30].color, command=partial(startBetting, "number", "30"))
button_31 = tk.Button(root, text = "31", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[31].color, command=partial(startBetting, "number", "31"))
button_32 = tk.Button(root, text = "32", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[32].color, command=partial(startBetting, "number", "32"))
button_33 = tk.Button(root, text = "33", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[33].color, command=partial(startBetting, "number", "33"))
button_34 = tk.Button(root, text = "34", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[34].color, command=partial(startBetting, "number", "34"))
button_35 = tk.Button(root, text = "35", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[35].color, command=partial(startBetting, "number", "35"))
button_36 = tk.Button(root, text = "36", width = 4, height = 3, font=("Courier", 12, "bold"), fg = nums[36].color, command=partial(startBetting, "number", "36"))

button_firstColumn = tk.Button(root, text = "Col 1", width = 4, height = 3, font=("Courier", 12, "bold"), command=partial(startBetting, "column", "1"))
button_secondColumn = tk.Button(root, text = "Col 2", width = 4, height = 3, font=("Courier", 12, "bold"), command=partial(startBetting, "column", "2"))
button_thirdColumn = tk.Button(root, text = "Col 3", width = 4, height = 3, font=("Courier", 12, "bold"), command=partial(startBetting, "column", "3"))

button_firstThird = tk.Button(root, text = "1-12", width = 4, height = 16, font=("Courier", 10, "bold"), command=partial(startBetting, "range1", "first"))
button_secondThird = tk.Button(root, text = "13-24", width = 4, height = 16, font=("Courier", 10, "bold"), command=partial(startBetting, "range1", "second"))
button_thirdThird = tk.Button(root, text = "25-36", width = 4, height = 16, font=("Courier", 10, "bold"), command=partial(startBetting, "range1", "third"))

button_firstHalf = tk.Button(root, text = "1-18", width = 4, height = 8, font=("Courier", 10, "bold"), command=partial(startBetting, "range2", "first"))
button_secondHalf = tk.Button(root, text = "19-36", width = 4, height = 8, font=("Courier", 10, "bold"), command=partial(startBetting, "range2", "second"))

button_even = tk.Button(root, text = "Even", width = 4, height = 8, font=("Courier", 10, "bold"), command=partial(startBetting, "evenOdd", "even"))
button_odd = tk.Button(root, text = "Odd", width = 4, height = 8, font=("Courier", 10, "bold"), command=partial(startBetting, "evenOdd", "odd"))

button_red = tk.Button(root, text = "Red", width = 4, height = 8, font=("Courier", 10, "bold"), fg = 'red', command=partial(startBetting, "color", "red"))
button_black = tk.Button(root, text = "Black", width = 4, height = 8, font=("Courier", 10, "bold"), fg = 'black', command=partial(startBetting, "color", "black"))



# Placing elements

button_0.place(x=350, y=50)
button_00.place(x=460, y=50)
button_1.place(x=350, y=115)
button_2.place(x=425, y=115)
button_3.place(x=500, y=115)
button_4.place(x=350, y=175)
button_5.place(x=425, y=175)
button_6.place(x=500, y=175)
button_7.place(x=350, y=235)
button_8.place(x=425, y=235)
button_9.place(x=500, y=235)
button_10.place(x=350, y=295)
button_11.place(x=425, y=295)
button_12.place(x=500, y=295)
button_13.place(x=350, y=355)
button_14.place(x=425, y=355)
button_15.place(x=500, y=355)
button_16.place(x=350, y=415)
button_17.place(x=425, y=415)
button_18.place(x=500, y=415)
button_19.place(x=350, y=475)
button_20.place(x=425, y=475)
button_21.place(x=500, y=475)
button_22.place(x=350, y=535)
button_23.place(x=425, y=535)
button_24.place(x=500, y=535)
button_25.place(x=350, y=595)
button_26.place(x=425, y=595)
button_27.place(x=500, y=595)
button_28.place(x=350, y=655)
button_29.place(x=425, y=655)
button_30.place(x=500, y=655)
button_31.place(x=350, y=715)
button_32.place(x=425, y=715)
button_33.place(x=500, y=715)
button_34.place(x=350, y=775)
button_35.place(x=425, y=775)
button_36.place(x=500, y=775)

button_firstColumn.place(x=350, y=855)
button_secondColumn.place(x=425, y=855)
button_thirdColumn.place(x=500, y=855)

button_firstThird.place(x=275, y=120)
button_secondThird.place(x=275, y=362)
button_thirdThird.place(x=275, y=602)

button_firstHalf.place(x=200, y=115)
button_secondHalf.place(x=200, y=710)

button_even.place(x=200, y=230)
button_odd.place(x=200, y=593)

button_red.place(x=200, y=355)
button_black.place(x=200, y=475)


root.deiconify()
root.mainloop()