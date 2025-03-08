'''
Problem Statement:
You are given two lists:
vessel_capacities – a list of available vessel capacities (in barrels).
shipment_demands – a list of shipment demands (in barrels).
Each vessel can be allocated to at most one shipment if 
its capacity is greater than or equal to the shipment’s demand. 
The “unused capacity” for a shipment is the difference between 
the vessel capacity and the shipment demand. Write a function 
min_unused_capacity(vessel_capacities: List[int], shipment_demands: List[int]) -> int 
that finds an allocation which minimizes the total unused capacity. 
If it’s not possible to allocate all shipments, return -1.

Example:
Input: vessel_capacities = [120, 150, 200], shipment_demands = [100, 140, 180]
Output: 50
Explanation: One optimal allocation:
- Vessel 120 for shipment 100 (unused = 20)
- Vessel 150 for shipment 140 (unused = 10)
- Vessel 200 for shipment 180 (unused = 20)
Total unused capacity = 20 + 10 + 20 = 50.
'''

from typing import List

def min_unused_capacity(vessel_capacities: List[int], shipment_demands: List[int]) -> int:
    vessel_capacities.sort()
    # print(vessel_capacities)
    shipment_demands.sort()
    # print(shipment_demands)
    total_unused_capacity = 0
    i = 0
    j = 0
    while i < len(vessel_capacities) and j < len(shipment_demands):
        if vessel_capacities[i] >= shipment_demands[j]:
            total_unused_capacity = total_unused_capacity + (vessel_capacities[i] - shipment_demands[j])
            i += 1
            j += 1
        else:
            i += 1
    if j < len(shipment_demands):
        return -1
    return total_unused_capacity

print(min_unused_capacity([120, 150, 200],  [100, 140, 180]))