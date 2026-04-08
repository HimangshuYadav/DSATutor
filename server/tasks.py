"""
Problem bank for DSATutor.
Contains 54 problems categorized by topic and difficulty level.
"""

import random

# Problems are categorized into Easy (0), Medium (1), and Hard (2).
PROBLEMS = [
    # Arrays - Easy
    {
        "id": "e01", "title": "Peak Finder in Temperature Data",
        "topic": "Arrays", "difficulty": 0,
        "description": "Given an array of daily temperatures, find any single 'peak' day where the temperature is strictly greater than both its neighbours. Return its index. Edge elements can be peaks if they are greater than their only neighbour. Example: [62, 65, 70, 68, 72] → index 2.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e02", "title": "Rotate Array by K Positions",
        "topic": "Arrays", "difficulty": 0,
        "description": "Given an integer array and a number K, rotate the array to the right by K steps in-place. Example: [1,2,3,4,5], K=2 → [4,5,1,2,3].",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e03", "title": "Find the Missing Number",
        "topic": "Arrays", "difficulty": 0,
        "description": "Given an array containing N distinct numbers in the range [0, N], find the one number missing from the array. Example: [3,0,1] → 2.",
        "expected_complexity": "O(N)"
    },

    # Strings
    {
        "id": "e04", "title": "Reverse Words in a Sentence",
        "topic": "Strings", "difficulty": 0,
        "description": "Given a sentence string, reverse the order of words. Remove leading/trailing spaces and reduce multiple spaces to one. Example: '  hello   world  ' → 'world hello'.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e05", "title": "Valid Palindrome Check",
        "topic": "Strings", "difficulty": 0,
        "description": "Given a string, determine if it is a palindrome considering only alphanumeric characters and ignoring cases. Example: 'A man, a plan, a canal: Panama' → True.",
        "expected_complexity": "O(N)"
    },

    # Linked Lists
    {
        "id": "e06", "title": "Remove Duplicates from Sorted Linked List",
        "topic": "Linked Lists", "difficulty": 0,
        "description": "Given the head of a sorted singly linked list, delete all duplicates so each element appears only once. Example: 1→1→2→3→3 → 1→2→3.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e07", "title": "Reverse a Linked List",
        "topic": "Linked Lists", "difficulty": 0,
        "description": "Given the head of a singly linked list, reverse the list and return the reversed list. Example: 1→2→3→4→5 → 5→4→3→2→1.",
        "expected_complexity": "O(N)"
    },

    # Stacks & Queues
    {
        "id": "e08", "title": "Balanced Bracket Validator",
        "topic": "Stacks & Queues", "difficulty": 0,
        "description": "Given a string containing only '(', ')', '{', '}', '[' and ']', determine if the input is valid. Every open bracket must be closed by the same type in the correct order. Example: '([{}])' → True, '([)]' → False.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e09", "title": "Implement Queue Using Two Stacks",
        "topic": "Stacks & Queues", "difficulty": 0,
        "description": "Implement a first-in-first-out (FIFO) queue using only two stacks. Support push(x), pop(), peek(), and empty() operations. All operations should work in amortized O(1) time.",
        "expected_complexity": "O(1) amortized"
    },

    # Trees
    {
        "id": "e10", "title": "Maximum Depth of Binary Tree",
        "topic": "Trees", "difficulty": 0,
        "description": "Given the root of a binary tree, return its maximum depth (the number of nodes along the longest path from root to leaf). Example: [3,9,20,null,null,15,7] → depth 3.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e11", "title": "Invert a Binary Tree",
        "topic": "Trees", "difficulty": 0,
        "description": "Given the root of a binary tree, invert it (mirror it) so that every left child becomes a right child and vice versa. Return the root of the inverted tree.",
        "expected_complexity": "O(N)"
    },

    # Graphs
    {
        "id": "e12", "title": "Find if Path Exists in Graph",
        "topic": "Graphs", "difficulty": 0,
        "description": "Given an undirected graph with N vertices and a list of edges, determine if there is a valid path from vertex 'source' to 'destination'. Example: n=4, edges=[[0,1],[1,2],[2,3]], src=0, dest=3 → True.",
        "expected_complexity": "O(V+E)"
    },

    # Dynamic Programming
    {
        "id": "e13", "title": "Climbing Stairs",
        "topic": "Dynamic Programming", "difficulty": 0,
        "description": "You are climbing a staircase of N steps. Each time you can climb 1 or 2 steps. How many distinct ways can you reach the top? Example: N=4 → 5 ways.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e14", "title": "Fibonacci Number",
        "topic": "Dynamic Programming", "difficulty": 0,
        "description": "Compute the Nth Fibonacci number. F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2). Example: N=10 → 55. Use memoization or tabulation for efficiency.",
        "expected_complexity": "O(N)"
    },

    # Recursion
    {
        "id": "e15", "title": "Power of Three Check",
        "topic": "Recursion", "difficulty": 0,
        "description": "Given an integer N, write a recursive function to determine whether it is a power of three. Example: 27 → True (3^3), 45 → False.",
        "expected_complexity": "O(log N)"
    },
    {
        "id": "e16", "title": "Sum of Digits (Recursive)",
        "topic": "Recursion", "difficulty": 0,
        "description": "Given a non-negative integer, repeatedly sum its digits until a single digit remains. Implement recursively. Example: 38 → 3+8=11 → 1+1=2.",
        "expected_complexity": "O(log N)"
    },

    # Greedy
    {
        "id": "e17", "title": "Best Time to Collect Coins",
        "topic": "Greedy", "difficulty": 0,
        "description": "You have N piles of coins. You can pick coins from any pile but picking from pile i locks piles i-1 and i+1. Find the maximum coins you can collect. Example: [3,1,5,8,2] → 3+5+2=10.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e18", "title": "Assign Cookies to Children",
        "topic": "Greedy", "difficulty": 0,
        "description": "Each child has a greed factor g[i] and each cookie has a size s[j]. A child is content if cookie size >= greed factor. Maximize the number of content children. Example: g=[1,2,3], s=[1,1] → 1 child.",
        "expected_complexity": "O(N log N)"
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  MEDIUM (difficulty=1) — 18 problems
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # Arrays
    {
        "id": "m01", "title": "Container With Most Water",
        "topic": "Arrays", "difficulty": 1,
        "description": "Given an array of N heights representing vertical lines, find two lines that form a container holding the most water. Example: [1,8,6,2,5,4,8,3,7] → 49.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "m02", "title": "Product of Array Except Self",
        "topic": "Arrays", "difficulty": 1,
        "description": "Given an integer array nums, return an array where answer[i] is the product of all elements except nums[i]. Solve without using division and in O(N) time. Example: [1,2,3,4] → [24,12,8,6].",
        "expected_complexity": "O(N)"
    },

    # Strings
    {
        "id": "m03", "title": "Longest Substring Without Repeating Characters",
        "topic": "Strings", "difficulty": 1,
        "description": "Given a string, find the length of the longest substring without repeating characters. Example: 'abcabcbb' → 3 ('abc').",
        "expected_complexity": "O(N)"
    },
    {
        "id": "m04", "title": "Group Anagrams Together",
        "topic": "Strings", "difficulty": 1,
        "description": "Given a list of strings, group the anagrams together. Example: ['eat','tea','tan','ate','nat','bat'] → [['eat','tea','ate'],['tan','nat'],['bat']].",
        "expected_complexity": "O(N * K log K)"
    },

    # Linked Lists
    {
        "id": "m05", "title": "Detect Cycle Start Node in Linked List",
        "topic": "Linked Lists", "difficulty": 1,
        "description": "Given the head of a linked list, detect if there is a cycle. If a cycle exists, return the node where the cycle begins. Use O(1) extra memory (Floyd's algorithm).",
        "expected_complexity": "O(N)"
    },
    {
        "id": "m06", "title": "Add Two Numbers as Linked Lists",
        "topic": "Linked Lists", "difficulty": 1,
        "description": "Given two non-empty linked lists representing two non-negative integers stored in reverse order, add the two numbers and return the sum as a linked list. Example: 2→4→3 + 5→6→4 = 7→0→8 (342+465=807).",
        "expected_complexity": "O(N)"
    },

    # Stacks & Queues
    {
        "id": "m07", "title": "Min Stack with O(1) GetMin",
        "topic": "Stacks & Queues", "difficulty": 1,
        "description": "Design a stack that supports push, pop, top, and getMin operations, all in O(1) time. Example: push(-2), push(0), push(-3), getMin() → -3, pop(), top() → 0, getMin() → -2.",
        "expected_complexity": "O(1)"
    },
    {
        "id": "m08", "title": "Daily Temperatures (Next Warmer Day)",
        "topic": "Stacks & Queues", "difficulty": 1,
        "description": "Given an array of daily temperatures, return an array where answer[i] says how many days you have to wait for a warmer temperature. If none, put 0. Example: [73,74,75,71,69,72,76,73] → [1,1,4,2,1,1,0,0].",
        "expected_complexity": "O(N)"
    },

    # Trees
    {
        "id": "m09", "title": "Binary Tree Level Order Zigzag",
        "topic": "Trees", "difficulty": 1,
        "description": "Given a binary tree, return the zigzag level order traversal (left→right for level 1, right→left for level 2, etc). Example: [3,9,20,null,null,15,7] → [[3],[20,9],[15,7]].",
        "expected_complexity": "O(N)"
    },
    {
        "id": "m10", "title": "Validate Binary Search Tree",
        "topic": "Trees", "difficulty": 1,
        "description": "Given the root of a binary tree, determine if it is a valid BST. A valid BST has left subtree values strictly less than root and right subtree values strictly greater. Example: [2,1,3] → True, [5,1,4,null,null,3,6] → False.",
        "expected_complexity": "O(N)"
    },

    # Graphs
    {
        "id": "m11", "title": "Course Schedule Feasibility",
        "topic": "Graphs", "difficulty": 1,
        "description": "There are N courses with prerequisites given as pairs [a,b] meaning you must take b before a. Determine if finishing all courses is possible (no circular dependency). Example: N=4, [[1,0],[2,1],[3,2]] → True.",
        "expected_complexity": "O(V+E)"
    },
    {
        "id": "m12", "title": "Number of Connected Islands",
        "topic": "Graphs", "difficulty": 1,
        "description": "Given an MxN grid of '1's (land) and '0's (water), count the number of islands. An island is surrounded by water and formed by connecting adjacent lands horizontally or vertically. Example: grid with two separate land masses → 2.",
        "expected_complexity": "O(M*N)"
    },

    # Dynamic Programming
    {
        "id": "m13", "title": "Coin Change: Minimum Coins",
        "topic": "Dynamic Programming", "difficulty": 1,
        "description": "Given coin denominations and a target amount, find the minimum number of coins needed. Return -1 if impossible. Example: coins=[1,5,10,25], amount=36 → 3 (25+10+1).",
        "expected_complexity": "O(amount * coins)"
    },
    {
        "id": "m14", "title": "Longest Increasing Subsequence",
        "topic": "Dynamic Programming", "difficulty": 1,
        "description": "Given an integer array, return the length of the longest strictly increasing subsequence. Example: [10,9,2,5,3,7,101,18] → 4 ([2,3,7,101]).",
        "expected_complexity": "O(N log N)"
    },

    # Recursion
    {
        "id": "m15", "title": "Generate All Valid Parentheses",
        "topic": "Recursion", "difficulty": 1,
        "description": "Given N pairs of parentheses, generate all valid combinations. Example: N=3 → ['((()))', '(()())', '(())()', '()(())', '()()()'].",
        "expected_complexity": "O(4^N / sqrt(N))"
    },
    {
        "id": "m16", "title": "Letter Combinations of Phone Number",
        "topic": "Recursion", "difficulty": 1,
        "description": "Given a string containing digits 2-9, return all possible letter combinations (like phone keypad). Example: '23' → ['ad','ae','af','bd','be','bf','cd','ce','cf'].",
        "expected_complexity": "O(4^N)"
    },

    # Greedy
    {
        "id": "m17", "title": "Activity Selection with Maximum Profit",
        "topic": "Greedy", "difficulty": 1,
        "description": "Given N activities each with a start/end time and profit, select the maximum-profit set of non-overlapping activities. Example: start=[1,3,0], end=[2,4,6], profit=[5,6,5] → max profit by choosing optimal subset.",
        "expected_complexity": "O(N log N)"
    },
    {
        "id": "m18", "title": "Jump Game: Can You Reach the End?",
        "topic": "Greedy", "difficulty": 1,
        "description": "Given an array where each element is the max jump length from that position, determine if you can reach the last index. Example: [2,3,1,1,4] → True, [3,2,1,0,4] → False.",
        "expected_complexity": "O(N)"
    },

    # Hard - difficulty 2

    # Arrays
    {
        "id": "h01", "title": "Median of Two Sorted Arrays",
        "topic": "Arrays", "difficulty": 2,
        "description": "Given two sorted arrays nums1 and nums2, return the median of the combined sorted array in O(log(m+n)) time. Example: nums1=[1,3], nums2=[2] → 2.0.",
        "expected_complexity": "O(log(m+n))"
    },
    {
        "id": "h02", "title": "Trapping Rain Water",
        "topic": "Arrays", "difficulty": 2,
        "description": "Given N non-negative integers representing an elevation map where the width of each bar is 1, compute how much water can be trapped after rain. Example: [0,1,0,2,1,0,1,3,2,1,2,1] → 6.",
        "expected_complexity": "O(N)"
    },

    # Strings
    {
        "id": "h03", "title": "Minimum Window Substring",
        "topic": "Strings", "difficulty": 2,
        "description": "Given strings S and T, find the minimum window substring of S that contains all characters of T (including duplicates). Example: S='ADOBECODEBANC', T='ABC' → 'BANC'.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "h04", "title": "Longest Palindromic Substring",
        "topic": "Strings", "difficulty": 2,
        "description": "Given a string S, find the longest palindromic substring. Example: 'babad' → 'bab' or 'aba'. Use expand-around-center or Manacher's algorithm.",
        "expected_complexity": "O(N^2)"
    },

    # Linked Lists
    {
        "id": "h05", "title": "Reverse Nodes in K-Group",
        "topic": "Linked Lists", "difficulty": 2,
        "description": "Given the head of a linked list, reverse the nodes K at a time. Remaining nodes (< K) are left as-is. Example: [1,2,3,4,5], K=3 → [3,2,1,4,5].",
        "expected_complexity": "O(N)"
    },
    {
        "id": "h06", "title": "Merge K Sorted Linked Lists",
        "topic": "Linked Lists", "difficulty": 2,
        "description": "Merge K sorted linked lists into one sorted linked list. Use a min-heap for optimal performance. Example: [[1,4,5],[1,3,4],[2,6]] → [1,1,2,3,4,4,5,6].",
        "expected_complexity": "O(N log K)"
    },

    # Stacks & Queues
    {
        "id": "h07", "title": "Largest Rectangle in Histogram",
        "topic": "Stacks & Queues", "difficulty": 2,
        "description": "Given an array of bar heights in a histogram, find the area of the largest rectangle that can be formed. Example: [2,1,5,6,2,3] → 10 (bars 5 and 6, width 2).",
        "expected_complexity": "O(N)"
    },
    {
        "id": "h08", "title": "Sliding Window Maximum",
        "topic": "Stacks & Queues", "difficulty": 2,
        "description": "Given an array and a sliding window of size K, return the maximum value in each window position as the window slides from left to right. Example: [1,3,-1,-3,5,3,6,7], K=3 → [3,3,5,5,6,7].",
        "expected_complexity": "O(N)"
    },

    # Trees
    {
        "id": "h09", "title": "Serialize and Deserialize Binary Tree",
        "topic": "Trees", "difficulty": 2,
        "description": "Design an algorithm to serialize a binary tree to a string and deserialize it back to the original tree. Handle null nodes properly. Example: [1,2,3,null,null,4,5] ↔ '1,2,null,null,3,4,null,null,5,null,null'.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "h10", "title": "Binary Tree Maximum Path Sum",
        "topic": "Trees", "difficulty": 2,
        "description": "Given a binary tree, find the maximum path sum. A path can start and end at any node. Example: [-10,9,20,null,null,15,7] → 42 (path: 15→20→7).",
        "expected_complexity": "O(N)"
    },

    # Graphs
    {
        "id": "h11", "title": "Shortest Path in Weighted Grid",
        "topic": "Graphs", "difficulty": 2,
        "description": "Given an MxN grid where each cell has a cost (0=blocked), find the shortest-cost path from top-left to bottom-right. Can move in 4 directions. Use Dijkstra's algorithm.",
        "expected_complexity": "O(M*N*log(M*N))"
    },
    {
        "id": "h12", "title": "Word Ladder: Shortest Transformation",
        "topic": "Graphs", "difficulty": 2,
        "description": "Given begin/end words and a dictionary, find the shortest transformation sequence where each step changes one letter and each intermediate word must be in the dictionary. Example: 'hit'→'cog' via ['hot','dot','dog','lot','log','cog'] → 5.",
        "expected_complexity": "O(M^2 * N)"
    },

    # Dynamic Programming
    {
        "id": "h13", "title": "Edit Distance Between Strings",
        "topic": "Dynamic Programming", "difficulty": 2,
        "description": "Given two strings word1 and word2, return the minimum operations (insert, delete, replace) required to convert word1 into word2. Example: 'horse' → 'ros' = 3.",
        "expected_complexity": "O(M*N)"
    },
    {
        "id": "h14", "title": "Wildcard Pattern Matching",
        "topic": "Dynamic Programming", "difficulty": 2,
        "description": "Given string S and pattern P with '?' (any single char) and '*' (any sequence including empty), determine if P matches entire S. Example: S='adceb', P='*a*b' → True.",
        "expected_complexity": "O(M*N)"
    },

    # Recursion
    {
        "id": "h15", "title": "N-Queens Solver",
        "topic": "Recursion", "difficulty": 2,
        "description": "Place N chess queens on an NxN board so no two threaten each other. Return all distinct solutions as lists of column positions per row. Example: N=4 → [[1,3,0,2],[2,0,3,1]].",
        "expected_complexity": "O(N!)"
    },
    {
        "id": "h16", "title": "Sudoku Solver",
        "topic": "Recursion", "difficulty": 2,
        "description": "Write a program to solve a 9x9 Sudoku puzzle by filling empty cells. Each row, column, and 3x3 sub-box must contain digits 1-9 exactly once. Use backtracking.",
        "expected_complexity": "O(9^(empty cells))"
    },

    # Greedy
    {
        "id": "h17", "title": "Job Scheduling with Cooldown",
        "topic": "Greedy", "difficulty": 2,
        "description": "Given an array of jobs (each with a type letter) and cooldown N (same-type jobs must be separated by N intervals), find minimum total intervals including idle. Example: ['A','A','A','B','B','B'], N=2 → 8.",
        "expected_complexity": "O(N log N)"
    },
    {
        "id": "h18", "title": "Minimum Number of Platforms",
        "topic": "Greedy", "difficulty": 2,
        "description": "Given arrival and departure times of trains at a station, find the minimum number of platforms required so no train has to wait. Example: arrivals=[9:00,9:40,9:50,11:00], departures=[9:10,12:00,11:20,11:30] → 3.",
        "expected_complexity": "O(N log N)"
    },

    # Additional Problems - Easy
    {
        "id": "e19", "title": "Move All Zeroes to End",
        "topic": "Arrays", "difficulty": 0,
        "description": "Given an array, move all 0's to the end while maintaining the relative order of the non-zero elements. Do this in-place. Example: [0,1,0,3,12] → [1,3,12,0,0].",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e20", "title": "Two Sum: Find Pair with Target",
        "topic": "Arrays", "difficulty": 0,
        "description": "Given an array of integers and a target sum, return indices of the two numbers that add up to the target. Each input has exactly one solution. Example: [2,7,11,15], target=9 → [0,1].",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e21", "title": "Count Vowels and Consonants",
        "topic": "Strings", "difficulty": 0,
        "description": "Given a string, count the number of vowels and consonants (ignoring non-alphabetic characters). Return both counts. Example: 'Hello World!' → vowels=3, consonants=7.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e22", "title": "First Non-Repeating Character",
        "topic": "Strings", "difficulty": 0,
        "description": "Given a string, find the first non-repeating character and return its index. If none exists, return -1. Example: 'leetcode' → 0 ('l'), 'aabb' → -1.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e23", "title": "Middle of Linked List",
        "topic": "Linked Lists", "difficulty": 0,
        "description": "Given the head of a singly linked list, return the middle node. If there are two middle nodes, return the second one. Example: 1→2→3→4→5 → node 3.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e24", "title": "Next Greater Element",
        "topic": "Stacks & Queues", "difficulty": 0,
        "description": "Given an array, for each element find the next greater element to its right. If none, output -1. Example: [4,5,2,25] → [5,25,25,-1].",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e25", "title": "Symmetric Tree Check",
        "topic": "Trees", "difficulty": 0,
        "description": "Given the root of a binary tree, check whether it is a mirror of itself (symmetric around its center). Example: [1,2,2,3,4,4,3] → True.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e26", "title": "Count Connected Components",
        "topic": "Graphs", "difficulty": 0,
        "description": "Given an undirected graph with N nodes and a list of edges, count the number of connected components. Example: n=5, edges=[[0,1],[1,2],[3,4]] → 2 components.",
        "expected_complexity": "O(V+E)"
    },
    {
        "id": "e27", "title": "House Robber",
        "topic": "Dynamic Programming", "difficulty": 0,
        "description": "You are a robber planning to rob houses along a street. Each house has money, but adjacent houses have linked alarms. Find maximum money without robbing two adjacent houses. Example: [2,7,9,3,1] → 12 (2+9+1).",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e28", "title": "Print All Subsets of a Set",
        "topic": "Recursion", "difficulty": 0,
        "description": "Given a set of distinct integers, return all possible subsets (the power set). Example: [1,2,3] → [[],[1],[2],[3],[1,2],[1,3],[2,3],[1,2,3]].",
        "expected_complexity": "O(2^N)"
    },
    {
        "id": "e29", "title": "Maximum Subarray Sum (Kadane's)",
        "topic": "Arrays", "difficulty": 0,
        "description": "Find the contiguous subarray (at least one element) with the largest sum. Example: [-2,1,-3,4,-1,2,1,-5,4] → 6 (subarray [4,-1,2,1]).",
        "expected_complexity": "O(N)"
    },
    {
        "id": "e30", "title": "Minimum Cost to Buy Fruits",
        "topic": "Greedy", "difficulty": 0,
        "description": "Given N fruit prices and a budget, buy as many fruits as possible. Each fruit has a different price. Maximize count of fruits bought within budget. Example: prices=[1,3,2,5], budget=6 → 3 fruits (1+2+3).",
        "expected_complexity": "O(N log N)"
    },

    # Additional Problems - Medium
    {
        "id": "m19", "title": "3Sum: Find All Triplets",
        "topic": "Arrays", "difficulty": 1,
        "description": "Given an array, find all unique triplets that sum to zero. Example: [-1,0,1,2,-1,-4] → [[-1,-1,2],[-1,0,1]].",
        "expected_complexity": "O(N^2)"
    },
    {
        "id": "m20", "title": "Sort Colors (Dutch National Flag)",
        "topic": "Arrays", "difficulty": 1,
        "description": "Given an array with values 0, 1, and 2 (representing red, white, blue), sort them in-place using one pass. Example: [2,0,2,1,1,0] → [0,0,1,1,2,2].",
        "expected_complexity": "O(N)"
    },
    {
        "id": "m21", "title": "String to Integer (atoi)",
        "topic": "Strings", "difficulty": 1,
        "description": "Implement atoi which converts a string to a 32-bit signed integer. Handle whitespace, signs, overflow, and non-digit characters. Example: '   -42' → -42, '4193 with words' → 4193.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "m22", "title": "Flatten a Nested Linked List",
        "topic": "Linked Lists", "difficulty": 1,
        "description": "Given a doubly linked list where nodes may have a child pointer to another doubly linked list, flatten all levels into a single-level doubly linked list.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "m23", "title": "Evaluate Reverse Polish Notation",
        "topic": "Stacks & Queues", "difficulty": 1,
        "description": "Evaluate an expression in Reverse Polish Notation (postfix). Valid operators: +, -, *, /. Example: ['2','1','+','3','*'] → 9 ((2+1)*3).",
        "expected_complexity": "O(N)"
    },
    {
        "id": "m24", "title": "Lowest Common Ancestor of BST",
        "topic": "Trees", "difficulty": 1,
        "description": "Given a BST and two nodes p and q, find their lowest common ancestor (LCA). The LCA is the deepest node that is an ancestor of both p and q. Example: root=[6,2,8,0,4,7,9], p=2, q=8 → 6.",
        "expected_complexity": "O(log N)"
    },
    {
        "id": "m25", "title": "Clone a Graph",
        "topic": "Graphs", "difficulty": 1,
        "description": "Given a reference to a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node has a value and list of neighbors.",
        "expected_complexity": "O(V+E)"
    },
    {
        "id": "m26", "title": "Unique Paths in Grid",
        "topic": "Dynamic Programming", "difficulty": 1,
        "description": "A robot starts at top-left of an MxN grid and can only move right or down. How many unique paths exist to reach bottom-right? Example: m=3, n=7 → 28.",
        "expected_complexity": "O(M*N)"
    },
    {
        "id": "m27", "title": "Permutations of Array",
        "topic": "Recursion", "difficulty": 1,
        "description": "Given an array of distinct integers, return all possible permutations in any order. Example: [1,2,3] → [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]].",
        "expected_complexity": "O(N!)"
    },
    {
        "id": "m28", "title": "Gas Station Circuit",
        "topic": "Greedy", "difficulty": 1,
        "description": "There are N gas stations arranged in a circle. You have gas[i] fuel at station i and cost[i] to travel to the next station. Find the starting station index to complete the circuit, or -1 if impossible. Example: gas=[1,2,3,4,5], cost=[3,4,5,1,2] → 3.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "m29", "title": "Top K Frequent Elements",
        "topic": "Arrays", "difficulty": 1,
        "description": "Given an integer array and an integer K, return the K most frequent elements. Example: [1,1,1,2,2,3], K=2 → [1,2].",
        "expected_complexity": "O(N log K)"
    },
    {
        "id": "m30", "title": "Decode String with Nested Brackets",
        "topic": "Stacks & Queues", "difficulty": 1,
        "description": "Given an encoded string like '3[a2[c]]', decode it. The rule is k[encoded_string] means the encoded_string is repeated k times. Example: '3[a2[c]]' → 'accaccacc'.",
        "expected_complexity": "O(N)"
    },

    # Additional Problems - Hard
    {
        "id": "h19", "title": "Merge Intervals",
        "topic": "Arrays", "difficulty": 2,
        "description": "Given an array of intervals where intervals[i]=[start_i, end_i], merge all overlapping intervals. Example: [[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]].",
        "expected_complexity": "O(N log N)"
    },
    {
        "id": "h20", "title": "First Missing Positive",
        "topic": "Arrays", "difficulty": 2,
        "description": "Given an unsorted integer array, find the smallest missing positive integer. Must run in O(N) time and O(1) extra space. Example: [3,4,-1,1] → 2.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "h21", "title": "Regular Expression Matching",
        "topic": "Strings", "difficulty": 2,
        "description": "Implement regular expression matching with support for '.' (any single character) and '*' (zero or more of the preceding element). Must match the entire string. Example: s='aab', p='c*a*b' → True.",
        "expected_complexity": "O(M*N)"
    },
    {
        "id": "h22", "title": "Copy List with Random Pointer",
        "topic": "Linked Lists", "difficulty": 2,
        "description": "A linked list has an additional 'random' pointer which could point to any node or null. Construct a deep copy of the list. Each node has val, next, and random fields.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "h23", "title": "Maximum Frequency Stack",
        "topic": "Stacks & Queues", "difficulty": 2,
        "description": "Design a stack-like data structure that pushes elements and pops the most frequent element. If there's a tie, pop the one closest to the stack's top. Support push(x) and pop().",
        "expected_complexity": "O(1)"
    },
    {
        "id": "h24", "title": "Construct Binary Tree from Preorder and Inorder",
        "topic": "Trees", "difficulty": 2,
        "description": "Given preorder and inorder traversal arrays of a binary tree, construct and return the tree. Example: preorder=[3,9,20,15,7], inorder=[9,3,15,20,7] → tree [3,9,20,null,null,15,7].",
        "expected_complexity": "O(N)"
    },
    {
        "id": "h25", "title": "Critical Connections in a Network",
        "topic": "Graphs", "difficulty": 2,
        "description": "Given N servers connected by edges, find all 'critical connections' — edges whose removal disconnects the graph (bridges). Use Tarjan's algorithm.",
        "expected_complexity": "O(V+E)"
    },
    {
        "id": "h26", "title": "Longest Common Subsequence",
        "topic": "Dynamic Programming", "difficulty": 2,
        "description": "Given two strings, find the length of their longest common subsequence. A subsequence is derived by deleting characters without changing order. Example: 'abcde', 'ace' → 3 ('ace').",
        "expected_complexity": "O(M*N)"
    },
    {
        "id": "h27", "title": "Word Search II (Trie + Backtrack)",
        "topic": "Recursion", "difficulty": 2,
        "description": "Given an MxN board of characters and a list of words, find all words that can be constructed by sequentially adjacent cells (horizontal/vertical, no reuse). Use a Trie for efficiency.",
        "expected_complexity": "O(M*N*4^L)"
    },
    {
        "id": "h28", "title": "Candy Distribution Problem",
        "topic": "Greedy", "difficulty": 2,
        "description": "N children stand in a line, each with a rating. Give candies such that: each child gets ≥1 candy, and children with higher ratings than neighbours get more candies. Minimize total candies. Example: ratings=[1,0,2] → 5.",
        "expected_complexity": "O(N)"
    },
    {
        "id": "h29", "title": "Alien Dictionary Order",
        "topic": "Graphs", "difficulty": 2,
        "description": "Given a sorted dictionary of an alien language (list of words), derive the order of characters in the alien alphabet. Use topological sort. Example: ['wrt','wrf','er','ett','rftt'] → 'wertf'.",
        "expected_complexity": "O(V+E)"
    },
    {
        "id": "h30", "title": "Burst Balloons for Maximum Coins",
        "topic": "Dynamic Programming", "difficulty": 2,
        "description": "Given N balloons with values, burst them to collect coins. Bursting balloon i earns nums[i-1]*nums[i]*nums[i+1] coins. Find the maximum coins by choosing the optimal burst order. Example: [3,1,5,8] → 167.",
        "expected_complexity": "O(N^3)"
    },
]


def get_task_by_difficulty(diff_level: int, exclude_id: str = None,
                           active_topics: list = None,
                           used_ids: list = None) -> dict:
    """
    Pick a random problem from the static bank matching the difficulty.
    Avoids repeating recently-used problems.
    No API calls — instant and free.
    """
    pool = [p for p in PROBLEMS if p["difficulty"] == diff_level]

    if active_topics:
        filtered = [p for p in pool if p["topic"] in active_topics]
        if filtered:
            pool = filtered

    if used_ids:
        fresh = [p for p in pool if p["id"] not in used_ids]
        if fresh:
            pool = fresh

    if exclude_id:
        pool = [p for p in pool if p["id"] != exclude_id]

    if not pool:
        # All problems used — allow repeats but exclude last one
        pool = [p for p in PROBLEMS if p["difficulty"] == diff_level
                and p["id"] != exclude_id]

    return random.choice(pool) if pool else PROBLEMS[0]
