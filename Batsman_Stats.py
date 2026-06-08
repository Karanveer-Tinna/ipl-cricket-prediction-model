import pandas as pd

# Step 1: Load the CSV
df = pd.read_csv('ipl_ball_by_ball.csv')

# Step 2: Group and Sum
batsman_runs = df.groupby('batsman')['runs_batsman'].sum().reset_index()

# Step 3: Sort (optional)
batsman_runs = batsman_runs.sort_values(by='runs_batsman', ascending=False)

# Step 4: Show the top 10
print(batsman_runs.head(10))