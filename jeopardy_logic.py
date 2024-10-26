# jeopardy_logic.py

class Category:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def add_question(self, question, answer, points):
        self.questions.append((question, answer, points))


class JeopardyGame:
    def __init__(self):
        self.categories = {}
        self.score = 0

    def add_category(self, category_name):
        self.categories[category_name] = Category(category_name)

    def add_question(self, category_name, question, answer, points):
        self.categories[category_name].add_question(question, answer, points)

    def update_score(self, points):
        self.score += points
