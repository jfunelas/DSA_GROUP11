import tkinter as tk
from tkinter import messagebox


class TowersOfHanoi:
    def __init__(self, root):
        self.window = root
        self.window.geometry("800x650")
        self.window.title("Tower of Hanoi")
        self.window.iconphoto(False, tk.PhotoImage(file="resources/ICON/TOH.png"))

        # header
        self.header = tk.Label(self.window, text="TOWERS OF HANOI", font=("Helvetica", 24, "bold"), fg="black")
        self.header.pack(pady=15)

        # Set up the canvas to expand with the window
        self.canvas = tk.Canvas(self.window, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.num_disks = 5  # Default number of disks
        self.rods = {1: [], 2: [], 3: []}  # Rods where disks will be stored
        self.disk_widths = []  # List to store disk widths
        self.disk_height = 20
        self.rod_positions = {1: 0, 2: 0, 3: 0}  # X positions for rods

        self.selected_disk = None  # To store the selected disk
        self.move_count = 0  # Counter for moves

        self.move_label = None
        self.create_controls()
        self.setup_game()
        self.update_rod_positions()
        self.draw_game()

        self.canvas.bind("<Button-1>", self.select_disk)
        self.canvas.bind("<ButtonRelease-1>", self.place_disk)
        self.window.bind("<Configure>", self.resize)

        self.window.mainloop()

    def create_controls(self):
        """Create buttons and controls for the game."""
        control_frame = tk.Frame(self.window)
        control_frame.pack()

        # Move Counter Label
        self.move_label = tk.Label(control_frame, text=f"Moves: {self.move_count}")
        self.move_label.grid(row=0, column=0, padx=10)

        # Reset Button
        reset_button = tk.Button(control_frame, text="Reset Game", command=self.reset_game)
        reset_button.grid(row=0, column=1, padx=10)

        # Add Disk Button
        add_disk_button = tk.Button(control_frame, text="Add Disk", command=self.add_disk)
        add_disk_button.grid(row=0, column=2, padx=10)

        # Remove Disk Button
        remove_disk_button = tk.Button(control_frame, text="Remove Disk", command=self.remove_disk)
        remove_disk_button.grid(row=0, column=3, padx=10)

    def setup_game(self):
        """Initialize game by placing disks on the first rod."""
        self.rods = {1: [], 2: [], 3: []}
        self.disk_widths = [40 + i * 20 for i in range(self.num_disks, 0, -1)]  # Disk widths
        for i in range(self.num_disks):
            self.rods[1].append(self.num_disks - i)  # Disk numbering from largest to smallest
        self.move_count = 0
        self.update_move_count()

    def update_rod_positions(self):
        """Update the positions of the rods based on the current canvas size."""
        width = self.canvas.winfo_width()
        self.rod_positions[1] = width // 4
        self.rod_positions[2] = width // 2
        self.rod_positions[3] = 3 * width // 4

    def draw_game(self):
        """Redraw the entire game state on the canvas."""
        self.canvas.delete("all")
        self.draw_rods()
        self.draw_disks()

    def draw_rods(self):
        """Draw rods as vertical lines."""
        height = self.canvas.winfo_height()
        for rod in self.rod_positions.values():
            self.canvas.create_line(rod, height // 4, rod, 3 * height // 4, width=4, fill="black")

    def draw_disks(self):
        """Draw disks on the rods."""
        height = self.canvas.winfo_height()
        for rod, disks in self.rods.items():
            x_center = self.rod_positions[rod]
            y_start = 3 * height // 4  # Base Y position
            for i, disk in enumerate(reversed(disks)):
                width = self.disk_widths[disk - 1]
                x1 = x_center - width // 2
                y1 = y_start - i * self.disk_height
                x2 = x_center + width // 2
                y2 = y1 - self.disk_height
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black", tags=f"disk-{disk}")
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(disk), fill="white")

    def select_disk(self, event):
        """Handle selecting a disk with the cursor."""
        clicked_items = self.canvas.find_withtag("current")
        if clicked_items:
            item = clicked_items[0]
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag.startswith("disk-"):
                    selected_disk = int(tag.split("-")[1])

                    # Ensure only the bottom disk of a rod can be selected
                    for rod, disks in self.rods.items():
                        if disks and disks[0] == selected_disk:  # Check if it's the bottom disk
                            self.selected_disk = selected_disk
                            self.canvas.itemconfig(item, fill="yellow")
                            return

    def place_disk(self, event):
        """Handle placing a selected disk onto a rod."""
        if self.selected_disk is None:
            return

        # Determine which rod was clicked
        clicked_rod = None
        for rod, x_pos in self.rod_positions.items():
            if abs(event.x - x_pos) < 50:
                clicked_rod = rod
                break

        if clicked_rod is None:
            self.reset_selection()
            return

        # Validate the move
        for rod, disks in self.rods.items():
            if self.selected_disk in disks:
                from_rod = rod
                break

        if not self.rods[clicked_rod] or self.rods[clicked_rod][0] < self.selected_disk:
            self.rods[from_rod].remove(self.selected_disk)
            self.rods[clicked_rod].insert(0, self.selected_disk)  # Place disk at the bottom of the new rod
            self.move_count += 1
            self.update_move_count()
            self.draw_game()
            self.check_win()
        else:
            messagebox.showerror("Invalid Move", "Cannot place a larger disk on top of a smaller disk.", parent=self.window)

        self.reset_selection()

    def reset_selection(self):
        """Reset the selected disk state."""
        self.selected_disk = None
        self.draw_game()

    def update_move_count(self):
        """Update the move counter display."""
        self.move_label.config(text=f"Moves: {self.move_count}")

    def check_win(self):
        """Check if the player has won the game."""
        if len(self.rods[3]) == self.num_disks:
            messagebox.showinfo("Congratulations!", "You solved the Tower of Hanoi!", parent=self.window)

    def reset_game(self):
        """Reset the game to its initial state."""
        self.setup_game()
        self.draw_game()

    def resize(self, event):
        """Handle window resizing."""
        self.update_rod_positions()
        self.draw_game()

    def add_disk(self):
        """Add a disk to the game."""
        if self.num_disks < 8:  # Limit the maximum number of disks
            self.num_disks += 1
            self.reset_game()
        else:
            messagebox.showinfo("Maximum Disks", "You cannot have more than 8 disks.", parent=self.window)

    def remove_disk(self):
        """Remove a disk from the game."""
        if self.num_disks > 1:  # Limit the minimum number of disks
            self.num_disks -= 1
            self.reset_game()
        else:
            messagebox.showinfo("Minimum Disks", "You must have at least 1 disk.", parent=self.window)
