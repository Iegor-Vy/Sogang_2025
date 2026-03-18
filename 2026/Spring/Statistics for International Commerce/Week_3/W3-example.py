import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# simulate coin tosses
np.random.seed(42)
n_tosses = 100

tosses = np.random.choice(["Heads", "Tails"], size=n_tosses)

df = pd.DataFrame({
    "Toss": range(1, n_tosses + 1),
    "Outcome": tosses
})

# cumulative proportion of heads
df["Heads_Count"] = (df["Outcome"] == "Heads").cumsum()
df["Heads_Proportion"] = df["Heads_Count"] / df["Toss"]

# interactive plot
fig = px.line(
    df,
    x="Toss",
    y="Heads_Proportion",
    title="Coin Toss Simulation: Convergence to 0.5",
)


fig = go.Figure()

for n in [10, 50, 100, 500, 1000]:
    tosses = np.random.choice(["Heads", "Tails"], size=n)
    heads_prop = (tosses == "Heads").cumsum() / np.arange(1, n+1)

    fig.add_trace(go.Scatter(
        x=list(range(1, n+1)),
        y=heads_prop,
        mode='lines',
        name=f"{n} tosses",
        visible=(n==100)
    ))

# slider
steps = []
for i, n in enumerate([10, 50, 100, 500, 1000]):
    step = dict(
        method="update",
        args=[{"visible": [False]*5},
              {"title": f"{n} Tosses"}],
    )
    step["args"][0]["visible"][i] = True
    steps.append(step)

fig.update_layout(
    sliders=[dict(active=2, steps=steps)],
    title="Interactive Coin Toss Simulation"
)

fig.add_hline(y=0.5, line_dash="dash")

fig.show()

# histogram of outcomes
fig2 = px.histogram(
    df,
    x="Outcome",
    title="Distribution of Coin Toss Outcomes",
)

fig2.show()


