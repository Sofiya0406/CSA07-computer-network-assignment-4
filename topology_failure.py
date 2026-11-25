"""Compare topologies for n offices: links, ports and single-link failures."""
from itertools import combinations
from collections import deque


def links(kind, n):
    nodes = list(range(n))
    if kind == "bus":
        return [(i, i + 1) for i in range(n - 1)]
    if kind == "ring":
        return [(i, (i + 1) % n) for i in range(n)]
    if kind == "star":
        return [("hub", i) for i in nodes]
    if kind == "mesh":
        return list(combinations(nodes, 2))
    raise ValueError(kind)


def connected_after_failure(edges, n, broken):
    """Return True when all n numbered offices remain connected to office 0."""
    remaining = [edge for edge in edges if edge != broken]
    graph = {node: set() for node in range(n)}
    for a, b in remaining:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)

    visited = {0}
    queue = deque([0])
    while queue:
        node = queue.popleft()
        for neighbour in graph.get(node, ()):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return all(node in visited for node in range(n))


def max_ports(edges):
    degree = {}
    for a, b in edges:
        degree[a] = degree.get(a, 0) + 1
        degree[b] = degree.get(b, 0) + 1
    return max(degree.values())


if __name__ == "__main__":
    n = 6
    for kind in ("bus", "ring", "star", "mesh"):
        edge_list = links(kind, n)
        survived = sum(
            connected_after_failure(edge_list, n, broken)
            for broken in edge_list
        )
        print(
            f"{kind:<5} links {len(edge_list):2d} "
            f"max ports on one device {max_ports(edge_list)} "
            f"single-link failures survived {survived}/{len(edge_list)}"
        )

    n = 20
    print(f"\nFor n=20: star links={len(links('star', n))}, "
          f"full mesh links={len(links('mesh', n))}")
