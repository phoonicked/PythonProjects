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