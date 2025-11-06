import tkinter as tk
import random

WIDTH = 500
HEIGHT = 400
BALL_SIZE = 15
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 12
BALL_SPEED = 6
PLAYER_SPEED = 20
START_LIVES = 3

class CatchGame:
    def __init__(self, root):
        self.root = root
        root.title("Catch the Ball")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="grey")
        self.canvas.pack()
        self.score = 0
        self.lives = START_LIVES
        self.paused = False

        # Create player paddle
        self.player_x = WIDTH // 2 - PLAYER_WIDTH // 2
        self.player = self.canvas.create_rectangle(
            self.player_x, HEIGHT - 40,
            self.player_x + PLAYER_WIDTH, HEIGHT - 40 + PLAYER_HEIGHT,
            fill="blue"
        )

        # Create ball
        self.ball = self.canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="red")
        self.reset_ball()

        # 🧾 Scoreboard / controls (moved to better positions)
        self.score_text = self.canvas.create_text(60, 25, text=f"Score: {self.score}", font=("Arial", 14, "bold"), fill="white")
        self.lives_text = self.canvas.create_text(180, 25, text=f"Lives: {self.lives}", font=("Arial", 14, "bold"), fill="white")
        self.info_text = self.canvas.create_text(
            WIDTH // 2, 50,
            text="← / → to move   |   Space to pause   |   R to restart",
            font=("Arial", 10), fill="black"
        )

        # Buttons
        self.restart_btn = tk.Button(root, text="Restart", command=self.restart)
        self.restart_btn.pack(side="left", padx=10, pady=6)
        self.quit_btn = tk.Button(root, text="Quit", command=root.quit)
        self.quit_btn.pack(side="right", padx=10, pady=6)

        # Bind keys
        root.bind("<Left>", lambda e: self.move_player(-PLAYER_SPEED))
        root.bind("<Right>", lambda e: self.move_player(PLAYER_SPEED))
        root.bind("<space>", lambda e: self.toggle_pause())
        root.bind("r", lambda e: self.restart())

        self.game_over_text = None

        # Start the game loop
        self.loop()

    def reset_ball(self):
        x = random.randint(0, WIDTH - BALL_SIZE)
        self.canvas.coords(self.ball, x, 0, x + BALL_SIZE, BALL_SIZE)
        # Random horizontal direction and speed as tuple (dx, dy)
        self.ball_dx = random.choice([-3, -2, 2, 3])
        self.ball_dy = BALL_SPEED

    def move_player(self, dx):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        new_x1 = max(0, x1 + dx)
        new_x2 = min(WIDTH, x2 + dx)
        # adjust correctly if hitting edges
        if new_x2 - new_x1 != PLAYER_WIDTH:
            if new_x1 == 0:
                new_x2 = PLAYER_WIDTH
            else:
                new_x1 = WIDTH - PLAYER_WIDTH
        self.canvas.coords(self.player, new_x1, y1, new_x2, y2)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.canvas.itemconfig(self.info_text, text="⏸ PAUSED - Press Space to Resume")
        else:
            self.canvas.itemconfig(
                self.info_text,
                text="← / → to move   |   Space to pause   |   R to restart"
            )

    def restart(self):
        self.score = 0
        self.lives = START_LIVES
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None
        self.reset_ball()
        self.paused = False
        self.canvas.itemconfig(
            self.info_text,
            text="← / → to move   |   Space to pause   |   R to restart"
        )

    def loop(self):
        if not self.paused and self.lives > 0:
            self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
            bx1, by1, bx2, by2 = self.canvas.coords(self.ball)

            # bounce from left/right
            if bx1 <= 0 or bx2 >= WIDTH:
                self.ball_dx = -self.ball_dx

            # check if ball reached bottom
            if by2 >= HEIGHT:
                self.lives -= 1
                self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
                if self.lives <= 0:
                    self.game_over()
                else:
                    self.reset_ball()

            # check collision with player
            px1, py1, px2, py2 = self.canvas.coords(self.player)
            if (bx2 >= px1 and bx1 <= px2) and (by2 >= py1 and by1 <= py2):
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                self.reset_ball()

        self.root.after(30, self.loop)

    def game_over(self):
        self.paused = True
        self.game_over_text = self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2,
            text=f"GAME OVER\nScore: {self.score}",
            font=("Arial", 24, "bold"),
            fill="white"
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = CatchGame(root)
    root.mainloop()
