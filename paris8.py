import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

SEED     = "https://www.univ-paris8.fr"
MAX_PAGES = 60
HEADERS  = {"User-Agent": "Mozilla/5.0 (compatible; student-bot/1.0)"}

# --- Crawl ---
def crawl(seed, max_pages):
    graph = {}          # url -> liste d'urls sortantes
    queue = deque([seed])
    visited = {seed}

    while queue and len(graph) < max_pages:
        url = queue.popleft()
        try:
            resp = requests.get(url, headers=HEADERS, timeout=8)
            if "text/html" not in resp.headers.get("Content-Type", ""):
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            print(f"  ✗ {url[:60]} → {e}")
            continue

        out_links = set()
        for tag in soup.find_all("a", href=True):
            full = urljoin(url, tag["href"]).split("#")[0].split("?")[0]
            parsed = urlparse(full)
            if "univ-paris8" in parsed.netloc and parsed.scheme in ("http", "https"):
                out_links.add(full)
                if full not in visited and len(visited) < max_pages * 2:
                    visited.add(full)
                    queue.append(full)

        graph[url] = list(out_links)
        print(f"  ✓ [{len(graph):2}/{max_pages}] {url[:70]}")

    return graph

print("=== Crawling univ-paris8.fr ===")
graph = crawl(SEED, MAX_PAGES)
print(f"\n{len(graph)} pages crawlées")

# --- Construction du graphe NetworkX ---
G = nx.DiGraph()
for src, targets in graph.items():
    for tgt in targets:
        G.add_edge(src, tgt)

# --- PageRank ---
pr = nx.pagerank(G, alpha=0.85)

# --- Top 20 ---
top20 = sorted(pr, key=pr.get, reverse=True)[:20]

print("\nTop 20 pages par PageRank :")
for i, url in enumerate(top20, 1):
    path = url.replace(SEED, "") or "/"
    print(f"  {i:2}. {pr[url]:.6f}  {path[:70]}")

# --- Visualisation ---
short = {u: (u.replace(SEED, "") or "/")[:35] for u in top20}
subgraph = G.subgraph(top20)
labels = {n: short[n] for n in subgraph.nodes()}
sizes  = [pr[n] * 300000 for n in subgraph.nodes()]
colors = ["#185FA5" if u in top20[:5] else "#1D9E75" for u in subgraph.nodes()]

plt.figure(figsize=(14, 9))
pos = nx.spring_layout(subgraph, seed=1, k=2.5)
nx.draw_networkx(
    subgraph, pos,
    labels=labels,
    node_size=sizes,
    node_color=colors,
    edge_color="#dddddd",
    font_size=7,
    font_color="white",
    arrows=True,
    arrowsize=8,
    width=0.7
)
plt.title(
    f"Top 20 pages — PageRank univ-paris8.fr ({len(graph)} pages crawlées)\n"
    "Bleu = top 5 | Vert = top 6–20 | Taille ∝ score",
    fontsize=12
)
plt.axis("off")
plt.tight_layout()
plt.savefig("pagerank_paris8.png", dpi=150)
plt.show()
print("Graphe sauvegardé : pagerank_paris8.png")