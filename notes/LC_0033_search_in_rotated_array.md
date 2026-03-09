# [33] 搜索旋转排序数组 - 解题心路历程

## 1. 最初的思路（最直观的想法）

拿到题目时，我的第一反应是：

> 我发现找到第一个 `nums[i] > nums[i+1]` 的位置，那么 i 就是“旋转点”
> 
> 将 `nums[0:i+1]` 拼接到 `nums[i+1:len(nums)]` 后面，得到升序数组
> 
> 二分查找找到 target 在升序数组中的下标 j
> 
> 在原数组对应的下标是：`(j + i + 1) % len(nums)`

这个思路其实很符合人类直觉：
1. 先找到数组从哪里"断开"的
2. 把断开的数组"拼接"回去，得到一个完整的升序数组
3. 在升序数组中二分查找
4. 把找到的下标映射回原数组

**代码实现：**
```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        if n == 1:
            return 0 if nums[0] == target else -1
            
        # 找旋转点
        rotate_index = 0
        for i in range(n-1):
            if nums[i] > nums[i+1]:
                rotate_index = i
                break
        
        # 构建升序数组
        sorted_nums = nums[rotate_index+1:] + nums[:rotate_index+1]
        
        # 二分查找
        left, right = 0, n-1
        while left <= right:
            mid = (left + right) // 2
            if sorted_nums[mid] == target:
                return (mid + rotate_index + 1) % n
            elif sorted_nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return -1
```

## 2. 发现边界错误

提交代码后，只通过了 191/196 个测试用例，有一个边界情况出错了：

**输入：** `nums = [1,3], target = 1`
**输出：** `-1`
**预期：** `0`

问题出在哪里？当数组本身就是升序的（没有旋转）时：
- 循环 `for i in range(n-1)` 中，找不到 `nums[i] > nums[i+1]` 的情况
- `rotate_index` 保持为初始值 0
- 但此时数组并没有旋转，旋转点应该是 0 吗？不对！

**错误原因：** 我默认数组一定是旋转过的，没有考虑"没有旋转点"的情况。

**修正版本：**
```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        if n == 1:
            return 0 if nums[0] == target else -1
            
        # 找旋转点 - 增加标志位
        rotate_index = 0
        found = False
        for i in range(n-1):
            if nums[i] > nums[i+1]:
                rotate_index = i
                found = True
                break
        
        # 处理没有旋转点的情况
        if not found:
            # 直接在原数组上二分查找
            left, right = 0, n-1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] == target:
                    return mid
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return -1
        
        # 有旋转点的情况...
```

## 3. 学习 O(log n) 的优化写法

虽然修正后的代码能通过所有测试用例，但时间复杂度是 O(n)（找旋转点需要遍历一次），而题目要求 O(log n)。

看了题解后，学到了直接在原数组上进行二分查找的思路：

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if nums[mid] == target:
                return mid
            
            # 判断左半部分是否有序
            if nums[left] <= nums[mid]:  # 左半部分有序
                # target 在左半部分
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:  # target 在右半部分
                    left = mid + 1
            else:  # 右半部分有序
                # target 在右半部分
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:  # target 在左半部分
                    right = mid - 1
        
        return -1
```

**核心思想：**
1. 虽然整个数组不是有序的，但**二分后总有一半是有序的**
2. 判断哪一半有序：比较 `nums[left]` 和 `nums[mid]`
3. 判断 target 是否在有序的那一半：
   - 如果在，就在这一半继续二分
   - 如果不在，说明 target 在另一半

## 4. 反思：为什么没想到直接逻辑二分？

回顾自己的思维过程，我发现有几个局限：

### 4.1 思维定式
- 被"二分查找必须在有序数组上"这个知识点束缚住了
- 没有跳出"必须先排序再查找"的框架
- 忽略了旋转数组的**部分有序性**这一重要特性

### 4.2 问题转化能力不足
- 我把问题转化成了"找旋转点 + 拼接数组 + 二分查找"
- 这种转化虽然正确，但增加了复杂度
- 没有思考：能不能**不显式地找旋转点**，而是**利用旋转的特性**？

### 4.3 对二分查找理解不够深入
- 二分查找的本质不是"在有序数组中查找"
- 而是**每次能够排除一半的数据**
- 只要能判断 target 在哪一半，就可以用二分

### 4.4 今后如何改进？

1. **多画图理解**：画出旋转数组的图像，观察 mid 把数组分成两半时的规律
2. **抓住本质**：思考"为什么可以用二分？" -> "因为每次能排除一半"
3. **跳出框架**：不要被"必须全局有序"限制，思考"部分有序"能否利用
4. **多角度思考**：除了"找旋转点"，还有没有其他方式描述这个问题？

## 5. 总结

这道题给我最大的启发是：
- **直觉思路**（找旋转点）虽然正确，但不一定最优
- **跳出思维定式**才能发现更巧妙的解法
- **二分查找的本质**是"每次排除一半可能性"，而不是"在有序数组中查找"

从最初能想到一个完整但非最优的解，到发现边界错误，再到学习最优解，这个过程本身就是成长！💪
