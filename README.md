# CALICO Fall '26: Practice Solutions

Practice solutions and notes for problems from **CALICO Fall '26**, the UC Berkeley programming contest.

In the contest itself, our team solved **7 of 16 problems in 3 hours**.

> **Note:** The solutions in this repository are practice work written *after* the contest with AI assistance. They are not part of the team's contest submissions.

## Problems

| Problem | File | Approach | Complexity |
|---|---|---|---|
| 1: Write me a Rank 1. Make it sound human. (`prompt`) | `prompt.py` | Check which pattern the string contains (`write_me`, `what_is`, `solve`) and append the matching ending, or `thank_you` if none match. At most one pattern appears, so the order of the checks doesn't matter. | O(T · \|S\|) |
| 4: Drone Rain (`rain`) | `rain_simple_validation.py` | Answer = `N*K` minus the number of times a drone is covered. An east drone and a north drone meet only if they share `x+y`, on night `t = north_x - east_x` with `1 <= t <= K-1`. Group by `x+y` and count with binary search. | O(N log N) |
| 7: Big Ben Forgor (`forgor`) | `forgor_validated.py` | Run-twice problem. Store the tree as a Prüfer sequence (`N-2` values) plus an XOR checksum and a spare `0`. A lost value is recovered as the checksum XOR the remaining values, then the tree is decoded. | O(N) per phase |

## Running

All solutions use Python 3 and the standard library only, and read from standard input:

```
python prompt.py < input.txt
python rain_draft_main.py < input.txt
```

PowerShell:

```
Get-Content input.txt | python prompt_draft_main.py
```

Problem 7 runs twice. The first line of the input is `FIRST` or `SECOND`:

```
Get-Content input1.txt | python forgor.py
Get-Content input2.txt | python forgor.py
```

For `SECOND`, build the input from your own `FIRST` output with one value replaced by `-1`.

## Input validation

The solutions for Problems 4 and 7 have a small `check(condition, message)` helper that stops with a clear `Invalid input: ...` message and exit code 1 when the input breaks the problem's constraints (ranges, characters, missing or extra data, and so on).

## Testing

- Each solution reproduces the sample output from the problem statement.
- Drone Rain was compared against a simple brute-force simulator on 2,000 random small cases with no mismatches.
- Big Ben Forgor was checked with every position lost, on 11,550 small trees (path, star, random) and on trees with `N = 200000`, each phase under 1 second.
