import threading
import queue
import time
import random

NUM_TELLERS = 3
NUM_CUSTOMERS = 5

# A queue to hold customers waiting in line.
customer_line = queue.Queue()

# Semaphore ensures bank is open before customers enter.
bank_open_sem = threading.Semaphore(0)

def teller(teller_id):
    # 1. Teller is ready
    print(f"Teller {teller_id}: Is ready to serve.")
    bank_open_sem.release()

    while True:
        try:
            # 2. Wait for a customer
            customer_id = customer_line.get()
            
            # 3. Serve customer
            print(f"Teller {teller_id}: [Customer {customer_id}] Now serving Customer {customer_id}.")
            time.sleep(random.uniform(0.1, 0.3)) 
            print(f"Teller {teller_id}: [Customer {customer_id}] Finished with Customer {customer_id}.")

            customer_line.task_done()
            
        except Exception as e:
            break

def customer(customer_id):
    
    time.sleep(random.uniform(0.0, 0.5)) 
    print(f"Customer {customer_id}: Arrives at the bank.")
    
    # 4. Customer gets in line
    # 5. Customer introduces self (by putting ID in queue)
    customer_line.put(customer_id)
    print(f"Customer {customer_id}: Is in line.")

if __name__ == "__main__":
    
    teller_threads = []
    # Launch teller threads
    for i in range(NUM_TELLERS):
        t = threading.Thread(target=teller, args=(i,), daemon=True)
        t.start()
        teller_threads.append(t)

    print("Main: Bank is closed. Waiting for all 3 tellers to be ready...")
    
    # Wait for all 3 tellers to be ready
    for i in range(NUM_TELLERS):
        bank_open_sem.acquire()
    
    print("Main: Bank is OPEN. Customers can now enter.")

    customer_threads = []
    # Launch customer threads
    for i in range(NUM_CUSTOMERS):
        t = threading.Thread(target=customer, args=(i,))
        t.start()
        customer_threads.append(t)

    # Wait for all customer threads to finish
    for t in customer_threads:
        t.join()

    # Wait for the queue to be fully processed
    customer_line.join()

    print("Main: All 5 customers have been served. Bank is CLOSING.")