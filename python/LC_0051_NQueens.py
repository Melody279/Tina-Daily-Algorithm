from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        res: List[List[str]] = []
        path = [-1] * n

        cols = [False] * n
        diag1 = [False] * (2 * n - 1)  # \ 方向：row - col + (n-1)
        diag2 = [False] * (2 * n - 1)  # / 方向：row + col

        def build_board() -> List[str]:
            board = []
            for r in range(n):
                row = ['.'] * n
                row[path[r]] = 'Q'
                board.append(''.join(row))
            return board

        def dfs(row: int) -> None:
            if row == n:
                res.append(build_board())
                return

            for col in range(n):
                idx1 = row - col + n - 1
                idx2 = row + col

                if cols[col] or diag1[idx1] or diag2[idx2]:
                    continue

                # 做选择
                path[row] = col
                cols[col] = True
                diag1[idx1] = True
                diag2[idx2] = True

                dfs(row + 1)

                # 撤销选择
                cols[col] = False
                diag1[idx1] = False
                diag2[idx2] = False
                path[row] = -1

        dfs(0)
        return res
