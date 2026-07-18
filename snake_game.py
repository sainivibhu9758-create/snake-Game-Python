import random
import tkinter as tk


CELL = 22
COLS = ROWS = 20
BOARD = CELL * COLS
SPEED = 105

BG = "#0b100e"
CARD = "#17231d"
CARD_EDGE = "#2c4034"
LCD = "#c9e88d"
LCD_GRID = "#b5d17d"
INK = "#17351f"
SNAKE = "#23683a"
ACCENT = "#e5ff9b"
MUTED = "#a4b3a4"
RED = "#f05d5e"


class ModernSnake:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake — Nokia Edition")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.running = False
        self.token = 0
        self.high_score = 0
        self.build_ui()
        self.bind_keys()
        self.show_menu()
        self.root.mainloop()

    def build_ui(self):
        wrapper = tk.Frame(self.root, bg=BG, padx=24, pady=22)
        wrapper.pack()

        header = tk.Frame(wrapper, bg=BG)
        header.pack(fill="x", pady=(0, 14))
        tk.Label(header, text="SNAKE", bg=BG, fg=ACCENT,
                 font=("Arial", 22, "bold")).pack(side="left")
        tk.Label(header, text="NOKIA EDITION", bg=BG, fg=MUTED,
                 font=("Arial", 9, "bold")).pack(side="left", padx=9, pady=(7, 0))
        self.status = tk.Label(header, text="READY", bg="#263b2c", fg=ACCENT,
                               font=("Arial", 9, "bold"), padx=9, pady=4)
        self.status.pack(side="right")

        hud = tk.Frame(wrapper, bg=CARD, highlightthickness=1,
                       highlightbackground=CARD_EDGE, padx=14, pady=10)
        hud.pack(fill="x", pady=(0, 12))
        self.score_value = self.stat(hud, "SCORE", "000")
        self.score_value.pack(side="left")
        self.best_value = self.stat(hud, "BEST", "000")
        self.best_value.pack(side="right")

        self.canvas = tk.Canvas(wrapper, width=BOARD, height=BOARD, bg=LCD,
                                highlightthickness=7, highlightbackground="#516b3c")
        self.canvas.pack()

        controls = tk.Frame(wrapper, bg=BG)
        controls.pack(fill="x", pady=(14, 0))
        self.button(controls, "START", self.start).pack(side="left", expand=True, padx=(0, 5))
        self.button(controls, "RESTART", self.restart).pack(side="left", expand=True, padx=5)
        self.button(controls, "EXIT", self.root.destroy).pack(side="left", expand=True, padx=(5, 0))

        tk.Label(wrapper, text="USE ARROW KEYS OR WASD  •  R TO RESTART",
                 bg=BG, fg=MUTED, font=("Arial", 8, "bold")).pack(pady=(13, 0))

    def stat(self, parent, label, initial):
        box = tk.Frame(parent, bg=CARD)
        tk.Label(box, text=label, bg=CARD, fg=MUTED,
                 font=("Arial", 8, "bold")).pack(anchor="w")
        value = tk.Label(box, text=initial, bg=CARD, fg=ACCENT,
                         font=("Courier New", 20, "bold"))
        value.pack(anchor="w")
        return box

    def button(self, parent, label, command):
        return tk.Button(parent, text=label, command=command, bg="#293b2e", fg="#eaf2e6",
                         activebackground="#435d48", activeforeground="white",
                         relief="flat", cursor="hand2", padx=11, pady=9,
                         font=("Arial", 9, "bold"))

    def bind_keys(self):
        keys = {"<Up>": "Up", "<Down>": "Down", "<Left>": "Left", "<Right>": "Right",
                "w": "Up", "s": "Down", "a": "Left", "d": "Right"}
        for key, direction in keys.items():
            self.root.bind(key, lambda event, d=direction: self.turn(d))
        self.root.bind("r", lambda event: self.restart())
        self.root.bind("R", lambda event: self.restart())
        self.root.bind("<Escape>", lambda event: self.root.destroy())

    def show_menu(self):
        self.draw_board()
        self.canvas.create_text(BOARD // 2, 146, text="SNAKE", fill=INK,
                                font=("Arial", 32, "bold"))
        self.canvas.create_text(BOARD // 2, 188, text="A MODERN CLASSIC", fill=INK,
                                font=("Arial", 10, "bold"))
        self.canvas.create_rectangle(105, 224, BOARD - 105, 258, fill=INK, outline="")
        self.canvas.create_text(BOARD // 2, 241, text="PRESS START", fill=LCD,
                                font=("Arial", 10, "bold"))

    def start(self):
        if not self.running:
            self.reset()
            self.running = True
            self.status.config(text="PLAYING", fg=ACCENT)
            self.tick(self.token)

    def restart(self):
        self.running = False
        self.reset()
        self.running = True
        self.status.config(text="PLAYING", fg=ACCENT)
        self.tick(self.token)

    def reset(self):
        self.token += 1
        self.score = 0
        self.direction = self.next_direction = "Right"
        self.snake = [(10, 10), (9, 10), (8, 10), (7, 10)]
        self.new_food()
        self.update_hud()
        self.draw_game()

    def new_food(self):
        available = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in self.snake]
        self.food = random.choice(available)

    def turn(self, direction):
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if self.running and direction != opposite[self.direction]:
            self.next_direction = direction

    def tick(self, token):
        if not self.running or token != self.token:
            return
        self.direction = self.next_direction
        dx, dy = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}[self.direction]
        head = (self.snake[0][0] + dx, self.snake[0][1] + dy)
        wall = not (0 <= head[0] < COLS and 0 <= head[1] < ROWS)
        collision = head in self.snake[:-1]
        if wall or collision:
            self.end_game()
            return
        self.snake.insert(0, head)
        if head == self.food:
            self.score += 1
            self.high_score = max(self.high_score, self.score)
            self.new_food()
            self.update_hud()
        else:
            self.snake.pop()
        self.draw_game()
        self.root.after(SPEED, lambda: self.tick(token))

    def update_hud(self):
        self.score_value.winfo_children()[1].config(text=f"{self.score:03}")
        self.best_value.winfo_children()[1].config(text=f"{self.high_score:03}")

    def draw_board(self):
        self.canvas.delete("all")
        for point in range(0, BOARD + 1, CELL):
            self.canvas.create_line(point, 0, point, BOARD, fill=LCD_GRID)
            self.canvas.create_line(0, point, BOARD, point, fill=LCD_GRID)

    def draw_game(self):
        self.draw_board()
        fx, fy = self.food[0] * CELL, self.food[1] * CELL
        self.canvas.create_oval(fx + 4, fy + 5, fx + CELL - 4, fy + CELL - 3, fill=RED, outline="")
        self.canvas.create_line(fx + CELL // 2, fy + 5, fx + CELL // 2 + 3, fy + 1, fill=INK, width=2)
        # Organic, overlapping rounded segments.
        for col, row in reversed(self.snake[1:]):
            x, y = col * CELL, row * CELL
            self.canvas.create_oval(x + 1, y + 1, x + CELL - 1, y + CELL - 1, fill=SNAKE, outline="")
        self.draw_head()

    def draw_head(self):
        col, row = self.snake[0]
        x, y = col * CELL, row * CELL
        self.canvas.create_oval(x + 1, y + 1, x + CELL - 1, y + CELL - 1, fill=INK, outline="")
        eyes = {
            "Up": ((x + 7, y + 7), (x + 15, y + 7)),
            "Down": ((x + 7, y + 15), (x + 15, y + 15)),
            "Left": ((x + 7, y + 7), (x + 7, y + 15)),
            "Right": ((x + 15, y + 7), (x + 15, y + 15)),
        }[self.direction]
        for ex, ey in eyes:
            self.canvas.create_oval(ex - 2, ey - 2, ex + 2, ey + 2, fill=LCD, outline="")

    def end_game(self):
        self.running = False
        self.status.config(text="GAME OVER", fg="#ff9898")
        self.canvas.create_rectangle(48, 154, BOARD - 48, 278, fill=INK, outline=ACCENT, width=2)
        self.canvas.create_text(BOARD // 2, 190, text="GAME OVER", fill=ACCENT,
                                font=("Arial", 20, "bold"))
        self.canvas.create_text(BOARD // 2, 220, text=f"FINAL SCORE  {self.score:03}", fill=LCD,
                                font=("Courier New", 12, "bold"))
        self.canvas.create_text(BOARD // 2, 250, text="PRESS RESTART OR R", fill=LCD_GRID,
                                font=("Arial", 9, "bold"))


if __name__ == "__main__":
    ModernSnake()
