import tkinter as tk
from PIL import Image, ImageTk
from random import choice


class TicTacToe:
    def __init__(self, root):
        # window
        self.window = root
        self.window.geometry("800x650")
        self.window.title("Tic-Tac-Toe")
        self.window.iconphoto(False, tk.PhotoImage(file="resources/ICON/TTT.png"))

        # Pillow images
        src = "resources/tic tac toe/"
        self.images = [
            Image.open(f"{src}TTT_BACKGROUND.png"),
            Image.open(f"{src}empty.png").resize((100, 100)),
            Image.open(f"{src}cross.png").resize((100, 100)),
            Image.open(f"{src}circle.png").resize((100, 100)),
            Image.open(f"{src}cross_w.png").resize((100, 100)),
            Image.open(f"{src}circle_w.png").resize((100, 100)),
            Image.open(f"{src}cross_d.png").resize((100, 100)),
            Image.open(f"{src}circle_d.png").resize((100, 100))
        ]

        # convert to Tk images
        self.tk_images = [ImageTk.PhotoImage(img) for img in self.images]

        # background image
        tk.Label(root, image=self.tk_images[0]).place(x=0, y=0, relwidth=1, relheight=1)

        # game state
        self.board = [0] * 9
        self.current_player = 1  # 1 for X, 2 for O
        self.game_over = False
        self.buttons = []
        self.mode = "com"

        # headers
        self.header = tk.Label(root, text="TIC-TAC-TOE", font=("Helvetica", 24, "bold"),
                               bg="#EE82EE", borderwidth=2, relief="sunken", fg="black")
        self.header.pack(pady=15, ipadx=5)

        # button frame
        self.board_frame = tk.Frame(root, bg="black")
        self.board_frame.pack(pady=20)
        self.create_buttons()

        # settings frame
        self.settings_frame = tk.Frame(root)
        self.settings_frame.pack(pady=20)
        restart = tk.Button(
            self.settings_frame,
            text="RESTART GAME",
            command=lambda: self.restart_game()
        )
        restart.grid(row=0, column=0, sticky="nsew")
        self.computer = tk.Button(
            self.settings_frame,
            text="COMPUTER",
            command=lambda: self.change_mode("com"),
            state=tk.DISABLED
        )
        self.computer.grid(row=0, column=1, sticky="nsew")
        self.player = tk.Button(
            self.settings_frame,
            text="PLAYER",
            command=lambda: self.change_mode("pvp")
        )
        self.player.grid(row=0, column=2, sticky="nsew")

        # run window
        self.window.mainloop()

    def create_buttons(self):
        for i in range(9):
            button = tk.Button(
                self.board_frame,
                image=self.tk_images[1],
                borderwidth=12, highlightthickness=0,
                bg="violet", activebackground="white",
                command=lambda i=i: self.on_click(i)
            )
            button.grid(row=i // 3, column=i % 3, padx=2, pady=2, ipadx=2, ipady=2, sticky="nsew")
            self.buttons.append(button)

    def change_mode(self, mode):
        if mode == "com":
            self.computer.config(state=tk.DISABLED)
            self.player.config(state=tk.NORMAL)
        elif mode == "pvp":
            self.computer.config(state=tk.NORMAL)
            self.player.config(state=tk.DISABLED)
        self.mode = mode
        self.restart_game()

    def on_click(self, index):
        if not self.game_over and self.board[index] == 0:
            self.board[index] = self.current_player
            self.buttons[index].config(image=self.tk_images[self.current_player+1])
            if self.check_win():
                self.header.config(text=f"Player {self.current_player} wins!")
            elif self.check_draw():
                self.header.config(text="It's a draw!", bg="lightyellow")
            else:
                if self.current_player == 1:
                    self.current_player = 2
                elif self.current_player == 2:
                    self.current_player = 1
                if self.mode == "com":
                    self.computer_move()
                elif self.mode == "pvp":
                    self.header.config(text=f"Player {self.current_player}'s turn...")

    def computer_move(self):
        if not self.game_over:
            move = choice([i for i, spot in enumerate(self.board) if spot == 0])
            self.board[move] = 2
            self.buttons[move].config(image=self.tk_images[3])
            if self.check_win():
                self.header.config(text="Computer wins!")
            elif self.check_draw():
                self.header.config(text="It's a draw!", bg="lightyellow")
            else:
                self.current_player = 1  # Switch back to player

    def check_win(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]
        for w in win_conditions:
            if self.board[w[0]] == self.board[w[1]] == self.board[w[2]] != 0:
                self.game_over = True
                self.header.config(bg="lightgreen")
                for i in w:
                    self.buttons[i].config(bg="lightgreen", image=self.tk_images[self.current_player+3])
                return True
        return False

    def check_draw(self):
        if 0 not in self.board:
            self.game_over = True
            for i, b in enumerate(self.board):
                self.buttons[i].config(bg="lightyellow", image=self.tk_images[b+5])
            return True

    def restart_game(self):
        for b in self.buttons:
            b.config(state=tk.NORMAL)
        self.board = [0]*9
        self.current_player = 1
        self.game_over = False
        self.header.config(text="TIC-TAC-TOE", bg="violet")
        for button in self.buttons:
            button.config(image=self.tk_images[1], bg="violet")
