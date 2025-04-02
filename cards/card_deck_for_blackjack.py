from collections import namedtuple
import tkinter as tk
from PIL import Image, ImageTk, Image


def change_image(image_to_change, image_path):
        img = Image.open(image_path)
        image_to_change.config(image=img)



card = namedtuple('card', ['name', 'number', 'suite', 'image_path'])


list_of_cards = [card('ace', '1', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/ace_of_clubs.png'), 
                 card('ace', '1', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/ace_of_diamonds.png'), 
                 card('ace', '1', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/ace_of_hearts.png'), 
                 card('ace', '1', 'spades', '/Users/dhruvsharma/projects/cards/card_images/ace_of_spades.png'),  
                 card('2', '2', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/2_of_clubs.png'), 
                 card('2', '2', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/2_of_diamonds.png'), 
                 card('2', '2', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/2_of_hearts.png'), 
                 card('2', '2', 'spades', '/Users/dhruvsharma/projects/cards/card_images/2_of_spades.png'), 
                 card('3', '3', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/3_of_clubs.png'), 
                 card('3', '3', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/3_of_diamonds.png'), 
                 card('3', '3', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/3_of_hearts.png'), 
                 card('3', '3', 'spades', '/Users/dhruvsharma/projects/cards/card_images/3_of_spades.png'), 
                 card('4', '4', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/4_of_clubs.png'), 
                 card('4', '4', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/4_of_diamonds.png'), 
                 card('4', '4', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/4_of_hearts.png'), 
                 card('4', '4', 'spades', '/Users/dhruvsharma/projects/cards/card_images/4_of_spades.png'), 
                 card('5', '5', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/5_of_clubs.png'), 
                 card('5', '5', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/5_of_diamonds.png'), 
                 card('5', '5', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/5_of_hearts.png'), 
                 card('5', '5', 'spades', '/Users/dhruvsharma/projects/cards/card_images/5_of_spades.png'), 
                 card('6', '6', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/6_of_clubs.png'), 
                 card('6', '6', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/6_of_diamonds.png'), 
                 card('6', '6', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/6_of_hearts.png'), 
                 card('6', '6', 'spades', '/Users/dhruvsharma/projects/cards/card_images/6_of_spades.png'), 
                 card('7', '7', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/7_of_clubs.png'), 
                 card('7', '7', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/7_of_diamonds.png'), 
                 card('7', '7', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/7_of_hearts.png'), 
                 card('7', '7', 'spades', '/Users/dhruvsharma/projects/cards/card_images/7_of_spades.png'), 
                 card('8', '8', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/8_of_clubs.png'), 
                 card('8', '8', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/8_of_diamonds.png'), 
                 card('8', '8', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/8_of_hearts.png'), 
                 card('8', '8', 'spades', '/Users/dhruvsharma/projects/cards/card_images/8_of_spades.png'), 
                 card('9', '9', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/9_of_clubs.png'), 
                 card('9', '9', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/9_of_diamonds.png'), 
                 card('9', '9', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/9_of_hearts.png'), 
                 card('9', '9', 'spades', '/Users/dhruvsharma/projects/cards/card_images/9_of_spades.png'), 
                 card('10', '10', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/10_of_clubs.png'), 
                 card('10', '10', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/10_of_diamonds.png'), 
                 card('10', '10', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/10_of_hearts.png'), 
                 card('10', '10', 'spades', '/Users/dhruvsharma/projects/cards/card_images/10_of_spades.png'), 
                 card('jack', '10', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/jack_of_clubs.png'), 
                 card('jack', '10', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/jack_of_diamonds.png'), 
                 card('jack', '10', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/jack_of_hearts.png'), 
                 card('jack', '10', 'spades', '/Users/dhruvsharma/projects/cards/card_images/jack_of_spades.png'), 
                 card('queen', '10', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/queen_of_clubs.png'), 
                 card('queen', '10', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/queen_of_diamonds.png'), 
                 card('queen', '10', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/queen_of_hearts.png'), 
                 card('queen', '10', 'spades', '/Users/dhruvsharma/projects/cards/card_images/queen_of_spades.png'), 
                 card('king', '10', 'clubs', '/Users/dhruvsharma/projects/cards/card_images/king_of_clubs.png'), 
                 card('king', '10', 'diamonds', '/Users/dhruvsharma/projects/cards/card_images/king_of_diamonds.png'), 
                 card('king', '10', 'hearts', '/Users/dhruvsharma/projects/cards/card_images/king_of_hearts.png'), 
                 card('king', '10', 'spades', '/Users/dhruvsharma/projects/cards/card_images/king_of_spades.png'), ]

blank_card_path = 'cards/card_images/blank_card.png'
d = Image.open(blank_card_path)
blank_card_image = ImageTk.PhotoImage(d)

