# ==========================================================
# Mean Absolute Error (MAE) Loss - Step by Step Demonstration
# ==========================================================
# Click "Next" to move forward through the 6 steps of the calculation.

import matplotlib.pyplot as plt
from matplotlib.widgets import Button   # lets us add clickable buttons

# ----------------------------------------------------------
# PART 1: THE DATA
# ----------------------------------------------------------
actual = [10, 20, 30, 40, 50]
predicted = [12, 18, 33, 37, 55]

print("Actual values   :", actual)
print("Predicted values:", predicted)
answer = input("Press Enter to keep these predictions, "
               "or type 5 new predicted values separated by spaces: ")

# If the user typed something, try to use it as the new predicted values
if answer.strip() != "":
    try:
        new_values = [float(v) for v in answer.split()]
        if len(new_values) == 5:
            predicted = new_values
        else:
            print("You must type exactly 5 numbers. Using the default values.")
    except ValueError:
        print("Those were not valid numbers. Using the default values.")

# ----------------------------------------------------------
# PART 2: THE MAE CALCULATION (plain Python, no tricks)
# ----------------------------------------------------------
n = len(actual)          # number of observations
errors = []              # actual - predicted (can be negative)
abs_errors = []          # |actual - predicted| (never negative)

for i in range(n):
    error = actual[i] - predicted[i]   # STEP 2
    errors.append(error)
    abs_errors.append(abs(error))      # STEP 3

total = sum(abs_errors)  # STEP 4: add all absolute errors
mae = total / n          # STEP 5: divide by n

print("Errors          :", errors)
print("Absolute errors :", abs_errors)
print("Sum             :", total)
print("MAE             :", mae)


# Small helper: shows 3.0 as "3" and 2.5 as "2.5" so numbers look clean
def fmt(number):
    return f"{number:g}"


# Text like "2 + 2 + 3 + 3 + 5" used in the calculation panel
parts = []
for a in abs_errors:
    parts.append(fmt(a))
sum_text = " + ".join(parts)

# ----------------------------------------------------------
# PART 3: TEXT SHOWN AT EACH STEP
# ----------------------------------------------------------
titles = [
    "Step 1: Actual vs Predicted values",
    "Step 2: Prediction errors",
    "Step 3: Absolute errors",
    "Step 4: Sum of absolute errors",
    "Step 5: Divide by n",
    "Step 6: Final result",
]

explanations = [
    "STEP 1: The blue bars are the real (actual) values.\n"
    "The orange bars are what our model predicted.",

    "STEP 2: Error = Actual - Predicted.\n"
    "Bars above zero: model guessed too LOW. Bars below zero: model guessed too HIGH.",

    "STEP 3: Absolute value removes the minus sign. A miss of -2 and a miss of +2\n"
    "are both 2 units wrong, so the negative bars flip upward (gray -> red).",

    "STEP 4: Add up all the absolute errors: " + sum_text + " = " + fmt(total),

    "STEP 5: Divide the sum by n (the number of observations)\n"
    "to get the AVERAGE error: " + fmt(total) + " / " + str(n) + " = " + fmt(mae),

    "STEP 6: On average, our predictions are off by " + fmt(mae) + " units.",
]

# Colors: one color for each idea
BLUE = "royalblue"       # actual values
ORANGE = "darkorange"    # predicted values
PURPLE = "mediumpurple"  # raw errors
RED = "crimson"          # absolute errors
GREEN = "seagreen"       # MAE result

# ----------------------------------------------------------
# PART 4: SET UP THE WINDOW
# ----------------------------------------------------------
fig = plt.figure(figsize=(13, 7))
fig.suptitle("Mean Absolute Error (MAE) Loss", fontsize=22, fontweight="bold")
fig.text(0.5, 0.88, "MAE = (1/n) * sum( |actual - predicted| )",
         ha="center", fontsize=15, color="dimgray")

ax = fig.add_axes([0.07, 0.30, 0.55, 0.50])       # left: bar chart
ax_text = fig.add_axes([0.66, 0.30, 0.32, 0.50])  # right: calculation panel
explain = fig.text(0.5, 0.20, "", ha="center", va="center", fontsize=12)

x = list(range(n))                      # bar positions 0,1,2,3,4
left = [i - 0.2 for i in x]             # positions for the left bar of a pair
right = [i + 0.2 for i in x]            # positions for the right bar of a pair

step = 0   # which step we are currently showing (0 to 5)


# Helper: write the value on top of (or below) each bar
def put_labels(positions, values):
    for i in range(n):
        if values[i] >= 0:
            ax.text(positions[i], values[i] + 0.3, fmt(values[i]),
                    ha="center", va="bottom", fontweight="bold")
        else:
            ax.text(positions[i], values[i] - 0.3, fmt(values[i]),
                    ha="center", va="top", fontweight="bold")


# ----------------------------------------------------------
# PART 5: DRAW ONE STEP
# ----------------------------------------------------------
def draw_step(step):
    ax.clear()              # wipe the old chart
    ax_text.clear()         # wipe the old calculation panel
    ax_text.axis("off")     # the panel has no axes lines, only text

    ax.axhline(0, color="black", linewidth=1)   # the zero line
    ax.set_xticks(x)
    ax.set_xticklabels(["Data " + str(i + 1) for i in range(n)])
    ax.set_ylabel("Value")
    ax.set_title(titles[step], fontsize=14, fontweight="bold")

    panel = ""   # the text for the right-hand panel

    if step == 0:
        ax.bar(left, actual, 0.4, color=BLUE, label="Actual")
        ax.bar(right, predicted, 0.4, color=ORANGE, label="Predicted")
        put_labels(left, actual)
        put_labels(right, predicted)
        ax.set_ylim(0, max(actual + predicted) * 1.2)
        panel = "Actual vs Predicted\n\n"
        for i in range(n):
            panel += "Data " + str(i + 1) + ": " + fmt(actual[i]) + " vs " + fmt(predicted[i]) + "\n"

    elif step == 1:
        ax.bar(x, errors, 0.5, color=PURPLE, label="Error = Actual - Predicted")
        put_labels(x, errors)
        ax.set_ylim(min(errors + [0]) - 2, max(errors + abs_errors + [0]) + 2)
        panel = "Error = Actual - Predicted\n\n"
        for i in range(n):
            panel += fmt(actual[i]) + " - " + fmt(predicted[i]) + " = " + fmt(errors[i]) + "\n"

    elif step == 2:
        ax.bar(left, errors, 0.4, color="lightgray", label="Error (can be negative)")
        ax.bar(right, abs_errors, 0.4, color=RED, label="Absolute error")
        put_labels(left, errors)
        put_labels(right, abs_errors)
        ax.set_ylim(min(errors + [0]) - 2, max(errors + abs_errors + [0]) + 2)
        panel = "Absolute Error = |Error|\n\n"
        for i in range(n):
            panel += "|" + fmt(errors[i]) + "| = " + fmt(abs_errors[i]) + "\n"
        panel += "\nWithout | | the errors cancel:\n"
        panel += "sum of errors = " + fmt(sum(errors))

    else:   # steps 3, 4 and 5 all show the absolute error bars
        ax.bar(x, abs_errors, 0.5, color=RED, label="Absolute error")
        put_labels(x, abs_errors)
        ax.set_ylim(0, max(abs_errors) + 2)

        if step == 3:
            panel = "Sum of absolute errors\n\n" + sum_text + "\n= " + fmt(total)

        if step >= 4:   # draw the average as a dashed green line
            ax.axhline(mae, color=GREEN, linestyle="--", linewidth=2.5,
                       label="MAE = " + fmt(mae))

        if step == 4:
            panel = ("Divide by n\n\nn = " + str(n) + "\n"
                     "MAE = " + fmt(total) + " / " + str(n) + "\n"
                     "    = " + fmt(mae))

        if step == 5:
            panel = ("MAE = (1/n) * sum|...|\n"
                     "    = (1/" + str(n) + ") * " + fmt(total) + "\n"
                     "    = " + fmt(mae))
            # the big final answer
            ax_text.text(0.0, 0.20, "MAE = " + fmt(mae), fontsize=34,
                         fontweight="bold", color=GREEN,
                         bbox=dict(boxstyle="round", facecolor="honeydew", edgecolor=GREEN))

    ax.legend(loc="upper left")
    ax_text.text(0, 1, panel, va="top", fontsize=12, family="monospace")
    explain.set_text(explanations[step])
    fig.canvas.draw_idle()   # refresh the window


# ----------------------------------------------------------
# PART 6: BUTTONS
# ----------------------------------------------------------
def next_clicked(event):
    global step
    if step < 5:
        step += 1
    draw_step(step)


def back_clicked(event):
    global step
    if step > 0:
        step -= 1
    draw_step(step)


def save_clicked(event):
    filename = "mae_step_" + str(step + 1) + ".png"
    fig.savefig(filename, dpi=150)
    print("Saved", filename)


# Each button needs its own small area on the window
back_button = Button(fig.add_axes([0.25, 0.04, 0.14, 0.07]), "Back")
next_button = Button(fig.add_axes([0.43, 0.04, 0.14, 0.07]), "Next")
save_button = Button(fig.add_axes([0.61, 0.04, 0.18, 0.07]), "Save screenshot")

back_button.on_clicked(back_clicked)
next_button.on_clicked(next_clicked)
save_button.on_clicked(save_clicked)

# ----------------------------------------------------------
# PART 7: START
# ----------------------------------------------------------
draw_step(0)   # show Step 1 first
plt.show()     # open the window
