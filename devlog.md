## 11/14/2025 3:35 PM
### Initial Thoughts
- Project: Bank Simulation
- Goal: Simulate 3 Tellers and 50 Customers using threads.
- Key challenge: Synchronization. Must use `threading.Semaphore` to manage all interactions and shared resources.

### Key Resources & Constraints
- Tellers: 3 threads.
- Customers: 50 threads.
- Manager: Shared resource, limit 1.
- Safe: Shared resource, limit 2.
- Door: Shared resource, limit.

### High-Level Plan
1.  Implement the simplest interaction first.
2.  First, build the basic `teller` and `customer` thread functions.
3.  Implement the core line logic: how a customer waits for any available teller.
4.  Implement the customer-teller handshake.
5.  Add the shared resource semaphores and the `time.sleep()` calls.
6.  Scale to 3/50 and ensure the bank open and close logic is correct.