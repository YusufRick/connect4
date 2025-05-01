import time
import random
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from classes.random_agent import Random_Agent
from classes.random_agent import Smart_Agent
from classes.minimax_agent import Minimax_Agent
from classes.ml_agent import MLAgent
from classes.board import Board
from ucimlrepo import fetch_ucirepo


connect_4 = fetch_ucirepo(id=26)

# Function to play a match between two agents
def play_match(agent1, agent2, first=1):
    board = Board()
    turn = 0 if first == 1 else 1
    stats = {
        "winner": None,
        "moves": 0,
        "nodes1": getattr(agent1, "total_nodes", 0),
        "nodes2": getattr(agent2, "total_nodes", 0),
        "prunes1": getattr(agent1, "total_prunes", 0),
        "prunes2": getattr(agent2, "total_prunes", 0),
        "depth1": getattr(agent1, "max_depth_reached", 0),
        "depth2": getattr(agent2, "max_depth_reached", 0),
    }
    start = time.perf_counter()


    if isinstance(agent1, MLAgent) and not agent1.trained:
        X = connect_4.data.features.replace({'x': 1, 'o': 2, 'b': 0}).astype(int)
        y = connect_4.data.targets.replace({'win': 0, 'draw': 1, 'loss': 2})
        agent1.load_data(X, y)
        agent1.train()

    if isinstance(agent2, MLAgent) and not agent2.trained:
        X = connect_4.data.features.replace({'x': 1, 'o': 2, 'b': 0}).astype(int)
        y = connect_4.data.targets.replace({'win': 0, 'draw': 1, 'loss': 2})
        agent2.load_data(X, y)
        agent2.train()
        
    while True:
        if turn == 0:
            col = agent1.best_move(board)
            piece = 1
        else:
            col = agent2.best_move(board)
            piece = 2
        row = board.get_next_open_row(col)
        board.drop_piece(row, col, piece)
        stats["moves"] += 1
        if board.check_win(piece) or board.is_full():
            stats["winner"] = piece if board.check_win(piece) else 0
            break
        turn ^= 1
    stats["time"] = time.perf_counter() - start
    return stats

# Tournament function to play matches between two agents
def tournament(agent1_cls, agent2_cls, n=500):
    records = []
    for i in range(n):
        # instantiate fresh agents
        a1 = agent1_cls(1, 2, 0)
        a2 = agent2_cls(2, 1, 1)
        # reset instrumentation
        for a in (a1, a2):
            for attr in ("total_nodes", "total_prunes", "max_depth_reached"):
                setattr(a, attr, 0)
        first = 1 if i % 2 == 0 else 2
        stats = play_match(a1, a2, first=first)
        stats["matchup"] = f"{agent1_cls.__name__} vs {agent2_cls.__name__}"
        records.append(stats)
    return pd.DataFrame(records)

# Run all three tournaments
df_RvS = tournament(Random_Agent, Smart_Agent, n=500)
df_SvM = tournament(Smart_Agent, Minimax_Agent, n=500)
df_MvML = tournament(Minimax_Agent, MLAgent, n=500)

# Combine dataframes from all tournaments
df = pd.concat([df_RvS, df_SvM, df_MvML], ignore_index=True)

# Summarize data
summary = df.groupby("matchup").agg(
    WinRate1=("winner", lambda x: (x == 1).mean()),
    DrawRate=("winner", lambda x: (x == 0).mean()),
    WinRate2=("winner", lambda x: (x == 2).mean()),
    AvgNodes1=("nodes1", "mean"),
    AvgNodes2=("nodes2", "mean"),
    AvgPrunes1=("prunes1", "mean"),
    AvgPrunes2=("prunes2", "mean"),
    AvgDepth1=("depth1", "mean"),
    AvgDepth2=("depth2", "mean"),
    AvgMoves=("moves", "mean"),
    AvgTime=("time", "mean"),
).reset_index()

print(summary)

# 1) Win/Draw/Loss stacked bar
melted = summary.melt(
    id_vars="matchup",
    value_vars=["WinRate1", "DrawRate", "WinRate2"],
    var_name="Outcome", value_name="Rate"
)
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
sns.barplot(data=melted, x="matchup", y="Rate", hue="Outcome")
plt.title("Win/Draw/Loss Rates by Matchup")
plt.ylim(0, 1)
plt.legend(loc="upper right")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

# 2) Avg nodes expanded
plt.figure(figsize=(8, 4))
sns.barplot(data=summary, x="matchup", y="AvgNodes1", label="Agent1")
sns.barplot(data=summary, x="matchup", y="AvgNodes2", label="Agent2", alpha=0.7)
plt.title("Average Nodes Expanded")
plt.ylabel("Nodes")
plt.xticks(rotation=15)
plt.legend()
plt.tight_layout()
plt.show()

# 3) Search depth reached
plt.figure(figsize=(8, 4))
sns.barplot(data=summary, x="matchup", y="AvgDepth1", label="Agent1")
sns.barplot(data=summary, x="matchup", y="AvgDepth2", label="Agent2", alpha=0.7)
plt.title("Average Search Depth Reached")
plt.ylabel("Depth")
plt.xticks(rotation=15)
plt.legend()
plt.tight_layout()
plt.show()

# 4) Pruning effectiveness
summary["PruneEffect1"] = summary["AvgPrunes1"] / summary["AvgNodes1"]
summary["PruneEffect2"] = summary["AvgPrunes2"] / summary["AvgNodes2"]
plt.figure(figsize=(8, 4))
sns.barplot(data=summary, x="matchup", y="PruneEffect1", label="Agent1")
sns.barplot(data=summary, x="matchup", y="PruneEffect2", label="Agent2", alpha=0.7)
plt.title("Pruning Effectiveness (#prunes / #nodes)")
plt.ylabel("Fraction")
plt.xticks(rotation=15)
plt.legend()
plt.tight_layout()
plt.show()

# 5) Game length distribution
plt.figure(figsize=(8, 4))
sns.histplot(data=df, x="moves", hue="matchup", element="step", stat="density", common_norm=False)
plt.title("Distribution of Game Length (#moves)")
plt.xlabel("Moves")
plt.tight_layout()
plt.show()
