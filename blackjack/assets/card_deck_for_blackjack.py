from collections import namedtuple
import tkinter as tk
from PIL import Image, ImageTk, Image


def change_image(image_to_change, image_path):
        img = Image.open(image_path)
        image_to_change.config(image=img)


card = namedtuple('card', ['name', 'number', 'suite', 'image_path'])


list_of_cards = [card('ace', '1', 'clubs', 'blackjack/assets/ace_of_clubs.png'), 
                 card('ace', '1', 'diamonds', 'blackjack/assets/ace_of_diamonds.png'), 
                 card('ace', '1', 'hearts', 'blackjack/assets/ace_of_hearts.png'), 
                 card('ace', '1', 'spades', 'blackjack/assets/ace_of_spades.png'),  
                 card('2', '2', 'clubs', 'blackjack/assets/2_of_clubs.png'), 
                 card('2', '2', 'diamonds', 'blackjack/assets/2_of_diamonds.png'), 
                 card('2', '2', 'hearts', 'blackjack/assets/2_of_hearts.png'), 
                 card('2', '2', 'spades', 'blackjack/assets/2_of_spades.png'), 
                 card('3', '3', 'clubs', 'blackjack/assets/3_of_clubs.png'), 
                 card('3', '3', 'diamonds', 'blackjack/assets/3_of_diamonds.png'), 
                 card('3', '3', 'hearts', 'blackjack/assets/3_of_hearts.png'), 
                 card('3', '3', 'spades', 'blackjack/assets/3_of_spades.png'), 
                 card('4', '4', 'clubs', 'blackjack/assets/4_of_clubs.png'), 
                 card('4', '4', 'diamonds', 'blackjack/assets/4_of_diamonds.png'), 
                 card('4', '4', 'hearts', 'blackjack/assets/4_of_hearts.png'), 
                 card('4', '4', 'spades', 'blackjack/assets/4_of_spades.png'), 
                 card('5', '5', 'clubs', 'blackjack/assets/5_of_clubs.png'), 
                 card('5', '5', 'diamonds', 'blackjack/assets/5_of_diamonds.png'), 
                 card('5', '5', 'hearts', 'blackjack/assets/5_of_hearts.png'), 
                 card('5', '5', 'spades', 'blackjack/assets/5_of_spades.png'), 
                 card('6', '6', 'clubs', 'blackjack/assets/6_of_clubs.png'), 
                 card('6', '6', 'diamonds', 'blackjack/assets/6_of_diamonds.png'), 
                 card('6', '6', 'hearts', 'blackjack/assets/6_of_hearts.png'), 
                 card('6', '6', 'spades', 'blackjack/assets/6_of_spades.png'), 
                 card('7', '7', 'clubs', 'blackjack/assets/7_of_clubs.png'), 
                 card('7', '7', 'diamonds', 'blackjack/assets/7_of_diamonds.png'), 
                 card('7', '7', 'hearts', 'blackjack/assets/7_of_hearts.png'), 
                 card('7', '7', 'spades', 'blackjack/assets/7_of_spades.png'), 
                 card('8', '8', 'clubs', 'blackjack/assets/8_of_clubs.png'), 
                 card('8', '8', 'diamonds', 'blackjack/assets/8_of_diamonds.png'), 
                 card('8', '8', 'hearts', 'blackjack/assets/8_of_hearts.png'), 
                 card('8', '8', 'spades', 'blackjack/assets/8_of_spades.png'), 
                 card('9', '9', 'clubs', 'blackjack/assets/9_of_clubs.png'), 
                 card('9', '9', 'diamonds', 'blackjack/assets/9_of_diamonds.png'), 
                 card('9', '9', 'hearts', 'blackjack/assets/9_of_hearts.png'), 
                 card('9', '9', 'spades', 'blackjack/assets/9_of_spades.png'), 
                 card('10', '10', 'clubs', 'blackjack/assets/10_of_clubs.png'), 
                 card('10', '10', 'diamonds', 'blackjack/assets/10_of_diamonds.png'), 
                 card('10', '10', 'hearts', 'blackjack/assets/10_of_hearts.png'), 
                 card('10', '10', 'spades', 'blackjack/assets/10_of_spades.png'), 
                 card('jack', '10', 'clubs', 'blackjack/assets/jack_of_clubs.png'), 
                 card('jack', '10', 'diamonds', 'blackjack/assets/jack_of_diamonds.png'), 
                 card('jack', '10', 'hearts', 'blackjack/assets/jack_of_hearts.png'), 
                 card('jack', '10', 'spades', 'blackjack/assets/jack_of_spades.png'), 
                 card('queen', '10', 'clubs', 'blackjack/assets/queen_of_clubs.png'), 
                 card('queen', '10', 'diamonds', 'blackjack/assets/queen_of_diamonds.png'), 
                 card('queen', '10', 'hearts', 'blackjack/assets/queen_of_hearts.png'), 
                 card('queen', '10', 'spades', 'blackjack/assets/queen_of_spades.png'), 
                 card('king', '10', 'clubs', 'blackjack/assets/king_of_clubs.png'), 
                 card('king', '10', 'diamonds', 'blackjack/assets/king_of_diamonds.png'), 
                 card('king', '10', 'hearts', 'blackjack/assets/king_of_hearts.png'), 
                 card('king', '10', 'spades', 'blackjack/assets/king_of_spades.png'), ]

blank_card_path = 'cards/card_images/blank_card.png'
d = Image.open(blank_card_path)
blank_card_image = ImageTk.PhotoImage(d)

