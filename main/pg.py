import tkinter as tk
from PIL import Image, ImageTk
import random
import string


class ParkingGarage:
    def __init__(self, root):
        # window
        self.window = root
        self.window.geometry("800x650")
        self.window.title("Parking Garage")
        self.window.config(bg="#f0f0f0")
        self.window.iconphoto(False, tk.PhotoImage(file="resources/ICON/PG.png"))

        # pillow images
        src = "resources/parking garage/"
        self.cw, self.ch = 348, 416
        resize = 10
        self.w, self.h = int(741/resize), int(337/resize)
        rs = (self.w, self.h)
        self.images = [
            Image.open(f"{src}PG_STACK.png").resize((self.cw, self.ch)),
            Image.open(f"{src}PG_QUEUE.png").resize((self.cw, self.ch)),
            Image.open(f"{src}PG_CAR1.png").resize(rs),
            Image.open(f"{src}PG_CAR2.png").resize(rs),
            Image.open(f"{src}PG_CAR3.png").resize(rs),
            Image.open(f"{src}PG_CAR4.png").resize(rs),
            Image.open(f"{src}PG_CAR5.png").resize(rs),
            Image.open(f"{src}PG_CAR6.png").resize(rs),
            Image.open(f"{src}PG_CAR7.png").resize(rs),
            Image.open(f"{src}PG_CAR8.png").resize(rs),
            Image.open(f"{src}PG_CAR9.png").resize(rs),
            Image.open(f"{src}PG_CAR10.png").resize(rs),
            Image.open(f"{src}PG_CAR11.png").resize(rs)
        ]

        # convert to Tk images
        self.tk_images = [ImageTk.PhotoImage(img) for img in self.images]

        # garage setup
        self.garage = []
        self.mode = None  # "stack" or "queue"
        self.tally = [0, 0]  # arrival, departure
        f = ("Arial", 12)

        # header
        self.label = tk.Label(root, text="PARKING GARAGE", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        self.label.pack(pady=10)

        # Canvas for Visualization
        self.canvas = tk.Canvas(root, width=self.cw, height=self.ch, bg="white", bd=2, relief="solid")
        self.canvas.pack(pady=20)

        # Display Garage Status
        self.tally_label = tk.Label(root, text="Arrival: 0 | Departure: 0", font=f, bg="#f0f0f0")
        self.tally_label.pack(pady=10)

        # frame
        self.frame = tk.Frame(root, bg="black")
        self.frame.pack()
        self.stack_button = tk.Button(self.frame, text="Stack", font=f, command=lambda: self.change_mode("stack"))
        self.stack_button.grid(row=0, column=0, sticky="nsew")
        self.queue_button = tk.Button(self.frame, text="Queue", font=f, command=lambda: self.change_mode("queue"))
        self.queue_button.grid(row=0, column=1, sticky="nsew")

        # Add and Remove Car Buttons
        self.add_button = tk.Button(self.frame, text="Add Car", font=f, command=self.add_car, state=tk.DISABLED)
        self.add_button.grid(row=0, column=2, sticky="nsew")

        self.remove_button = tk.Button(self.frame, text="Remove Car", font=f, command=self.remove_car, state=tk.DISABLED)
        self.remove_button.grid(row=0, column=3, sticky="nsew")

        self.window.mainloop()

    def change_mode(self, mode):
        if mode == "stack":
            self.stack_button.config(state=tk.DISABLED)
            self.queue_button.config(state=tk.NORMAL)
        elif mode == "queue":
            self.stack_button.config(state=tk.NORMAL)
            self.queue_button.config(state=tk.DISABLED)
        self.mode = mode
        self.tally = [0, 0]
        self.garage = []
        self.update_buttons()
        self.update_tally_label()
        self.draw_garage()

    def update_buttons(self):
        if self.mode:
            self.add_button.config(state=tk.NORMAL)
            self.remove_button.config(state=tk.NORMAL)
        else:
            self.add_button.config(state=tk.DISABLED)
            self.remove_button.config(state=tk.DISABLED)

    def add_car(self):
        if len(self.garage) >= 5:
            self.tally_label.config(text="Garage is full! Cannot add more cars.")
            return
        self.tally[0] += 1
        car = Car()
        self.garage.append(car)
        self.update_tally_label()
        self.draw_garage()

    def remove_car(self):
        if not self.garage:
            self.tally_label.config(text="Garage is empty! No cars to remove.")
            return

        self.tally[1] += 1
        if self.mode == "stack":
            self.garage.pop()  # Remove the last car
        elif self.mode == "queue":
            self.garage.pop(0)  # Remove the first car

        self.update_tally_label()
        self.draw_garage()

    def update_tally_label(self):
        self.tally_label.config(text=f"Arrival: {self.tally[0]} | Departure: {self.tally[1]}")

    def draw_garage(self):
        self.canvas.delete("all")  # Clear the canvas
        a = 4
        if self.mode == "stack":
            x, y = 90, 340  # Starting position for the first car
            self.canvas.create_image(self.cw/2 + a, self.ch/2 + a, image=self.tk_images[0])
        elif self.mode == "queue":
            x, y = 150, 315
            self.canvas.create_image(self.cw/2 + a, self.ch/2 + a, image=self.tk_images[1])

        for i, car in enumerate(self.garage):
            # Draw a rectangle for each car
            self.canvas.create_image(
                x, y, image=self.tk_images[car.index+2]
            )
            # Add car ID text
            self.canvas.create_text(
                x + self.w / 2, y + self.h / 2, text=car, font=("Arial", 10), fill="white"
            )
            y -= self.h + 18  # Move to the next position


class Car:
    def __init__(self, generic=False):
        self.model_list = [
            "Red",
            "Orange",
            "Yellow",
            "Green",
            "Blue",
            "Violet",
            "Black",
            "Brown",
            "Pink",
            "White",
            "Gray",
        ]
        if generic:
            self.model = "Blue"
            self.plate_number = "ABC 1234"
        else:
            self.index = random.randint(0, 10)
            self.model = self.model_list[self.index]
            self.plate_number = self.generate_plate_number()
        self.image = None

    @staticmethod
    def generate_plate_number():
        r1 = random.choice(string.ascii_uppercase)
        r2 = random.choice(string.ascii_uppercase)
        r3 = random.choice(string.ascii_uppercase)
        abc = f"{r1}{r2}{r3}"
        num = random.randint(1000, 9999)
        return f"{abc} {num}"

    def __str__(self):
        return str(f"{self.plate_number}")
