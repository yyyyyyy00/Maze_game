import tkinter as tk
from algorithms import bfs
import random
from tkinter import messagebox

class Grid:
    def __init__(self, master, rows, cols, cell_size):
        # Initialize variables
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # Create canvas
        self.canvas = tk.Canvas(master,
                                width=cols * cell_size,
                                height=rows * cell_size)
        self.canvas.pack()

        # Initialize game state
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.end = None
        self.player_pos = None
        self.player_path = []

        self.current_key = None
        self.movement_job = None
        self.game_over = False

        # Bind input events
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.on_key_press)
        self.canvas.bind("<KeyRelease>", self.on_key_release)

        # Timer
        self.time_limit = self.get_time_limit(rows, cols)
        self.remaining_time = self.time_limit
        self.timer_id = None
        self.time_label = tk.Label(master, text=f"Time Left: {self.remaining_time}s", font=("Arial", 12))
        self.time_label.pack()

        self.draw_grid()

        

    def draw_grid(self):
        # Clear and redraw grid
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size

                # cell color
                if self.grid[i][j] == 1:
                    fill = "black"
                elif (i, j) == self.end:
                    fill = "red"
                elif (i, j) == self.player_pos and (i, j) == self.start:
                    fill = "green"
                elif (i, j) == self.player_pos:
                    fill = "blue"
                elif (i, j) == self.start:
                    fill = "green"
                elif (i, j) in self.player_path:
                    fill = "orange"
                else:
                    fill = "white"

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="gray")

    def on_key_press(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.current_key = event.keysym
            if self.movement_job is None:
                self.handle_continuous_movement()

    def on_key_release(self, event):
        if event.keysym == self.current_key:
            self.current_key = None
            if self.movement_job:
                self.master.after_cancel(self.movement_job)
                self.movement_job = None

    def handle_continuous_movement(self):
        if self.current_key is None or self.game_over:
            self.movement_job = None
            return

        direction = {
            "Up": (-1, 0), "Down": (1, 0),
            "Left": (0, -1), "Right": (0, 1)
        }.get(self.current_key)

        if direction:
            self.move_player(*direction)

        # ====CUSTOMIZABLE====: Adjust movement speed (milliseconds between steps)
        self.movement_speed = 80
        self.movement_job = self.master.after(self.movement_speed, self.handle_continuous_movement)

    def move_player(self, dr, dc):
        if not self.player_pos or self.game_over:
            return

        r, c = self.player_pos
        nr, nc = r + dr, c + dc

        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != 1:
            next_pos = (nr, nc)
            if len(self.player_path) >= 2 and self.player_path[-2] == next_pos:
                self.player_path.pop()
            else:
                self.player_path.append(next_pos)

            self.player_pos = next_pos
            self.draw_grid()

            if self.player_pos == self.end:
                self.game_over = True
                self.show_end_menu()

    def generate_perfect_maze(self):
        # ====CUSTOMIZABLE====: You could replace this with a different maze generation algorithm
        self.player_path = []
        self.grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        def in_bounds(r, c):
            return 0 <= r < self.rows and 0 <= c < self.cols

        def carve_passages_from(r, c, visited):
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if in_bounds(nr, nc) and (nr, nc) not in visited:
                    mid_r, mid_c = r + dr // 2, c + dc // 2
                    self.grid[nr][nc] = 0
                    self.grid[mid_r][mid_c] = 0
                    visited.add((nr, nc))
                    carve_passages_from(nr, nc, visited)

        # Start from a random cell
        start_r = random.randrange(0, self.rows, 2)
        start_c = random.randrange(0, self.cols, 2)
        visited = {(start_r, start_c)}
        self.grid[start_r][start_c] = 0
        carve_passages_from(start_r, start_c, visited)

        # Choose random start and end
        empty_cells = [(r, c) for r in range(self.rows)
                       for c in range(self.cols) if self.grid[r][c] == 0]
        self.start = random.choice(empty_cells)
        self.end = random.choice([cell for cell in empty_cells if cell != self.start])
        self.grid[self.start[0]][self.start[1]] = 2
        self.grid[self.end[0]][self.end[1]] = 3

        self.player_pos = self.start
        self.player_path = [self.start]
        self.draw_grid()
        self.remaining_time = self.time_limit
        self.start_timer()
        self.game_over = False

    def show_end_menu(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

        popup = tk.Toplevel()
        popup.title("Victory!")
        popup.geometry("300x150")
        tk.Label(popup, text="You reached the end!\nWhat would you like to do?", font=("Arial", 12)).pack(pady=15)

        tk.Button(popup, text="Continue (same level)", width=20, command=lambda: [popup.destroy(), self.generate_perfect_maze()]).pack(pady=2)
        tk.Button(popup, text="Choose Level", width=20, command=lambda: [popup.destroy(), self.master.destroy(), __import__("main").main()]).pack(pady=2)
        tk.Button(popup, text="Exit", width=20, command=lambda: [popup.destroy(), self.master.quit(), self.master.destroy()]).pack(pady=2)

    def get_time_limit(self, rows, cols):
        # ====CUSTOMIZABLE====: Define time limits based on grid size
        area = rows * cols
        if area <= 150:
            return 40
        elif area <= 600:
            return 80
        return 120

    def start_timer(self):
        if self.remaining_time <= 0:
            self.handle_timeout()
            return
        self.time_label.config(text=f"Time Left: {self.remaining_time}s")
        self.remaining_time -= 1
        self.timer_id = self.master.after(1000, self.start_timer)

    def handle_timeout(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

        # Show final solution 
        if self.start and self.end:
            path = bfs(self.grid, self.start, self.end)
            if path:
                for r, c in path:
                    if (r, c) != self.start and (r, c) != self.end:
                        x1 = c * self.cell_size
                        y1 = r * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="purple", outline="gray")

        popup = tk.Toplevel()
        popup.title("Time's Up!")
        popup.geometry("300x150")
        tk.Label(popup, text="You ran out of time!\nWhat would you like to do?", font=("Arial", 12)).pack(pady=15)

        tk.Button(popup, text="Try Again (same level)", width=20, command=lambda: [popup.destroy(), self.generate_perfect_maze()]).pack(pady=2)
        tk.Button(popup, text="Choose Level", width=20, command=lambda: [popup.destroy(), self.master.destroy(), __import__("main").main()]).pack(pady=2)
        tk.Button(popup, text="Exit", width=20, command=lambda: [popup.destroy(), self.master.quit(), self.master.destroy()]).pack(pady=2)
