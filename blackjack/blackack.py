import tkinter as tk
import random
root = tk.Tk()
root.title("Blackjack")
root.geometry("1000x700")
root.resizable(False, False)
from assets.card_deck_for_blackjack import *
from functools import partial

deck = list_of_cards


dealer_number_of_cards = 0
your_number_of_cards = 0

your_card_images = [blank_card_image, blank_card_image, blank_card_image, blank_card_image, blank_card_image, blank_card_image]
dealer_card_images = [blank_card_image, blank_card_image, blank_card_image, blank_card_image, blank_card_image, blank_card_image]


your_cards = []
dealer_cards = []

your_total = 0
dealer_total = 0

your_total_stringvar = tk.StringVar()
your_total_stringvar.set(0)

dealer_total_stringvar = tk.StringVar()
dealer_total_stringvar.set(0)


your_total_label = tk.Label(root, textvariable=your_total_stringvar, font=("Arial", 18))
dealer_total_label = tk.Label(root, textvariable=dealer_total_stringvar, font=("Arial", 18))

card_1_label = tk.Label(root, image=your_card_images[0])
card_2_label = tk.Label(root, image=your_card_images[1])
card_3_label = tk.Label(root, image=your_card_images[2])
card_4_label = tk.Label(root, image=your_card_images[3])
card_5_label = tk.Label(root, image=your_card_images[4])
card_6_label = tk.Label(root, image=your_card_images[5])

card_1_dealer_label = tk.Label(root, image=dealer_card_images[0])
card_2_dealer_label = tk.Label(root, image=dealer_card_images[1])
card_3_dealer_label = tk.Label(root, image=dealer_card_images[2])
card_4_dealer_label = tk.Label(root, image=dealer_card_images[3])
card_5_dealer_label = tk.Label(root, image=dealer_card_images[4])
card_6_dealer_label = tk.Label(root, image=dealer_card_images[5])

your_card_labels = [card_1_label, card_2_label, card_3_label, card_4_label, card_5_label, card_6_label]
dealer_card_labels = [card_1_dealer_label, card_2_dealer_label, card_3_dealer_label, card_4_dealer_label, card_5_dealer_label, card_6_dealer_label]
ace_drawn = False

selection = " "
def set_to_11():
    global your_cards
    global selection
    global your_number_of_cards
    global your_total
    global your_total_stringvar
    global deck
    global ace_drawn
    if your_cards[your_number_of_cards - 1].name == "ace":
        temp = your_cards[your_number_of_cards-1]._replace(number=11)
        your_cards[your_number_of_cards-1] = temp
        your_total = your_total + 11
    
        your_total_stringvar.set(str(your_total))
        print(your_total)
        
        if your_total > 21:
            lose()
        button_for_1.place_forget()
        button_for_11.place_forget()
        ace_drawn = False
def set_to_1():
    global your_cards
    global selection
    global your_number_of_cards
    global your_total
    global your_total_stringvar
    global deck
    global ace_drawn
    if your_cards[your_number_of_cards - 1].name == "ace":
        temp = your_cards[your_number_of_cards-1]._replace(number=1)
        your_cards[your_number_of_cards-1] = temp
        your_total = your_total + 1
    
        your_total_stringvar.set(str(your_total))
        print(your_total)
        
        if your_total > 21:
            lose()
        button_for_1.place_forget()
        button_for_11.place_forget()   
        ace_drawn = False 


button_for_1 = tk.Button(root, text = "1", font = ("Arial", 15), command=set_to_1)
button_for_11 = tk.Button(root, text = "11", font = ("Arial", 15), command=set_to_11)

def hit():
    global deck
    global your_cards
    global dealer_cards
    global your_number_of_cards
    global dealer_number_of_cards
    global your_card_images
    global dealer_card_images
    global your_total
    global dealer_total
    global dealer_total_label
    global your_total_label
    global dealer_total_stringvar
    global your_total_stringvar
    global selection
    global a
    global ace_drawn
    selection = " "
    a = random.randint(0, len(deck)-1)
    your_cards.append(deck[a])
    img = ImageTk.PhotoImage(Image.open(deck[a].image_path))
    your_card_images[your_number_of_cards] = img
    your_card_labels[your_number_of_cards].config(image=img)
    your_card_labels[your_number_of_cards].image = img
    if deck[a].name == 'ace':
        deck.pop(a)
        label_info = your_card_labels[your_number_of_cards].place_info()
        button_for_1.place(x=int((label_info['x'])), y=475)
        button_for_11.place(x=int((label_info['x']))+65, y=475)
        your_number_of_cards += 1
        ace_drawn = True

    else:
        your_total = your_total + int(deck[a].number)
        deck.pop(a)
        your_number_of_cards += 1
        your_total_stringvar.set(str(your_total))
        print(your_total)
        if your_total > 21:
            lose()






def stand():
    global deck
    global your_cards
    global dealer_cards
    global your_number_of_cards
    global dealer_number_of_cards
    global your_card_images
    global dealer_card_images
    global your_total
    global dealer_total
    global dealer_total_label
    global your_total_label
    global dealer_total_stringvar
    global your_total_stringvar

    while dealer_total <= 17:
        a = random.randint(0, len(deck)-1)
        dealer_cards.append(deck[a])
        dealer_card_images[dealer_number_of_cards] = list_of_cards[a]
        img = ImageTk.PhotoImage(Image.open(deck[a].image_path))
        dealer_card_images[dealer_number_of_cards] = img
        dealer_card_labels[dealer_number_of_cards].config(image=img)
        dealer_card_labels[dealer_number_of_cards].image = img
        if dealer_cards[dealer_number_of_cards - 1].name == "ace":
            if dealer_total <= 10:
                dealer_total = dealer_total + 11
            else:
                dealer_total = dealer_total + 1
        else:
            dealer_total = dealer_total + int(deck[a].number)
        deck.pop(a)
        dealer_number_of_cards += 1
        dealer_total_stringvar.set(str(dealer_total))
        print(dealer_total)
    if dealer_total > 21:
        win()
    else:
        if your_total > dealer_total:
            win()
        elif dealer_total > your_total:
            lose()
        else:
            tie()



def win():
    global dealer_total_stringvar
    global your_total_stringvar
    global your_total
    global dealer_total
    dealer_total_stringvar.set(f"You win! Dealer had {dealer_total}")
    your_total_stringvar.set(f"You win! You had {your_total}")

def lose():
    global dealer_total_stringvar
    global your_total_stringvar
    global your_total
    global dealer_total
    dealer_total_stringvar.set(f"You lose. Dealer had {dealer_total}")
    your_total_stringvar.set(f"You lose. You had {your_total}")
def tie():
    global dealer_total_stringvar
    global your_total_stringvar
    global your_total
    global dealer_total
    dealer_total_stringvar.set(f"It was a tie. You both had {dealer_total}")
    your_total_stringvar.set(f"It was a tie. You both had {your_total}")


card_1_label.place(x=0, y=513)
card_2_label.place(x=130, y=513)
card_3_label.place(x=260, y=513)
card_4_label.place(x=390, y=513)
card_5_label.place(x=520, y=513)
card_6_label.place(x=650, y=513)

card_1_dealer_label.place(x=0, y=0)
card_2_dealer_label.place(x=130, y=0)
card_3_dealer_label.place(x=260, y=0)
card_4_dealer_label.place(x=390, y=0)
card_5_dealer_label.place(x=520, y=0)
card_6_dealer_label.place(x=650, y=0)

your_total_label.place(x=400, y=450)
dealer_total_label.place(x=400, y=200)

hit_button = tk.Button(root, text="Hit", font=("Arial", 18), command=hit)
stand_button = tk.Button(root, text="Stand", font=("Arial", 18), command=stand)

hit_button.place(x=800, y=513)
stand_button.place(x=800, y=550)

hit()
hit()

a = random.randint(0, len(deck)-1)
dealer_cards.append(deck[a])
dealer_card_images[dealer_number_of_cards] = list_of_cards[a]
img = ImageTk.PhotoImage(Image.open(deck[a].image_path))
dealer_card_images[dealer_number_of_cards] = img
dealer_card_labels[dealer_number_of_cards].config(image=img)
dealer_card_labels[dealer_number_of_cards].image = img
dealer_total = dealer_total + int(deck[a].number)
deck.pop(a)
dealer_number_of_cards += 1
dealer_total_stringvar.set(str(dealer_total))





root.mainloop()