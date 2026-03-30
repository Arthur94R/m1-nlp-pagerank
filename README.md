# TP5 — PageRank

## Dépendances

```bash
pip install networkx matplotlib requests beautifulsoup4
```

---

## Partie 1 — Graphe aléatoire (`graph.py`)

Un graphe orienté de **N nœuds** (tiré aléatoirement entre 50 et 100) est généré avec `nx.gnm_random_graph`, puis le **PageRank** de chaque nœud est calculé avec `nx.pagerank` (facteur d'amortissement α = 0.85, 100 itérations).

Le script affiche le top 20 dans le terminal et sauvegarde une visualisation (`pagerank_graphe.png`) où la taille des nœuds est proportionnelle à leur score.

```bash
python pagerank_graphe.py
```

---

## Partie 2 — Scraping Paris 8 (`paris8.py`)

Le script crawle `univ-paris8.fr` (jusqu'à 60 pages) avec `requests` + `BeautifulSoup`. Pour chaque page visitée, il extrait tous les liens internes et construit un **graphe orienté** de liens hypertexte.

Le PageRank est ensuite calculé sur ce graphe. Le top 20 des pages les plus populaires est affiché dans le terminal et sauvegardé en image (`pagerank_paris8.png`).

```bash
python pagerank_paris8.py
```

---

## Comment fonctionne le PageRank

Le PageRank attribue à chaque page un score basé sur le nombre et la qualité des pages qui pointent vers elle. À chaque itération :

```
PR(u) = (1 - d) / N  +  d × Σ PR(v) / OutDeg(v)
```

- `d = 0.85` : probabilité de suivre un lien (vs. sauter aléatoirement)
- `N` : nombre total de nœuds
- La somme porte sur tous les nœuds `v` qui pointent vers `u`

Un nœud est populaire s'il reçoit des liens de pages elles-mêmes populaires.
