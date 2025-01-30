import tkinter as tk
from PIL import Image, ImageTk
from button_effects import highlight
import ttt
import pg
import bt
import toh


class MainMenu:
    def __init__(self):
        # window
        self.root = tk.Tk()
        self.root.geometry("600x550")
        self.root.title("MEAL.FUN")
        self.root.config(bg="white")

        # Pillow images
        src = "resources/BUTTONS/"
        self.images = [
            Image.open(f"{src}TicTacToe Button.png").resize((250, 150)),
            Image.open(f"{src}ParkingGarage Button.png").resize((250, 150)),
            Image.open(f"{src}BinaryTree Button.png").resize((250, 150)),
            Image.open(f"{src}TowerOfHanoi Button.png").resize((250, 150)),
        ]

        # current new window
        self.active_window = None

        # the rest
        self.unpack()

        # run window
        self.root.mainloop()

    def unpack(self):
        # headers
        tk.Label(self.root, text="MEAL.FUN", font=("Helvetica", 24, "bold"), bg="white", fg="black").pack(pady=15)
        tk.Label(self.root, text="Data Structures and Algorithms", font=("Helvetica", 12), bg="white", fg="gray").pack()

        # button frame
        menu_frame = tk.Frame(self.root, bg="white")
        menu_frame.pack(pady=20)

        # button data
        button_data = [
            {"name": "Tic Tac Toe", "image": self.images[0]},
            {"name": "Parking Garage", "image": self.images[1]},
            {"name": "Binary Tree", "image": self.images[2]},
            {"name": "Towers of Hanoi", "image": self.images[3]}
        ]

        # button actions
        def on_click(game):
            # prevents window duplication
            if self.active_window is None or not self.active_window.winfo_exists():
                self.active_window = tk.Toplevel()  # sub-window
                if game == "Tic Tac Toe":
                    ttt.TicTacToe(self.active_window)
                elif game == "Parking Garage":
                    pg.ParkingGarage(self.active_window)
                elif game == "Binary Tree":
                    bt.BinaryTree(self.active_window)
                elif game == "Towers of Hanoi":
                    toh.TowersOfHanoi(self.active_window)

        # creates buttons
        def create_button(frame, name, image, row, column, index):
            button = tk.Button(
                frame,
                image=image,
                borderwidth=0, highlightthickness=0,
                bg="white", activebackground="white",
                command=lambda: on_click(name)
            )
            button.image = image
            button.grid(row=row, column=column, padx=20, pady=10, ipadx=2, ipady=2, sticky="nsew")
            highlight(button_data[index]["image"], button)  # creates highlight effect
        for i, b in enumerate(button_data):
            create_button(menu_frame, b["name"], ImageTk.PhotoImage(b["image"]), i // 2, i % 2, i)

        # expandable buttons
        for i in range(2):
            menu_frame.grid_rowconfigure(i, weight=1)
            menu_frame.grid_columnconfigure(i, weight=1)

if __name__ == "__main__":
    MainMenu()
