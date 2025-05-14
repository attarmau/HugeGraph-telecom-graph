import networkx as nx
import matplotlib.pyplot as plt

telco_cluster = {
    "+6591234567": "Singtel",
    "+6598765432": "Starhub",
    "+6587654321": "Singtel",
    "+6588123456": "M1",
    "+6599111122": "Singtel",
    "+6588777666": "Starhub",
    "+6581234567": "M1",
    "+6588222333": "M1",
    "+6588111222": "Starhub",
    "+6588333444": "Starhub",
    "+6588444555": "M1",
    "+6588555666": "Starhub",
    "+6588666777": "M1",
    "+6588777888": "Starhub",
    "+6588888999": "Singtel",
    "+6588999000": "Singtel",
    "+6588000111": "M1",
    "+6588000333": "Starhub",
    "+6588000555": "M1"
}

telco_colors = {
    "Singtel": "#1f77b4",
    "Starhub": "#2ca02c",
    "M1": "#ff7f0e"
}

G = nx.DiGraph()

for node, telco in telco_cluster.items():
    G.add_node(node, telco=telco)

edges = [
    ("+6591234567", "+6598765432", "2025-05-14 08:00", 120),
    ("+6598765432", "+6591234567", "2025-05-14 09:00", 80),
    ("+6591234567", "+6587654321", "2025-05-14 10:00", 95),
    ("+6591234567", "+6588123456", "2025-05-14 10:05", 70),
    ("+6588123456", "+6598765432", "2025-05-14 11:00", 100),
    ("+6598765432", "+6588333444", "2025-05-14 11:30", 60),
    ("+6587654321", "+6599111122", "2025-05-14 12:00", 110),
    ("+6599111122", "+6588777666", "2025-05-14 13:00", 55),
    ("+6588777666", "+6591234567", "2025-05-14 14:00", 95),
    ("+6581234567", "+6588222333", "2025-05-14 15:00", 100),
    ("+6588222333", "+6588111222", "2025-05-14 15:30", 85),
    ("+6588333444", "+6588444555", "2025-05-14 16:00", 70),
    ("+6588555666", "+6588666777", "2025-05-14 17:00", 65),
    ("+6588777888", "+6588888999", "2025-05-14 18:00", 90),
    ("+6588999000", "+6588000111", "2025-05-14 18:30", 40),
    ("+6588111222", "+6588444555", "2025-05-14 19:00", 50),
    ("+6588000555", "+6588000333", "2025-05-14 20:00", 100),
    ("+6588000555", "+6588555666", "2025-05-14 20:30", 85),
    ("+6588777888", "+6588000111", "2025-05-14 21:00", 95),
]

for src, tgt, time, duration in edges:
    G.add_edge(src, tgt, time=time, duration=duration)

clustering_coeffs = nx.clustering(G.to_undirected())
pos = nx.spring_layout(G, seed=42)
node_colors = [clustering_coeffs.get(n, 0.0) for n in G.nodes()]
vmin, vmax = min(node_colors), max(node_colors)
fig, ax = plt.subplots(figsize=(14, 10))

for node in G.nodes():
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[node],
        node_color=[clustering_coeffs[node]],
        cmap=plt.cm.viridis,
        vmin=vmin,
        vmax=vmax,
        node_size=800,
        edgecolors=telco_colors[G.nodes[node]['telco']],
        linewidths=2,
        ax=ax
    )

nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
edge_labels = {(u, v): f"{d['duration']}s" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=ax)
sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, label="Clustering Coefficient")


for telco, color in telco_colors.items():
    ax.scatter([], [], c='white', edgecolors=color, linewidths=2, s=100, label=telco)
ax.legend(title="Telco Cluster (Border Color)")

ax.set_title("Call Graph: Clustering Coefficient + Telco Cluster")
plt.axis('off')
plt.tight_layout()
plt.savefig("clustered_graph_with_coefficient.png", dpi=300)
plt.show()
