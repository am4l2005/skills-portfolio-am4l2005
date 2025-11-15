import tkinter as tk                     # Import the Tkinter GUI library
from tkinter import messagebox           # Import messagebox for popup warnings
import random                            # Import random for generating random numbers
import os                                # Import os for building a safe path to the image
from PIL import Image, ImageTk           # Import Pillow for image loading

# ----------------- Game Settings & State -----------------

TOTAL_QUESTIONS = 10                     # Total number of questions in a quiz
POINTS_FIRST_TRY = 10                    # Points for a correct answer on first attempt
POINTS_SECOND_TRY = 5                    # Points for a correct answer on second attempt
MAX_SCORE = TOTAL_QUESTIONS * POINTS_FIRST_TRY  # Maximum possible score

score = 0                                # Actual game score
displayed_score = 0                      # Score shown on screen (for animation)
current_q = 0                            # Index of the current question (0-based)
difficulty_level = 1                     # Current difficulty level (1=Easy, 2=Moderate, 3=Advanced)
num1 = 0                                 # First operand in the math problem
num2 = 0                                 # Second operand in the math problem
operation = ''                           # Operation symbol ('+' or '-')
attempt = 1                              # Current attempt number for this question
max_attempts = 2                         # Maximum attempts allowed per question

# Mapping for difficulty names (for display if needed later)
difficulty_names = {
    1: "Easy",
    2: "Moderate",
    3: "Advanced"
}

# ----------------- Functions -----------------

def displayMenu():
    """Show the main menu and hide other screens."""
    quiz_frame.pack_forget()            # Hide quiz frame
    result_frame.pack_forget()          # Hide result frame
    # Center menu frame, don't stretch it over the whole window
    menu_frame.pack(expand=True)
    updateScoreLabel()                  # Refresh score display without animation
    attempts_label.config(
        text=f"Attempts Left: {max_attempts}"
    )                                   # Reset attempts label text
    progress_label.config(
        text=f"Q 0 / {TOTAL_QUESTIONS}"
    )                                   # Reset question progress label

def randomInt(level):
    """Return a random integer based on the chosen difficulty level."""
    if level == 1:                      # Easy: single-digit numbers
        return random.randint(0, 9)
    elif level == 2:                    # Moderate: two-digit numbers
        return random.randint(10, 99)
    else:                               # Advanced: four-digit numbers
        return random.randint(1000, 9999)

def decideOperation():
    """Randomly choose between addition and subtraction."""
    return random.choice(['+', '-'])

def isCorrect(user_ans, correct_ans):
    """Check if the user's answer matches the correct answer."""
    return user_ans == correct_ans

def updateScoreLabel(animated=False):
    """
    Update the score label.
    If animated=True, smoothly count up to the new score.
    """
    global displayed_score
    if not animated:
        displayed_score = score
        score_value_label.config(text=str(displayed_score))
    else:
        if displayed_score < score:
            displayed_score += 1
            score_value_label.config(text=str(displayed_score))
            root.after(30, lambda: updateScoreLabel(animated=True))

def updateAttemptsLabel():
    """Update the attempts left label based on the current attempt number."""
    attempts_left = max_attempts - attempt + 1
    attempts_label.config(text=f"Attempts Left: {attempts_left}")

def updateProgressLabel():
    """Update the question progress label (e.g., Q 3 / 10)."""
    shown_q = min(current_q + 1, TOTAL_QUESTIONS)
    progress_label.config(text=f"Q {shown_q} / {TOTAL_QUESTIONS}")

def startQuiz(level):
    """Start the quiz at the chosen difficulty level."""
    global difficulty_level, current_q, attempt, score
    difficulty_level = level
    current_q = 0
    attempt = 1
    score = 0
    menu_frame.pack_forget()
    result_frame.pack_forget()
    # Center quiz frame instead of filling everything
    quiz_frame.pack(expand=True)
    updateScoreLabel()
    updateAttemptsLabel()
    updateProgressLabel()
    displayProblem()

def displayProblem():
    """Generate and display a new math problem or show results if quiz is done."""
    global num1, num2, operation, attempt, current_q
    if current_q >= TOTAL_QUESTIONS:
        displayResults()
        return

    attempt = 1
    num1 = randomInt(difficulty_level)
    num2 = randomInt(difficulty_level)
    operation = decideOperation()

    if operation == '-' and num2 > num1:
        num1, num2 = num2, num1

    problem_label.config(
        text=f"Q{current_q + 1}:  {num1} {operation} {num2} ="
    )

    answer_entry.delete(0, tk.END)
    feedback_label.config(text="")
    updateAttemptsLabel()
    updateProgressLabel()
    answer_entry.focus_set()

def checkAnswer():
    """Check the user's answer, update score, and control quiz flow."""
    global score, current_q, attempt

    if not quiz_frame.winfo_ismapped():
        return

    try:
        user_ans = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a number!")
        return

    correct_ans = num1 + num2 if operation == '+' else num1 - num2

    if isCorrect(user_ans, correct_ans):
        points = POINTS_FIRST_TRY if attempt == 1 else POINTS_SECOND_TRY
        score += points

        feedback_label.config(
            text=f"✅ Correct! +{points} points",
            fg="#2ecc71"
        )

        current_q += 1
        updateScoreLabel(animated=True)
        quiz_frame.after(800, displayProblem)
    else:
        if attempt < max_attempts:
            feedback_label.config(
                text="❌ Incorrect! Try again.",
                fg="#e74c3c"
            )
            attempt += 1
            answer_entry.delete(0, tk.END)
            updateAttemptsLabel()
        else:
            feedback_label.config(
                text=f"❌ Incorrect! The answer was {correct_ans}",
                fg="#e74c3c"
            )
            current_q += 1
            attempt = max_attempts
            updateAttemptsLabel()
            quiz_frame.after(1000, displayProblem)

def displayResults():
    """Show the final score and grade after the quiz is finished."""
    quiz_frame.pack_forget()
    # Center result frame instead of full-screen
    result_frame.pack(expand=True)

    result_label.config(text=f"Your Score: {score}/{MAX_SCORE}")

    if score > 0.9 * MAX_SCORE:
        grade = "A+"
    elif score > 0.8 * MAX_SCORE:
        grade = "A"
    elif score > 0.7 * MAX_SCORE:
        grade = "B+"
    elif score > 0.6 * MAX_SCORE:
        grade = "B"
    else:
        grade = "C"

    grade_label.config(text=f"Grade: {grade}")

def tryAgain():
    """Restart the quiz with the same difficulty."""
    global current_q, attempt, score
    current_q = 0
    attempt = 1
    score = 0
    result_frame.pack_forget()
    quiz_frame.pack(expand=True)
    updateScoreLabel()
    updateAttemptsLabel()
    updateProgressLabel()
    displayProblem()

def returnToMenu():
    """Go back to the main menu from any screen."""
    result_frame.pack_forget()
    quiz_frame.pack_forget()
    displayMenu()

def quitGame():
    """Close the application."""
    root.destroy()

def on_enter_key(event):
    """Handle Enter key press to submit the answer during the quiz."""
    checkAnswer()

# ----------------- GUI Setup -----------------

root = tk.Tk()
root.title("🎨 Math Quiz")
root.geometry("600x480")
root.configure(bg="#f2f3f7")
root.resizable(False, False)

root.bind('<Return>', on_enter_key)

# ----------------- Background Image -----------------

# Build a safe absolute path to background.png in the SAME folder as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "background.png")

# Load with Pillow (handles PNG/JPG/etc.) and resize to window size
bg_pil = Image.open(image_path)
bg_pil = bg_pil.resize((600, 480), Image.LANCZOS)
background_image = ImageTk.PhotoImage(bg_pil)

background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# ----------------- Fonts -----------------

header_font = ("Helvetica", 20, "bold")
question_font = ("Helvetica", 18, "bold")
button_font = ("Helvetica", 12, "bold")
feedback_font = ("Helvetica", 12)
topbar_font = ("Helvetica", 10, "bold")

# ----------------- Top Bar (Score + Attempts + Progress) -----------------

top_bar = tk.Frame(root, bg="#1e272e")
top_bar.pack(side="top", fill="x")

left_top = tk.Frame(top_bar, bg="#1e272e")
left_top.pack(side="left", padx=10, pady=6)

score_title_label = tk.Label(
    left_top,
    text="⭐ Score",
    font=topbar_font,
    bg="#1e272e",
    fg="#f1c40f"
)
score_title_label.pack(anchor="w")

score_value_label = tk.Label(
    left_top,
    text=str(displayed_score),
    font=("Helvetica", 16, "bold"),
    bg="#1e272e",
    fg="#ecf0f1"
)
score_value_label.pack(anchor="w")

attempts_label = tk.Label(
    left_top,
    text=f"Attempts Left: {max_attempts}",
    font=("Helvetica", 9),
    bg="#1e272e",
    fg="#dcdde1"
)
attempts_label.pack(anchor="w", pady=(4, 0))

progress_label = tk.Label(
    left_top,
    text=f"Q 0 / {TOTAL_QUESTIONS}",
    font=("Helvetica", 9),
    bg="#1e272e",
    fg="#dcdde1"
)
progress_label.pack(anchor="w")

title_label = tk.Label(
    top_bar,
    text="🎮 Math Quest",
    font=("Helvetica", 16, "bold"),
    bg="#1e272e",
    fg="#ecf0f1"
)
title_label.pack(side="right", padx=15)

# ----------------- Menu Frame -----------------

menu_frame = tk.Frame(root, bg="#f2f3f7")

menu_title = tk.Label(
    menu_frame,
    text="Choose Your Challenge",
    font=header_font,
    bg="#f2f3f7",
    fg="#2d3436"
)
menu_title.pack(pady=(40, 10))

menu_subtitle = tk.Label(
    menu_frame,
    text="Pick a difficulty to start your math adventure!",
    font=("Helvetica", 11),
    bg="#f2f3f7",
    fg="#636e72"
)
menu_subtitle.pack(pady=(0, 20))

tk.Button(
    menu_frame,
    text="Easy 🌱",
    font=button_font,
    width=20,
    fg="#27ae60",
    bg="#ecf0f1",
    activebackground="#d1f2eb",
    command=lambda: startQuiz(1)
).pack(pady=8)

tk.Button(
    menu_frame,
    text="Moderate ⚡",
    font=button_font,
    width=20,
    fg="#f1c40f",
    bg="#ecf0f1",
    activebackground="#fcf3cf",
    command=lambda: startQuiz(2)
).pack(pady=8)

tk.Button(
    menu_frame,
    text="Advanced 🔥",
    font=button_font,
    width=20,
    fg="#e74c3c",
    bg="#ecf0f1",
    activebackground="#f9e0e0",
    command=lambda: startQuiz(3)
).pack(pady=8)

# ----------------- Quiz Frame -----------------

quiz_frame = tk.Frame(root, bg="#f2f3f7")

top_quiz_row = tk.Frame(quiz_frame, bg="#f2f3f7")
top_quiz_row.pack(fill="x", pady=(10, 0), padx=15)

tk.Button(
    top_quiz_row,
    text="⟵ Menu",
    font=("Helvetica", 10, "bold"),
    bg="#0984e3",
    fg="white",
    activebackground="#74b9ff",
    command=returnToMenu
).pack(side="right")

card_frame = tk.Frame(
    quiz_frame,
    bg="white",
    bd=2,
    relief="ridge",
    highlightbackground="#dfe6e9",
    highlightthickness=1
)
card_frame.pack(pady=40, ipadx=40, ipady=30)

problem_label = tk.Label(
    card_frame,
    text="",
    font=question_font,
    bg="white",
    fg="#2d3436"
)
problem_label.pack(pady=(5, 15))

answer_entry = tk.Entry(
    card_frame,
    font=question_font,
    width=8,
    justify='center',
    bd=2,
    relief="groove"
)
answer_entry.pack(pady=5)

tk.Button(
    card_frame,
    text="Submit Answer",
    font=button_font,
    bg="#00b894",
    fg="white",
    activebackground="#55efc4",
    width=18,
    command=checkAnswer
).pack(pady=15)

feedback_label = tk.Label(
    card_frame,
    text="",
    font=feedback_font,
    bg="white",
    fg="#2d3436"
)
feedback_label.pack(pady=5)

# ----------------- Result Frame -----------------

result_frame = tk.Frame(root, bg="#f2f3f7")

result_card = tk.Frame(
    result_frame,
    bg="white",
    bd=2,
    relief="ridge",
    highlightbackground="#dfe6e9",
    highlightthickness=1
)
result_card.pack(pady=40, ipadx=40, ipady=30)

result_label = tk.Label(
    result_card,
    text="",
    font=header_font,
    bg="white",
    fg="#2d3436"
)
result_label.pack(pady=10)

grade_label = tk.Label(
    result_card,
    text="",
    font=question_font,
    bg="white",
    fg="#636e72"
)
grade_label.pack(pady=10)

tk.Button(
    result_card,
    text="Try Again 🔁",
    font=button_font,
    bg="#6c5ce7",
    fg="white",
    activebackground="#a29bfe",
    width=20,
    command=tryAgain
).pack(pady=5)

tk.Button(
    result_card,
    text="Main Menu ⟲",
    font=button_font,
    bg="#0984e3",
    fg="white",
    activebackground="#74b9ff",
    width=20,
    command=returnToMenu
).pack(pady=5)

tk.Button(
    result_card,
    text="Quit Game ⏹",
    font=button_font,
    bg="#d63031",
    fg="white",
    activebackground="#ff7675",
    width=20,
    command=quitGame
).pack(pady=5)

# ----------------- Start with Menu -----------------

displayMenu()

root.mainloop()
