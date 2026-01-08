#!/usr/bin/env python3
"""Sample workload for WasteCompute demonstration."""

import time
import random
import sys

def main():
    print("WasteCompute Workload Started")
    print("-" * 40)
    
    # Simulate computation
    for i in range(1, 4):
        time.sleep(0.5)
        cpu_load = random.randint(30, 95)
        print(f"Processing batch {i}/3 [CPU: {cpu_load}%]")
    
    print("-" * 40)
    print("Workload completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
