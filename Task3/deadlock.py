#!/usr/bin/env python3
"""
Deadlock Detection Algorithm - USER INPUT VERSION
Lab 13 - Deadlock Detection
"""

from typing import List, Tuple


class DeadlockDetector:
    """
    Deadlock Detection Algorithm using:
    - Available vector
    - Allocation matrix  
    - Request matrix
    """
    
    def __init__(self, num_processes: int, num_resources: int):
        self.n = num_processes
        self.m = num_resources
        self.available: List[int] = []
        self.allocation: List[List[int]] = []
        self.request: List[List[int]] = []
    
    def set_available(self, available: List[int]):
        self.available = available.copy()
    
    def set_allocation(self, allocation: List[List[int]]):
        self.allocation = [row.copy() for row in allocation]
    
    def set_request(self, request: List[List[int]]):
        self.request = [row.copy() for row in request]
    
    def detect_deadlock(self) -> Tuple[bool, List[int]]:
        """
        Deadlock Detection Algorithm
        
        Returns: (is_deadlocked, list_of_deadlocked_processes)
        """
        # Step 1: Initialize
        work = self.available.copy()
        finish = [False] * self.n
        
        # If Allocation[i] == 0, mark as finished
        for i in range(self.n):
            if all(self.allocation[i][j] == 0 for j in range(self.m)):
                finish[i] = True
        
        # Step 2-3: Find process that can complete
        while True:
            found = False
            for i in range(self.n):
                if not finish[i]:
                    # Check if Request[i] <= Work
                    can_proceed = all(
                        self.request[i][j] <= work[j] 
                        for j in range(self.m)
                    )
                    if can_proceed:
                        # Process completes, release resources
                        for j in range(self.m):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        found = True
                        break
            
            if not found:
                break
        
        # Step 4: Check for deadlocked processes
        deadlocked = [i for i in range(self.n) if not finish[i]]
        return len(deadlocked) > 0, deadlocked


def get_input():
    """Get all inputs from user"""
    print("=" * 60)
    print("DEADLOCK DETECTION - USER INPUT")
    print("=" * 60)
    
    # Get number of processes and resources
    n = int(input("\nEnter number of processes: "))
    m = int(input("Enter number of resource types: "))
    
    # Get Available vector
    print(f"\nEnter Available vector ({m} integers, space-separated):")
    available = list(map(int, input().split()))
    
    # Get Allocation matrix
    print(f"\nEnter Allocation matrix ({n} rows x {m} columns):")
    print("(Enter each row as space-separated integers)")
    allocation = []
    for i in range(n):
        row = list(map(int, input(f"P{i}: ").split()))
        allocation.append(row)
    
    # Get Request matrix
    print(f"\nEnter Request matrix ({n} rows x {m} columns):")
    print("(Enter each row as space-separated integers)")
    request = []
    for i in range(n):
        row = list(map(int, input(f"P{i}: ").split()))
        request.append(row)
    
    return n, m, available, allocation, request


def display_matrices(available, allocation, request):
    """Display all matrices nicely"""
    print("\n" + "-" * 60)
    print("INPUT MATRICES")
    print("-" * 60)
    
    print(f"\nAvailable: {available}")
    
    print(f"\nAllocation Matrix:")
    for i, row in enumerate(allocation):
        print(f"  P{i}: {row}")
    
    print(f"\nRequest Matrix:")
    for i, row in enumerate(request):
        print(f"  P{i}: {row}")
    print("-" * 60)


def main():
    """Main: Get user input and detect deadlock"""
    
    # Get input from user
    n, m, available, allocation, request = get_input()
    
    # Display what was entered
    display_matrices(available, allocation, request)
    
    # Create detector and run algorithm
    detector = DeadlockDetector(n, m)
    detector.set_available(available)
    detector.set_allocation(allocation)
    detector.set_request(request)
    
    # Detect
    is_deadlock, deadlocked = detector.detect_deadlock()
    
    # Show result
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    
    if is_deadlock:
        print(f"\n❌ DEADLOCK DETECTED!")
        print(f"Deadlocked Processes: {deadlocked}")
        print(f"\nProcesses that CANNOT complete:")
        for i in deadlocked:
            print(f"  P{i}: Allocation={allocation[i]}, Request={request[i]}")
    else:
        print(f"\n✅ NO DEADLOCK - System is in SAFE state")
        print(f"All processes can complete successfully")
    
    print("\n" + "=" * 60)


    if __name__ == "__main__":
    main()