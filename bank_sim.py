import threading
import queue
import time
import random

NUM_TELLERS = 3
NUM_CUSTOMERS = 50

manager_sem = threading.Semaphore(1)
safe_sem = threading.Semaphore(2)
door_sem = threading.Semaphore(2)
teller_ready_sem = threading.Semaphore(0)
free_tellers_queue = queue.Queue()

# List to hold interaction objects for each teller
teller_interactions = []
for _ in range(NUM_TELLERS):
    teller_interactions.append({
        "customer_sem": threading.Semaphore(0),
        "teller_sem": threading.Semaphore(0),
        "customer_id": None,
        "transaction_type": None
    })

def teller(teller_id):
    
    # 1. Teller lets everyone know it is ready
    print(f"Teller {teller_id}: Ready to serve.")
    teller_ready_sem.release()

    while True:
        # Put teller ID in queue, indicating they are free
        free_tellers_queue.put(teller_id)
        
        # 2. Wait for a customer to approach
        teller_interactions[teller_id]["teller_sem"].acquire()
        
        customer_id = teller_interactions[teller_id]["customer_id"]
        print(f"Teller {teller_id} [Customer {customer_id}]: Serving customer {customer_id}.")

        # 3. Ask for the transaction
        print(f"Teller {teller_id} [Customer {customer_id}]: Asking for transaction.")
        teller_interactions[teller_id]["customer_sem"].release()

        # 4. Wait until customer gives the transaction
        teller_interactions[teller_id]["teller_sem"].acquire()
        
        transaction = teller_interactions[teller_id]["transaction_type"]
        print(f"Teller {teller_id} [Customer {customer_id}]: Received transaction: {transaction}.")

        # 5. If Withdraw, go to manager
        if transaction == "Withdrawal":
            print(f"Teller {teller_id} [Customer {customer_id}]: Going to manager.")
            manager_sem.acquire()
            print(f"Teller {teller_id} [Customer {customer_id}]: Interacting with manager.")
            time.sleep(random.uniform(0.005, 0.030))
            print(f"Teller {teller_id} [Customer {customer_id}]: Done with manager.")
            manager_sem.release()

        # 6. Go to the safe
        print(f"Teller {teller_id} [Customer {customer_id}]: Going to safe.")
        safe_sem.acquire()
        
        # 7. In the safe, perform transaction
        print(f"Teller {teller_id} [Customer {customer_id}]: Performing transaction in safe.")
        time.sleep(random.uniform(0.010, 0.050))
        print(f"Teller {teller_id} [Customer {customer_id}]: Done with transaction in safe.")
        safe_sem.release()

        # 8. Inform customer transaction is done
        print(f"Teller {teller_id} [Customer {customer_id}]: Transaction complete.")
        teller_interactions[teller_id]["customer_sem"].release()

        # 9. Wait for customer to leave
        teller_interactions[teller_id]["teller_sem"].acquire()
        print(f"Teller {teller_id} [Customer {customer_id}]: Customer has left.")


def customer(customer_id):

    # 1. Decide on transaction type
    transaction_type = random.choice(["Deposit", "Withdrawal"])

    # 2. Wait between 0-100ms
    time.sleep(random.uniform(0.0, 0.100))
    print(f"Customer {customer_id}: Arrives at bank with transaction: {transaction_type}.")

    # 3. Enter the bank
    print(f"Customer {customer_id}: Waiting to enter bank.")
    door_sem.acquire()
    print(f"Customer {customer_id}: Enters bank.")
    door_sem.release()

    # 4. Get in line
    print(f"Customer {customer_id}: Waiting in line.")
    teller_id = free_tellers_queue.get()
    print(f"Customer {customer_id} [Teller {teller_id}]: Approaching teller {teller_id}.")

    # 5. Introduce self to teller
    teller_interactions[teller_id]["customer_id"] = customer_id
    teller_interactions[teller_id]["teller_sem"].release()

    # 6. Wait for teller to ask for transaction
    teller_interactions[teller_id]["customer_sem"].acquire()

    # 7. Tell teller the transaction
    print(f"Customer {customer_id} [Teller {teller_id}]: Giving transaction type: {transaction_type}.")
    teller_interactions[teller_id]["transaction_type"] = transaction_type
    teller_interactions[teller_id]["teller_sem"].release()

    # 8. Wait for teller to complete transaction
    teller_interactions[teller_id]["customer_sem"].acquire()
    print(f"Customer {customer_id} [Teller {teller_id}]: Transaction is complete. Thank you.")

    # 9. Leave the bank
    teller_interactions[teller_id]["teller_sem"].release()
    print(f"Customer {customer_id}: Leaves the bank.")


if __name__ == "__main__":
    print("Main: Bank simulation starting.")
    print("Main: Launching 3 teller threads.")
    
    teller_threads = []
    # Launch teller threads
    for i in range(NUM_TELLERS):
        t = threading.Thread(target=teller, args=(i,), daemon=True)
        t.start()
        teller_threads.append(t)

    # Wait for all 3 tellers to be ready
    print("Main: Waiting for all 3 tellers to be ready...")
    for i in range(NUM_TELLERS):
        teller_ready_sem.acquire()
    
    print("Main: Bank is OPEN. Launching 50 customer threads.")
    
    customer_threads = []
    # Launch customer threads
    for i in range(NUM_CUSTOMERS):
        t = threading.Thread(target=customer, args=(i,))
        t.start()
        customer_threads.append(t)

    # Wait for all customer threads to complete
    for i, t in enumerate(customer_threads):
        t.join()
        
    print(f"Main: All {NUM_CUSTOMERS} customers have left the bank.")
    print("Main: Bank is CLOSING. Simulation complete.")