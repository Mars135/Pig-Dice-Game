import random
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import time

class PigDiceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pig Dice Game")
        self.root.geometry("650x550")
        self.root.configure(bg='black')   
        self.target_score = 30
        self.players = []
        self.current_player = 0
        self.scores = {}
        self.turn_points = 0
        self.dice_roll = 0
        self.difficulty = "medium"
        self.game_active = False
        self.turn_ended = False
        self.dice_images = []
        for i in range(1, 7):
            try:
                img = Image.open(f"dice_{i}.png")
            except:
                img = Image.new('RGB', (100, 100), 'white')
            img = img.resize((80, 80), Image.LANCZOS)
            self.dice_images.append(ImageTk.PhotoImage(img))
        self.setup_ui()

    def setup_ui(self):
        self.setup_frame = tk.Frame(self.root, bg='black')
        self.setup_frame.pack(pady=20)
        tk.Label(self.setup_frame, text="Welcome to Pig Dice Game!", 
                font=("Arial", 16, 'bold'), fg='white', bg='black').pack()
        tk.Label(self.setup_frame, text=f"First to {self.target_score} points wins!", 
                font=("Arial", 12), fg='white', bg='black').pack(pady=10)
        tk.Button(self.setup_frame, text="Show Rules", 
                 command=self.show_rules, bg='#444', fg='white').pack(pady=5)
        self.mode_var = tk.StringVar(value="1")
        tk.Radiobutton(self.setup_frame, text="Play vs Computer", variable=self.mode_var, 
                      value="1", command=self.update_ui, fg='white', bg='black').pack(anchor='w')
        tk.Radiobutton(self.setup_frame, text="Play with Friends", variable=self.mode_var, 
                      value="2", command=self.update_ui, fg='white', bg='black').pack(anchor='w')
        self.difficulty_frame = tk.Frame(self.setup_frame, bg='black')
        self.difficulty_frame.pack(pady=5)
        tk.Label(self.difficulty_frame, text="Computer Difficulty:", 
                fg='white', bg='black').pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="medium")
        ttk.Combobox(self.difficulty_frame, textvariable=self.difficulty_var, 
                    values=["easy", "medium", "hard"], width=8, state='readonly').pack(side=tk.LEFT, padx=5)
        self.num_players_label = tk.Label(self.setup_frame, text="Number of players (2-4):", 
                                        fg='white', bg='black')
        self.num_players_entry = tk.Entry(self.setup_frame, width=5)
        tk.Button(self.setup_frame, text="Start Game", 
                 command=self.start_game, bg='#333', fg='white').pack(pady=10)
        tk.Button(self.setup_frame, text="Exit Game", 
                 command=self.root.destroy, bg='red', fg='white').pack(pady=5)
        self.update_ui()
        self.game_frame = tk.Frame(self.root, bg='black')
        self.turn_label = tk.Label(self.game_frame, font=("Arial", 14, 'bold'), 
                                 fg='white', bg='black')
        self.turn_label.pack(pady=10)
        self.scores_label = tk.Label(self.game_frame, font=("Arial", 12), 
                                   fg='white', bg='black')
        self.scores_label.pack()
        self.dice_canvas = tk.Canvas(self.game_frame, width=100, height=100, bg='black', 
                                    highlightthickness=0)
        self.dice_canvas.pack(pady=20)
        self.dice_display = self.dice_canvas.create_image(50, 50, image=None)
        self.button_frame = tk.Frame(self.game_frame, bg='black')
        self.button_frame.pack(pady=10)
        self.roll_button = tk.Button(self.button_frame, text="Roll", command=self.roll_dice, 
                                   state=tk.DISABLED, bg='#333', fg='white', width=10)
        self.roll_button.pack(side=tk.LEFT, padx=20)
        self.hold_button = tk.Button(self.button_frame, text="Hold", command=self.hold_turn, 
                                   state=tk.DISABLED, bg='#333', fg='white', width=10)
        self.hold_button.pack(side=tk.RIGHT, padx=20)
        self.bottom_buttons_frame = tk.Frame(self.game_frame, bg='black')
        self.bottom_buttons_frame.pack(pady=20)
        self.go_back_button = tk.Button(self.bottom_buttons_frame, text="Go Back to Main Menu", 
                                      command=self.return_to_main, bg='#444', fg='white')
        self.go_back_button.pack(side=tk.LEFT, padx=10)
        self.exit_button = tk.Button(self.bottom_buttons_frame, text="Exit Game", 
                                   command=self.root.destroy, bg='red', fg='white')
        self.exit_button.pack(side=tk.RIGHT, padx=10)
        self.go_back_button.pack_forget()
        self.exit_button.pack_forget()

    def show_rules(self):
        rules = """PIG DICE GAME RULES:
1. Players take turns rolling a die
2. Roll as many times as you want, accumulating points
3. If you roll a 1, you lose all points for that turn
4. First to reach 30 points wins!
5. Choose 'Hold' to bank your points and end your turn
SPECIAL RULES:
- If rolling would exceed 30, subtract the roll value
- Except when at exactly 29 points
- At exactly 29 points, rolling a 2 ends your turn (not 1)"""
        messagebox.showinfo("Game Rules", rules)

    def update_ui(self):
        if self.mode_var.get() == "1":
            self.num_players_label.pack_forget()
            self.num_players_entry.pack_forget()
            self.difficulty_frame.pack()
        else:
            self.num_players_label.pack()
            self.num_players_entry.pack()
            self.difficulty_frame.pack_forget()

    def animate_dice_roll(self, final_value, callback):
        self.animation_counter = 0
        self.animation_frames = 10
        def update_animation():
            if self.animation_counter < self.animation_frames:
                random_face = random.randint(0, 5)
                self.dice_canvas.itemconfig(self.dice_display, image=self.dice_images[random_face])
                self.animation_counter += 1
                self.root.after(50, update_animation)
            else:
                self.dice_canvas.itemconfig(self.dice_display, image=self.dice_images[final_value-1])
                callback()
        update_animation()

    def return_to_main(self):
        self.game_frame.pack_forget()
        self.setup_frame.pack(pady=20)
        self.go_back_button.pack_forget()
        self.exit_button.pack_forget()

    def start_game(self):
        mode = self.mode_var.get()
        if mode == "1":
            self.players = ["Player", "Computer"]
            self.difficulty = self.difficulty_var.get()
        else:
            try:
                num_players = int(self.num_players_entry.get())
                if num_players < 2 or num_players > 4:
                    messagebox.showerror("Error", "Please enter 2-4 players")
                    return
                self.players = [f"Player {i+1}" for i in range(num_players)]
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
                return
        self.scores = {player: 0 for player in self.players}
        self.current_player = 0
        self.turn_points = 0
        self.game_active = True
        self.turn_ended = False
        self.setup_frame.pack_forget()
        self.game_frame.pack()
        self.update_game_ui()
        if self.players[self.current_player] == "Computer":
            self.root.after(1000, self.computer_turn)

    def update_game_ui(self):
        player = self.players[self.current_player]
        self.turn_label.config(text=f"{player}'s Turn")
        scores_text = "\n".join([f"{p}: {s}" for p, s in self.scores.items()])
        self.scores_label.config(text=f"Scores:\n{scores_text}")
        if player == "Computer" or self.turn_ended:
            self.roll_button.config(state=tk.DISABLED)
            self.hold_button.config(state=tk.DISABLED)
        else:
            self.roll_button.config(state=tk.NORMAL)
            self.hold_button.config(state=tk.NORMAL)

    def roll_dice(self):
        if not self.game_active or self.turn_ended:
            return
        self.roll_button.config(state=tk.DISABLED)
        self.hold_button.config(state=tk.DISABLED)
        self.dice_roll = random.randint(1, 6)
        def after_animation():
            current_player = self.players[self.current_player]
            current_score = self.scores[current_player]
            potential_total = current_score + self.turn_points + self.dice_roll
            if potential_total > 30 and current_score != 29:
                self.turn_points -= self.dice_roll
                result_text = f"Rolled {self.dice_roll}! (Special Rule: -{self.dice_roll}) Turn points: {self.turn_points}"
            elif current_score == 29 and self.dice_roll == 2:
                self.turn_points = 0
                result_text = f"Rolled {self.dice_roll}! (Special Rule: Turn ends on 2 at 29 points)"
                self.turn_ended = True
                self.root.after(1000, self.next_player)
            elif self.dice_roll == 1 and current_score != 29:
                self.turn_points = 0
                result_text = f"Rolled {self.dice_roll}! Turn ends"
                self.turn_ended = True
                self.root.after(1000, self.next_player)
            else:
                self.turn_points += self.dice_roll
                result_text = f"Rolled {self.dice_roll}! Turn points: {self.turn_points}"
            self.turn_label.config(text=result_text)
            if self.scores[current_player] + self.turn_points >= self.target_score:
                self.end_game()
            elif not self.turn_ended:
                self.roll_button.config(state=tk.NORMAL)
                self.hold_button.config(state=tk.NORMAL)
        self.animate_dice_roll(self.dice_roll, after_animation)

    def hold_turn(self):
        if not self.game_active or self.turn_ended:
            return
        player = self.players[self.current_player]
        self.scores[player] += self.turn_points
        self.turn_label.config(text=f"{player} holds! +{self.turn_points} points")
        self.turn_points = 0
        self.turn_ended = True
        self.root.after(1000, self.next_player)

    def next_player(self):
        self.turn_ended = False
        self.current_player = (self.current_player + 1) % len(self.players)
        self.turn_points = 0
        self.dice_canvas.itemconfig(self.dice_display, image=None)
        self.update_game_ui()
        if self.players[self.current_player] == "Computer":
            self.root.after(1000, self.computer_turn)

    def computer_turn(self):
        if not self.game_active:
            return
        player = self.players[self.current_player]
        current_score = self.scores[player]
        remaining = self.target_score - current_score
        if self.difficulty == "easy":
            hold_threshold = random.randint(5, 15)
            risk_factor = 0.3
        elif self.difficulty == "medium":
            hold_threshold = min(10, remaining // 2)
            risk_factor = 0.1
        else:
            hold_threshold = min(15, remaining // 1.5)
            risk_factor = 0.05
        if current_score + self.turn_points >= self.target_score:
            decision = 'r'
        elif random.random() < risk_factor and self.turn_points < hold_threshold:
            decision = 'r'
        elif self.turn_points >= hold_threshold:
            decision = 'h'
        else:
            decision = 'r'
        def after_animation(decision):
            player = self.players[self.current_player]
            current_score = self.scores[player]
            potential_total = current_score + self.turn_points + self.dice_roll
            if decision == 'h':
                self.scores[player] += self.turn_points
                self.turn_label.config(text="Computer holds!")
                if self.scores[player] >= self.target_score:
                    self.end_game()
                else:
                    self.turn_points = 0
                    self.root.after(1000, self.next_player)
            else:
                if potential_total > 30 and current_score != 29:
                    self.turn_points -= self.dice_roll
                    result_text = f"Computer rolled {self.dice_roll}! (Special Rule: -{self.dice_roll})"
                elif current_score == 29 and self.dice_roll == 2:
                    self.turn_label.config(text="Computer rolled 2! (Special Rule: Turn ends on 2 at 29 points)")
                    self.turn_points = 0
                    self.root.after(1000, self.next_player)
                    return
                elif self.dice_roll == 1 and current_score != 29:
                    self.turn_label.config(text="Computer rolled 1! Turn ends")
                    self.turn_points = 0
                    self.root.after(1000, self.next_player)
                    return
                else:
                    self.turn_points += self.dice_roll
                    result_text = f"Computer rolled {self.dice_roll}!"
                self.turn_label.config(text=result_text)
                if self.scores[player] + self.turn_points >= self.target_score:
                    self.end_game()
                else:
                    self.root.after(1000, self.computer_turn)
        if decision == 'h':
            after_animation(decision)
        else:
            self.dice_roll = random.randint(1, 6)
            self.animate_dice_roll(self.dice_roll, lambda: after_animation(decision))

    def end_game(self):
        self.game_active = False
        player = self.players[self.current_player]
        self.scores[player] += self.turn_points
        winner = max(self.scores.items(), key=lambda x: x[1])[0]
        messagebox.showinfo("Game Over", f"🏆 {winner} wins with {self.scores[winner]} points! 🏆")
        self.go_back_button.pack(side=tk.LEFT, padx=10)
        self.exit_button.pack(side=tk.RIGHT, padx=10)
        self.roll_button.config(state=tk.DISABLED)
        self.hold_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = PigDiceGame(root)
    root.mainloop()