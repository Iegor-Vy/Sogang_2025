# Generate the requested supply-demand plot with equilibrium
import numpy as np
import matplotlib.pyplot as plt

# Define price range
P = np.arange(0, 20.5, 0.5)

# Demand and supply
Qd = 100 - 5*P
Qs = 20 + 3*P

# Equilibrium
P_eq = 10
Q_eq = 50

# Plot
plt.figure()
plt.plot(Qd, P, label="Demand Curve")
plt.plot(Qs, P, label="Supply Curve")
plt.scatter([Q_eq], [P_eq], label="Equilibrium")
plt.text(Q_eq, P_eq, "  E(50, 10)")

plt.title("Market Equilibrium")
plt.xlabel("Quantity (Q)")
plt.ylabel("Price (P)")
plt.legend()

# Save figure
path = "C:\\Users\\vyshn\\OneDrive - kdis.ac.kr\\Sogang\\Work\\Spring_2026\\Mathematical Methods for International Commerce\\Week 2_2\\market_equilibrium_plot.png"
plt.savefig(path, dpi=150, bbox_inches="tight")
plt.close()

path