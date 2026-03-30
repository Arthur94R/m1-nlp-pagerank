import random
import networkx as nx
import matplotlib.pyplot as plt

# --- Génération du graphe ---
N = random.randint(50, 100)
G = nx.gnm_random_graph(N, 3*N, directed=True, seed=42)

# --- PageRank ---
pr = nx.pagerank(G, alpha=0.85)

# --- Top 20 ---
top20 = sorted(pr, key=pr.get, reverse=True)[:20]
subgraph = G.subgraph(top20)

print("\nTop 20 nœuds par PageRank :")
for i, node in enumerate(top20, 1):
    print(f"  {i:2}. Nœud {node:3d} → {pr[node]:.6f}")

# --- Visualisation ---
pos = nx.spring_layout(subgraph, seed=0)
sizes = [pr[n] * 80000 for n in subgraph.nodes()]
colors = ["#185FA5" if i < 5 else "#1D9E75" for i, n in enumerate(top20)]

plt.figure(figsize=(12, 8))
nx.draw_networkx(
    subgraph, pos,
    node_size=sizes,
    node_color=colors,
    edge_color="#cccccc",
    font_size=9,
    font_color="white",
    arrows=True,
    arrowsize=10,
    width=0.8
)
plt.title(f"Top 20 nœuds — PageRank (N={N})\nBleu = top 5 | Vert = top 6–20 | Taille ∝ score", fontsize=13)
plt.axis("off")
plt.tight_layout()
plt.savefig("pagerank_graphe.png", dpi=150)
plt.show()
print("Graphe sauvegardé : pagerank_graphe.png")