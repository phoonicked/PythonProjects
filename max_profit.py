'''
Problem Statement:
Given an array prices where each element represents the price of a commodity (e.g., crude oil) 
on a given day, write a function max_profit(prices: List[int]) -> int that calculates 
the maximum profit you can achieve by buying on one day and selling on a later day. 
If no profit is possible, return 0.

Example:
Input: prices = [100, 180, 260, 310, 40, 535, 695]
Output: 655
Explanation: The best strategy is to buy at 40 and sell at 695.
'''

from typing import List

def max_profit(prices: List[int]) -> int:
    if not prices:
        return 0
    buy_price = prices[0]
    max_profit_so_far = 0
    for price in prices:
        if price < buy_price:
            buy_price = price
        else:
            profit = price - buy_price
            if profit > max_profit_so_far:
                max_profit_so_far = profit
    return max_profit_so_far

print(max_profit([100, 180, 260, 310, 40, 535, 695]))
        