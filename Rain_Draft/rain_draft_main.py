import sys
from bisect import bisect_right
from unittest import case

def check(condition, message):
    """Stop with a proper message if something in the input is wrong."""
    if not condition:
        sys.exit(f"Invalid input: {message}")


def main():
    tokens = sys.stdin.buffer.read().split()
    check(tokens, "input is empty")
    pointer = 0

    test_count = int(tokens[pointer])
    pointer += 1
    check(1 <= test_count <= 100, f"T = {test_count} must be between 1 and 100")
    answers = []

    for _ in range(test_count):
        drone_count = int(tokens[pointer])
        nights = int(tokens[pointer + 1])
        pointer += 2

        check(1 <= drone_count <= 10**5, f"test {case}: N = {drone_count} must be between 1 and 10^5")
        check(1 <= nights <= 10**9, f"test {case}: K = {nights} must be between 1 and 10^9")
        check(pointer + 4 * drone_count <= len(tokens), f"test {case}: not enough drone lines")

        # Drones can only meet if they share the same x + y (same diagonal),
        # so group the x values of east / north drones by that sum.
        east_x_by_diagonal = {}
        north_x_by_diagonal = {}
        start_positions = set()
        for _ in range(drone_count):
            x = int(tokens[pointer])
            y = int(tokens[pointer + 1])
            direction = tokens[pointer + 3]
            pointer += 4

            check(direction in (b"E", b"N"), f"test {case}: direction must be E or N")
            check((x, y) not in start_positions, f"test {case}: two drones start at ({x}, {y})")
            
            start_positions.add((x, y))

            diagonal = x + y
            if direction == b"E":
                east_x_by_diagonal.setdefault(diagonal, []).append(x)
            else:
                north_x_by_diagonal.setdefault(diagonal, []).append(x)

        # one unit of rain (the lower drone is covered once).
        # They meet on night t = north_x - east_x, and we need 1 <= t <= nights - 1.
        covered_units = 0
        for diagonal, east_xs in east_x_by_diagonal.items():
            north_xs = north_x_by_diagonal.get(diagonal)
            if not north_xs:
                continue
            north_xs.sort()
            for east_x in east_xs:
                covered_units += (bisect_right(north_xs, east_x + nights - 1)
                - bisect_right(north_xs, east_x))

        answers.append(drone_count * nights - covered_units)

    print("\n".join(map(str, answers)))


if __name__ == "__main__":
    main()