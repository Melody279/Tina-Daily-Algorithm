from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        is_pal = [[False] * n for _ in range(n)]

        # Precompute palindrome table: is_pal[i][j] indicates s[i..j] is palindrome.
        for length in range(1, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                    is_pal[i][j] = True

        res: List[List[str]] = []
        path: List[str] = []

        def dfs(start: int) -> None:
            if start == n:
                res.append(path.copy())
                return
            for end in range(start, n):
                if is_pal[start][end]:
                    path.append(s[start : end + 1])
                    dfs(end + 1)
                    path.pop()

        dfs(0)
        return res
