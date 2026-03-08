# N 皇后问题解题笔记

## 问题描述

**LeetCode 51: N-Queens**

按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。

N 皇后问题研究的是如何将 N 个皇后放置在 N×N 的棋盘上，并且使皇后彼此之间不能相互攻击。

给你一个整数 `n`，返回所有不同的 N 皇后问题的解决方案。

每一种解法包含一个不同的 N 皇后问题的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。

**示例 1：**
- 输入：`n = 4`
- 输出：`[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]`
- 解释：如上图所示，4 皇后问题存在两个不同的解法。

**示例 2：**
- 输入：`n = 1`
- 输出：`[["Q"]]`

**约束：**
- `1 <= n <= 9`

## 解题思路

### 核心思路：回溯法（DFS + 剪枝）
- **按行放置**：我们按行从 0 到 n-1 依次放置皇后，确保每行只有一个皇后。
- **状态表示**：
  - `path[row] = col`：第 row 行皇后��在第 col 列。
  - 使用三个数组记录占用：
    - `cols[col]`：第 col 列是否被占用。
    - `diag1[row - col + n - 1]`：主对角线（\ 方向）是否被占用。
    - `diag2[row + col]`：副对角线（/ 方向）是否被占用。
- **冲突检查**：O(1) 时间，通过上述三个数组判断是否冲突。
- **回溯过程**：
  - 递归函数 `dfs(row)`：尝试在第 row 行放置皇后。
  - 遍历所有列 `col`，如果不冲突，则放置皇后，递归到下一行，回溯时撤销选择。
  - 当 `row == n` 时，收集当前方案。

### 时间复杂度
- 最坏情况下：O(N!)，因为需要探索所有可能的放置方式，但通过剪枝大大减少。
- 对于 N=9，实际运行时间可接受。

### 空间复杂度
- O(N)：path、cols、diag1、diag2 等数组。
- 递归栈深度 O(N)。

## 代码实现 (Python)

```python
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        res: List[List[str]] = []
        path = [-1] * n  # path[row] = col，表示第 row 行皇后放在 col 列

        cols = [False] * n  # cols[col] = True 表示第 col 列已被占用
        diag1 = [False] * (2 * n - 1)  # 主对角线（\）：row - col + (n-1) 索引
        diag2 = [False] * (2 * n - 1)  # 副对角线（/）：row + col 索引

        def build_board(path: list[int], n: int) -> List[str]:
            board = []
            for r in range(n):
                row = ['.'] * n
                row[path[r]] = 'Q'
                board.append(''.join(row))
            return board

        def dfs(row: int) -> None:
            if row == n:
                res.append(build_board(path, n))
                return

            for col in range(n):
                idx1 = row - col + n - 1
                idx2 = row + col

                if cols[col] or diag1[idx1] or diag2[idx2]:
                    continue  # 冲突，跳过

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
```

### 代码解释
- `build_board`：根据 `path` 构造棋盘字符串列表。
- `dfs`：核心回溯函数。
- 对角线索引计算：
  - `diag1`：`row - col` 范围为 `-(n-1)` 到 `+(n-1)`，平移 `+ (n-1)` 使其为 0 到 2n-2。
  - `diag2`：`row + col` 范围为 0 到 2n-2，无需平移。

## 测试案例
- `n=1`：`[["Q"]]`
- `n=4`：2 个解，如示例所示。
- `n=8`：92 个解（经典结果）。

## 常见坑点 & 优化
- **作用域**：`build_board` 使用闭包访问外部变量，如果不习惯，可改为传参。
- **下标计算**：确保 `diag1` 和 `diag2` 索引正确，避免越界。
- **剪枝**：本实现已 O(1) 剪枝；如果用绝对值检查对角线，复杂度会更高，但对小 N 无影响。
- **扩展**：类似问题如 N 皇后计数（只需返回数量，不收集方案）可在此基础上修改。


