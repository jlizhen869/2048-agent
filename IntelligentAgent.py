import time
from BaseAI import BaseAI

# Weights for the evaluation function.
# Empty space dominates — once the board fills up the game is basically over.
# Monotonicity matters a lot too: large tiles trapped in the middle are hard to merge.
# Max tile and smoothness are secondary.
W_EMPTY  = 500
W_MONO   = 200
W_MAX    = 10
W_SMOOTH = 5


class IntelligentAgent(BaseAI):
    def __init__(self):
        self.time_limit = 0.18  # leave a small buffer under the 0.2s limit

    def getMove(self, grid):
        self.start_time = time.process_time()

        # search deeper when the board is crowded — fewer moves available
        # so the tree is smaller and we can afford more depth
        empty = len(grid.getAvailableCells())
        if empty > 6:
            depth = 3
        elif empty > 2:
            depth = 4
        else:
            depth = 5

        move, _ = self.maximize(grid, depth, -float('inf'), float('inf'))
        return move

    def maximize(self, grid, depth, alpha, beta):
        if (time.process_time() - self.start_time > self.time_limit
                or depth == 0 or not grid.canMove()):
            return None, self.evaluate(grid)

        max_child, max_val = None, -float('inf')
        for move, child_grid in grid.getAvailableMoves():
            _, val = self.chance(child_grid, depth - 1, alpha, beta)
            if val > max_val:
                max_val, max_child = val, move
            if max_val >= beta:
                break
            alpha = max(alpha, max_val)

        return max_child, max_val

    def chance(self, grid, depth, alpha, beta):
        # computer places a 2 (90%) or 4 (10%) on a random empty cell
        if (time.process_time() - self.start_time > self.time_limit
                or depth == 0):
            return None, self.evaluate(grid)

        cells = grid.getAvailableCells()
        if not cells:
            return None, self.evaluate(grid)

        expected_val = 0
        for cell in cells:
            grid.setCellValue(cell, 2)
            _, val2 = self.maximize(grid, depth - 1, alpha, beta)
            grid.setCellValue(cell, 0)

            grid.setCellValue(cell, 4)
            _, val4 = self.maximize(grid, depth - 1, alpha, beta)
            grid.setCellValue(cell, 0)

            expected_val += (val2 * 0.9 + val4 * 0.1) / len(cells)

        return None, expected_val

    def evaluate(self, grid):
        if not grid.canMove():
            return -1e9

        empty        = len(grid.getAvailableCells())
        monotonicity = self.calculate_monotonicity(grid)
        max_tile     = grid.getMaxTile()
        smoothness   = self.calculate_smoothness(grid)

        return (W_EMPTY  * empty
              + W_MONO   * monotonicity
              + W_MAX    * max_tile
              + W_SMOOTH * smoothness)

    def calculate_monotonicity(self, grid):
        # take the better of increasing or decreasing order for each row/col
        # max(inc, dec) avoids penalizing sequences that are partially ordered
        score = 0
        for i in range(4):
            row = [grid.map[i][j] for j in range(4)]
            col = [grid.map[j][i] for j in range(4)]
            for seq in [row, col]:
                inc = sum(seq[k] <= seq[k+1] for k in range(3))
                dec = sum(seq[k] >= seq[k+1] for k in range(3))
                score += max(inc, dec)
        return score

    def calculate_smoothness(self, grid):
        # penalize large differences between adjacent tiles
        smooth = 0
        for i in range(4):
            for j in range(3):
                smooth -= abs(grid.map[i][j] - grid.map[i][j+1])
                smooth -= abs(grid.map[j][i] - grid.map[j+1][i])
        return smooth
