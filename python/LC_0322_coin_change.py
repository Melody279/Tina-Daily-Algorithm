from math import inf
from typing import List

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # dp[j] = 凑成金额 j 的最少硬币数；无解为 inf
        dp = [0] + [inf] * amount

        for coin in coins:
            for j in range(coin, amount + 1):  # 完全背包：j 升序
                dp[j] = min(dp[j], dp[j - coin] + 1)

        return -1 if dp[amount] == inf else dp[amount]
