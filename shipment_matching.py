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