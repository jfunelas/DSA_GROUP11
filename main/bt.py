import tkinter as tk
from PIL import Image, ImageTk
import os
import time




class BinaryTree:
    def __init__(self, root):
        self.window = root
        self.window.title("Binary Tree Game")
        self.window.iconphoto(False, tk.PhotoImage(file="resources/ICON/BT.png"))

        # tree setup
        self.root = None
        self.node_count = 0

        image_path = "resources/binary tree"
        # Load images in the correct color cycle order
        self.bg_image = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "BT_BACKGROUND.png")).resize((1200, 800)))
        self.node_images = [
            ImageTk.PhotoImage(Image.open(os.path.join(image_path, f"BT_NODE {i}.png")).resize((50, 50))) for i in range(1, 7)
        ]

        # Create canvas
        self.canvas = tk.Canvas(root, width=800, height=650)
        self.canvas.pack()
        self.canvas.create_image(600, 400, image=self.bg_image)
        self.draw_background()
        self.start()

    def insert(self, key):
        self.animate_insertion(key)
        color_index = self.node_count % 6  # Ensure colors follow the cycle correctly
        if self.root is None:
            self.root = TreeNode(key, color_index)
        else:
            self._insert(self.root, key, color_index)
        self.node_count += 1
        self.draw_tree()

    def _insert(self, node, key, color_index):
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, color_index)
            else:
                self._insert(node.left, key, color_index)
        else:
            if node.right is None:
                node.right = TreeNode(key, color_index)
            else:
                self._insert(node.right, key, color_index)

    def animate_insertion(self, key):
        x, y = 400, 50
        for _ in range(10):
            self.canvas.delete("animation")
            self.canvas.create_text(x, y, text=str(key), font=("Arial", 14), tags="animation")
            self.window.update()
            time.sleep(0.05)
            y += 5
        self.canvas.delete("animation")

    def draw_tree(self):
        self.canvas.delete("tree")
        if self.root:
            self._draw_tree(self.root, 400, 50, 120)

    def _draw_tree(self, node, x, y, x_offset=120):
        if node.left:
            self.canvas.create_line(x, y, x - x_offset, y + 100, fill="black", tags="tree")
            self._draw_tree(node.left, x - x_offset, y + 100, x_offset // 1.5)
        if node.right:
            self.canvas.create_line(x, y, x + x_offset, y + 100, fill="black", tags="tree")
            self._draw_tree(node.right, x + x_offset, y + 100, x_offset // 1.5)

        node_image = self.node_images[node.color_index]
        self.canvas.create_image(x, y, image=node_image, tags="tree")
        self.canvas.create_text(x, y, text=str(node.key), font=("Arial", 14), fill="white", tags="tree")

    def delete(self, key):
        self.root = self._delete(self.root, key)
        self.draw_tree()

    def _delete(self, node, key):
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def draw_background(self):
        # brick ground settings
        brick_width = 50
        brick_height = 30
        rows = 2  # number of rows of bricks
        columns = (1200 // brick_width) + 1  # fit bricks across width including left padding

        # draw bricks
        for row in range(rows):
            y_offset = 600 + (row * brick_height)
            for col in range(columns):
                x_offset = col * brick_width - 25  # shift left to add bricks in the gap

                # stagger every other row for a real brick pattern
                if row % 2 == 1:
                    x_offset += brick_width // 2

                self.canvas.create_rectangle(
                    x_offset, y_offset,
                    x_offset + brick_width, y_offset + brick_height,
                    fill="saddlebrown", outline="black"
                )

        # draw clouds
        self.canvas.create_oval(100, 50, 180, 100, fill="white", outline="white")  # left cloud
        self.canvas.create_oval(130, 30, 210, 80, fill="white", outline="white")  # left cloud overlap
        self.canvas.create_oval(750, 50, 650, 100, fill="white", outline="white")  # right cloud
        self.canvas.create_oval(780, 30, 680, 80, fill="white", outline="white")  # right cloud overlap

        pipe_width = 60
        pipe_height = 200  # Increased pipe height
        top_width = 80
        top_height = 30

        left_pipe_x = 150
        self.canvas.create_rectangle(left_pipe_x, 700 - pipe_height, left_pipe_x + pipe_width, 700, fill="green", outline="black")
        self.canvas.create_rectangle(left_pipe_x - 10, 700 - pipe_height, left_pipe_x - 10 + top_width, 700 - pipe_height + top_height, fill="green", outline="black")

        right_pipe_x = 600
        self.canvas.create_rectangle(right_pipe_x, 700 - pipe_height, right_pipe_x + pipe_width, 700, fill="green", outline="black")
        self.canvas.create_rectangle(right_pipe_x - 10, 700 - pipe_height, right_pipe_x - 10 + top_width, 700 - pipe_height + top_height, fill="green", outline="black")


        # draw birds
        bird_positions = [(200, 150), (90, 180), (600, 120), (450, 350)]
        for x, y in bird_positions:
            self.draw_bird(x, y)

        # function to draw a simple bird at a given position

    def draw_bird(self, x, y):
        # draw the wings using arcs
        self.canvas.create_arc(x, y, x + 40, y + 30, start=0, extent=180, style=tk.ARC, outline="black", width=2)
        self.canvas.create_arc(x + 20, y, x + 60, y + 30, start=0, extent=180, style=tk.ARC, outline="black", width=2)

    def start(self):
        frame = tk.Frame(self.window)
        frame.pack()
        tk.Label(frame, text="Key:").grid(row=0, column=0)
        entry = tk.Entry(frame)
        entry.grid(row=0, column=1)

        def insert_key():
            key = entry.get()
            if key.isdigit():
                self.insert(int(key))
                entry.delete(0, tk.END)

        def delete_key():
            key = entry.get()
            if key.isdigit():
                self.delete(int(key))
                entry.delete(0, tk.END)

        entry.bind("<Return>", lambda event: insert_key())
        tk.Button(frame, text="Insert", command=insert_key).grid(row=0, column=2)
        tk.Button(frame, text="Delete", command=delete_key).grid(row=0, column=3)
        self.window.mainloop()


class TreeNode:
    def __init__(self, key, color_index):
        self.key = key
        self.left = None
        self.right = None
        self.color_index = color_index