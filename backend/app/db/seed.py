import logging
from typing import List, Dict, Any

logger = logging.getLogger("codementor.seed")

SEED_PROBLEMS: List[Dict[str, Any]] = [
    {
        "_id": "prob_recursion_factorial",
        "title": "Factorial using Recursion",
        "description": "Write a recursive function `factorial(n)` that returns the factorial of a non-negative integer `n`. Remember: `factorial(0) = 1` and `factorial(n) = n * factorial(n - 1)`.",
        "topic": "Recursion",
        "subconcept": "base_case",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 10,
        "tags": ["recursion", "math", "base_case"],
        "examples": [
            {"input_str": "factorial(5)", "output_str": "120", "explanation": "5 * 4 * 3 * 2 * 1 = 120"},
            {"input_str": "factorial(0)", "output_str": "1", "explanation": "0! is defined as 1"}
        ],
        "constraints": ["0 <= n <= 15"],
        "starter_code": "def factorial(n: int) -> int:\n    # Write your recursive code here\n    pass\n",
        "test_cases": [
            {"input_args": [0], "expected_output": 1, "is_hidden": False},
            {"input_args": [1], "expected_output": 1, "is_hidden": False},
            {"input_args": [5], "expected_output": 120, "is_hidden": False},
            {"input_args": [7], "expected_output": 5040, "is_hidden": True}
        ],
        "solution": "def factorial(n: int) -> int:\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
        "explanation": "A recursive function must have two parts: a base case that stops recursion (n <= 1 returns 1) and a recursive step reducing the problem (n * factorial(n - 1)). Without the base case, the function causes Infinite Recursion / RecursionError.",
        "better_approach": "For large n, an iterative approach or tail recursion prevents maximum recursion depth stack overflow.",
        "time_complexity": "O(n)",
        "space_complexity": "O(n) call stack"
    },
    {
        "_id": "prob_recursion_fibonacci",
        "title": "N-th Fibonacci Number",
        "description": "Write a function `fibonacci(n)` that returns the n-th Fibonacci number where `fibonacci(0) = 0`, `fibonacci(1) = 1`, and `fibonacci(n) = fibonacci(n-1) + fibonacci(n-2)`.",
        "topic": "Recursion",
        "subconcept": "multiple_recursive_calls",
        "difficulty": "intermediate",
        "language": "python",
        "type": "coding",
        "estimated_time": 15,
        "tags": ["recursion", "dynamic_programming", "memoization"],
        "examples": [
            {"input_str": "fibonacci(4)", "output_str": "3", "explanation": "0, 1, 1, 2, 3"},
            {"input_str": "fibonacci(6)", "output_str": "8", "explanation": "0, 1, 1, 2, 3, 5, 8"}
        ],
        "constraints": ["0 <= n <= 20"],
        "starter_code": "def fibonacci(n: int) -> int:\n    # Implement Fibonacci\n    pass\n",
        "test_cases": [
            {"input_args": [0], "expected_output": 0, "is_hidden": False},
            {"input_args": [1], "expected_output": 1, "is_hidden": False},
            {"input_args": [4], "expected_output": 3, "is_hidden": False},
            {"input_args": [8], "expected_output": 21, "is_hidden": True}
        ],
        "solution": "def fibonacci(n: int) -> int:\n    if n <= 0:\n        return 0\n    if n == 1:\n        return 1\n    return fibonacci(n - 1) + fibonacci(n - 2)",
        "explanation": "Handles two base cases (n=0 and n=1) and recurses on both prior terms.",
        "better_approach": "Naive recursion takes O(2^n) time. Using memoization or dynamic programming reduces complexity to O(n) time and O(1) extra space.",
        "time_complexity": "O(2^n) naive or O(n) memoized",
        "space_complexity": "O(n) call stack"
    },
    {
        "_id": "prob_arrays_twosum",
        "title": "Two Sum",
        "description": "Given a list of integers `nums` and an integer `target`, return the indices `[i, j]` of the two numbers such that they add up to `target`. Each input has exactly one solution.",
        "topic": "Arrays",
        "subconcept": "hash_lookup",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 15,
        "tags": ["arrays", "hashmap", "two_pointer"],
        "examples": [
            {"input_str": "two_sum([2, 7, 11, 15], 9)", "output_str": "[0, 1]", "explanation": "nums[0] + nums[1] == 9"}
        ],
        "constraints": ["2 <= len(nums) <= 10^4", "-10^9 <= nums[i] <= 10^9"],
        "starter_code": "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Return indices [i, j]\n    pass\n",
        "test_cases": [
            {"input_args": [[2, 7, 11, 15], 9], "expected_output": [0, 1], "is_hidden": False},
            {"input_args": [[3, 2, 4], 6], "expected_output": [1, 2], "is_hidden": False},
            {"input_args": [[3, 3], 6], "expected_output": [0, 1], "is_hidden": True}
        ],
        "solution": "def two_sum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []",
        "explanation": "Store previously encountered values in a dictionary with their index. For each number, compute target - num and check for O(1) existence in the map.",
        "better_approach": "Using a hash table solves the problem in a single pass O(n) time, superior to nested loop brute-force O(n^2).",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "_id": "prob_arrays_first_duplicate",
        "title": "Find First Duplicate",
        "description": "Given a list of integers `nums`, find and return the first duplicate element. If no duplicate exists, return -1.",
        "topic": "Arrays",
        "subconcept": "set_membership",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 10,
        "tags": ["arrays", "set", "lookup"],
        "examples": [
            {"input_str": "find_first_duplicate([2, 1, 3, 5, 3, 2])", "output_str": "3", "explanation": "3 occurs second at index 4 before 2 occurs at index 5"}
        ],
        "constraints": ["1 <= len(nums) <= 10^5"],
        "starter_code": "def find_first_duplicate(nums: list[int]) -> int:\n    # Find first recurring duplicate\n    pass\n",
        "test_cases": [
            {"input_args": [[2, 1, 3, 5, 3, 2]], "expected_output": 3, "is_hidden": False},
            {"input_args": [[1, 2, 3, 4]], "expected_output": -1, "is_hidden": False},
            {"input_args": [[5, 5]], "expected_output": 5, "is_hidden": True}
        ],
        "solution": "def find_first_duplicate(nums: list[int]) -> int:\n    seen = set()\n    for num in nums:\n        if num in seen:\n            return num\n        seen.add(num)\n    return -1",
        "explanation": "Iterate sequentially through the array, storing visited elements in a hash set. The first element encountered that is already in seen is the duplicate.",
        "better_approach": "Set lookup is O(1) average time. Total O(n) time and O(n) space.",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "_id": "prob_loops_count_vowels",
        "title": "Count Vowels in String",
        "description": "Write a function `count_vowels(s)` that takes a string `s` and counts all vowels ('a', 'e', 'i', 'o', 'u', case-insensitive).",
        "topic": "Loops",
        "subconcept": "string_iteration",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 10,
        "tags": ["loops", "strings", "counting"],
        "examples": [
            {"input_str": "count_vowels('CodeMentor')", "output_str": "4", "explanation": "o, e, e, o -> 4 vowels"}
        ],
        "constraints": ["0 <= len(s) <= 10^4"],
        "starter_code": "def count_vowels(s: str) -> int:\n    # Count vowels in string\n    pass\n",
        "test_cases": [
            {"input_args": ["CodeMentor"], "expected_output": 4, "is_hidden": False},
            {"input_args": ["xyz"], "expected_output": 0, "is_hidden": False},
            {"input_args": ["AEIOUaeiou"], "expected_output": 10, "is_hidden": True}
        ],
        "solution": "def count_vowels(s: str) -> int:\n    vowels = {'a', 'e', 'i', 'o', 'u'}\n    count = 0\n    for char in s.lower():\n        if char in vowels:\n            count += 1\n    return count",
        "explanation": "Convert string characters to lowercase and check membership against a set of vowels.",
        "better_approach": "Using sum(1 for char in s.lower() if char in 'aeiou') gives a clean pythonic one-liner.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "_id": "prob_loops_bubble_sort",
        "title": "Bubble Sort",
        "description": "Implement the `bubble_sort(nums)` function that sorts an array of numbers in ascending order in-place using bubble sort.",
        "topic": "Loops",
        "subconcept": "nested_loop_boundaries",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 15,
        "tags": ["sorting", "loops", "in_place"],
        "examples": [
            {"input_str": "bubble_sort([5, 1, 4, 2, 8])", "output_str": "[1, 2, 4, 5, 8]", "explanation": "Sorted ascending"}
        ],
        "constraints": ["0 <= len(nums) <= 500"],
        "starter_code": "def bubble_sort(nums: list[int]) -> list[int]:\n    # Implement bubble sort\n    pass\n",
        "test_cases": [
            {"input_args": [[5, 1, 4, 2, 8]], "expected_output": [1, 2, 4, 5, 8], "is_hidden": False},
            {"input_args": [[1]], "expected_output": [1], "is_hidden": False},
            {"input_args": [[3, 2, 1]], "expected_output": [1, 2, 3], "is_hidden": True}
        ],
        "solution": "def bubble_sort(nums: list[int]) -> list[int]:\n    n = len(nums)\n    for i in range(n):\n        swapped = False\n        for j in range(0, n - i - 1):\n            if nums[j] > nums[j + 1]:\n                nums[j], nums[j + 1] = nums[j + 1], nums[j]\n                swapped = True\n        if not swapped:\n            break\n    return nums",
        "explanation": "Repeatedly swap adjacent elements if out of order. The inner loop boundary `n - i - 1` ensures we do not go out of bounds or re-check sorted elements.",
        "better_approach": "Early exit flag `swapped` allows O(n) best case on nearly sorted data.",
        "time_complexity": "O(n^2)",
        "space_complexity": "O(1)"
    },
    {
        "_id": "prob_searching_binary_search",
        "title": "Binary Search",
        "description": "Given a sorted array of distinct integers `nums` and a target value `target`, write a function `binary_search(nums, target)` to return the index of `target`, or `-1` if not found.",
        "topic": "Searching",
        "subconcept": "boundary_pointers",
        "difficulty": "intermediate",
        "language": "python",
        "type": "coding",
        "estimated_time": 15,
        "tags": ["searching", "binary_search", "pointers"],
        "examples": [
            {"input_str": "binary_search([-1, 0, 3, 5, 9, 12], 9)", "output_str": "4", "explanation": "9 exists at index 4"}
        ],
        "constraints": ["1 <= len(nums) <= 10^4", "nums is sorted in ascending order"],
        "starter_code": "def binary_search(nums: list[int], target: int) -> int:\n    # Implement binary search in O(log n) time\n    pass\n",
        "test_cases": [
            {"input_args": [[-1, 0, 3, 5, 9, 12], 9], "expected_output": 4, "is_hidden": False},
            {"input_args": [[-1, 0, 3, 5, 9, 12], 2], "expected_output": -1, "is_hidden": False},
            {"input_args": [[5], 5], "expected_output": 0, "is_hidden": True}
        ],
        "solution": "def binary_search(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
        "explanation": "Maintain `left` and `right` pointers. Update `left = mid + 1` or `right = mid - 1` to halve the search space each step. Loop condition must be `left <= right` to inspect single-element intervals.",
        "better_approach": "Calculating mid as `left + (right - left) // 2` avoids potential integer overflow in languages with fixed integer limits.",
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)"
    },
    {
        "_id": "prob_strings_valid_parentheses",
        "title": "Valid Parentheses",
        "description": "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        "topic": "Strings",
        "subconcept": "stack_matching",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 15,
        "tags": ["strings", "stack", "data_structures"],
        "examples": [
            {"input_str": "is_valid('()[]{}')", "output_str": "True", "explanation": "All brackets closed properly"},
            {"input_str": "is_valid('(]')", "output_str": "False", "explanation": "Mismatched bracket"}
        ],
        "constraints": ["1 <= len(s) <= 10^4"],
        "starter_code": "def is_valid(s: str) -> bool:\n    # Check valid parentheses\n    pass\n",
        "test_cases": [
            {"input_args": ["()[]{}"], "expected_output": True, "is_hidden": False},
            {"input_args": ["(]"], "expected_output": False, "is_hidden": False},
            {"input_args": ["([)]"], "expected_output": False, "is_hidden": True},
            {"input_args": ["{[]}"], "expected_output": True, "is_hidden": True}
        ],
        "solution": "def is_valid(s: str) -> bool:\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top_element = stack.pop() if stack else '#'\n            if mapping[char] != top_element:\n                return False\n        else:\n            stack.append(char)\n    return not stack",
        "explanation": "Use a stack (LIFO) to push opening brackets and pop matching opening brackets when closing brackets appear.",
        "better_approach": "Fast return `if len(s) % 2 != 0: return False` eliminates odd length strings immediately.",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "_id": "prob_strings_palindrome",
        "title": "Valid Palindrome",
        "description": "Write a function `is_palindrome(s)` that determines if a string `s` is a palindrome, considering only alphanumeric characters and ignoring cases.",
        "topic": "Strings",
        "subconcept": "two_pointer_check",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 10,
        "tags": ["strings", "two_pointer"],
        "examples": [
            {"input_str": "is_palindrome('A man, a plan, a canal: Panama')", "output_str": "True", "explanation": "'amanaplanacanalpanama' is a palindrome"}
        ],
        "constraints": ["1 <= len(s) <= 2 * 10^5"],
        "starter_code": "def is_palindrome(s: str) -> bool:\n    # Check if alphanumeric palindrome\n    pass\n",
        "test_cases": [
            {"input_args": ["A man, a plan, a canal: Panama"], "expected_output": True, "is_hidden": False},
            {"input_args": ["race a car"], "expected_output": False, "is_hidden": False},
            {"input_args": [" "], "expected_output": True, "is_hidden": True}
        ],
        "solution": "def is_palindrome(s: str) -> bool:\n    cleaned = [c.lower() for c in s if c.isalnum()]\n    return cleaned == cleaned[::-1]",
        "explanation": "Filter out non-alphanumeric chars, lower the case, and compare with reverse.",
        "better_approach": "Two-pointer approach using `left` and `right` indices allows O(1) space without creating a copy of the string.",
        "time_complexity": "O(n)",
        "space_complexity": "O(n) or O(1) with two pointers"
    },
    {
        "_id": "prob_dictionaries_group_anagrams",
        "title": "Group Anagrams",
        "description": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.",
        "topic": "Dictionaries",
        "subconcept": "hash_key_canonicalization",
        "difficulty": "intermediate",
        "language": "python",
        "type": "coding",
        "estimated_time": 20,
        "tags": ["dictionaries", "strings", "hashmap"],
        "examples": [
            {"input_str": "group_anagrams(['eat','tea','tan','ate','nat','bat'])", "output_str": "[['eat','tea','ate'],['tan','nat'],['bat']]", "explanation": "Anagram groups"}
        ],
        "constraints": ["1 <= len(strs) <= 10^4"],
        "starter_code": "def group_anagrams(strs: list[str]) -> list[list[str]]:\n    # Group strings that are anagrams\n    pass\n",
        "test_cases": [
            {"input_args": [["eat", "tea", "tan", "ate", "nat", "bat"]], "expected_output": [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]], "is_hidden": False},
            {"input_args": [[""]], "expected_output": [[""]], "is_hidden": False}
        ],
        "solution": "from collections import defaultdict\ndef group_anagrams(strs: list[str]) -> list[list[str]]:\n    ans = defaultdict(list)\n    for s in strs:\n        ans[tuple(sorted(s))].append(s)\n    return list(ans.values())",
        "explanation": "Canonicalize each string by sorting its characters. All anagrams will have the exact same sorted character tuple.",
        "better_approach": "Using a 26-element character count tuple as the dict key avoids sorting each string and runs in O(N * K) time.",
        "time_complexity": "O(N * K log K)",
        "space_complexity": "O(N * K)"
    },
    {
        "_id": "prob_dp_climbing_stairs",
        "title": "Climbing Stairs",
        "description": "You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "topic": "Dynamic Programming",
        "subconcept": "state_transition",
        "difficulty": "intermediate",
        "language": "python",
        "type": "coding",
        "estimated_time": 15,
        "tags": ["dynamic_programming", "recursion", "math"],
        "examples": [
            {"input_str": "climb_stairs(3)", "output_str": "3", "explanation": "1+1+1, 1+2, 2+1"}
        ],
        "constraints": ["1 <= n <= 45"],
        "starter_code": "def climb_stairs(n: int) -> int:\n    # Return number of distinct ways to climb\n    pass\n",
        "test_cases": [
            {"input_args": [2], "expected_output": 2, "is_hidden": False},
            {"input_args": [3], "expected_output": 3, "is_hidden": False},
            {"input_args": [5], "expected_output": 8, "is_hidden": True}
        ],
        "solution": "def climb_stairs(n: int) -> int:\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b",
        "explanation": "To reach step n, you can arrive from step (n-1) or step (n-2). Hence ways(n) = ways(n-1) + ways(n-2).",
        "better_approach": "Only tracking the last two values in variables `a` and `b` reduces space to O(1).",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "_id": "prob_dp_max_subarray",
        "title": "Maximum Subarray (Kadane's)",
        "description": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.",
        "topic": "Dynamic Programming",
        "subconcept": "kadanes_algorithm",
        "difficulty": "intermediate",
        "language": "python",
        "type": "coding",
        "estimated_time": 20,
        "tags": ["arrays", "dynamic_programming", "kadane"],
        "examples": [
            {"input_str": "max_sub_array([-2,1,-3,4,-1,2,1,-5,4])", "output_str": "6", "explanation": "[4,-1,2,1] has the largest sum = 6"}
        ],
        "constraints": ["1 <= len(nums) <= 10^5"],
        "starter_code": "def max_sub_array(nums: list[int]) -> int:\n    # Implement Kadane's algorithm\n    pass\n",
        "test_cases": [
            {"input_args": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expected_output": 6, "is_hidden": False},
            {"input_args": [[1]], "expected_output": 1, "is_hidden": False},
            {"input_args": [[5, 4, -1, 7, 8]], "expected_output": 23, "is_hidden": True}
        ],
        "solution": "def max_sub_array(nums: list[int]) -> int:\n    max_so_far = nums[0]\n    curr_max = nums[0]\n    for i in range(1, len(nums)):\n        curr_max = max(nums[i], curr_max + nums[i])\n        max_so_far = max(max_so_far, curr_max)\n    return max_so_far",
        "explanation": "Kadane's algorithm: at each element, decide whether to start a new subarray or extend the existing running subarray.",
        "better_approach": "Runs in a single O(n) pass with O(1) space.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "_id": "prob_functions_merge_sorted",
        "title": "Merge Two Sorted Lists",
        "description": "Write a function `merge_sorted(list1, list2)` that merges two sorted integer lists into one sorted list.",
        "topic": "Functions",
        "subconcept": "two_pointer_merging",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 12,
        "tags": ["functions", "arrays", "two_pointer"],
        "examples": [
            {"input_str": "merge_sorted([1, 2, 4], [1, 3, 4])", "output_str": "[1, 1, 2, 3, 4, 4]", "explanation": "Combined sorted order"}
        ],
        "constraints": ["0 <= len(list1), len(list2) <= 5000"],
        "starter_code": "def merge_sorted(list1: list[int], list2: list[int]) -> list[int]:\n    # Merge two sorted lists\n    pass\n",
        "test_cases": [
            {"input_args": [[1, 2, 4], [1, 3, 4]], "expected_output": [1, 1, 2, 3, 4, 4], "is_hidden": False},
            {"input_args": [[], []], "expected_output": [], "is_hidden": False},
            {"input_args": [[], [0]], "expected_output": [0], "is_hidden": True}
        ],
        "solution": "def merge_sorted(list1: list[int], list2: list[int]) -> list[int]:\n    result = []\n    i = j = 0\n    while i < len(list1) and j < len(list2):\n        if list1[i] <= list2[j]:\n            result.append(list1[i])\n            i += 1\n        else:\n            result.append(list2[j])\n            j += 1\n    result.extend(list1[i:])\n    result.extend(list2[j:])\n    return result",
        "explanation": "Maintain pointers for each list and sequentially pick the smaller item.",
        "better_approach": "Linear O(N + M) merge step without re-sorting.",
        "time_complexity": "O(N + M)",
        "space_complexity": "O(N + M)"
    },
    {
        "_id": "prob_oop_bank_account",
        "title": "Bank Account Class",
        "description": "Implement a class `BankAccount` with methods: `deposit(amount)`, `withdraw(amount)`, and `get_balance()`. Withdrawals exceeding balance should raise a `ValueError` with 'Insufficient funds'.",
        "topic": "OOP",
        "subconcept": "encapsulation_and_state",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 15,
        "tags": ["oop", "classes", "state"],
        "examples": [
            {"input_str": "acc = BankAccount(100); acc.deposit(50); acc.withdraw(30); acc.get_balance()", "output_str": "120", "explanation": "100 + 50 - 30 = 120"}
        ],
        "constraints": ["Initial balance >= 0"],
        "starter_code": "class BankAccount:\n    def __init__(self, initial_balance: float = 0.0):\n        # Initialize balance\n        pass\n\n    def deposit(self, amount: float) -> None:\n        pass\n\n    def withdraw(self, amount: float) -> None:\n        pass\n\n    def get_balance(self) -> float:\n        pass\n",
        "test_cases": [
            {"input_args": ["test_oop"], "expected_output": 120, "is_hidden": False}
        ],
        "solution": "class BankAccount:\n    def __init__(self, initial_balance: float = 0.0):\n        self._balance = initial_balance\n\n    def deposit(self, amount: float) -> None:\n        if amount <= 0:\n            raise ValueError('Deposit must be positive')\n        self._balance += amount\n\n    def withdraw(self, amount: float) -> None:\n        if amount > self._balance:\n            raise ValueError('Insufficient funds')\n        self._balance -= amount\n\n    def get_balance(self) -> float:\n        return self._balance",
        "explanation": "Encapsulate account balance in an instance attribute with validation guards.",
        "better_approach": "Using property decorators `@property` provides pythonic encapsulation.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "_id": "prob_conditions_leap_year",
        "title": "Leap Year Checker",
        "description": "Write a function `is_leap_year(year)` that returns `True` if a year is a leap year, and `False` otherwise. (Divisible by 4, except end-of-century years which must be divisible by 400).",
        "topic": "Conditions",
        "subconcept": "compound_boolean_logic",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 10,
        "tags": ["conditions", "boolean_logic", "math"],
        "examples": [
            {"input_str": "is_leap_year(2000)", "output_str": "True", "explanation": "2000 is divisible by 400"},
            {"input_str": "is_leap_year(1900)", "output_str": "False", "explanation": "1900 is divisible by 100 but not 400"}
        ],
        "constraints": ["1 <= year <= 9999"],
        "starter_code": "def is_leap_year(year: int) -> bool:\n    # Check leap year logic\n    pass\n",
        "test_cases": [
            {"input_args": [2000], "expected_output": True, "is_hidden": False},
            {"input_args": [1900], "expected_output": False, "is_hidden": False},
            {"input_args": [2024], "expected_output": True, "is_hidden": True}
        ],
        "solution": "def is_leap_year(year: int) -> bool:\n    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)",
        "explanation": "A year is a leap year if (divisible by 4 AND NOT divisible by 100) OR (divisible by 400).",
        "better_approach": "Combine into a single boolean return statement.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "_id": "prob_variables_swap",
        "title": "Reverse Words in a Sentence",
        "description": "Write a function `reverse_words(s)` that takes a string `s` and returns a string with the words reversed in order while preserving single whitespace separation.",
        "topic": "Variables",
        "subconcept": "string_reversal",
        "difficulty": "beginner",
        "language": "python",
        "type": "coding",
        "estimated_time": 10,
        "tags": ["variables", "strings", "builtins"],
        "examples": [
            {"input_str": "reverse_words('the sky is blue')", "output_str": "'blue is sky the'", "explanation": "Words reversed"}
        ],
        "constraints": ["1 <= len(s) <= 10^4"],
        "starter_code": "def reverse_words(s: str) -> str:\n    # Reverse word order\n    pass\n",
        "test_cases": [
            {"input_args": ["the sky is blue"], "expected_output": "blue is sky the", "is_hidden": False},
            {"input_args": ["  hello world  "], "expected_output": "world hello", "is_hidden": False}
        ],
        "solution": "def reverse_words(s: str) -> str:\n    return ' '.join(s.split()[::-1])",
        "explanation": "Split words by whitespace, reverse the list, and join with single spaces.",
        "better_approach": "Using `s.split()` handles variable leading/trailing and multiple internal spaces automatically.",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    }
]

KNOWLEDGE_CHECK_QUESTIONS: List[Dict[str, Any]] = [
    {
        "question_id": "q_loops_1",
        "question": "What is the output of the following Python loop?\n\nx = 0\nfor i in range(1, 5):\n    x += i\nprint(x)",
        "type": "predict_output",
        "topic": "Loops",
        "subconcept": "loop_boundary",
        "difficulty": "beginner",
        "options": ["10", "15", "6", "4"],
        "correct_answer": "10",
        "explanation": "range(1, 5) produces values 1, 2, 3, 4 (up to but not including 5). 1 + 2 + 3 + 4 = 10.",
        "misconception": "Thinking range(1, 5) includes the endpoint 5."
    },
    {
        "question_id": "q_arrays_1",
        "question": "What is the time complexity of looking up a value by key in a standard Python dictionary / hash table on average?",
        "type": "complexity",
        "topic": "Arrays",
        "subconcept": "hash_lookup",
        "difficulty": "intermediate",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        "correct_answer": "O(1)",
        "explanation": "Python dictionaries use hash tables which provide O(1) constant time average lookup.",
        "misconception": "Confusing list linear search O(n) with hash table lookup O(1)."
    },
    {
        "question_id": "q_recursion_1",
        "question": "What happens if a recursive function does NOT include a valid base case?",
        "type": "conceptual",
        "topic": "Recursion",
        "subconcept": "base_case",
        "difficulty": "beginner",
        "options": [
            "It causes infinite recursion and raises a RecursionError (Stack Overflow)",
            "It automatically returns None after 10 calls",
            "It converts into a while loop automatically",
            "It runs in O(1) time"
        ],
        "correct_answer": "It causes infinite recursion and raises a RecursionError (Stack Overflow)",
        "explanation": "Without a base case, recursive calls continue allocating new frames on the call stack until memory/recursion depth limit is exhausted.",
        "misconception": "Assuming the runtime automatically detects and terminates runaway recursion safely."
    },
    {
        "question_id": "q_recursion_2",
        "question": "Consider the following recursive function:\n\ndef fun(n):\n    if n <= 1:\n        return 1\n    return n + fun(n - 2)\n\nWhat is the return value of fun(5)?",
        "type": "predict_output",
        "topic": "Recursion",
        "subconcept": "recursive_trace",
        "difficulty": "intermediate",
        "options": ["9", "15", "10", "5"],
        "correct_answer": "9",
        "explanation": "fun(5) = 5 + fun(3) -> fun(3) = 3 + fun(1) -> fun(1) = 1. Therefore 5 + 3 + 1 = 9.",
        "misconception": "Forgetting that the step decreases by 2 (n - 2), not 1."
    },
    {
        "question_id": "q_functions_1",
        "question": "In Python, what is the danger of using a mutable default argument like `def append_to(item, target=[])`?",
        "type": "identify_bug",
        "topic": "Functions",
        "subconcept": "mutable_defaults",
        "difficulty": "intermediate",
        "options": [
            "The same list instance is shared across subsequent function calls",
            "It raises a TypeError on execution",
            "The list gets deleted after the first call",
            "It makes the function run in O(2^n) time"
        ],
        "correct_answer": "The same list instance is shared across subsequent function calls",
        "explanation": "Default parameter expressions in Python are evaluated once when the function is defined, so the same mutable object persists across all calls.",
        "misconception": "Believing default arguments are recreated freshly on every invocation."
    },
    {
        "question_id": "q_searching_1",
        "question": "What prerequisite MUST be satisfied before applying Binary Search on an array?",
        "type": "conceptual",
        "topic": "Searching",
        "subconcept": "binary_search_prerequisite",
        "difficulty": "beginner",
        "options": [
            "The array must be sorted",
            "All numbers must be positive",
            "The length of the array must be an even number",
            "The array cannot contain duplicates"
        ],
        "correct_answer": "The array must be sorted",
        "explanation": "Binary search relies on monotonicity (sorted order) to decide whether to search the left or right half.",
        "misconception": "Attempting binary search on unsorted collections without prior sorting."
    },
    {
        "question_id": "q_strings_1",
        "question": "What is the output of `'python'[::-1]` in Python?",
        "type": "predict_output",
        "topic": "Strings",
        "subconcept": "slicing",
        "difficulty": "beginner",
        "options": ["'nohtyp'", "'python'", "''", "Error"],
        "correct_answer": "'nohtyp'",
        "explanation": "A step of -1 in slicing reverses the string.",
        "misconception": "Thinking negative slicing indexes from the front."
    },
    {
        "question_id": "q_dictionaries_1",
        "question": "Which of the following data types CANNOT be used as a key in a Python dictionary?",
        "type": "conceptual",
        "topic": "Dictionaries",
        "subconcept": "hashability",
        "difficulty": "intermediate",
        "options": ["[1, 2, 3] (list)", "'hello' (string)", "(1, 2) (tuple)", "42 (integer)"],
        "correct_answer": "[1, 2, 3] (list)",
        "explanation": "Dictionary keys must be hashable and immutable. Lists are mutable and unhashable, raising a TypeError.",
        "misconception": "Assuming any sequence type can be used as a dictionary key."
    }
]

async def seed_database(db):
    problems_col = db["problems"]
    assessments_bank = db["assessment_bank"]
    
    prob_count = await problems_col.count_documents({})
    if prob_count == 0:
        logger.info(f"Seeding {len(SEED_PROBLEMS)} curated coding problems...")
        for prob in SEED_PROBLEMS:
            await problems_col.insert_one(prob)
        logger.info("Problems seeded successfully.")

    q_count = await assessments_bank.count_documents({})
    if q_count == 0:
        logger.info(f"Seeding {len(KNOWLEDGE_CHECK_QUESTIONS)} curated knowledge check questions...")
        for q in KNOWLEDGE_CHECK_QUESTIONS:
            await assessments_bank.insert_one(q)
        logger.info("Knowledge check questions seeded successfully.")
