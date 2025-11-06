import tkinter as tk
import random

WIDTH = 500
HEIGHT = 400
BALL_SIZE = 15        # smaller ball
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 12
BALL_SPEED = 6
PLAYER_SPEED = 20
START_LIVES = 3

class CatchGame:
    def __init__(self, root):
        self.root = root
        root.title("Catch the Ball (Fireball Edition)")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")  # arcade-style background
        self.canvas.pack()
        self.score = 0
        self.lives = START_LIVES
        self.level = 1
        self.paused = False

        # Player paddle
        self.player_x = WIDTH // 2 - PLAYER_WIDTH // 2
        self.player = self.canvas.create_rectangle(
            self.player_x, HEIGHT - 40,
            self.player_x + PLAYER_WIDTH, HEIGHT - 40 + PLAYER_HEIGHT,
            fill="cyan"
        )

        # Ball
        self.ball = self.canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="magenta")
        self.reset_ball()

        # Power-up (extra life)
        self.powerup = self.canvas.create_oval(0, 0, 15, 15, fill="green", state='hidden')
        self.powerup_active = False

        # Scoreboard & instructions
        self.score_text = self.canvas.create_text(60, 25, text=f"Score: {self.score}", font=("Arial", 14, "bold"), fill="yellow")
        self.lives_text = self.canvas.create_text(180, 25, text=f"Lives: {self.lives}", font=("Arial", 14, "bold"), fill="yellow")
        self.level_text = self.canvas.create_text(WIDTH - 60, 25, text=f"Level: {self.level}", font=("Arial", 14, "bold"), fill="lightgreen")
        self.info_text = self.canvas.create_text(
            WIDTH // 2, 50,
            text="← / → to move   |   Space to pause   |   R to restart",
            font=("Arial", 10), fill="white"
        )

        # Buttons
        self.restart_btn = tk.Button(root, text="Restart", command=self.restart, bg="grey", fg="white")
        self.restart_btn.pack(side="left", padx=10, pady=6)
        self.quit_btn = tk.Button(root, text="Quit", command=root.quit, bg="grey", fg="white")
        self.quit_btn.pack(side="right", padx=10, pady=6)

        # Key bindings
        root.bind("<Left>", lambda e: self.move_player(-PLAYER_SPEED))
        root.bind("<Right>", lambda e: self.move_player(PLAYER_SPEED))
        root.bind("<space>", lambda e: self.toggle_pause())
        root.bind("r", lambda e: self.restart())

        self.game_over_text = None

        # Start game loop
        self.loop()

    def reset_ball(self):
        x = random.randint(0, WIDTH - BALL_SIZE)
        self.canvas.coords(self.ball, x, 0, x + BALL_SIZE, BALL_SIZE)
        self.ball_dx = random.choice([-3, -2, 2, 3])
        self.ball_dy = BALL_SPEED

    def move_player(self, dx):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        new_x1 = max(0, x1 + dx)
        new_x2 = min(WIDTH, x2 + dx)
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
        self.level = 1
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
        self.canvas.itemconfig(self.level_text, text=f"Level: {self.level}")
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None
        self.reset_ball()
        self.paused = False
        self.canvas.itemconfig(
            self.info_text,
            text="← / → to move   |   Space to pause   |   R to restart"
        )
        self.canvas.itemconfigure(self.powerup, state='hidden')
        self.powerup_active = False
        self.canvas.itemconfig(self.ball, fill="magenta")  # reset ball color

    def loop(self):
        if not self.paused and self.lives > 0:
            self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
            bx1, by1, bx2, by2 = self.canvas.coords(self.ball)

            # Fireball effect if score >= 5
            if self.score >= 5:
                fire_colors = ["yellow", "orange", "red"]
                self.canvas.itemconfig(self.ball, fill=random.choice(fire_colors))

            # Bounce from walls and top
            if bx1 <= 0 or bx2 >= WIDTH:
                self.ball_dx = -self.ball_dx
            if by1 <= 0:
                self.ball_dy = -self.ball_dy

            # Ball missed paddle
            if by2 >= HEIGHT:
                self.lives -= 1
                self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
                if self.lives <= 0:
                    self.game_over()
                else:
                    self.reset_ball()

            # Ball hits paddle
            px1, py1, px2, py2 = self.canvas.coords(self.player)
            if (bx2 >= px1 and bx1 <= px2) and (by2 >= py1 and by1 <= py2) and self.ball_dy > 0:
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

                # Level progression every 5 points
                new_level = self.score // 5 + 1
                if new_level > self.level:
                    self.level = new_level
                    self.ball_dx *= 1.1
                    self.ball_dy *= 1.1
                    self.canvas.itemconfig(self.level_text, text=f"Level: {self.level}")

                self.ball_dy = -self.ball_dy  # bounce upward
                hit_pos = ((bx1 + bx2) / 2 - (px1 + px2) / 2) / (PLAYER_WIDTH / 2)
                self.ball_dx += hit_pos * 2

            # Spawn power-up randomly
            if not self.powerup_active and random.random() < 0.002:
                px = random.randint(0, WIDTH - 15)
                self.canvas.coords(self.powerup, px, 0, px + 15, 15)
                self.canvas.itemconfigure(self.powerup, state='normal')
                self.powerup_active = True

            # Move power-up
            if self.powerup_active:
                self.canvas.move(self.powerup, 0, 4)
                pu_x1, pu_y1, pu_x2, pu_y2 = self.canvas.coords(self.powerup)
                if (pu_x2 >= px1 and pu_x1 <= px2) and (pu_y2 >= py1 and pu_y1 <= py2):
                    self.lives += 1
                    self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
                    self.canvas.itemconfigure(self.powerup, state='hidden')
                    self.powerup_active = False
                elif pu_y2 >= HEIGHT:
                    self.canvas.itemconfigure(self.powerup, state='hidden')
                    self.powerup_active = False

        self.root.after(30, self.loop)

    def game_over(self):
        self.paused = True
        self.game_over_text = self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2,
            text=f"GAME OVER\nScore: {self.score}\nLevel: {self.level}",
            font=("Arial", 24, "bold"),
            fill="yellow"
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = CatchGame(root)
    root.mainloop()
