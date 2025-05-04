import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from classes.random_agent import Random_Agent
from classes.random_agent import Smart_Agent
from classes.minimax_agent import Minimax_Agent
from classes.ml_agent import MLAgent
from classes.board import Board
from ucimlrepo import fetch_ucirepo

# Fetch Connect-4 dataset
connect_4 = fetch_ucirepo(id=26)

def play_match(agent1, agent2, first=1):
    board = Board()
    turn = 0 if first == 1 else 1

    # Stats to collect
    stats = {
        "winner": None,
        "moves": 0,
        "nodes1": 0,
        "prunes1": 0,
        "depth1": 0.0,   # avg depth per move
        "nodes2": 0,
        "prunes2": 0,
        "depth2": 0.0,   # avg depth per move
    }

    # Helpers to accumulate depth
    depth_sum1 = 0
    depth_sum2 = 0
    move_count1 = 0
    move_count2 = 0

    start = time.perf_counter()

    # Train MLAgents if needed
    for agent in (agent1, agent2):
        if isinstance(agent, MLAgent) and not agent.trained:
            X = connect_4.data.features.replace({'x': 1, 'o': 2, 'b': 0}).astype(int)
            y = connect_4.data.targets.replace({'win': 0, 'draw': 1, 'loss': 2})
            agent.load_data(X, y)
            agent.train()

    # Main game loop
    while True:
        if turn == 0:
            # reset & play agent1
            agent1.max_depth_reached = 0
            col = agent1.best_move(board)
            depth_sum1 += agent1.max_depth_reached
            move_count1 += 1
            piece = 1
        else:
            # reset & play agent2
            agent2.max_depth_reached = 0
            col = agent2.best_move(board)
            depth_sum2 += agent2.max_depth_reached
            move_count2 += 1
            piece = 2

        row = board.get_next_open_row(col)
        board.drop_piece(row, col, piece)
        stats["moves"] += 1

        # check for terminal
        if board.check_win(piece) or board.is_full():
            stats["winner"] = piece if board.check_win(piece) else 0
            break

        turn ^= 1

    # finalize stats
    stats["time"]    = time.perf_counter() - start
    stats["nodes1"]  = agent1.total_nodes
    stats["prunes1"] = agent1.total_prunes
    stats["depth1"]  = (depth_sum1 / move_count1) if move_count1 else 0.0
    stats["nodes2"]  = agent2.total_nodes
    stats["prunes2"] = agent2.total_prunes
    stats["depth2"]  = (depth_sum2 / move_count2) if move_count2 else 0.0

    # reset all counters for next match
    for a in (agent1, agent2):
        a.total_nodes = 0
        a.total_prunes = 0
        a.max_depth_reached = 0

    return stats

def tournament(agent1_cls, agent2_cls, n=500):
    records = []
    for i in range(n):
        a1 = agent1_cls(1, 2, 0)
        a2 = agent2_cls(2, 1, 1)
        # clear instrumentation
        for a in (a1, a2):
            a.total_nodes = 0
            a.total_prunes = 0
            a.max_depth_reached = 0

        first = 1 if i % 2 == 0 else 2
        stats = play_match(a1, a2, first=first)
        stats["matchup"] = f"{agent1_cls.__name__} vs {agent2_cls.__name__}"
        records.append(stats)

    return pd.DataFrame(records)

# Run tournaments
df_RvS  = tournament(Random_Agent, Smart_Agent,  n=500)
df_SvM  = tournament(Smart_Agent,  Minimax_Agent, n=500)
df_MvML = tournament(Minimax_Agent, MLAgent,       n=500)

# Combine + summarize
df = pd.concat([df_RvS, df_SvM, df_MvML], ignore_index=True)
summary = df.groupby("matchup").agg(
    WinRate1   = ("winner", lambda x: (x == 1).mean()),
    DrawRate   = ("winner", lambda x: (x == 0).mean()),
    WinRate2   = ("winner", lambda x: (x == 2).mean()),
    AvgNodes1  = ("nodes1", "mean"),
    AvgPrunes1 = ("prunes1", "mean"),
    AvgDepth1  = ("depth1", "mean"),
    AvgNodes2  = ("nodes2", "mean"),
    AvgPrunes2 = ("prunes2", "mean"),
    AvgDepth2  = ("depth2", "mean"),
    AvgMoves   = ("moves", "mean"),
    AvgTime    = ("time", "mean"),
).reset_index()

print(summary)

# === Plots ===
sns.set(style="whitegrid")

# Win/Draw/Loss
melted = summary.melt(
    id_vars    = "matchup",
    value_vars = ["WinRate1", "DrawRate", "WinRate2"],
    var_name   = "Outcome",
    value_name = "Rate"
)
plt.figure(figsize=(8,5))
sns.barplot(data=melted, x="matchup", y="Rate", hue="Outcome")
plt.title("Win/Draw/Loss Rates by Matchup")
plt.ylim(0,1)
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

# Avg nodes expanded
plt.figure(figsize=(8,4))
sns.barplot(data=summary, x="matchup", y="AvgNodes1", label="Agent1")
sns.barplot(data=summary, x="matchup", y="AvgNodes2", label="Agent2", alpha=0.7)
plt.title("Average Nodes Expanded")
plt.ylabel("Nodes")
plt.xticks(rotation=15)
plt.legend()
plt.tight_layout()
plt.show()

# Avg depth per move
plt.figure(figsize=(8,4))
sns.barplot(data=summary, x="matchup", y="AvgDepth1", label="Agent1")
sns.barplot(data=summary, x="matchup", y="AvgDepth2", label="Agent2", alpha=0.7)
plt.title("Average Search Depth per Move")
plt.ylabel("Depth")
plt.xticks(rotation=15)
plt.legend()
plt.tight_layout()
plt.show()

# Pruning effectiveness
summary["PruneEffect1"] = summary["AvgPrunes1"] / summary["AvgNodes1"]
summary["PruneEffect2"] = summary["AvgPrunes2"] / summary["AvgNodes2"]
plt.figure(figsize=(8,4))
sns.barplot(data=summary, x="matchup", y="PruneEffect1", label="Agent1")
sns.barplot(data=summary, x="matchup", y="PruneEffect2", label="Agent2", alpha=0.7)
plt.title("Pruning Effectiveness (#prunes / #nodes)")
plt.ylabel("Fraction")
plt.xticks(rotation=15)
plt.legend()
plt.tight_layout()
plt.show()

# Game length distribution
plt.figure(figsize=(8,4))
sns.histplot(data=df, x="moves", hue="matchup", element="step", stat="density", common_norm=False)
plt.title("Distribution of Game Length (#moves)")
plt.xlabel("Moves")
plt.tight_layout()
plt.show()
