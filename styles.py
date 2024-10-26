# styles.py

BACKGROUND_COLOR = "#1e1e2f"
BUTTON_COLOR = "#5a9"
TEXT_COLOR = "#fafafa"
CATEGORY_COLOR = "#3b3b51"
FONT_TITLE = ("Helvetica", 20, "bold")
FONT_TEXT = ("Helvetica", 12)
FONT_SCORE = ("Helvetica", 16, "bold")

def apply_styles(widget):
    widget.configure(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
