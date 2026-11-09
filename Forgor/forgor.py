import sys


def check(condition, message):
    """Stop with a clear message if something is wrong in the input."""
    if not condition:
        sys.exit(f"Invalid input: {message}")


def compress_tree_nodes(n, edges):
    """Tree -> list of n numbers: Pruefer sequence, its XOR checksum, one spare 0."""
    neighbour_edges = [[] for _ in range(n + 1)]
    power = [0] * (n + 1)
    for u, v in edges:
        neighbour_edges[u].append(v)
        neighbour_edges[v].append(u)
        power[u] += 1
        power[v] += 1

    # Root the tree at vertex n so every other vertex has a parent.
    parent = [0] * (n + 1)
    stack = [n]
    seen = [False] * (n + 1)
    seen[n] = True
    while stack:
        node = stack.pop()
        for neighbour in neighbour_edges[node]:
            if not seen[neighbour]:
                seen[neighbour] = True
                parent[neighbour] = node
                stack.append(neighbour)
    check(all(seen[1:]), "the edges do not form one connected tree")

    # Linear-time Pruefer sequence: repeatedly remove the smallest leaf.
    sequence = []
    pointer = 1
    while power[pointer] != 1:
        pointer += 1
    leaf = pointer
    for _ in range(n - 2):
        neighbour = parent[leaf]
        sequence.append(neighbour)
        power[neighbour] -= 1
        if power[neighbour] == 1 and neighbour < pointer:
            leaf = neighbour
        else:
            pointer += 1
            while power[pointer] != 1:
                pointer += 1
            leaf = pointer

    checksum = 0
    for value in sequence:
        checksum ^= value
    return sequence + [checksum, 0]


def rebuild_tree_nodes(n, values):
    """List with one value replaced by -1 -> list of the original edges."""
    sequence = values[:n - 2]
    checksum = values[n - 2]

    # If the lost value is inside the Pruefer part, rebuild it from the checksum.
    for index, value in enumerate(sequence):
        if value == -1:
            recovered = checksum
            for other_index, other in enumerate(sequence):
                if other_index != index:
                    recovered ^= other
            sequence[index] = recovered
            break
    # (If the lost value was the checksum or the spare slot, nothing to repair.)

    check(all(1 <= value <= n for value in sequence),
            "the list is corrupted (a Pruefer value is not between 1 and N)")

    power = [1] * (n + 1)
    for value in sequence:
        power[value] += 1

    edges = []
    pointer = 1
    while power[pointer] != 1:
        pointer += 1
    leaf = pointer
    for value in sequence:
        edges.append((leaf, value))
        power[value] -= 1
        if power[value] == 1 and value < pointer:
            leaf = value
        else:
            pointer += 1
            while power[pointer] != 1:
                pointer += 1
            leaf = pointer
    edges.append((leaf, n))
    return edges


def main():
    tokens = sys.stdin.buffer.read().split()
    check(len(tokens) >= 2, "input is too short")
    phase = tokens[0]
    check(phase in (b"FIRST", b"SECOND"), "first word must be FIRST or SECOND")
    n = int(tokens[1])
    check(2 <= n <= 2 * 10**5, f"N = {n} must be between 2 and 2*10^5")

    if phase == b"FIRST":
        check(len(tokens) >= 2 + 2 * (n - 1), f"expected {n - 1} edges")
        tree_edges = []
        for i in range(n - 1):
            u = int(tokens[2 + 2 * i])
            v = int(tokens[3 + 2 * i])
            check(1 <= u <= n and 1 <= v <= n, f"edge {i + 1}: vertices must be between 1 and N")
            tree_edges.append((u, v))
        print(" ".join(map(str, compress_tree_nodes(n, tree_edges))))
    else:
        check(len(tokens) >= 2 + n, f"expected {n} numbers in the list")
        values = [int(token) for token in tokens[2:2 + n]]
        check(values.count(-1) == 1, "the list must contain exactly one -1")
        check(all(value == -1 or 0 <= value <= 10**6 for value in values),
                "list values must be between 0 and 10^6 (or -1)")
        tree_edges = rebuild_tree_nodes(n, values)
        print("\n".join(f"{u} {v}" for u, v in tree_edges))


if __name__ == "__main__":
    main()