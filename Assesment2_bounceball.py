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
        root.title("Catch the Ball (Power-Up & Challenge Edition)")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Game state
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
        self.current_player_speed = PLAYER_SPEED

        # Ball
        self.ball = self.canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="magenta")
        self.reset_ball()

        # Power-ups
        self.powerup = self.canvas.create_oval(0, 0, 15, 15, fill="green", state='hidden')
        self.powerup_active = False

        self.shield_powerup = self.canvas.create_oval(0, 0, 15, 15, fill="blue", state='hidden')
        self.shield_powerup_active = False
        self.shield_active = False

        self.speed_powerup = self.canvas.create_oval(0, 0, 15, 15, fill="yellow", state='hidden')
        self.speed_powerup_active = False
        self.speed_boost_active = False

        # Texts
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
        root.bind("<Left>", lambda e: self.move_player(-1))
        root.bind("<Right>", lambda e: self.move_player(1))
        root.bind("<space>", lambda e: self.toggle_pause())
        root.bind("r", lambda e: self.restart())

        self.game_over_text = None
        self.loop()

    def reset_ball(self):
        x = random.randint(0, WIDTH - BALL_SIZE)
        self.canvas.coords(self.ball, x, 0, x + BALL_SIZE, BALL_SIZE)
        self.ball_dx = random.choice([-3, -2, 2, 3])
        self.ball_dy = BALL_SPEED

    def move_player(self, direction):
        dx = direction * self.current_player_speed
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        new_x1 = max(0, x1 + dx)
        new_x2 = min(WIDTH, x2 + dx)
        if new_x2 - new_x1 != x2 - x1:
            if new_x1 == 0:
                new_x2 = x1 + (x2 - x1)
            else:
                new_x1 = WIDTH - (x2 - x1)
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
        self.current_player_speed = PLAYER_SPEED
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
        self.canvas.itemconfigure(self.shield_powerup, state='hidden')
        self.canvas.itemconfigure(self.speed_powerup, state='hidden')
        self.powerup_active = False
        self.shield_powerup_active = False
        self.speed_powerup_active = False
        self.shield_active = False
        self.speed_boost_active = False
        self.canvas.itemconfig(self.player, fill="cyan")
        self.canvas.coords(self.player, WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - 40,
                           WIDTH//2 + PLAYER_WIDTH//2, HEIGHT - 40 + PLAYER_HEIGHT)

    def disable_shield(self):
        self.shield_active = False
        if self.speed_boost_active:
            self.canvas.itemconfig(self.player, fill="gold")
        else:
            self.canvas.itemconfig(self.player, fill="cyan")

    def activate_speed_boost(self):
        if not self.speed_boost_active:
            self.speed_boost_active = True
            self.current_player_speed = PLAYER_SPEED * 2
            self.canvas.itemconfig(self.player, fill="gold")
            self.root.after(4000, self.disable_speed_boost)

    def disable_speed_boost(self):
        self.speed_boost_active = False
        self.current_player_speed = PLAYER_SPEED
        if self.shield_active:
            self.canvas.itemconfig(self.player, fill="deepskyblue")
        else:
            self.canvas.itemconfig(self.player, fill="cyan")

    def loop(self):
        if not self.paused and self.lives > 0:
            self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
            bx1, by1, bx2, by2 = self.canvas.coords(self.ball)

            # Fireball effect
            if self.score >= 5:
                fire_colors = ["yellow", "orange", "red"]
                self.canvas.itemconfig(self.ball, fill=random.choice(fire_colors))

            # Wall bounces
            if bx1 <= 0 or bx2 >= WIDTH:
                self.ball_dx = -self.ball_dx
            if by1 <= 0:
                self.ball_dy = -self.ball_dy

            # Paddle and positions
            px1, py1, px2, py2 = self.canvas.coords(self.player)

            # Missed ball
            if by2 >= HEIGHT:
                if self.shield_active:
                    self.reset_ball()
                else:
                    self.lives -= 1
                    self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
                    if self.lives <= 0:
                        self.game_over()
                    else:
                        self.reset_ball()

            # Ball hits paddle
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

                    # 🆕 Shrink paddle on level up
                    current_width = px2 - px1
                    if current_width > 40:
                        shrink_amount = 10
                        new_width = current_width - shrink_amount
                        center_x = (px1 + px2) / 2
                        self.canvas.coords(self.player,
                                           center_x - new_width / 2,
                                           py1,
                                           center_x + new_width / 2,
                                           py2)

                self.ball_dy = -self.ball_dy
                hit_pos = ((bx1 + bx2) / 2 - (px1 + px2) / 2) / (px2 - px1)
                self.ball_dx += hit_pos * 2

            # 🟢 Extra life power-up
            if not self.powerup_active and random.random() < 0.002:
                px = random.randint(0, WIDTH - 15)
                self.canvas.coords(self.powerup, px, 0, px + 15, 15)
                self.canvas.itemconfigure(self.powerup, state='normal')
                self.powerup_active = True

            if self.powerup_active:
                self.canvas.move(self.powerup, 0, 4)
                pu_x1, pu_y1, pu_x2, pu_y2 = self.canvas.coords(self.powerup)
                if (pu_x2 >= px1 and pu_x1 <= px2) and (pu_y2 >= py1 and pu_y1 <= py2):
                    self.lives += 1
                    self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
                    self.canvas.itemconfigure(self.powerup, state='hidden')
                    self.powerup_active = False

                    # 🆕 Grow paddle slightly (max width = PLAYER_WIDTH)
                    current_width = px2 - px1
                    if current_width < PLAYER_WIDTH:
                        grow_amount = 10
                        new_width = min(current_width + grow_amount, PLAYER_WIDTH)
                        center_x = (px1 + px2) / 2
                        self.canvas.coords(self.player,
                                           center_x - new_width / 2,
                                           py1,
                                           center_x + new_width / 2,
                                           py2)
                elif pu_y2 >= HEIGHT:
                    self.canvas.itemconfigure(self.powerup, state='hidden')
                    self.powerup_active = False

            # 🔵 Shield Power-up
            if not self.shield_powerup_active and random.random() < 0.0015:
                px = random.randint(0, WIDTH - 15)
                self.canvas.coords(self.shield_powerup, px, 0, px + 15, 15)
                self.canvas.itemconfigure(self.shield_powerup, state='normal')
                self.shield_powerup_active = True

            if self.shield_powerup_active:
                self.canvas.move(self.shield_powerup, 0, 4)
                sx1, sy1, sx2, sy2 = self.canvas.coords(self.shield_powerup)
                if (sx2 >= px1 and sx1 <= px2) and (sy2 >= py1 and sy1 <= py2):
                    self.shield_active = True
                    self.canvas.itemconfigure(self.shield_powerup, state='hidden')
                    self.shield_powerup_active = False
                    self.canvas.itemconfig(self.player, fill="deepskyblue")
                    self.root.after(5000, self.disable_shield)
                elif sy2 >= HEIGHT:
                    self.canvas.itemconfigure(self.shield_powerup, state='hidden')
                    self.shield_powerup_active = False

            # ⚡ Speed Boost Power-up
            if not self.speed_powerup_active and random.random() < 0.001:
                px = random.randint(0, WIDTH - 15)
                self.canvas.coords(self.speed_powerup, px, 0, px + 15, 15)
                self.canvas.itemconfigure(self.speed_powerup, state='normal')
                self.speed_powerup_active = True

            if self.speed_powerup_active:
                self.canvas.move(self.speed_powerup, 0, 4)
                sx1, sy1, sx2, sy2 = self.canvas.coords(self.speed_powerup)
                if (sx2 >= px1 and sx1 <= px2) and (sy2 >= py1 and sy1 <= py2):
                    self.activate_speed_boost()
                    self.canvas.itemconfigure(self.speed_powerup, state='hidden')
                    self.speed_powerup_active = False
                elif sy2 >= HEIGHT:
                    self.canvas.itemconfigure(self.speed_powerup, state='hidden')
                    self.speed_powerup_active = False

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
