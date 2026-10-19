# Three simple figures about MAE for the report.
# Run:  python mae_figures.py   (creates figure1.png, figure2.png, figure3.png)
import matplotlib.pyplot as plt

actual = [10, 20, 30, 40, 50]
predicted = [12, 18, 33, 37, 55]
points = [1, 2, 3, 4, 5]

# ---------- Figure 1: actual vs predicted, red line = absolute error ----------
plt.figure(figsize=(8, 5))
plt.scatter(points, actual, color="royalblue", s=90, label="Actual", zorder=3)
plt.scatter(points, predicted, color="darkorange", s=90, label="Predicted", zorder=3)
for i in range(5):
    plt.plot([points[i], points[i]], [actual[i], predicted[i]], color="crimson", linewidth=3)
plt.plot([], [], color="crimson", linewidth=3, label="Absolute error (line length)")
plt.title("Figure 1: Actual vs Predicted values")
plt.xlabel("Data point")
plt.ylabel("Value")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("figure1.png", dpi=150)

# ---------- Figure 2: MAE loss for ONE sample (V-shape) ----------
# The actual value is 30. We try many predictions and see the loss.
guesses = list(range(10, 51))
losses = []
for g in guesses:
    losses.append(abs(30 - g))
plt.figure(figsize=(8, 5))
plt.plot(guesses, losses, color="crimson", linewidth=3)
plt.scatter([33], [3], color="seagreen", s=100, zorder=3, label="Prediction 33 -> loss 3")
plt.title("Figure 2: MAE loss for one sample (actual = 30)")
plt.xlabel("Predicted value")
plt.ylabel("Absolute error")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("figure2.png", dpi=150)

# ---------- Figure 3: MAE loss vs squared (MSE) loss ----------
errs = []
for i in range(-50, 51):
    errs.append(i / 10)           # -5.0, -4.9, ... , 5.0
mae_curve = []
mse_curve = []
for e in errs:
    mae_curve.append(abs(e))
    mse_curve.append(e * e)
plt.figure(figsize=(8, 5))
plt.plot(errs, mae_curve, color="crimson", linewidth=3, label="MAE loss  |error|")
plt.plot(errs, mse_curve, color="royalblue", linewidth=3, label="Squared loss  error^2")
plt.title("Figure 3: MAE grows steadily, squared loss grows fast")
plt.xlabel("Error (actual - predicted)")
plt.ylabel("Loss")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("figure3.png", dpi=150)

print("Saved figure1.png, figure2.png, figure3.png")
