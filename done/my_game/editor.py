import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Editor")
root.geometry("1800x1100")
root.resizable(False, False)


image_pil_block = Image.open("my_game/tile_textures/platform.png")
image_block = ImageTk.PhotoImage(image_pil_block)








root.mainloop()


