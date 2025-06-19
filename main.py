import tkinter as tk
from grid import Grid

# ====CUSTOMIZABLE====: You can adjust default cell size
DEFAULT_CELL_SIZE = 25


class DifficultySelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Game - Select Difficulty")
        self.root.geometry("300x200")

        tk.Label(root, text="Choose Difficulty", font=("Arial", 14)).pack(pady=20)

        # Buttons for difficulty options
        tk.Button(root, text="Easy", width=20, command=self.start_easy).pack(pady=5)
        tk.Button(root, text="Medium", width=20, command=self.start_medium).pack(pady=5)
        tk.Button(root, text="Hard", width=20, command=self.start_hard).pack(pady=5)

    def start_game(self, rows, cols):
        # Close current window and open game window
        self.root.destroy()
        game_window = tk.Tk()
        game_window.title("Maze Game")
        Grid(game_window, rows, cols, DEFAULT_CELL_SIZE).generate_perfect_maze()
        game_window.mainloop()

    # ====CUSTOMIZABLE====: You can adjust grid size
    def start_easy(self):
        self.start_game(11, 11)  # Small grid

    def start_medium(self):
        self.start_game(21, 21)  # Medium grid

    def start_hard(self):
        self.start_game(31, 31)  # Large grid


def main():
    # Entry point of the application
    root = tk.Tk()
    DifficultySelector(root)
    root.mainloop()


if __name__ == "__main__":
    main()
