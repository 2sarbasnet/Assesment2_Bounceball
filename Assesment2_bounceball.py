import tkinter as tk
import random

WIDTH = 600
HEIGHT = 450
BALL_SIZE = 15
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 12
BALL_SPEED = 6
PLAYER_SPEED = 20
START_LIVES = 3


class CatchGame:
    def __init__(self, root):
        self.root = root
        root.title("🔥 Catch the Ball - Power-Up Edition 🔥")
        root.configure(bg="#0b0b0d")

        # Canvas (main play area)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#101820", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

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
            fill="#00FFFF", width=0
        )
        self.current_player_speed = PLAYER_SPEED

        # Ball
        self.ball = self.canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="magenta", width=0)
        self.reset_ball()

        # Power-ups
        self.powerup = self.canvas.create_oval(0, 0, 15, 15, fill="#00FF00", state='hidden', width=0)
        self.shield_powerup = self.canvas.create_oval(0, 0, 15, 15, fill="#0096FF", state='hidden', width=0)
        self.speed_powerup = self.canvas.create_oval(0, 0, 15, 15, fill="#FFD700", state='hidden', width=0)

        # Status bar
        self.status_bar = tk.Frame(root, bg="#161b22")
        self.status_bar.pack(fill="x", pady=(0, 6))

        self.score_label = tk.Label(self.status_bar, text=f"🏆 Score: {self.score}", font=("Consolas", 12, "bold"), fg="#F9F871", bg="#161b22")
        self.lives_label = tk.Label(self.status_bar, text=f"❤️ Lives: {self.lives}", font=("Consolas", 12, "bold"), fg="#FF6B6B", bg="#161b22")
        self.level_label = tk.Label(self.status_bar, text=f"🚀 Level: {self.level}", font=("Consolas", 12, "bold"), fg="#7CFC00", bg="#161b22")

        self.score_label.pack(side="left", padx=15)
        self.lives_label.pack(side="left", padx=15)
        self.level_label.pack(side="right", padx=15)

        # Info text
        self.info_text = self.canvas.create_text(
            WIDTH // 2, 30,
            text="← / → to move   |   Space = Pause   |   R = Restart",
            font=("Consolas", 11), fill="#AAAAAA"
        )

        # Buttons
        self.btn_frame = tk.Frame(root, bg="#0b0b0d")
        self.btn_frame.pack(pady=5)

        self.restart_btn = tk.Button(self.btn_frame, text="🔁 Restart", command=self.restart,
                                     bg="#2d2f3a", fg="white", font=("Arial", 10, "bold"),
                                     relief="flat", padx=10, pady=5)
        self.quit_btn = tk.Button(self.btn_frame, text="❌ Quit", command=root.quit,
                                  bg="#2d2f3a", fg="white", font=("Arial", 10, "bold"),
                                  relief="flat", padx=10, pady=5)

        self.restart_btn.pack(side="left", padx=10)
        self.quit_btn.pack(side="left", padx=10)

        # Key bindings
        root.bind("<Left>", lambda e: self.move_player(-1))
        root.bind("<Right>", lambda e: self.move_player(1))
        root.bind("<space>", lambda e: self.toggle_pause())
        root.bind("r", lambda e: self.restart())

        # Game variables
        self.powerup_active = False
        self.shield_powerup_active = False
        self.speed_powerup_active = False
        self.shield_active = False
        self.speed_boost_active = False
        self.game_over_text = None

        self.loop()

    # ------------------ GAME LOGIC ------------------ #

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
            self.canvas.itemconfig(self.info_text, text="⏸ PAUSED - Press Space to Resume", fill="#FFAE42")
        else:
            self.canvas.itemconfig(self.info_text, text="← / → to move   |   Space = Pause   |   R = Restart", fill="#AAAAAA")

    def restart(self):
        self.score = 0
        self.lives = START_LIVES
        self.level = 1
        self.current_player_speed = PLAYER_SPEED
        self.update_labels()
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None
        self.reset_ball()
        self.paused = False
        self.canvas.itemconfig(self.player, fill="#00FFFF")
        self.canvas.coords(self.player, WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 40,
                           WIDTH // 2 + PLAYER_WIDTH // 2, HEIGHT - 40 + PLAYER_HEIGHT)

    def update_labels(self):
        self.score_label.config(text=f"🏆 Score: {self.score}")
        self.lives_label.config(text=f"❤️ Lives: {self.lives}")
        self.level_label.config(text=f"🚀 Level: {self.level}")

    def disable_shield(self):
        self.shield_active = False
        self.canvas.itemconfig(self.player, fill="#00FFFF")

    def activate_speed_boost(self):
        if not self.speed_boost_active:
            self.speed_boost_active = True
            self.current_player_speed = PLAYER_SPEED * 2
            self.canvas.itemconfig(self.player, fill="#FFD700")
            self.root.after(4000, self.disable_speed_boost)

    def disable_speed_boost(self):
        self.speed_boost_active = False
        self.current_player_speed = PLAYER_SPEED
        color = "#0096FF" if self.shield_active else "#00FFFF"
        self.canvas.itemconfig(self.player, fill=color)

    # ------------------ MAIN LOOP ------------------ #

    def loop(self):
        if not self.paused and self.lives > 0:
            self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
            bx1, by1, bx2, by2 = self.canvas.coords(self.ball)

            # 🔥 Fireball animation
            if self.score >= 5:
                fire_colors = ["#FFA500", "#FF4500", "#FF0000", "#FF8C00"]
                self.canvas.itemconfig(self.ball, fill=random.choice(fire_colors))

            # Bounce logic
            if bx1 <= 0 or bx2 >= WIDTH:
                self.ball_dx = -self.ball_dx
            if by1 <= 0:
                self.ball_dy = -self.ball_dy

            px1, py1, px2, py2 = self.canvas.coords(self.player)

            # Missed ball
            if by2 >= HEIGHT:
                if not self.shield_active:
                    self.lives -= 1
                    self.update_labels()
                    if self.lives <= 0:
                        self.game_over()
                        return
                self.reset_ball()

            # Hit paddle
            if (bx2 >= px1 and bx1 <= px2) and (by2 >= py1 and by1 <= py2) and self.ball_dy > 0:
                self.score += 1
                self.update_labels()
                new_level = self.score // 5 + 1
                if new_level > self.level:
                    self.level = new_level
                    self.ball_dx *= 1.1
                    self.ball_dy *= 1.1
                    self.update_labels()
                    # Shrink paddle
                    current_width = px2 - px1
                    if current_width > 40:
                        new_width = current_width - 10
                        center_x = (px1 + px2) / 2
                        self.canvas.coords(self.player, center_x - new_width / 2, py1, center_x + new_width / 2, py2)

                self.ball_dy = -self.ball_dy

            # Power-ups
            self.handle_powerups(px1, py1, px2, py2)

        self.root.after(30, self.loop)

    def handle_powerups(self, px1, py1, px2, py2):
        # Green (life)
        if not self.powerup_active and random.random() < 0.002:
            px = random.randint(0, WIDTH - 15)
            self.canvas.coords(self.powerup, px, 0, px + 15, 15)
            self.canvas.itemconfigure(self.powerup, state='normal')
            self.powerup_active = True

        if self.powerup_active:
            self.canvas.move(self.powerup, 0, 4)
            x1, y1, x2, y2 = self.canvas.coords(self.powerup)
            if (x2 >= px1 and x1 <= px2) and (y2 >= py1 and y1 <= py2):
                self.lives += 1
                self.update_labels()
                self.canvas.itemconfigure(self.powerup, state='hidden')
                self.powerup_active = False
                # Grow paddle
                current_width = px2 - px1
                if current_width < PLAYER_WIDTH:
                    new_width = min(current_width + 10, PLAYER_WIDTH)
                    center_x = (px1 + px2) / 2
                    self.canvas.coords(self.player, center_x - new_width / 2, py1, center_x + new_width / 2, py2)
            elif y2 >= HEIGHT:
                self.canvas.itemconfigure(self.powerup, state='hidden')
                self.powerup_active = False

        # Blue (shield)
        if not self.shield_powerup_active and random.random() < 0.0015:
            px = random.randint(0, WIDTH - 15)
            self.canvas.coords(self.shield_powerup, px, 0, px + 15, 15)
            self.canvas.itemconfigure(self.shield_powerup, state='normal')
            self.shield_powerup_active = True

        if self.shield_powerup_active:
            self.canvas.move(self.shield_powerup, 0, 4)
            x1, y1, x2, y2 = self.canvas.coords(self.shield_powerup)
            if (x2 >= px1 and x1 <= px2) and (y2 >= py1 and y1 <= py2):
                self.shield_active = True
                self.canvas.itemconfigure(self.shield_powerup, state='hidden')
                self.shield_powerup_active = False
                self.canvas.itemconfig(self.player, fill="#0096FF")
                self.root.after(5000, self.disable_shield)
            elif y2 >= HEIGHT:
                self.canvas.itemconfigure(self.shield_powerup, state='hidden')
                self.shield_powerup_active = False

        # Yellow (speed)
        if not self.speed_powerup_active and random.random() < 0.001:
            px = random.randint(0, WIDTH - 15)
            self.canvas.coords(self.speed_powerup, px, 0, px + 15, 15)
            self.canvas.itemconfigure(self.speed_powerup, state='normal')
            self.speed_powerup_active = True

        if self.speed_powerup_active:
            self.canvas.move(self.speed_powerup, 0, 4)
            x1, y1, x2, y2 = self.canvas.coords(self.speed_powerup)
            if (x2 >= px1 and x1 <= px2) and (y2 >= py1 and y1 <= py2):
                self.activate_speed_boost()
                self.canvas.itemconfigure(self.speed_powerup, state='hidden')
                self.speed_powerup_active = False
            elif y2 >= HEIGHT:
                self.canvas.itemconfigure(self.speed_powerup, state='hidden')
                self.speed_powerup_active = False

    def game_over(self):
        self.paused = True
        self.game_over_text = self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2,
            text=f"💀 GAME OVER 💀\nScore: {self.score}\nLevel: {self.level}",
            font=("Consolas", 20, "bold"),
            fill="#FF5F1F"
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = CatchGame(root)
    root.mainloop()
