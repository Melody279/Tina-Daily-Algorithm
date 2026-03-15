# LeetCode 322. Coin Change — Notes

## 题意总结

- 给定硬币面额数组 `coins`（每种硬币数量无限）和总金额 `amount`。
- 要求：**用最少的硬币数**凑出 `amount`。
- 若无法凑出，返回 `-1`。

典型的「**完全背包问题（求最小个数）**」。

---

## 一维 DP 状态与转移

### 状态定义

```python
dp[j] = 凑出金额 j 所需的最少硬币数（不能凑出则视为 +∞）
```

目标：`dp[amount]`。

### 初始化

```python
dp = [0] + [inf] * amount
# dp[0] = 0：凑出 0 元需要 0 个硬币
# 其他初始化为 inf：一开始视为“凑不出”
```

### 状态转移（完全背包）

遍历每种硬币 `coin`：

```python
for coin in coins:
    for j in range(coin, amount + 1):
        dp[j] = min(dp[j], dp[j - coin] + 1)
```

含义：

- 当前要更新的是「凑出金额 j 的最少硬币数」。
- 若使用一枚当前硬币 `coin`，则剩余金额是 `j - coin`，  
  对应状态为 `dp[j - coin]`，再加上这 1 枚硬币：`dp[j - coin] + 1`。
- 与不用当前硬币的情况（旧值 `dp[j]`）取最小值。

---

## 为什么内层循环是 `for j in range(coin, amount + 1)`（j 从 coin 开始）？

这是本题/完全背包写法的**关键细节**：

### 1. 语义上：小于 coin 的金额不可能用到当前硬币

对于金额 `j < coin`：

- 连一枚当前硬币都放不进去（`j - coin < 0`），
- 自然不可能通过“用当前硬币一次”这种方式来更新。

换句话说：

- 对于 `j < coin`，这一轮（当前 `coin`）**不会改变 `dp[j]`**，
- 它们仍然保持之前的值，表示“只用前面处理过的硬币能达到的最优解”。

用代码体现就是：**直接从 `j = coin` 开始循环**，跳过所有 `j < coin`。

### 2. 从实现上：避免非法访问和无意义计算

转移公式是：

```python
dp[j] = min(dp[j], dp[j - coin] + 1)
```

若从 `j = 0` 开始：

- 对于 `j < coin`，表达式 `dp[j - coin]` 会访问负下标，语义上是错误的（在 Python 里会从尾部倒数，完全不是我们要的）。
- 即便你加判断 `if j >= coin`，`j < coin` 的部分其实也只是“什么都不做”，多了一层分支判断，徒增复杂度。

因此，直接写成：

```python
for j in range(coin, amount + 1):
    dp[j] = min(dp[j], dp[j - coin] + 1)
```

更安全、更清晰：

- 保证 `j - coin >= 0`，不会越界；
- 明确表达了「只有金额至少是 `coin` 时，才有资格使用当前硬币」。

### 3. 与「完全背包」特性匹配（j 升序）

在完全背包中，**每种硬币可以用无限次**，转移关系用的是「当前行的 dp[j - coin]」：

- `dp[j]` 依赖的是**本次已更新后的** `dp[j - coin]`（同一层 i）；
- 因此 `j` 需要**从小到大**遍历，保证在更新 `dp[j]` 时，`dp[j - coin]` 已经是「考虑了当前硬币后的结果」。

从 `j = coin` 到 `amount` 的升序遍历，既满足「不越界」又满足「完全背包的正确转移」。

---

## 最终答案处理

计算结束后：

```python
ans = dp[amount]
return -1 if ans == inf else ans
```

- 若 `dp[amount]` 仍是 `inf`，说明无论怎么选硬币都凑不出 `amount`，返回 `-1`。
- 否则返回实际最小硬币数。

---

## 完整一维 DP 实现（放仓库用）

```python
from math import inf
from typing import List

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [0] + [inf] * amount  # dp[j]：凑出 j 所需最少硬币数

        for coin in coins:
            for j in range(coin, amount + 1):  # j 从 coin 开始，避免 j-coin < 0
                dp[j] = min(dp[j], dp[j - coin] + 1)

        return -1 if dp[amount] == inf else dp[amount]
```

> 记忆口诀：  
> - `dp[j] = min(dp[j], dp[j - coin] + 1)`：当前硬币要么不用，要么多用一枚。  
> - `j` 从 `coin` 开始：金额至少能放下一枚当前硬币时，才考虑“用它”这一种选择。
