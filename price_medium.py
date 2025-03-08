'''
Problem Statement:
Given a list prices representing daily commodity prices 
and an integer window_size, implement a function 
moving_average(prices: List[float], window_size: int) -> List[float] 
that returns a list of the moving average for 
each full window of the last window_size days.

Example:
Input: prices = [10, 20, 30, 40, 50], window_size = 3
Output: [20.0, 30.0, 40.0]
Explanation: Averages: (10+20+30)/3 = 20, (20+30+40)/3 = 30, (30+40+50)/3 = 40.
'''

from typing import List

def moving_average(prices: List[float], window_size: int) -> List[float]:
    if(len(prices) < window_size):
        return []
    
    moving_averages= []
    for i in range(len(prices)-window_size+1):
        window = prices[i:i+window_size]
        moving_averages.append(sum(window)/window_size)
    return moving_averages

print(moving_average([10,20,30,40,50], 3))