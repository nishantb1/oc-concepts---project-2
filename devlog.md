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
- Next Step: I'll need to refactor this. I'll still use a queue to manage the line of free tellers, but I'll need a way to pass a dedicated set of semaphores or a shared object between a specific customer and teller to manage their private conversation.

## 11/14/2025 6:30 PM
### Thoughts So Far
- The Next Step from the last session is the plan for this one. The simple queue model is not enough for the required handshake.
- I need to refactor the code to support a full, two-way conversation between a specific customer and a specific teller, as shown in the `example.py`.
- My plan is to create a list of Interaction objects, one for each teller, to manage this private communication. The `queue.Queue` will now just be for managing the *line* of free tellers.

### Plan for This Session
- Refactor: `bank_sim.py` to implement the full handshake and all final requirements.
- Interaction Channel:
    - Created a `teller_interactions` list. Each element is a dictionary holding:
        - `customer_sem = threading.Semaphore(0)`
        - `teller_sem = threading.Semaphore(0)`
        - `customer_id = None`
        - `transaction_type = None`
- Full Handshake Logic:
    - `teller` function: `put()` its ID into `free_tellers_queue`, `acquire()` its `teller_sem`, `release()` `customer_sem`, `acquire()` `teller_sem`, etc.
    - `customer` function: `get()` `teller_id` from `free_tellers_queue`, put ID in `teller_interactions`, `release()` `teller_sem`, `acquire()` `customer_sem`, put transaction in `teller_interactions`, `release()` `teller_sem`, etc.
- Implement Final Requirements:
- Semaphores Added:
    - `manager_sem = threading.Semaphore(1)`
    - `safe_sem = threading.Semaphore(2)`
    - `door_sem = threading.Semaphore(2)`
- Customer Function Updates:
    - Added random `time.sleep()` before arrival.
    - `acquire()` and `release()` `door_sem` when entering.
- Teller Function Updates:
    - If `transaction == "Withdrawal"`, `acquire()` and `release()` `manager_sem` with its sleep.
    - `acquire()` and `release()` `safe_sem` with its sleep.
- Final Handshake Steps:
    - Added the final "wait for customer to leave" signal.
- Output:
    - Added all required `print()` statements in the `THREAD_TYPE ID [THREAD_TYPE ID]: MSG` format.
- Scale:
    - Changed `NUM_CUSTOMERS` to 50.

### End of Session
- This was a long session, but the full refactor and all final requirements are complete.
- The simulation is complete and appears to be working correctly with 50 customers.
- All required print statements are in place, and the output shows the semaphores are correctly limiting access.
- The bank open and close logic works: customers wait for all tellers, and the main thread `join()`s all 50 customer threads, which signifies the bank closing.
- The project is now functionally complete and ready for the `readme.md`.