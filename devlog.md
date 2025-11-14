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

## 11/14/2025 4:00 PM
### Thoughts So Far
- I'm starting with the simplest interaction: a customer introducing themself to a teller.
- I'm using a small number of threads to make debugging easier.
- The "line" and "introduction" seem like they can be handled at the same time.

### Plan for This Session
- Code: Implemented `bank_sim.py` using the `threading` and `queue` modules.
- Bank Open Logic:
    - Created a `bank_open_sem = threading.Semaphore(0)`.
    - Each `teller` thread `release()`s this semaphore once it's ready.
    - The main thread `acquire()`s it 3 times before starting any customer threads. This ensures the bank doesn't open until all 3 tellers are ready.
- Line & Introduction:
    - Created a `customer_line = queue.Queue()`.
    - The `customer` thread "gets in line" and "introduces" themself by `put()`ing their `customer_id` into the queue.
    - The `teller` thread `get()`s a `customer_id` from the queue, which blocks if the line is empty.
- Bank Close Logic:
    - Teller threads are `daemon=True` so they exit when the main thread finishes.
    - The main thread `join()`s all customer threads, then waits for the queue to be empty, ensuring all 5 customers are served before closing.

### End of Session
- The code successfully implements the bank open and introduction steps. Tellers wait for customers, and customers queue up and get served.
- Problem: This simple queue model doesn't support the full interaction. The spec requires a multi-step back-and-forth handshake. A teller `get()`s a customer, but there's no way to communicate back to that specific customer.
- Next Step: I'll need to refactor this. I'll still use a queue to manage the line of free tellers, but I'll need a way to pass a dedicated set of semaphores or a shared object between a *specific* customer and teller to manage their private conversation.