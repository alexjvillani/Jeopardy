# game_screen.py

import tkinter as tk
from tkinter import messagebox

class GameScreen:
    def __init__(self, category_names, questions_data, player_names):
        self.window = tk.Toplevel()
        self.window.title("Jeopardy Game Screen")
        self.window.geometry("800x600")
        self.window.configure(bg="#003366")  # Dark blue background
        self.category_names = category_names
        self.questions_data = questions_data
        self.player_names = player_names
        self.scores = {name: 0 for name in player_names}

        # Create the scoreboard
        self.create_scoreboard()
        # Create the game board with categories and questions
        self.create_game_board()

    def create_scoreboard(self):
        # Scoreboard Frame at the top
        self.scoreboard_frame = tk.Frame(self.window, bg="#00509e", bd=2, relief=tk.RAISED)
        self.scoreboard_frame.grid(row=0, column=0, columnspan=len(self.category_names), pady=10, padx=10)

        # Display each player's name and score
        self.score_labels = {}
        for i, player in enumerate(self.player_names):
            tk.Label(self.scoreboard_frame, text=player, font=("Helvetica", 14, "bold"), bg="#00509e", fg="#ffffff").grid(row=0, column=i*2, padx=5)
            score_label = tk.Label(self.scoreboard_frame, text=f"Score: {self.scores[player]}", font=("Helvetica", 12), bg="#00509e", fg="#ffffff")
            score_label.grid(row=1, column=i*2, padx=5)
            self.score_labels[player] = score_label  # Store label for score updates

    def create_game_board(self):
        # Start categories and questions one row below the scoreboard
        for col, category in enumerate(self.category_names):
            tk.Label(self.window, text=category, font=("Helvetica", 16, "bold"), bg="#007acc", fg="#ffffff", width=15, height=2).grid(row=1, column=col, padx=5, pady=5)

            for row, question_data in enumerate(self.questions_data[category], start=2):
                points = question_data[2].get() or "0"
                question_button = tk.Button(self.window, text=f"${points}", width=15, height=2,
                                            command=lambda c=category, r=row: self.reveal_question(c, r),
                                            bg="#f0c040", fg="#003366", font=("Helvetica", 12),
                                            borderwidth=2, relief=tk.RAISED)
                question_button.grid(row=row, column=col, padx=5, pady=5)

                # Add hover effect
                question_button.bind("<Enter>", lambda e: e.widget.config(bg="#f1a500"))
                question_button.bind("<Leave>", lambda e: e.widget.config(bg="#f0c040"))

    def reveal_question(self, category, row):
        question_data = self.questions_data[category][row - 2]  # Adjusted row index for offset
        question_text = question_data[0].get()
        answer_text = question_data[1].get()
        points = int(question_data[2].get() or "0")

        if question_text:
            question_popup = tk.Toplevel(self.window)
            question_popup.title("Question")
            question_popup.configure(bg="#ffffff")
            tk.Label(question_popup, text=question_text, font=("Helvetica", 14), bg="#ffffff").pack(pady=10)
            tk.Button(question_popup, text="Reveal Answer", command=lambda: self.reveal_answer(question_popup, answer_text, points)).pack(pady=5)
        else:
            messagebox.showinfo("Info", "This question is empty.")

    def reveal_answer(self, popup, answer_text, points):
        popup.destroy()
        answer_popup = tk.Toplevel(self.window)
        answer_popup.title("Answer")
        answer_popup.configure(bg="#ffffff")
        tk.Label(answer_popup, text=f"Answer: {answer_text}", font=("Helvetica", 14), bg="#ffffff").pack(pady=10)

        tk.Label(answer_popup, text="Who answered correctly?", font=("Helvetica", 12), bg="#ffffff").pack(pady=5)
        for player in self.player_names:
            tk.Button(answer_popup, text=player, command=lambda p=player, pts=points: self.update_score(answer_popup, p, pts),
                      bg="#007acc", fg="#ffffff", font=("Helvetica", 12)).pack(pady=2)

    def update_score(self, popup, player, points):
        # Update the player's score and refresh the scoreboard
        self.scores[player] += points
        self.score_labels[player].config(text=f"Score: {self.scores[player]}")  # Update score display
        popup.destroy()
        messagebox.showinfo("Score Update", f"{player} now has {self.scores[player]} points!")
