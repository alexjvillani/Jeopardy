import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
from game_screen import GameScreen  # Import the new GameScreen class

class JeopardyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jeopardy Game")
        self.geometry("800x600")  # Increased window size for better visibility
        self.configure(bg="#f0f0f0")
        
        self.category_names = []
        self.questions_data = {}
        self.player_names = []
        self.current_player_index = 0
        
        self.setup_initial_ui()

    def setup_initial_ui(self):
        self.label = tk.Label(self, text="Jeopardy Game", bg="#f0f0f0", font=("Arial", 24))
        self.label.pack(pady=20)

        self.load_button = tk.Button(self, text="Load Questions", command=self.load_questions)
        self.load_button.pack(pady=10)

        self.start_setup_button = tk.Button(self, text="Setup New Game", command=self.setup_categories)
        self.start_setup_button.pack(pady=10)

        self.start_game_button = tk.Button(self, text="Start Game", command=self.start_game, state='disabled')
        self.start_game_button.pack(pady=10)

        self.save_questions_button = tk.Button(self, text="Save Questions", command=self.save_questions)
        self.save_questions_button.pack(pady=10)

    def setup_categories(self):
        num_categories = simpledialog.askinteger("Categories", "Enter number of categories (1-5):", minvalue=1, maxvalue=5)
        if num_categories:
            self.category_names = []
            self.questions_data = {}
            self.category_frame = tk.Frame(self)
            self.category_frame.pack(pady=20)

            for i in range(num_categories):
                category_name = simpledialog.askstring("Category Name", f"Enter name for category {i + 1}:")
                if category_name:
                    self.category_names.append(category_name)
                    tk.Label(self.category_frame, text=category_name, bg="#f0f0f0", font=("Arial", 16)).grid(row=0, column=i)

                    self.questions_data[category_name] = []
                    for j in range(1, 8):
                        question_frame = tk.Frame(self.category_frame)
                        question_frame.grid(row=j, column=i)

                        question_entry = tk.Entry(question_frame, width=30)
                        question_entry.grid(row=0, column=0, padx=5, pady=5)

                        answer_entry = tk.Entry(question_frame, width=30)
                        answer_entry.grid(row=0, column=1, padx=5, pady=5)

                        points_entry = tk.Entry(question_frame, width=5)
                        points_entry.grid(row=0, column=2, padx=5, pady=5)

                        self.questions_data[category_name].append((question_entry, answer_entry, points_entry))

            messagebox.showinfo("Setup Complete", "Categories and questions set up successfully!")

    def save_questions(self):
        questions_data = {category: [{'question': entry[0].get(), 'answer': entry[1].get(), 'points': int(entry[2].get() or 0)} for entry in entries]
                                for category, entries in self.questions_data.items()}
        
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(questions_data, file)
            messagebox.showinfo("Saved", "Questions saved successfully!")

    def load_questions(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                questions_data = json.load(file)

            self.category_names = list(questions_data.keys())
            self.questions_data = {}

            # Create a canvas for scrolling
            self.canvas = tk.Canvas(self)
            self.scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.scrollable_frame = tk.Frame(self.canvas)

            self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

            self.scrollbar.pack(side="bottom", fill="x")
            self.canvas.pack(side="top", fill="both", expand=True)

            for col, category in enumerate(self.category_names):
                tk.Label(self.scrollable_frame, text=category, bg="#f0f0f0", font=("Arial", 16)).grid(row=0, column=col)

                self.questions_data[category] = []
                for row in range(1, 8):
                    question_info = questions_data[category][row - 1] if row - 1 < len(questions_data[category]) else {'question': '', 'answer': '', 'points': 0}
                    
                    question_frame = tk.Frame(self.scrollable_frame)
                    question_frame.grid(row=row, column=col)

                    question_entry = tk.Entry(question_frame, width=30)
                    question_entry.insert(0, question_info['question'])
                    question_entry.grid(row=0, column=0, padx=5, pady=5)

                    answer_entry = tk.Entry(question_frame, width=30)
                    answer_entry.insert(0, question_info['answer'])
                    answer_entry.grid(row=0, column=1, padx=5, pady=5)

                    points_entry = tk.Entry(question_frame, width=5)
                    points_entry.insert(0, str(question_info['points']))
                    points_entry.grid(row=0, column=2, padx=5, pady=5)

                    self.questions_data[category].append((question_entry, answer_entry, points_entry))

            self.start_game_button['state'] = 'normal'  # Enable Start Game button after loading

    def start_game(self):
        # Ask for the number of players
        num_players = simpledialog.askinteger("Players", "Enter number of players:", minvalue=1, maxvalue=4)
        if num_players:
            self.player_names = []
            for i in range(num_players):
                player_name = simpledialog.askstring("Player Name", f"Enter name for player {i + 1}:")
                if player_name:
                    self.player_names.append(player_name)
                else:
                    messagebox.showerror("Error", "Player name cannot be empty.")
                    return  # Exit if player name is empty

            if len(self.player_names) > 0:
                GameScreen(self.category_names, self.questions_data, self.player_names)  # Pass player names to GameScreen

if __name__ == "__main__":
    app = JeopardyApp()
    app.mainloop()
