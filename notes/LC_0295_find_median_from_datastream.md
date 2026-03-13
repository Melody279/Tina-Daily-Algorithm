
## 1. 算法思路

### 核心思想
使用两个堆来维护数据流：
- **左堆（left）**：最大堆，存储较小的一半数字
- **右堆（right）**：最小堆，存储较大的一半数字

### 平衡策略
始终保持两个堆的大小平衡：
- 左堆的大小 >= 右堆的大小
- 左堆最多比右堆多一个元素

### 中位数计算
- 如果总数为奇数：中位数 = 左堆的堆顶（最大值）
- 如果总数为偶数：中位数 = (左堆最大值 + 右堆最小值) / 2

## 2. 语法细节详解

### Python中的堆
Python的`heapq`模块默认只提供**最小堆**。要模拟最大堆，需要存入负值。

```python
import heapq

# 最小堆（默认）
min_heap = []
heapq.heappush(min_heap, 3)
heapq.heappush(min_heap, 1)
heapq.heappush(min_heap, 2)
print(min_heap[0])  # 输出: 1（最小值）

# 最大堆（通过存入负值实现）
max_heap = []
heapq.heappush(max_heap, -3)  # 存入-3
heapq.heappush(max_heap, -1)  # 存入-1
heapq.heappush(max_heap, -2)  # 存入-2
print(-max_heap[0])  # 输出: 3（最大值）
```

### 完整实现版本（可直接运行）

```python
import heapq

class MedianFinder:
    def __init__(self):
        # 左堆：最大堆（存储较小的一半）
        self.left = []  # 实际存储负值来实现最大堆
        # 右堆：最小堆（存储较大的一半）
        self.right = []  # 直接存储正值

    def addNum(self, num: int) -> None:
        # 如果两个堆大小相等，加入左堆
        if len(self.left) == len(self.right):
            # 先将数字加入右堆（最小堆），然后取出最小值加入左堆（最大堆）
            # 这里将值取负，实现最大堆效果
            heapq.heappush(self.left, -heapq.heappushpop(self.right, num))
        else:
            # 先将数字加入左堆（最大堆），然后取出最大值（取负后）加入右堆（最小堆）
            heapq.heappush(self.right, -heapq.heappushpop(self.left, -num))

    def findMedian(self) -> float:
        # 如果左堆更大（奇数个元素）
        if len(self.left) > len(self.right):
            return -self.left[0]  # 左堆堆顶是最大值（但存储的是负值）
        # 偶数个元素，取两个堆顶的平均值
        return (-self.left[0] + self.right[0]) / 2
```

### 原始版本对比

为了方便理解，我写一个不使用复合函数的版本：

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.left = []  # 最大堆
        self.right = []  # 最小堆

    def addNum(self, num: int) -> None:
        # 原始版本（更易理解）
        if len(self.left) == len(self.right):
            # 先放入右堆（最小堆）
            heapq.heappush(self.right, num)
            # 取出右堆的最小值
            min_from_right = heapq.heappop(self.right)
            # 放入左堆（取负实现最大堆）
            heapq.heappush(self.left, -min_from_right)
        else:
            # 先放入左堆（取负）
            heapq.heappush(self.left, -num)
            # 取出左堆的最大值（取负后）
            max_from_left = -heapq.heappop(self.left)
            # 放入右堆
            heapq.heappush(self.right, max_from_left)

    def findMedian(self) -> float:
        if len(self.left) > len(self.right):
            return -self.left[0]
        return (-self.left[0] + self.right[0]) / 2
```

### 关键函数解释

1. **`heappush(heap, item)`**：将元素压入堆
2. **`heappop(heap)`**：弹出并返回堆顶元素
3. **`heappushpop(heap, item)`**：先压入元素，然后弹出堆顶（比分别调用更高效）
4. **`heap[0]`**：查看堆顶元素（不弹出）

### 使用示例

```python
# 测试代码
mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())  # 输出: 1.5
mf.addNum(3)
print(mf.findMedian())  # 输出: 2
```

## 3. 复杂度分析

- **时间复杂度**：O(log n) 每次插入
- **空间复杂度**：O(n) 存储所有元素


