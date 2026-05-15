# 2048 Intelligent Agent

Expectiminimax agent for 2048, written for COMS 4701 at Columbia.

## How it works

Expectiminimax with Alpha-Beta pruning. The computer's tile placements
are modeled as chance nodes weighted 90/10 for 2 vs 4.

Search depth adjusts dynamically — goes deeper when the board is crowded
since there are fewer branches to explore and survival matters more.

## Evaluation

Four heuristics:

| | weight | why |
|---|---|---|
| empty tiles | 500 | once the board fills up it's basically over |
| monotonicity | 200 | large tiles trapped in the middle are hard to merge |
| max tile | 10 | mild incentive to keep growing |
| smoothness | 5 | neighboring tiles that are close in value are easier to merge |

Monotonicity uses `max(increasing, decreasing)` per row/column so partially
ordered sequences still get credit.

## Result

Consistently reaches 2048 in local testing.

## Run

```bash
python3 GameManager.py
```
